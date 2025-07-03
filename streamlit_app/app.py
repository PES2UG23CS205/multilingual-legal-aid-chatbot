# streamlit_app/app.py
import streamlit as st
import requests
import base64
from streamlit_mic_recorder import mic_recorder

# --- PAGE CONFIGURATION & BOT NAME ---
BOT_NAME = " Legal Aid Chatbot"
st.set_page_config(page_title=BOT_NAME, page_icon="⚖️", layout="wide")

# --- API URLS ---
CHAT_API_URL = "http://127.0.0.1:8000/v2/chat"
AID_API_URL = "http://127.0.0.1:8000/find_aid_centers"

# --- LANGUAGE MAPPING ---
LANGUAGES = {
    "English": "en", "हिन्दी (Hindi)": "hi", "ಕನ್ನಡ (Kannada)": "kn",
    "தமிழ் (Tamil)": "ta", "తెలుగు (Telugu)": "te", "മലയാളം (Malayalam)": "ml"
}

# --- APPLICATION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "editing_index" not in st.session_state:
    st.session_state.editing_index = None
if "play_audio" not in st.session_state:
    st.session_state.play_audio = None
# Set defaults
if "language_code" not in st.session_state: st.session_state.language_code = "en"
if "chat_mode" not in st.session_state: st.session_state.chat_mode = "Legal Aid (RAG)"

# --- AUDIO PLAYBACK LOGIC ---
if st.session_state.play_audio:
    try:
        audio_bytes = base64.b64decode(st.session_state.play_audio)
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    except Exception as e:
        st.error(f"Could not play audio. Error: {e}")
    st.session_state.play_audio = None

# --- SIDEBAR ---
with st.sidebar:
    st.title("Settings")
    selected_lang_name = st.selectbox("Select Language", options=list(LANGUAGES.keys()))
    st.session_state.language_code = LANGUAGES[selected_lang_name]
    st.session_state.chat_mode = st.radio("Select Chat Mode", options=["Legal Aid (RAG)", "General Chat"])
    st.divider()
    st.title("Find Legal Aid")
    city_input = st.text_input("Enter your city")
    if st.button("Search for Aid"):
        with st.spinner("Searching..."):
            if city_input:
                try:
                    res = requests.get(AID_API_URL, params={"city": city_input})
                    if res.status_code == 200:
                        data = res.json()
                        if isinstance(data, list) and data:
                            for center in data:
                                st.success(f"**{center['name']}**")
                                st.write(f"📍 {center['address']}\n\n📞 {center['phone_number']}")
                                st.divider()
                        else: st.warning(f"No centers found for '{city_input}'.")
                    else: st.error("Server error.")
                except requests.RequestException: st.error("Connection failed.")
            else: st.warning("Please enter a city name.")
    st.divider()
    st.write("Or Speak Your Question:")
    audio_input = mic_recorder(start_prompt="🎤 Record", stop_prompt="⏹️ Stop", key='recorder')

# --- MAIN CHAT INTERFACE ---
st.title(f"⚖️ {BOT_NAME}")
st.caption(f"Mode: {st.session_state.chat_mode} | Language: {selected_lang_name}")

# Display entire chat history from session state
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        # Handling for User messages
        if msg["role"] == "user":
            if st.session_state.editing_index == i:
                # EDIT VIEW
                edited_text = st.text_area("Edit message:", value=msg["content"], key=f"edit_{i}")
                save_col, cancel_col = st.columns(2)
                if save_col.button("✅ Save", key=f"save_{i}"):
                    st.session_state.messages[i]["content"] = edited_text
                    # Delete the old response and get a new one
                    if (i + 1) < len(st.session_state.messages) and st.session_state.messages[i+1]["role"] == "assistant":
                        del st.session_state.messages[i+1]
                    st.session_state.editing_index = None
                    st.rerun() # Rerun to exit edit mode and trigger a new response
                if cancel_col.button("❌ Cancel", key=f"cancel_{i}"):
                    st.session_state.editing_index = None
                    st.rerun()
            else:
                # NORMAL VIEW with buttons
                col1, col2, col3 = st.columns([0.85, 0.075, 0.075])
                col1.write(msg["content"])
                if "[Audio Question]" not in msg["content"]:
                    if col2.button("✏️", key=f"editbtn_{i}", help="Edit message"):
                        st.session_state.editing_index = i
                        st.rerun()
                if col3.button("🗑️", key=f"delbtn_{i}", help="Delete message & response"):
                    # Delete this message and the next if it's the bot's response
                    del st.session_state.messages[i]
                    if i < len(st.session_state.messages) and st.session_state.messages[i]["role"] == "assistant":
                        del st.session_state.messages[i]
                    st.rerun()
        # Handling for Assistant messages
        else:
            col1, col2 = st.columns([0.9, 0.1])
            col1.write(msg.get("content", ""))
            if msg.get("audio_base64"):
                if col2.button("🔊", key=f"play_{i}", help="Read aloud"):
                    st.session_state.play_audio = msg["audio_base64"]
                    st.rerun()

# This block checks if the last message in the state is a user message needing a response.
# This is crucial for handling re-submissions after an edit.
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_message = st.session_state.messages[-1]
    # Check if this user message already has an assistant response after it
    if len(st.session_state.messages) < 2 or st.session_state.messages[-2] != user_message:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        CHAT_API_URL,
                        data={'language': st.session_state.language_code, 'mode': st.session_state.chat_mode, 'text_query': user_message['content']},
                        timeout=180
                    )
                    if response.status_code == 200:
                        response_data = response.json()
                        text_answer = response_data.get("text_answer", "Error.")
                        audio_base64 = response_data.get("audio_answer_base64")
                        st.write(text_answer)
                        # Add new assistant message to state
                        st.session_state.messages.append({"role": "assistant", "content": text_answer, "audio_base64": audio_base64})
                except Exception as e:
                    st.error(f"Connection error: {e}")

# Handle new user input from chat box
if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Handle new audio input
if audio_input:
    with st.chat_message("user"):
        st.write("[Audio Question]")
        st.audio(audio_input['bytes'])
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    CHAT_API_URL,
                    data={'language': st.session_state.language_code, 'mode': st.session_state.chat_mode},
                    files={'audio_file': audio_input['bytes']},
                    timeout=180
                )
                if response.status_code == 200:
                    response_data = response.json()
                    text_answer = response_data.get("text_answer", "Error.")
                    audio_base64 = response_data.get("audio_answer_base64")
                    st.write(text_answer)
                    # Add both user and assistant messages to state
                    st.session_state.messages.append({"role": "user", "content": "[Audio Question]"})
                    st.session_state.messages.append({"role": "assistant", "content": text_answer, "audio_base64": audio_base64})
            except Exception as e:
                st.error(f"Connection error: {e}")