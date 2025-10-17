
import os
import contextlib
from llama_cpp import Llama

def load_model(model_path):
    """
    Load the GGUF model once and cache it.
    This function should be cached by Streamlit with @st.cache_resource
    """
    if not model_path or not os.path.exists(model_path):
        raise ValueError("Please provide a valid model path")
    
    # Suppress llama.cpp initialization logs
    with open(os.devnull, 'w') as devnull:
        with contextlib.redirect_stderr(devnull):
            llm = Llama(
                model_path=model_path,
                n_ctx=1024,
                n_threads=4,
                n_batch=1,
                verbose=False,
            )
    
    print(f"✓ Model loaded successfully from {model_path}")
    return llm

def inference(llm, messages, temperature=0.7):
    """
    Run inference with the loaded model.
    
    Args:
        llm: Loaded Llama model instance
        messages: List of message dicts with 'role' and 'content'
        temperature: Sampling temperature
    
    Returns:
        str: Model's response
    """
    if not llm:
        return "Model not loaded"
    
    if not messages:
        return "No messages provided"
    
    try:
        output = llm.create_chat_completion(
            messages=messages,
            temperature=temperature,
        )
        
        response = output['choices'][0]['message']['content']
        return response
    except Exception as e:
        return f"Error during inference: {e}"

if __name__ == "__main__":
    model_path = "./models/Qwen/Qwen3-0.6B-GGUF/Qwen3-0.6B-Q8_0.gguf"
    
    # Load model once
    llm = load_model(model_path)
    
    # Run inference
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    response = inference(llm, messages)
    print(response)