import torch
import sys

def verify_pytorch():
    print(f"Python version: {sys.version}")
    try:
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"CUDA version: {torch.version.cuda}")
            print(f"Device count: {torch.cuda.device_count()}")
            print(f"Current device: {torch.cuda.get_device_name(0)}")
        else:
            print("CUDA is NOT available. Using CPU.")
    except ImportError:
        print("PyTorch is not installed or import failed.")

if __name__ == "__main__":
    verify_pytorch()
