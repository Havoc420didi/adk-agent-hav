from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from django.http import StreamingHttpResponse, HttpResponse
import json
import os
import time
from rest_framework.decorators import api_view

from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate
from agent_with_memory.core.agent.react.base import ReActAgent
from agent_with_memory.core.agent.pool import AgentPool
from algorithm.drug_property.main import drug_property_prediction
from algorithm.drug_cell_response_regression.main import drug_cell_response_regression_predict
from algorithm.drug_target_affinity_regression.main import drug_target_affinity_regression_predict
from algorithm.drug_target_affinity_classification.main import drug_target_classification_prediction
from algorithm.drug_drug_response.main import drug_drug_response_predict
from algorithm.drug_generation.main import drug_cell_response_regression_generation
from algorithm.drug_synthesis_design.scripts.main import Retrosynthetic_reaction_pathway_prediction
from algorithm.drug_cell_response_regression_optimization.main import drug_cell_response_regression_optimization
# 
from smiles_file.models import File
# TEMP
import pandas as pd

# 设置工作目录
os.chdir('/home/data2/rhj/project/bsl_drug_backend')
os.environ['CUDA_VISIBLE_DEVICES'] = '6'

# 为每个任务工具创建实例
drug_property_prediction_tool = FunctionTool.from_defaults(fn=drug_property_prediction)
drug_target_affinity_regression_predict_tool = FunctionTool.from_defaults(fn=drug_target_affinity_regression_predict)
drug_target_classification_prediction_tool = FunctionTool.from_defaults(fn=drug_target_classification_prediction)
drug_cell_response_regression_predict_tool = FunctionTool.from_defaults(fn=drug_cell_response_regression_predict)
drug_drug_response_predict_tool = FunctionTool.from_defaults(fn=drug_drug_response_predict)
drug_cell_response_regression_generation_tool = FunctionTool.from_defaults(fn=drug_cell_response_regression_generation)
retrosynthetic_reaction_pathway_prediction_tool = FunctionTool.from_defaults(fn=Retrosynthetic_reaction_pathway_prediction)
drug_cell_response_regression_optimization_tool = FunctionTool.from_defaults(fn=drug_cell_response_regression_optimization)

# 工具列表
tools = [
    drug_property_prediction_tool, drug_target_affinity_regression_predict_tool,
    drug_target_classification_prediction_tool, drug_cell_response_regression_predict_tool,
    drug_drug_response_predict_tool, drug_cell_response_regression_generation_tool,
    retrosynthetic_reaction_pathway_prediction_tool, drug_cell_response_regression_optimization_tool
]

# 创建 Ollama 模型实例，指定模型和超时时间
llm = Ollama(model="drug_tools_v4:latest", request_timeout=120.0)

# 读取系统提示模板文件
file_path = '/home/data2/rhj/project/bsl_drug_backend/agent_with_memory/core/agent/react/templates/read_memory_pool.md'
with open(file_path, 'r') as file:
    react_system_header_str = str(file.read())
react_system_prompt = PromptTemplate(react_system_header_str)  # 使用模板创建 PromptTemplate 实例

from rest_framework.permissions import AllowAny  # 添加此行以允许所有访问
from rest_framework.decorators import authentication_classes, permission_classes

# 初始化 AgentPool
AgentPool.initialize(tools, llm, react_system_prompt)

def create_agent(user_id: str, chat_id: str):
    """获取Agent实例，优先从池中获取"""
    try:
        return AgentPool.get_instance().get_agent(user_id, chat_id)
    except RuntimeError as e:
        # 记录错误并重新引发，让上层处理
        print(f"Error getting agent: {str(e)}")
        raise

def release_agent(agent):
    """释放Agent实例回池中"""
    if agent:
        AgentPool.get_instance().release_agent(agent)

from queue import Queue  # TEST Queue
import threading
from utils.mongoClient import mongo_db
import datetime
from llama_index.core.base.llms.types import (
    MessageRole, ChatMessage
)

