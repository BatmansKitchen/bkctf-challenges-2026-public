import os, socket, threading, verify

WELCOME_MESSAGE = f"""
Finish the code below (send two consecutive empty lines to submit):
{verify.SUBMISSION_TEMPLATE}"""

with open("server/submission_index.txt", 'r') as f:
    submission_index = int(f.read().strip())

def handle_client(client_socket, client_address):
    """Handle a single client connection in a separate thread"""
    print(f"New connection from {client_address}")

    global submission_index
        
    try:
        client_socket.sendall(WELCOME_MESSAGE.encode('utf-8'))
    
        client_file = client_socket.makefile('r', encoding='utf-8')
        lines = []
        consecutive_empty = 0
        for line in client_file:
            stripped = line.rstrip('\n')
            if stripped == '':
                consecutive_empty += 1
                if consecutive_empty >= 2:
                    break
            else:
                consecutive_empty = 0
            lines.append(stripped)

        response = '\n'.join(lines)
        
        submission_index += 1
        with open("server/submission_index.txt", 'w') as f:
            f.write(str(submission_index))
        client_socket.sendall(("Submission Received. Testing now \n\r").encode('utf-8'))
        client_socket.sendall(verify.main("submissions/submission" + str(submission_index) + ".lean", response).encode('utf-8'))

    except Exception as e:
        print(f"Error with client {client_address}: {str(e)}")
    finally:
        client_socket.close()
        print(f"Connection closed: {client_address}")

def main():
    HOST = '0.0.0.0'
    PORT = int(os.getenv('PORT', 5000))
    # MAX_CONNECTIONS = int(os.getenv('MAX_CONNECTIONS', 50))
    
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