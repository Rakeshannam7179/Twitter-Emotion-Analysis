try:
    import transformers
    print(f"Transformers location: {transformers.__file__}")
    from transformers import AutoModelForSequenceClassification
    print(f"AutoModelForSequenceClassification module: {AutoModelForSequenceClassification.__module__}")
    print("Successfully imported AutoModelForSequenceClassification")
except ImportError as e:
    print(f"Failed to import AutoTokenizer: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
