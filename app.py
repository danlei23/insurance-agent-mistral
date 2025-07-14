import streamlit as st
from agents.insurance_agent_mistral import InsuranceAgent  
import logging


agent = InsuranceAgent(config={})
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="🏠 Insurance Coverage Checker",
    page_icon="💬",
    layout="wide"
)

st.title("🏠 Insurance Coverage Checker (Local Mistral)")
st.markdown("Ask any insurance coverage question based on your policy file.")

if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if user_input := st.chat_input("Ask about your insurance coverage..."):
    
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = agent.process_message(user_input)
                response = result.get("response", "❌ Failed to respond")

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        logger.error(f"Streamlit error: {str(e)}")
