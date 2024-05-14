import streamlit as st
import ollama
import random

st.title("Phi3 Chatbot (by Aditya Sharma)")

# Initialize session state
st.session_state.setdefault("messages", [])

# Define topics for conversation
topics = [
    "your hobbies",
    "your hometown",
    "the best thing that's happened in your day",
    "the weather",
    "your family",
    "your favorite book",
    "your favorite movie"
]

# Define conversation prompts
conversation_prompts = {
    "your hobbies": "Tell me about your favorite hobby.",
    "your hometown": "Describe your hometown.",
    "the best thing that's happened in your day": "What's the best thing that happened to you today?",
    "the weather": "What's the weather like where you are?",
    "your family": "Tell me about your family.",
    "your favorite book": "What's your favorite book?",
    "your favorite movie": "What's your favorite movie?"
}

# Function to choose a random topic
def choose_random_topic_and_prompt():
    selected_topic = random.choice(topics)
    prompt = conversation_prompts[selected_topic]
    return selected_topic, prompt


selected_topic, prompt = choose_random_topic_and_prompt()

    
st.session_state["messages"].append({"role": "assistant", "content": prompt})
st.chat_message("assistant", avatar="🤖").write(prompt)
st.session_state["messages"].append({"role": "user", "content": selected_topic})
st.chat_message("user").write(selected_topic)

# User input: Response to the prompt
user_response = st.text_input("Your response:")

# If user submits a response
if st.button("Submit"):
    if user_response:
        # Add user response to messages
        st.session_state["messages"].append({"role": "user", "content": user_response})
        
        # Configure the model
        def generate_response():
            if "full_message" not in st.session_state:
                st.session_state["full_message"] = ""
            
            response = ollama.chat(model='phi3', stream=True, messages=st.session_state["messages"])
            for partial_resp in response:
                token = partial_resp["message"]["content"]
                st.session_state["full_message"] += token
                # Truncate response to maximum length of 150 characters
                if len(st.session_state["full_message"]) > 150:
                    st.session_state["full_message"] = st.session_state["full_message"][:150] + "..."

                yield token

        # Initiate conversation with the selected topic and user's response
        st.chat_message("user").write(user_response)
        st.session_state["full_message"] = ""
        st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
        st.session_state["messages"].append({"role": "assistant", "content": st.session_state["full_message"]})

# Display chat history
if st.session_state.get("messages"):
    st.markdown("---")
    st.subheader("Chat History:")
    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            st.chat_message("assistant", avatar="🤖").write(msg["content"])
        else:
            st.chat_message("user").write(msg["content"])
