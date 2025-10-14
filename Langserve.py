import langchain_core
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()
import openai
from langserve import add_routes

openai.api_key=os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
model=ChatGroq(model="llama-3.3-70b-versatile",groq_api_key=groq_api_key)

#1. Creating prompt Template
from langchain_core.prompts import ChatPromptTemplate

system_template="Translate the following into {language}:"

prompt_template= ChatPromptTemplate.from_messages(
    [("system",system_template),
     ("user","{text}")]
)

from langchain_core.output_parsers import StrOutputParser
parser=StrOutputParser()

###create chain
chain=prompt_template|model|parser

## App definition
app=FastAPI(title="Langchain Server",version="1.0",description="A simple API server using Langchain runnable Interface")


##Adding chain routes
add_routes(
    app,
    chain,
    path="/chain"
)


if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)