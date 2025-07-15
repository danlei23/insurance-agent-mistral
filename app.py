import streamlit as st
from agents.insurance_agent_mistral import InsuranceAgent  
import logging

# Initialize the insurance agent with empty config
agent = InsuranceAgent(config={})
# Set up logger for error tracking
logger = logging.getLogger(__name__)
# Configure Streamlit page appearance
st.set_page_config(
    page_title="🏠 Insurance Coverage Checker",
    page_icon="💬",
    layout="wide"
)
# Page title and instruction
st.title("🏠 Insurance Coverage Checker (Local Mistral)")
st.markdown("Ask any insurance coverage question based on your policy file.")

# Initialize session state for storing chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Main chat input logic
if user_input := st.chat_input("Ask about your insurance coverage..."):
    # Show user message on screen and store it
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Display assistant response box with spinner while processing
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Send user query to the agent
                result = agent.process_message(user_input)
                # Extract response (or show fallback error message)
                response = result.get("response", "❌ Failed to respond")
                # Display and save assistant response
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        # Show error message on the UI and log it
        st.error(f"❌ Error: {str(e)}")
        logger.error(f"Streamlit error: {str(e)}")
