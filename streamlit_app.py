import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Pop Star persona system message
pop_star_persona = {
    "role": "system",
    "content": (
        "You are a famous pop star assistant! Always answer with flair, charm, and a touch of stardom. "
        "Add some pop culture references, be enthusiastic, and sprinkle in musical emojis or song lyrics where appropriate. "
        "Your replies should feel like you're chatting backstage with your biggest fans. Never stop shining!"
    )
}

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        # Pre-load with the pop star persona system message
        st.session_state.messages = [pop_star_persona]

    # Display the existing chat messages (excluding system prompt).
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message.
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API, always including the pop star persona system message.
        stream = client.chat.completions.create(
            model="gpt-4.1",
            messages=st.session_state.messages,
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
