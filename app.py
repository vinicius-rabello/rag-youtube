from rag.pipeline import process_youtube_video, process_query
from rag.response_parser import parse_response

import streamlit as st
import random
import time

st.title("Chat")

# Streamed response simulator
def response_streamer(response):
    response = response['response'] + "\nTimestamps: \n" + str(response['timestamps'])
    for word in response.split():
        yield word + " "
        time.sleep(0.02)

# Function to get the video ID
if 'video_id' not in st.session_state:
    st.session_state.video_id = "adw-vKbbhrY"

# Process the video and create the index
index, chunks, embedding_dim = process_youtube_video(st.session_state.video_id, languages=["pt", "en"])

# Initialize Chat History
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type a message..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    response, relevant_chunks = process_query(prompt, index, chunks, embedding_dim, "text-embedding-3-small")
    formatted_response = parse_response(response, relevant_chunks)

    # Display bot message in chat container
    with st.chat_message("assistant"):
        response = st.write_stream(response_streamer(formatted_response))
    
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Append bot message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})