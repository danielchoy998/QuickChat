import streamlit as st
import os 

# Auto-install llama-cpp-python if not installed (must run before importing inference)
try:
    import llama_cpp
except ImportError:
    st.warning("⏳ Installing llama-cpp-python... This may take a few minutes.")
    from utils import install_llama_cpp
    if install_llama_cpp():
        st.success("✅ Installation complete! Please refresh the page.")
        st.stop()
    else:
        st.error("❌ Installation failed. Please install manually: pip install llama-cpp-python")
        st.stop()

from inference import load_model, inference
from ui.sidebar import render_sidebar

st.title("Model Testing Platform")

# Render sidebar and get configuration
model_path, temperature, system_prompt = render_sidebar()

# Load model (cached - only loads once per model path)
@st.cache_resource
def get_model(model_path):
    """Cache the loaded model to avoid reloading on every interaction"""
    if not model_path or not os.path.exists(model_path):
        st.error(f"Model not found at: {model_path}")
        return None
    
    with st.spinner(f"Loading model from {model_path}..."):
        return load_model(model_path)

def main():
    # Initialize chat history (simple format)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    prompt = st.chat_input("Type your message here...")

    # Handle user input
    if prompt:
        # Load the model
        llm = get_model(model_path)
        
        if llm is None:
            st.error("Please provide a valid model path.")
            st.stop()
        
        # Add user message to chat history and display
        user_message = {"role": "user", "content": prompt}
        st.session_state.messages.append(user_message)
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Prepare messages for inference (include system prompt)
        inference_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = inference(llm, inference_messages, temperature=temperature)
            st.markdown(response)
        
        # Add assistant response to chat history
        assistant_message = {"role": "assistant", "content": response}
        st.session_state.messages.append(assistant_message)

if __name__ == "__main__":
    main()