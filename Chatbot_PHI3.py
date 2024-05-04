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

st.title("Phi3 Chatbot (by Aditya Sharma)")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello there, how can I assist you today?"}]

if st.session_state.get("messages"):
    for msg in st.session_state.get("messages"):
        if msg["role"] == "user":
            st.chat_message(msg["role"]).write(msg["content"])
        else:
            st.chat_message(msg["role"]).write(msg["content"])

## Configure the model
def generate_response():
    if "full_message" not in st.session_state:
        st.session_state["full_message"] = ""
        
    response = ollama.chat(model='phi3', stream=True, messages=st.session_state["messages"])
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token

if prompt := st.chat_input():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
    st.session_state["messages"].append({"role": "assistant", "content": st.session_state["full_message"]})
