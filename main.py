from operator import itemgetter


from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import  RunnablePassthrough, RunnableLambda
from langchain.memory import ConversationBufferMemory

from chainlit.types import ThreadDict
import chainlit as cl
import ollama
import os


def setup_runnable():
    memory = cl.user_session.get("memory")  # type: ConversationBufferMemory
    runnable = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | StrOutputParser()
    )
    cl.user_session.set("runnable", runnable)

@cl.password_auth_callback
def auth_callback(username: str, password: str):

    env_username = os.getenv("USERNAME")
    env_password = os.getenv("PASSWORD")

    if env_username is None or env_password is None:
        return None

    if (username, password) == (env_username, env_password):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None

@cl.on_chat_start
async def start_chat():
    cl.user_session.set("memory", ConversationBufferMemory(return_messages=True))

    app_user = cl.user_session.get("user")

    cl.user_session.set("interaction",
        [{"role" : "system", "content": "You are helpfull devops engineer assistant"}],
    )

    start_message = f"Hello {app_user.metadata['role']}! How can I help you today?"

    msg = cl.Message(content="")
    for token in start_message:
        await msg.stream_token(token)

    await msg.send()

@cl.step(type="tool")
async def tool(input_massage):

    interaction = cl.user_session.get("interaction")

    interaction.append({"role" : "user", "content": input_massage})

    response = ollama.chat(model="llama3.2", messages=interaction)

    interaction.append({"role" : "user", "content": response.message.content})

    return response

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    memory = ConversationBufferMemory(return_messages=True)
    root_messages = [m for m in thread["steps"] if m["parentId"] == None]
    for message in root_messages:
        if message["type"] == "user_message":
            memory.chat_memory.add_user_message(message["output"])
        else:
            memory.chat_memory.add_ai_message(message["output"])

    cl.user_session.set("memory", memory)

    setup_runnable()
@cl.on_message
async def main(message: cl.message):

    tool_res = await tool(message.content)

    msg = cl.Message(content="")

    for token in tool_res.message.content:
        await msg.stream_token(token)

    await msg.send()
