#!/usr/bin/env python3

import sys
import os
from typing import Optional
from datetime import datetime
import argparse

from src.agent.llm.ollama.client import OllamaAgent
from src.agent.context.conversation_manager import ConversationManager
from src.memory.chroma.queries.storage import MemoryManager

class JeffCLI:
    def __init__(self):
        self.jeff = OllamaAgent()
        self.conversation = ConversationManager()
        self.memory = MemoryManager()
        
        # CLI state
        self.debug_mode = False
        self.show_context = False
        self.user_id = "cli_user"
        
    def print_banner(self):
        banner = """
==========================================
             JEFF CLI v1.0                
==========================================
Commands:
  /debug    - Toggle debug mode
  /context  - Show conversation context
  /clear    - Clear conversation history
  /help     - Show this help message
  /exit     - Exit the chat
"""
        print(banner)
        
    def handle_command(self, command: str) -> bool:
        """Handle CLI commands. Returns True if should continue."""
        if command == "/exit":
            return False
        elif command == "/debug":
            self.debug_mode = not self.debug_mode
            print(f"Debug mode: {'on' if self.debug_mode else 'off'}")
        elif command == "/context":
            self.show_context = not self.show_context
            print(f"Context display: {'on' if self.show_context else 'off'}")
        elif command == "/clear":
            self.conversation = ConversationManager()
            print("Conversation history cleared")
        elif command == "/help":
            self.print_banner()
        else:
            print(f"Unknown command: {command}")
        return True
        
    def chat_loop(self):
        """Main chat loop"""
        self.print_banner()
        
        while True:
            try:
                # Get user input
                user_input = input("You: ")
                
                # Handle commands
                if user_input.startswith("/"):
                    if not self.handle_command(user_input):
                        break
                    continue
                
                # Store interaction
                self.conversation.add_message(self.user_id, user_input, "user")
                
                # Get context if enabled
                context = self.conversation.get_context(self.user_id) if self.show_context else None
                
                if self.debug_mode:
                    print(f"Context: {context}")
                
                # Generate response
                response = self.jeff.generate_response(user_input, context)
                
                # Store response
                self.conversation.add_message(self.user_id, response, "assistant")
                
                # Print response
                print(f"JEFF: {response}")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                if self.debug_mode:
                    import traceback
                    traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description='JEFF CLI')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--context', action='store_true', help='Show conversation context')
    args = parser.parse_args()
    
    cli = JeffCLI()
    cli.debug_mode = args.debug
    cli.show_context = args.context
    cli.chat_loop()

if __name__ == "__main__":
    main() 