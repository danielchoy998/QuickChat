import os 
import sys
import platform
import subprocess
from huggingface_hub import snapshot_download

# ===Install the llama-cpp-python library===

def install_llama_cpp():
    """Automatically install llama-cpp-python based on the operating system"""
    
    # Check if llama_cpp is already installed
    try:
        import llama_cpp
        print("llama-cpp-python is already installed")
        return True
    except ImportError:
        print("llama-cpp-python not found. Installing...")
    
    # Detect operating system
    os_name = platform.system()
    
    try:
        if os_name == "Darwin":  # macOS
            print("Running on macOS - Installing with Metal support...")
            # Install with Metal GPU acceleration for macOS using pre-built wheels
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "llama-cpp-python",
                "--extra-index-url", "https://abetlen.github.io/llama-cpp-python/whl/metal"
            ], check=True)
            
        elif os_name == "Windows":
            print("Running on Windows - Installing...")
            
            # Standard CPU version:
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "llama-cpp-python"
            ], check=True)
            
            # For CUDA support (uncomment if you have NVIDIA GPU):
            # subprocess.run([
            #     sys.executable, "-m", "pip", "install", 
            #     "llama-cpp-python",
            #     "--extra-index-url", "https://abetlen.github.io/llama-cpp-python/whl/cu121"
            # ], check=True)
            
        elif os_name == "Linux":
            print("Running on Linux - Installing...")
            
            # Standard CPU version:
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "llama-cpp-python"
            ], check=True)
            
            # For CUDA support on Linux (uncomment if you have NVIDIA GPU):
            # subprocess.run([
            #     sys.executable, "-m", "pip", "install", 
            #     "llama-cpp-python",
            #     "--extra-index-url", "https://abetlen.github.io/llama-cpp-python/whl/cu121"
            # ], check=True)
        else:
            print(f"Unknown OS: {os_name}")
            return False
            
        print("llama-cpp-python installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        return False

def list_gguf_files(repo_id):
    """
    List all GGUF files in a HuggingFace repository without downloading.
    
    Args:
        repo_id: HuggingFace repository ID
    
    Returns:
        list: List of GGUF filenames, or None if error
    """
    try:
        from huggingface_hub import list_repo_files
        
        all_files = list_repo_files(repo_id)
        gguf_files = [f for f in all_files if f.endswith('.gguf')]
        return gguf_files

    except Exception as e:
        print(f"Error listing files: {e}")
        return None

def download_hf_model(repo_id, filename=None, local_dir=None):
    """
    Download a specific GGUF model from HuggingFace Hub.
    """
    if not repo_id:
        return None, "Repository ID is required"
    
    try:
        from huggingface_hub import hf_hub_download
        
        # If no filename specified, list available GGUF files
        if filename is None:
            gguf_files = list_gguf_files(repo_id)
            if not gguf_files:
                return None, f"No GGUF files found in {repo_id}"
            return gguf_files, None
        
        # Set default local directory
        if local_dir is None:
            local_dir = f"./models/{repo_id}"
        
        print(f"Downloading {filename} from {repo_id}...")
        
        # Download the file (progress shows in terminal)
        downloaded_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        
        print(f"Downloaded to: {downloaded_path}")
        return downloaded_path, None
        
    except Exception as e:
        return None, f"Error downloading model: {str(e)}"


# Run the installer
if __name__ == "__main__":
    install_llama_cpp()
    
    # Test download - Now requires repo_id and filename separately
    repo_id = "ggml-org/gemma-3-1b-it-GGUF"
    filename = "gemma-3-1b-it-Q4_K_M.gguf"
    
    print(f"\n=== Downloading {filename} from {repo_id} ===")
    model_path, error = download_hf_model(repo_id, filename=filename)
    if error:
        print(f"Error: {error}")
    else:
        print(f"Success! Model at: {model_path}")
