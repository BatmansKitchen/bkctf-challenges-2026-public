import os
import sys
import time
import threading
import socket
import os
import hashlib
import binascii
from openai import OpenAI

SOCKET_TIMEOUT = 60

class AnimationController:
    def __init__(self, client_socket):
        self.running = False
        self.thread = None
        self.client_socket = client_socket
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        try:
            self.client_socket.sendall(b"\r" + b" " * 50 + b"\r")
        except:
            pass
    
    def _animate(self):
        frames = [".", "..", "..."]
        frame_idx = 0
        
        while self.running:
            try:
                message = f"\rPlease hold, DM is rolling dice{frames[frame_idx]}"
                self.client_socket.sendall(message.encode('utf-8'))
                frame_idx = (frame_idx + 1) % len(frames)
                time.sleep(0.5)
            except:
                break

def call_chatgpt(conversation_history, animator):
    """Call ChatGPT API with the conversation history"""
    api_key = os.getenv("OPENAI_API_KEY")
    flag    = os.getenv("FLAG")

    client = OpenAI(api_key=api_key)
    
    if not api_key:
        return "Error: OPENAI_API_KEY environment variable not set"
    
    try:
        animator.start()
        response = client.responses.create(
            prompt={
                "id": "pmpt_696d31b95254819480ae6229722c58000dce4d80147d1047",
                "variables": {
                "flag": flag
                }
            },
            input=conversation_history
        )

        animator.stop()
        return response.output_text
    
    except Exception as e:
        animator.stop()
        return f"Error calling ChatGPT: {str(e)}"

def handle_client(client_socket, client_address):
    """Handle a single client connection in a separate thread"""
    print(f"New connection from {client_address}")

    client_socket.settimeout(SOCKET_TIMEOUT)

    try:
        # Proof of work
        challenge = binascii.hexlify(os.urandom(16)).decode()
        expected = hashlib.sha256(challenge.encode()).hexdigest()

        banner = f"""
=== Proof of Work Required ===

Run the following command and send ONLY the hex digest:

echo -n "{challenge}" | sha256sum | cut -d' ' -f1

Answer:
    """
        client_socket.sendall(banner.encode('utf-8'))
        response = client_socket.recv(1024).strip().decode()

        if response != expected:
            client_socket.sendall(b"Proof failed.\n")
            client_socket.close()
            return

        client_socket.sendall(b"Proof accepted.\n")

    except Exception:
        try:
            client_socket.sendall(b"Proof failed.\n")
        except:
            pass
        client_socket.close()
        return
        
    try:
        # Send welcome message
        welcome = "=== Dungeons and Dungeons ===\n\n"
        client_socket.sendall(welcome.encode('utf-8'))
        
        flag = os.getenv("FLAG")
        conversation_history = []
        animator = AnimationController(client_socket)
        
        # Initial game response
        response = "Torches flicker in the dank halls. You wake shackled to a stone bench. Somewhere deep below, legends say, the Flag warps reality itself. Heavy footsteps echo—what do you do?"
        client_socket.sendall(f"{response}\n\n".encode('utf-8'))
        
        conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Game loop
        while "YOU ARE DEAD" not in response.strip() and flag not in response.strip():
            # Send prompt
            client_socket.sendall(b"> ")
            
            # Receive user input
            data = b""
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    raise ConnectionError("Client disconnected")
                data += chunk
                if b'\n' in data:
                    break
            
            prompt = data.decode('utf-8').strip()
            
            if not prompt:
                continue
            
            conversation_history.append({
                "role": "user",
                "content": prompt
            })
            
            response = call_chatgpt(conversation_history, animator)
            client_socket.sendall(f"\n{response}\n\n".encode('utf-8'))
            
            conversation_history.append({
                "role": "assistant",
                "content": response
            })
        
        client_socket.sendall(b"Game Over!\n")
        
    except Exception as e:
        print(f"Error with client {client_address}: {str(e)}")
    finally:
        client_socket.close()
        print(f"Connection closed: {client_address}")

def main():
    HOST = '0.0.0.0'
    PORT = int(os.getenv('PORT', 5000))
    # MAX_CONNECTIONS = int(os.getenv('MAX_CONNECTIONS', 50)) # Turned off during CTF because some LLM was hogging all the ports.
    
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            
            # Create a new thread for each client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True
            )
            client_thread.start()
            
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()