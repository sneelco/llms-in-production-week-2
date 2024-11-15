from langchain_openai import ChatOpenAI

MODEL_NAME = "gpt-4o-mini"

llm = ChatOpenAI(
    model_name=MODEL_NAME,
    temperature=0.0
)