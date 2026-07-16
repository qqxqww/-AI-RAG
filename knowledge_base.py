#知识库更新服务
"""
知识库
"""

import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
import  config_data as config
import hashlib
from datetime import datetime


def check_md5(md5_str):
    #检查传入过来的md5字符串是否已经被处理过了
    if not os.path.exists(config.md5_path):
        #md5文件不存在，md5字符串肯定不存在
        open(config.md5_path,'w',encoding="utf-8").close()   #md5文件不存在，我们还是把它创建出来，方便后面使用
        return False
    else:
        for line in open(config.md5_path,'r',encoding="utf-8").readlines():
            line=line.strip()    #处理字符串前后的空格和回车
            if line==md5_str:
                return True
        return False
"""
open(config.md5_path,'r',encoding="utf-8")
以只读模式打开保存 MD5 字符串的文本文件，指定 utf-8 编码，避免中文乱码。
readlines()
一次性读取文件所有行，返回每行字符串组成的列表，每行末尾自带换行符 \n。
for line in ...
循环遍历每一行内容，变量 line 初始值类似 abc123\n、 d456ef \n。
line.strip()
删除字符串首尾：空格、换行 \n、制表符 \t，中间内容不受影响。
示例：" e10adc3949ba59abbe56e057f20f883e\n" → "e10adc3949ba59abbe56e057f20f883e"
存在的小问题：文件未关闭
直接用 open() 不手动关闭，大量循环读写会占用文件句柄，推荐 with 自动关闭文件：
"""

def save_md5(md5_str):
    #将传入的md5字符串，记录到文件中保存
    with open(config.md5_path,'a',encoding="utf-8") as f:
        f.write(md5_str+'\n')


def get_string_md5(input_str:str,encoding="utf-8"):
    #将传入的字符串转换为md5字符串
    #先将传入的字符串转换成bytes字节数组
    str_bytes=input_str.encode(encoding=encoding)
    #再将bytes字节数组存入成md5对象中
    md5_obj=hashlib.md5()     #得到md5对象md5_obj
    md5_obj.update(str_bytes)  #更新内容（将bytes字节数组存入md5_obj中）
    md5_hex=md5_obj.hexdigest()  #得到md5的16进制
    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        self.chroma=config.chroma                  #向量存储的实例 Chroma向量库对象
        self.spliter=config.splitter               #文本分割的对象

    def upload_by_str(self,data:str,filename):
        #将传入的字符串，进行向量化，存入向量数据库中
        #判断数据是否已经存在向量数据库里，用md5字符串来判断
        md5_hex=get_string_md5(data)
        if check_md5(md5_hex):
            return "跳过，数据已存在向量数据库里"
        if len(data) > config.max_split_char_number:
            knowledge_chunks:list[str]=self.spliter.split_text(data)
        else:
            knowledge_chunks=[data]

        metdata={
            "source":filename,
            #2025-10-10 10:10:34
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"小钱"
        }
        #添加至向量数据库中
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metdata for _ in knowledge_chunks]
        )

        #md5_hex存入我们的文件里去
        save_md5(md5_hex)
        return "成功，数据已成功存入向量数据库里"


