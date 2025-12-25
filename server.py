import socket
import json
import time
from datetime import datetime

def add(a, b):
    return a + b

def get_time():
    return datetime.now().isoformat()

def reverse_string(s):
    return s[::-1]

def handle_request(data):
    try:
        request = json.loads(data)
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("request_id")
        
        print(f"Processing request {request_id}: {method} {params}")
        
        print("Simulating server delay (5 seconds)")
        time.sleep(5)
        
        if method == "add":
            result = add(params.get("a", 0), params.get("b", 0))
        elif method == "get_time":
            result = get_time()
        elif method == "reverse":
            result = reverse_string(params.get("s", ""))
        else:
            return json.dumps({
                "request_id": request_id,
                "result": f"Unknown method: {method}",
                "status": "ERROR"
            })
        
        return json.dumps({
            "request_id": request_id,
            "result": result,
            "status": "OK"
        })
        
    except Exception as e:
        return json.dumps({
            "request_id": request.get("request_id", "unknown"),
            "result": f"Server error: {str(e)}",
            "status": "ERROR"
        })

def start_server(host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print(f"RPC Server listening on {host}:{port}")
    print(f"Available methods: add, get_time, reverse")
    print(f"Artificial delay: 5 seconds (for timeout demonstration)")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"New connection from {addr[0]}:{addr[1]}")
            
            try:
                data = conn.recv(1024).decode('utf-8')
                if data:
                    print(f"Received: {data[:80]}...")
                    response = handle_request(data)
                    conn.sendall(response.encode('utf-8'))
                    print(f"Sent response: {response[:80]}...")
                    
            except Exception as e:
                print(f"Error handling request: {e}")
            finally:
                conn.close()
                print(f"Connection closed\n")
                
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    finally:
        server_socket.close()
        print("Server socket closed")

if __name__ == "__main__":
    start_server()