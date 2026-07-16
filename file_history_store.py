#长期会话记忆存储服务
import json
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
import os
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict


#message_to_dict:单个消息对象转字典
#message_from_dict:[字典、字典...]->[消息、消息...]
#AIMessage、HumanMessage、SystemMessage都是BaseMessage的子类

class FileChatMessageHistory(BaseChatMessageHistory):
    #获取对应文件夹下的文件ID以及文件路径
    def __init__(self,session_id,storage_path):
        self.session_id=session_id           #会话ID
        self.storage_path=storage_path       #每个会话ID的对应文件名的文件路径
        #完整的文件路径
        self.file_path=os.path.join(self.storage_path,session_id)

        #确保文件夹是存在的
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    #添加消息，将消息组成一个list[消息]，再将list[消息]里面的每个消息传换成字典组成list[字典]写入文件
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        #Sequence序列 类似于list、tuple
        all_messages=list(self.messages)     #已有的消息列表
        all_messages.extend(messages)        #新的和已有的融合成一个list

        #将数据同步写入本地文件中
        #类对象写入文件->一堆二进制
        #为了方便，可以将BaseMessage消息转为字典（借助json模块以json字符串写入文件）
        #官方message_to_dict:单个消息对象（BaseMessage类实例）转字典

        # new_messages=[]
        # for message in all_messages:
        #     d=message_to_dict(message)
        #     new_messages.append(d)
        #用列表的推导式来写
        new_messages=[message_to_dict(message) for message in all_messages]
        #将数据写入文件
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump(new_messages,f)

    #读取文件，将文件里的类型：list[字典]->list[消息]     用message_from_dict
    @property    #装饰器
    def messages(self)->list[BaseMessage]:
        #当前文件内: list[字典]
        try:
            with open(self.file_path,"r",encoding="utf-8") as f:
                message_data=json.load(f)
            return messages_from_dict(message_data)
        except FileNotFoundError:
            return []

    #清除文件里的消息
    def clear(self)->None:
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([], f)

def get_history(session_id):
    return FileChatMessageHistory(session_id,"./chat_history")

