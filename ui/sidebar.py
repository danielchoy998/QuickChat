import streamlit as st
import os
from utils import download_hf_model

def render_sidebar():
    # Sidebar for model configuration
    with st.sidebar:
        st.header("Model Configuration")
        
        # Choose between local and HuggingFace
        model_source = st.radio(
            "Model Source",
            ["Local File", "HuggingFace Hub"]
        )
        
        if model_source == "Local File":
            # Local model path input
            model_path = st.text_input(
                "Model Path",
                placeholder="Enter the full path of GGUF model file"
            )
            
            # Show if model exists
            if model_path:
                if os.path.exists(model_path):
                    st.success("Model found")
                    st.caption(f"Size: {os.path.getsize(model_path) / (1024**3):.2f} GB")
                else:
                    st.error("Model not found")
                    st.info("Path is invalid")
        
        else:  # HuggingFace Hub
            st.markdown("---")
            
            # Direct input method
            hf_repo = st.text_input(
                "Repository ID",
                placeholder="eg. Qwen/Qwen3-0.6B-GGUF"
            )
            
            hf_filename = st.text_input(
                "GGUF Filename",
                placeholder="eg. Qwen3-0.6B-Q8_0.gguf"
            )
            
            # Browse available files
            if st.button("Browse Available Files"):
                if hf_repo:
                    with st.spinner("Fetching files..."):
                        from utils import list_gguf_files
                        gguf_files = list_gguf_files(hf_repo)
                        
                        if gguf_files:
                            st.success(f"Found {len(gguf_files)} GGUF files:")
                            for file in gguf_files:
                                st.code(file)
                        else:
                            st.error("No GGUF files found")
                else:
                    st.warning("Enter a repository ID first")
            
            # Download button
            if st.button("Download", type="primary"):
                if not hf_repo or not hf_filename:
                    st.error("Please provide both Repository ID and Filename")
                else:
                    with st.spinner(f"Downloading {hf_filename}..."):
                        downloaded_path, error = download_hf_model(hf_repo, filename=hf_filename)
                    
                    if error:
                        st.error(error)
                    else:
                        st.success("Download complete")
                        st.session_state.downloaded_model_path = downloaded_path
                        st.caption(f"Path: {downloaded_path}")
            
            # Use downloaded model if available
            if "downloaded_model_path" in st.session_state:
                model_path = st.session_state.downloaded_model_path
                st.info(f"Using: {os.path.basename(model_path)}")
                st.caption(f"Size: {os.path.getsize(model_path) / (1024**3):.2f} GB")
            else:
                model_path = None
                st.warning("Download a model first")
        
        st.markdown("---")
        
        # Temperature slider
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        
        # System prompt
        system_prompt = st.text_area(
            "System Prompt", 
            value="You are a helpful AI assistant."
        )
        
        # Clear and Export buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear Chat"):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.button("Export"):
                st.session_state.show_export = True
        
        # Google Sheets export
        if st.session_state.get("show_export", False):
            st.markdown("---")
            
            sheet_url = st.text_input(
                "Google Sheet URL",
            )
            
            if st.button("Export to Google Sheets"):
                if sheet_url:
                    from export import export_to_google_sheets
                    
                    # Extract model name from path
                    model_display_name = "unknown"

                    if model_path:
                        model_display_name = os.path.basename(model_path)
                    
                    success, message = export_to_google_sheets(
                        st.session_state.messages,
                        sheet_url,
                        model_name=model_display_name
                    )
                    
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.warning("Enter a Google Sheet URL")
            
            if st.button("Close"):
                st.session_state.show_export = False
                st.rerun()

    return model_path, temperature, system_prompt