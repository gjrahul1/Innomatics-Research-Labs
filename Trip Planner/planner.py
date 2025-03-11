import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import json
import re

api_key = st.secrets['gemini_key']

# Output Parser
def output_parse(raw_result: str) -> dict:
    try:
        # Attempt to extract JSON from the raw result (remove non-JSON text)
        json_match = re.search(r'\{.*\}', raw_result, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            parsed = json.loads(json_str)
            return parsed
        else:
            raise ValueError("No valid JSON found in the response")
    except Exception as e:
        print(f"Failed to parse JSON: {raw_result}")  # Debug output
        return {"road": "No plan available", "train": "No plan available", "flight": "No plan available"}

# Core Method
def plan_trip(current_location: str, destination: str) -> dict:
    # Model Selection with a valid model name
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

    # Updated Prompt Template with strict JSON instruction
    prompt_template = PromptTemplate(
        input_variables=["current_location", "destination"],
        template=(
            "Provide the best travel route from {current_location} to {destination}. "
            "Include the travel cost and which route is best to take given the cost and the time it takes to reach the {destination}. "
            "Return ONLY a JSON Object with keys 'road', 'train', and 'flight'. "
            "Each key should contain a nested object with fields: 'best_route', 'description', 'estimated_travel_time', 'estimated_cost' (as a nested object), 'total_estimated_cost', 'pros' (as a list), and 'cons' (as a list). "
            "Do NOT include any additional text outside the JSON object. "
            "Example: "
            "{{'road': {{'best_route': 'Route via NH44', 'description': 'Scenic drive', 'estimated_travel_time': '10h', 'estimated_cost': {{'fuel': '₹3000'}}, 'total_estimated_cost': '₹3500', 'pros': ['Flexible'], 'cons': ['Tiring']}}, "
            "'train': {{...}}, 'flight': {{...}}}}"
        )
    )

    # Chaining
    chain = prompt_template | llm

    # Raw Results
    raw_result = chain.invoke({"current_location": current_location, "destination": destination})

    # Content from results
    result_content = raw_result.content

    # Cleaned Results
    result = output_parse(result_content)

    return result