import streamlit as st
from backend_process import response

st.title("Data Science Tutor")

if "messages" not in st.session_state:
    st.session_state['messages'] = []

for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.write(message['content'])

# Chat Input        
input_field = st.chat_input("Ask me anything!")

# File Upload
with st.sidebar:

    st.markdown("""
    ## About
    This app is an LLM-powered chatbot built using:
                
    * Langchain

    *  Gemini 1.5 pro

    ## Usage
    * This app solves your doubts just like your mentor!

    * Real Insights 🔎

    * Precise Solutions ⌛

    * In-depth 💭            
    
""")
    
    st.subheader("Upload Files")
    uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True, type=['jpeg', 'jpg', 'png', 'csv'])

    st.markdown("Developed by **G.J.Rahul**")

if input_field and input_field.strip():
    user_message = {'role': 'user', 'content': input_field}
    st.session_state['messages'].append(user_message)

    # Display user input
    st.write(f"**User:** {input_field}")

    # Process files
    file_content_list = [file.name for file in uploaded_files] if uploaded_files else []

    # Files name display
    if file_content_list:
        st.write(f"**Files Received:** {', '.join(file_content_list)}")

    # AI Response
    ai_response = response(input_field, uploaded_files or [])  # Ensure uploaded_files is a list

    # Chatbot Response
    bot_message = {'role': 'assistant', 'content': ai_response}
    st.session_state['messages'].append(bot_message)

    with st.chat_message('assistant'):
        st.write(ai_response)
