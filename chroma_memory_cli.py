#!/usr/bin/env python3

import argparse
from src.memory.chroma.queries.storage import MemoryManager
from src.agent.llm.ollama.client import OllamaAgent

class ChromaMemoryCLI:
    def __init__(self):
        self.memory = MemoryManager()
        self.agent = OllamaAgent()
        self.user_id = "cli_user"

    def store_message(self, message: str):
        """Store a message in the memory system."""
        embedding = self.agent.generate_embedding(message)
        self.memory.store_interaction(self.user_id, message, embedding)
        print(f"Stored message: {message}")

    def retrieve_context(self, limit: int = 5):
        """Retrieve the context for the user."""
        context = self.memory.retrieve_context(self.user_id, limit)
        print(f"Retrieved context:\n{context}")

    def run(self):
        """Run the CLI loop."""
        print("Chroma Memory CLI. Type 'exit' to quit.")
        while True:
            try:
                command = input("Enter command (store/retrieve/exit): ").strip().lower()
                if command == "exit":
                    break
                elif command == "store":
                    message = input("Enter message to store: ").strip()
                    self.store_message(message)
                elif command == "retrieve":
                    limit = int(input("Enter number of messages to retrieve: ").strip())
                    self.retrieve_context(limit)
                else:
                    print("Unknown command. Please use 'store', 'retrieve', or 'exit'.")
            except Exception as e:
                print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Chroma Memory CLI')
    args = parser.parse_args()
    
    cli = ChromaMemoryCLI()
    cli.run()

if __name__ == "__main__":
    main() 