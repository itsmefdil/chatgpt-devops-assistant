import chainlit as cl
import ollama
import os


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

@cl.on_message
async def main(message: cl.message):

    tool_res = await tool(message.content)

    msg = cl.Message(content="")

    for token in tool_res.message.content:
        await msg.stream_token(token)

    await msg.send()
