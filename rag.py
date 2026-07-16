#rag核心服务

from langchain_core.output_parsers import StrOutputParser
import config_data as config
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

from file_history_store import get_history


class RagService(object):
    def __init__(self):
        self.vector_service=config.chroma
        self.prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的已知参考资料为主，简洁和专业的回答用户问题，参考资料{content}"),
                ("system","并且我提供历史的聊天记录，如下："),
                MessagesPlaceholder("history"),
                ("human","我的问题是{input}")
            ]
        )
        self.chat_model=config.model
        self.chain=self.get_chain()

    def get_chain(self):
        #获取最终的链
        retriever=self.vector_service.as_retriever(search_kwargs={"k":config.similarity_threshold})

        def format_for_rettriever(value:dir)->str:
            return value["input"]

        def format_for_prompt(value: dir) -> str:
            new_value={}
            new_value["input"] = value["input"]["input"]
            new_value["content"] = value["content"]
            new_value["history"] = value["input"]["history"]
            return new_value

        def print_prompt(full_prompt):
            print("*"*20)
            print(full_prompt.to_string())
            return full_prompt

        def format_document(docs: list):
            if not docs :
                return "无相关资料"
            format_str=""
            for doc in docs:
                format_str+=f"文档片段:{doc.page_content}\n文档元数据:{doc.metadata}\n\n"
            return format_str

        chain=(
            {
                "input":RunnablePassthrough(),
                "content": RunnableLambda(format_for_rettriever) | retriever | format_document
            } | RunnableLambda(format_for_prompt) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        #增强链
        conversation_chain=RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )


        return conversation_chain