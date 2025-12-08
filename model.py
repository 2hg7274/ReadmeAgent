from configs import LLM_API_CONFIGS
from langchain_openai import ChatOpenAI
from llama_index.llms.langchain import LangChainLLM

def load_llm_model(temperature, top_p, max_tokens):
    llm = ChatOpenAI(
        **LLM_API_CONFIGS,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )

    llm_model = LangChainLLM(llm=llm)
    return llm_model

