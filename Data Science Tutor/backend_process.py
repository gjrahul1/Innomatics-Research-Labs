from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import base64
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough

# Define API Key
gemini_key = st.secrets['gemini_key']

# Initialize memory buffer to store conversation history
memory = ConversationBufferMemory(return_messages=True)

def prompt_template():
    return PromptTemplate(
        input_variables=["raw_input", "files_data", "image_data", "history"],
        template = """
You are a data scientist who tailors your tone based on the seriousness of the query.

Guidelines:
- If the user's input or provided files (CSV or image) indicate a serious issue, respond using the detailed structure below (include only sections that apply):
    0. Problem Identification (if any)
    1. Key Points
    2. Introduction
    3. Flow Chart (if useful)
    4. Direct Answer
    5. Hybrid Approach (if relevant)
    6. How It Fits Your Workflow
    7. Conclusion
    8. Citation

- If the query is casual, reply in a friendly, brief manner with light humor.
- If the query is out of Data Science context, politely decline.

User Query: {raw_input}

Chat History: {history}

CSV Details: {files_data}

Image Details: {image_data}
"""
    )

def encode_image(image_file):
    # Convert image to base64 string
    image_bytes = image_file.read()
    return base64.b64encode(image_bytes).decode('utf-8')

def model_selection():
    return ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=gemini_key)

def response(raw_input, files=None):
    formated_prompt = prompt_template()
    model_ = model_selection()

    # Instead of a separate get_history function, merge the current conversation history directly.
    def merge_history(inputs):
        history = memory.load_memory_variables({}).get("history", "")
        inputs["history"] = history
        return inputs

    merge_history_runner = RunnablePassthrough(merge_history)
    
    # Chain using the pipe operator:
    # 1. merge_history_runner: Adds current conversation history.
    # 2. formated_prompt: Renders the prompt with all required variables.
    # 3. model_: Sends the prompt to the model.
    chain = merge_history_runner | formated_prompt | model_

    # Process files (CSV or image) into a format the model understands.
    file_content = ""
    encoded_image = None
    if files:
        for file in files:
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
                column_info = ",".join(df.columns)
                num_rows = len(df)
                sample_data = df.head(5).to_string(index=False)
                file_content = f"Columns: {column_info}\nTotal Rows: {num_rows}\nSample Data: {sample_data}"
            elif file.name.endswith((".png", ".jpeg", ".jpg")):
                encoded_image = encode_image(file)
            else:
                file_content = "unsupported file format"

    # Prepare inputs. Note that we include an "original_input" key for later memory logging.
    inputs = {
        "raw_input": raw_input,
        "files_data": file_content,
        "image_data": encoded_image,
        "original_input": raw_input
    }

    result = chain.invoke(inputs)

    # Save the conversation context so future calls can retrieve updated history.
    memory.save_context({"input": inputs["original_input"]}, {"output": result.content})
    return result.content
