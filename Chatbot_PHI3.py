#import pip

# Define the package to install
#package_name = 'ollama'

# Install the package
#try:
 #   pip.main(['install', package_name])
  #  print("Ollama installed successfully!")
#except Exception as e:
 #   print("Error installing Ollama:", e)


#import streamlit as st
#import ollama

streamlit.title("Phi3 Chatbot (by Aditya Sharma)")

if "messages" not in streamlit.session_state:
    streamlit.session_state["messages"] = [{"role": "assistant", "content": "Hello there, how can I assist you today?"}]

if streamlit.session_state.get("messages"):
    for msg in streamlit.session_state.get("messages"):
        if msg["role"] == "user":
            streamlit.chat_message(msg["role"]).write(msg["content"])
        else:
            streamlit.chat_message(msg["role"]).write(msg["content"])

## Configure the model
def generate_response():
    if "full_message" not in streamlit.session_state:
        streamlit.session_state["full_message"] = ""
        
    response = ollama.chat(model='phi3', stream=True, messages=streamlit.session_state["messages"])
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        streamlit.session_state["full_message"] += token
        yield token

if prompt := streamlit.chat_input():
    if "messages" not in streamlit.session_state:
        streamlit.session_state["messages"] = []
    streamlit.session_state["messages"].append({"role": "user", "content": prompt})
    streamlit.chat_message("user").write(prompt)
    streamlit.session_state["full_message"] = ""
    streamlit.chat_message("assistant", avatar="🤖").write_stream(generate_response)
    streamlit.session_state["messages"].append({"role": "assistant", "content": streamlit.session_state["full_message"]})
