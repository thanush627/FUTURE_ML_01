import streamlit as st
from google.cloud import dialogflow_v2 as dialogflow
import os
import uuid

# Set Google Credentials
os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "dialogflow-key.json")

# Dialogflow variables
PROJECT_ID = os.environ.get("DIALOGFLOW_PROJECT_ID", "customersupportbot-lvuh")

# Streamlit re-runs this whole script on every interaction, so a session id
# generated at module level would be new on every message - Dialogflow would
# treat each turn as a fresh conversation and lose all context between them.
# Storing it in session_state keeps one id for the life of the browser session.
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Function to detect intent
def detect_intent_texts(project_id, session_id, text, language_code='en'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text

# Streamlit UI
st.title("💬 Customer Support Chatbot")
st.markdown("Ask your question below:")

user_input = st.text_input("You:", "")

if user_input:
    response = detect_intent_texts(PROJECT_ID, st.session_state.session_id, user_input)
    st.text_area("Bot:", response, height=100)
