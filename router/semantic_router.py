from langchain_core.messages import HumanMessage, SystemMessage


class SemanticRouter:
    def __init__(self, llm, samples="", sys=""):
        self.llm = llm
        self.samples = samples
        self.system = sys
        self.prompt = self.system

    def is_chitchat(self, query):
        question = [SystemMessage(content=self.prompt), HumanMessage(content=query)]
        response = self.llm.invoke(question)
        ischitchat = response.content.strip() == "true"
        return ischitchat
