import sys
import ollama

print(f"--- System Check ---")
print(f"Python Version: {sys.version}")

try:
    # Fix for the new Ollama library version
    response = ollama.list()
    print("Ollama Connection: SUCCESS")

    # Check for the 'models' attribute and access name properly
    models = [m.model for m in response.models]
    print(f"Available Models: {models}")
except Exception as e:
    print(f"Ollama Connection: FAILED. Error: {e}")