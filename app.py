
import streamlit as st
import replicate

# Define the system prompt
SYSTEM_PROMPT = """
You are an advanced assistant specializing in genomic research and variant analysis.
1. Interpret and provide information about gene-disease relationships.
2. Answer user queries with clear and concise responses.
3. Offer feedback if data is missing.
"""

# Replicate API setup
API_TOKEN = "r8_5nmTGAw6deplpWf76NQjYBZg4cNTCvK14IaEg"  # Replace with your Replicate API token
MODEL_NAME = "replicate/meta/llama-2-7b"        # Replace with your Replicate model name
client = replicate.Client(api_token=API_TOKEN)

# Streamlit app UI
st.title("Llama AI Assistant")
st.write("Powered by Llama-2 and Replicate")

# Input section
user_input = st.text_input("Enter your question:")
if st.button("Submit"):
    if user_input:
        with st.spinner("Processing..."):
            # Combine system prompt and user input
            full_prompt = SYSTEM_PROMPT + f"
User: {user_input}
Assistant:"
            
            # Call the Replicate API
            try:
                output = client.run(
                    MODEL_NAME,
                    input={"prompt": full_prompt, "max_tokens": 200}
                )
                st.success("Response:")
                st.write(output)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")
