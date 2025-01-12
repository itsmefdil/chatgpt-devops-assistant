import chainlit as cl
import ollama

@cl.on_chat_start
async def start_chat():

    cl.user_session.set("interaction",
        [{"role" : "system", "content": "You are helpfull devops engineer assistant"}],
    )

    start_message = """ Hello , I'm your local AI devops assistant. How can I help you today? """

    msg = cl.Message(content="")
    for token in start_message:
        await msg.stream_token(token)

    await msg.send()

@cl.step(type="tool")
async def tool(input_massage, image=None):

    interaction = cl.user_session.get("interaction")

    if image:
        interaction.append({"role" : "user", "content": input_massage , "image": image})

    else:
        interaction.append({"role" : "user", "content": input_massage})

    response = ollama.chat(model="llama3.2", messages=interaction)

    interaction.append({"role" : "assistent", "content": response.message.content})

    return response

@cl.on_message
async def main(message: cl.message):

    images = [file for file in message.elements if "image" in file.mime]

    if images:
        tool_res = await tool(message.content, [i.path for i in images])

    else:
        tool_res = await tool(message.content)

    msg = cl.Message(content="")

    for token in tool_res.message.content:
        await msg.stream_token(token)

    await msg.send()
