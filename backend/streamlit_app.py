from rag.pipeline import process_youtube_video, process_query
from rag.response_parser import parse_response
from utils import get_video_id_from_youtube_url, response_streamer
import time

import streamlit as st

st.title("Youtube Video Chatbot")

def initialize_video_processing():
    # Check if video was already processed
    if not any(value in st.session_state for value in ["index", "chunks", "embedding_dim"]):
        # Process the video and create the index
        with st.spinner(text="Processing video...", show_time=True):
            index, chunks, embedding_dim = process_youtube_video(st.session_state.video_id, languages=["pt", "en"])
            st.session_state.index = index
            st.session_state.chunks = chunks
            st.session_state.embedding_dim = embedding_dim
            time.sleep(5)

# Views
def display_video_id_input_screen():
    # Show the video ID input screen
    st.text_input("Enter the YouTube video URL:", "https://www.youtube.com/watch?v=6CJiM3E2mAA", key="video_url_input")

    def onclick_callback():
        url_input = st.session_state.video_url_input
        video_id_input = get_video_id_from_youtube_url(url_input)
        st.session_state.video_id = video_id_input
        st.session_state.submit_button_pressed = True

    if "submit_button_pressed" not in st.session_state or st.session_state.submit_button_pressed == False:
        st.button("Submit", on_click=onclick_callback)
    else:
        initialize_video_processing()

def display_chatbot_screen():
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type a message..."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        response, relevant_chunks = process_query(
            prompt,
            st.session_state.index,
            st.session_state.chunks,
            st.session_state.embedding_dim,
            "text-embedding-3-small"
        )
        formatted_response = parse_response(response, relevant_chunks)

        # Display bot message in chat container
        with st.chat_message("assistant"):
            response = st.write_stream(response_streamer(formatted_response))
        
        # Append user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Append bot message to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


# Initialize Chat History
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to get the video ID
if 'video_id' not in st.session_state:
    display_video_id_input_screen()
else:
    display_chatbot_screen()