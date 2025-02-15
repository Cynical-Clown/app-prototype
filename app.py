import streamlit as st
import replicate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App title and description
st.set_page_config(page_title="DxVar: Genomic Analysis Assistant")
st.title("DxVar")
st.write("Powered by Llama-2 and Replicate")

# Ensure API token is available
API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not API_TOKEN:
    st.error("API token not found! Please set `REPLICATE_API_TOKEN` in your environment.")
    st.stop()
os.environ['REPLICATE_API_TOKEN'] = API_TOKEN

# Model configuration
MODEL_NAME = "meta/llama-2-7b"  # Fixed model
TEMPERATURE = 0.7
TOP_P = 0.95
MAX_TOKENS = 1000

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Welcome to DxVar! How can I assist you with genomic research and variant analysis?"}]

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# System prompt for the assistant
SYSTEM_PROMPT = """
You are an advanced assistant specializing in genomic research and variant analysis.
1. Interpret and provide information about gene-disease relationships.
2. Answer user queries with clear and concise responses.
3. Offer feedback if data is missing.
"""

# Function to generate response using Replicate API
def generate_response(user_input):
    full_prompt = f"""
    {SYSTEM_PROMPT}

    User Query: {user_input}

    Assistant's Detailed Response:
    """
    try:
        # Call the model via the API
        output = replicate.run(
            MODEL_NAME,
            input={
                "prompt": full_prompt,
                "max_tokens": MAX_TOKENS,
                "temperature": TEMPERATURE,
                "top_p": TOP_P,
            },
        )

        # Join list of strings if output is fragmented and remove redundancies
        if isinstance(output, list):
            cleaned_output = "".join(output).strip()  # Combine fragments
            lines = cleaned_output.split("\n")
            deduplicated = []
            seen = set()
            for line in lines:
                if line.strip() and line not in seen:  # Avoid duplicate lines
                    deduplicated.append(line.strip())
                    seen.add(line.strip())
            return "\n".join(deduplicated)  # Join cleaned lines
        return output or "No response generated."
    except Exception as e:
        return f"Error: {str(e)}"

# Handle user input
if user_input := st.chat_input("Enter your query about genomic research and variant analysis..."):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            response = generate_response(user_input)
            st.write(response)
            st.session_state["messages"].append({"role": "assistant", "content": response})

# Clear chat history button
if st.sidebar.button("Clear Chat History"):
    st.session_state["messages"] = [{"role": "assistant", "content": "Welcome to DxVar! How can I assist you with genomic research and variant analysis?"}]
