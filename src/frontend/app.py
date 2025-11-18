import streamlit as st
from pathlib import Path
from http_service import api_service
import requests

st.title("💬 Simple Chat App")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0  # used to reset uploader

uploaded = st.file_uploader("Choose a PDF", type=["pdf"])


# --- Load external CSS ---
def local_css(file_name):
    css_path = Path(file_name)
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Could not find CSS file: {file_name}")

local_css("./frontend/style.css")




# --- Chat input ---
user_input = st.text_input("Type a message and press Enter...")

st.session_state.setdefault("uploaded_pdf", None)
# --- File upload below input ---
# uploaded = st.file_uploader("📎 Attach a PDF (optional)", type=["pdf"])
# if uploaded:
#     st.session_state.uploaded_pdf = uploaded
#     st.success(f"📄 Uploaded: {uploaded.name}")

# --- When user sends message ---
if user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})

    # if st.session_state.uploaded_pdf:
    #     bot_reply = f"(PDF attached: {st.session_state.uploaded_pdf.name}) You said: {user_input}"
    # else:
    bot_reply = api_service.query_bot(user_query=user_input).get("content", "Error: No response from bot.")

    st.session_state.messages.append({"role": "bot", "text": bot_reply})
    #st.experimental_rerun()



if uploaded is not None:
    upload_response = api_service.upload_pdf(uploaded)
    st.session_state.messages.append({"role": "bot", "text": upload_response})

    # ---- Clear uploader ----
    st.session_state.uploader_key += 1  # force Streamlit to recreate the widget
    st.rerun()


# Display chat history
for msg in st.session_state.messages:
    role = msg["role"]
    text = msg["text"]
    align_class = "user" if role == "user" else "bot"
    msg_class = "user-msg" if role == "user" else "bot-msg"

    st.markdown(
        f"""
        <div class="chat-row {align_class}">
            <div class="{msg_class}">
                <b>{'You' if role == 'user' else 'Bot'}:</b> {text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

if st.button("🧹 Clear chat"):
    st.session_state.messages.clear()
    st.rerun()   # Refresh app to clear the screen