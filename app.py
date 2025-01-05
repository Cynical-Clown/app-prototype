
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
MODEL_NAME = "replicate/meta-llama-2-7b"  # Replace with your Replicate model name
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
            full_prompt = SYSTEM_PROMPT + f"\nUser: {user_input}\nAssistant:"
            
            # Call the Replicate API
            try:
                # Call the model and handle the output
                output = client.run(
                    MODEL_NAME,
                    input={"prompt": full_prompt, "max_tokens": 200}
                )
                
                # Handle and display the response
                if isinstance(output, list):
                    st.success("Response:")
                    st.write(output[0])  # If the output is a list, show the first item
                else:
                    st.success("Response:")
                    st.write(output)  # If it's a string or other type, display directly
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a question.")
