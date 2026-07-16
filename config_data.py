#配置文件
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_deepseek import ChatDeepSeek
from langchain_chroma import Chroma

#md5字符串存放文件点
md5_path="./md5.text"

#chroma配置
chroma=Chroma(
    collection_name="RAG1",    # 给向量数据库起个名字
    embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),    #指定嵌入模型
    persist_directory="./chroma_db"                  #指定数据存放的文件夹
)                                                   # 向量存储的实例 Chroma向量库对象


#文本分割器
# 注意：keep_separator 是 langchain-text-splitters >= 0.3.0 的参数，
# 如果报错 "unexpected keyword argument"，请执行：pip install langchain-text-splitters --upgrade
splitter = RecursiveCharacterTextSplitter(
    # 块大小：1000字符，和官方RAG平台标准对齐，兼顾上下文与检索精度
    chunk_size=1500,
    # 重叠10%，防止章节/句子被拦腰切断
    chunk_overlap=150,
    # 分割优先级：先大块分隔符，再空行、换行，最后标点，空字符串兜底按字符拆分
    separators=[
        "========================================================",  # 文档大章节分割线（最高优先级）
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", # 目录分割线
        "\n\n",  # 空段落
        "\n",    # 单行换行
        "。", "；", "！", "？", "，", ".", "?", "!", ",", " ",
        ""       # 兜底：按字符逐个拆分（LangChain 默认行为）
    ],
    length_function=len,
    # 保持分隔符（默认即为 True，显式声明便于理解）
    keep_separator=True
)

# 自定义阈值：超过1000字符才分割，短章节直接整块入库
max_split_char_number = 1100

# 相似度阈值（文档用DashScope/BGE embedding，区间0~1）
similarity_threshold = 4

#大模型配置
model=ChatDeepSeek(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    model="deepseek-v4-pro"
)

#session_id配置
session_id={
        "configurable":{
            "session_id":"user_001",
        }
    }


"""
#文本分割器
splitter=RecursiveCharacterTextSplitter(
    chunk_size=10000,                         #分割后的文本段最大长度
    chunk_overlap=100,                       #连续文本段之间的字符重叠数量
    separators=['\n','\n\n',' ','?',"？","。","."],   #自然段落划分的符号
    length_function=len                      #使用python自带的len函数统计依据
)                                            #文本分割的对象


#文本分割预值
max_split_char_number=7000

#检索值
similarity_threshold=4
"""