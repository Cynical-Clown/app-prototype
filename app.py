import streamlit as st
import replicate
import os
from dotenv import load_dotenv

# Load environment variables for local development
load_dotenv()

# Define the system prompt
SYSTEM_PROMPT = """
You are an advanced assistant specializing in genomic research and variant analysis.
1. Interpret and provide information about gene-disease relationships.
2. Answer user queries with clear and concise responses.
3. Offer feedback if data is missing.
"""

# Replicate API setup
API_TOKEN = os.getenv("REPLICATE_API_TOKEN")  # Use environment variable
if not API_TOKEN:
    st.error("API token not found! Please set `REPLICATE_API_TOKEN` in your environment or Streamlit Secrets.")
    st.stop()

MODEL_NAME = "meta/llama-2-7b"  # Replace with your Replicate model name

client = replicate.Client(api_token=API_TOKEN)

# Streamlit app UI
st.title("DxVar")
st.write("Powered by Llama-2 and Replicate")

# Input section
user_input = st.text_input("Enter your question:")
if st.button("Submit"):
    if user_input:
        with st.spinner("Processing..."):
            # Combine system prompt and user input
            full_prompt = f"""
            {SYSTEM_PROMPT}

            User Query: {user_input}

            Assistant's Detailed Response:
            """

            # Call the Replicate API
            try:
                output = client.run(
                    MODEL_NAME,
                    input={
                        "prompt": full_prompt,
                        "max_tokens": 1000,  # Allow longer responses
                        "temperature": 0.7,
                        "top_p": 0.95
                    }
                )
                # Handle and display the response
                if isinstance(output, list) and len(output) > 0:
                    response = output[0]
                else:
                    response = output or "No response generated."  # Provide default if output is None
                st.success("Response:")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a question.")
