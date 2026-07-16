#向量存储服务
import config_data as config

class VectorStoreService(object):
    def __init__(self):    #构造函数
        self.vector_store=config.chroma       # 向量存储的实例 Chroma向量库对象

    def get_retriever(self):
        self.vector_store.as_retriever(search_kwargs={"k",config.similarity_threshold})