class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    # only_one = False
    
    @staticmethod
    def generate(message_queue, message_list, processing_event=None):
        while True:
            data = message_queue.get()
            if data == "DONE" or data == "STOP":
                # yield f"data: {json.dumps({'chunk': 'DONE'})}\n\n"
                yield "data: [DONE]"
                if processing_event:
                    processing_event.set()  # 标记处理完成
                break
            else:
                yield f"data: {json.dumps({'chunk': data})}\n\n"
                message_list.append(data)
    
    def post(self, request, *args, **kwargs):
        """
        POST /agent/chat/

        Args:
            query: query
            memory_pool: memory_pool
            chat_id: chat_id

        Returns:
            message: message
        """
        # if self.only_one:
        #     return Response({"message": "当前服务器繁忙，请稍后再试"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        # self.only_one = True
        
        user = request.user
        # 解析请求体中的 JSON 数据
        data = request.data
        # 提取 query, tool_type 和 memory_pool
        user_input = data.get('query', '')
        memory_pool = data.get('memory_pool', [])
        history_messages = data.get('history_messages', [])
        
        # STAGE - 0 pre: 数据接受器
        message_queue = Queue()
        messages_list = []  # 用于存储所有消息
        processing_event = threading.Event()  # 用于同步消息处理
        
        # 检查 CUDA 错误
        try:
            import torch
            if not torch.cuda.is_available():
                return Response({"message": "当前服务器繁忙，请稍后再试"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            if "CUDA error" in str(e):
                return Response({"message": "当前服务器繁忙，请稍后再试"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
        # STAGE - 1： chat meta 信息的返回
        chat_id = data.get('chat_id')
        if not chat_id:
            chat_meta = ChatMetaView.create_chat(user, user_input)
            message_queue.put(f'Meta: {str(chat_meta)}')
        else:
            chat_meta = ChatMetaView.get_chat(user, chat_id)
            if not chat_meta:
                return Response({'message': 'ChatMeta not found'}, status=status.HTTP_404_NOT_FOUND)
        # 将新对话记录存入 MongoDB
        mongo_db.get_collection().insert_one({
            'chat_id': str(chat_meta.id),
            'user_id': str(user.id),
            'role': MessageRole.USER,
            'content': user_input,
            'created_at': datetime.datetime.now()
        })

        # 尝试创建Agent，捕获可能的池已满异常
        try:
            agent = create_agent(user.id, chat_id)
        except RuntimeError as e:
            return Response({"message": "当前服务器繁忙，请稍后再试"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        for kv in memory_pool:
            if kv.get('type') == 1:
                value = kv.get('value')
            elif kv.get('type') == 2:
                file_record = None
                try:
                    file_id = kv.get('file', {}).get('file_id')
                    if not file_id:
                        continue
                        
                    file_record = File.objects.get(id=file_id) # , user=user)
                except File.DoesNotExist:
                    continue
                except Exception as e:
                    release_agent(agent)
                    raise e
                
                if file_record is None:
                    continue
                    
                file_path = file_record.file_path
                try:
                    # 检查文件是否存在
                    if not os.path.exists(file_path):
                        raise FileNotFoundError()
                    
                    col_names = kv['file']['col_names']
                    if col_names:
                        df = pd.read_csv(file_path, names=col_names)
                        if len(col_names) == 1:
                            value = df[col_names[0]].values.tolist()[1:]
                            # TAG MASK 后处理 # TODO 集成到 FileHandler 之后
                            if (kv['key'] == 'durg_optimization_mask'):
                                value = [int(i) for i in value]
                        else:
                            df = df[col_names].values.tolist()[1:]
                    
                except FileNotFoundError:
                    release_agent(agent)
                    raise NotFound("File not found")
                except PermissionDenied:
                    release_agent(agent)
                    raise PermissionDenied("You do not have permission to access this file")
                except Exception as e:
                    release_agent(agent)
                    raise Exception(f"Failed to read file header: {str(e)}")
            else:
                release_agent(agent)
                return Response({"message": "Failed", "error": "Failed to add memory pool",}, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)

            agent.memory_pool.add_to_memory(kv['key'], value)
            print('😺 set', kv['key'], 'with', value)

        # STAGE - 3
        chat_history = [
            ChatMessage(role=message.get('role'), content=message.get('content')) for message in history_messages
        ]

        # 创建 ReActAgent 实例，将功能工具列表和模型传入代理
        # 启动异步任务，将数据放入队列
        def async_chat():
            try:
                response = agent.chat(user_input, chat_history=chat_history, message_queue=message_queue)
                # 拆解出 Thought 和 Answer
                response = str(response)
                # TAG Save MemPool
                chat_meta.memory_pool = agent.memory_pool.get()
                chat_meta.save()
                try: 
                    thought, answer = response.split('\nAnswer: ')
                except:
                    thought, answer = '', response
                finally:
                    # INFO 如果 Answer 以 Thought: 开头，则去除 Thought:
                    if answer.startswith('Thought:'):
                        answer = answer.replace('Thought:', '')
                # 去除 Thought: 前缀
                thought = thought.replace('Thought: ', '')
                # 将 Thought 和 Answer 分别放入消息队列
                if thought:
                    message_queue.put(f"Thought: {thought}")
                message_queue.put(f"Answer: {answer}")
                message_queue.put("DONE")  # 结束标志
                
                # 等待消息处理完成
                processing_event.wait(timeout=10)  # 最多等待10秒
                
                # 将对话结果存入 MongoDB
                mongo_db.get_collection().insert_one({
                    'chat_id': str(chat_meta.id),
                    'user_id': str(user.id),
                    'role': MessageRole.MODEL,
                    'task_message': messages_list,
                    'content': "".join(messages_list),  # 存储所有消息
                    'created_at': datetime.datetime.now()
                })
            except Exception as e:
                # 记录异常并通知用户
                error_message = f"Error: 处理请求时发生错误"
                print(error_message, {str(e)})
                # 检查是否是 CUDA 错误
                if "CUDA error" in str(e):
                    message_queue.put("Error: 当前服务器繁忙，请稍后再试")
                else:
                    message_queue.put(error_message)
                message_queue.put('STOP')
                
                # 等待消息处理完成
                processing_event.wait(timeout=10)  # 最多等待10秒
                
                # 将对话结果存入 MongoDB
                mongo_db.get_collection().insert_one({
                    'chat_id': str(chat_meta.id),
                    'user_id': str(user.id),
                    'role': MessageRole.MODEL,
                    'task_message': messages_list,
                    'content': "".join(messages_list),
                    'created_at': datetime.datetime.now()
                })
            finally:
                # 无论是否发生异常，都释放Agent资源
                release_agent(agent)
            
        # 启动异步任务
        threading.Thread(target=async_chat).start()

        response = StreamingHttpResponse(
            ChatView.generate(message_queue, messages_list, processing_event),
            content_type='text/event-stream',
        )
        return response
    
# """
# v0.1: POST 同步方式的 Chat
# """            
# @authentication_classes([])
# class ChatTempView(APIView):
    
#     def post(self, request, *args, **kwargs):
#         # user = request.user
#         # 解析请求体中的 JSON 数据
#         data = request.data
        
#         user_input = data.get('query', '')
#         memory_pool = data.get('memory_pool', [])
        
#         # 尝试获取Agent实例
#         try:
#             agent = create_agent()
#         except RuntimeError as e:
#             return Response({"message": "Failed", "error": "当前服务器繁忙，请稍后再试"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

#         try:
#             # handle memory pool
#             for kv in memory_pool:
#                 print('🐶', kv)
#                 if kv.get('type') == 1:
#                     value = kv.get('value')
#                 elif kv.get('type') == 2:
#                     try:
#                         file_record = File.objects.get(id=kv['file']['file_id']) # , user=user)
#                     except File.DoesNotExist:
#                         continue
#                     file_path = file_record.file_path
#                     try:
#                         # 检查文件是否存在
#                         if not os.path.exists(file_path):
#                             raise FileNotFoundError()
                        
#                         col_names = kv['file']['col_names']
#                         if col_names:
#                             df = pd.read_csv(file_path, names=col_names)
#                             if len(col_names) == 1:
#                                 value = df[col_names[0]].values.tolist()[1:]
#                                 # TAG MASK 后处理 # TODO 集成到 FileHandler 之后
#                                 if (kv['key'] == 'durg_optimization_mask'):
#                                     value = [int(i) for i in value]
#                             else:
#                                 df = df[col_names].values.tolist()[1:]
                        
#                     except FileNotFoundError:
#                         raise NotFound("File not found")
#                     except PermissionDenied:
#                         raise PermissionDenied("You do not have permission to access this file")
#                     except Exception as e:
#                         raise Exception(f"Failed to read file header: {str(e)}")
#                 else:
#                     return Response({"message": "Failed", "error": "Failed to add memory pool",}, content_type='application/json', status=status.HTTP_400_BAD_REQUEST)

#                 agent.memory_pool.add_to_memory(kv['key'], value)
#                 print('😺 set', kv['key'], 'with', value)

#             # 调用 Agent 处理用户输入
#             response = agent.chat(user_input)
#             answer = str(response)
            
#             return Response({"message": "Success", "data": {
#                 "answer": answer,
#             }}, content_type='application/json', status=status.HTTP_200_OK)
#         finally:
#             # 无论是否发生异常，都释放Agent资源
#             release_agent(agent)

from .models import chatMeta
import uuid
from utils.llmClient import llmClient
# import pymongo

class ChatMetaView(APIView):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def create_chat(user, user_input):
        chat_id = uuid.uuid4()
        title = llmClient.gen_title(llm, user_input)
        
        chat = chatMeta.objects.create(
            id=chat_id,
            user=user,
            title=title,
        )
        chat.save()
        return chat
    
    @staticmethod
    def get_chat(user, chat_id):
        try:
            chat = chatMeta.objects.get(id=chat_id, user=user)
            return chat
        except chatMeta.DoesNotExist:
            return None
    
    def get(self, request, chat_id, *args, **kwargs):
        user = request.user
        chat_meta = self.get_chat(user, chat_id)
        if not chat_meta:
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
            
        history_messages = list(mongo_db.get_collection().find({
            'chat_id': str(chat_id),
            'user_id': str(user.id)
        }))  
        # 将ObjectId转换为字符串以便序列化
        for message in history_messages:
            message['_id'] = str(message['_id'])
        
        return Response({
            "chat_meta": chat_meta.to_dict(),
            "history_messages": history_messages
        }, status=status.HTTP_200_OK)
    
    def put(self, request, chat_id, *args, **kwargs):
        user = request.user
        chat_title = request.data.get('chat_title')
        try:
            chat = chatMeta.objects.get(id=chat_id, user=user)
            chat.title = chat_title
            chat.save()
            return Response({"message": "Chat name updated successfully"}, status=status.HTTP_200_OK)
        except chatMeta.DoesNotExist:
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def delete(self, request, chat_id, *args, **kwargs):
        user = request.user
        try:
            # 1.
            mongo_db.get_collection().delete_many({
                'chat_id': str(chat_id),
                'user_id': str(user.id)
            })
            # 2.
            chat = chatMeta.objects.get(id=chat_id, user=user)
            chat.delete()
            return Response({"message": "Chat deleted successfully"}, status=status.HTTP_200_OK)
        except chatMeta.DoesNotExist:
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatMemoryPoolView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, chat_id, *args, **kwargs):
        """
        GET /agent/chat/{chat_id}/memory-pool/

        Args:
            chat_id: chat_id

        Returns:
            _type_: _description_
        """
        user = request.user
        chat_meta = ChatMetaView.get_chat(user, chat_id)
        if not chat_meta:
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
        
        memory_pool = chat_meta.memory_pool
        return Response({
            "memory_pool": memory_pool
        }, status=status.HTTP_200_OK)


class ChatMetaListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """
        GET /agent/chat-list/

        Args:

        Returns:
            chat_list: chat_list
        """
        user = request.user
        chats = chatMeta.objects.filter(user=user).order_by('-created_at')
        chat_list = [{
            'id': str(chat.id),
            'title': chat.title,
            'created_at': chat.created_at,
            'updated_at': chat.updated_at
        } for chat in chats]
        return Response({
            'data': chat_list
        }, status=status.HTTP_200_OK)
        

class ChatTaskClearView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, chat_id, *args, **kwargs):
        """
        DELETE /agent/chat-stop/{chat_id}/

        Args:
            chat_id: chat_id

        Returns:
            message: message
        """
        user = request.user
        
        if AgentPool.get_instance()._stop_agent(user.id, chat_id):
            return Response({"message": "Chat task stopped successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)