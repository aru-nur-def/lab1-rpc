import socket
import json
import uuid
import time

SERVER_IP = "18.206.165.165"
PORT = 5000
TIMEOUT = 2
MAX_RETRIES = 3

class RPCClient:
    def __init__(self, server_ip, port=5000, timeout=2, max_retries=3):
        self.server_ip = server_ip
        self.port = port
        self.timeout = timeout
        self.max_retries = max_retries
    
    def call(self, method, params):
        request_id = str(uuid.uuid4())
        request = {
            "request_id": request_id,
            "method": method,
            "params": params
        }
        request_json = json.dumps(request)
        
        print(f"Calling {method} with params: {params}")
        print(f"Request ID: {request_id}")
        
        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"\nAttempt {attempt}/{self.max_retries}")
                
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(self.timeout)
                
                print(f"Connecting to {self.server_ip}:{self.port}")
                client_socket.connect((self.server_ip, self.port))
                print("Connected")
                
                print(f"Sending: {request_json}")
                client_socket.send(request_json.encode('utf-8'))
                
                print("Waiting for response")
                response = client_socket.recv(1024).decode('utf-8')
                client_socket.close()
                
                response_data = json.loads(response)
                print(f"Response: {response_data}")
                
                if response_data.get("status") == "OK":
                    print(f"SUCCESS. Result: {response_data.get('result')}")
                    return response_data.get("result")
                else:
                    print(f"Server error: {response_data.get('result')}")
                    
            except socket.timeout:
                print(f"Timeout. No response in {self.timeout} seconds")
            except ConnectionRefusedError:
                print("Connection refused. Server may be down")
            except Exception as e:
                print(f"Error: {type(e).__name__}: {e}")
            
            if attempt < self.max_retries:
                print("Retrying in 1 second")
                time.sleep(1)
        
        print(f"FAILED: All {self.max_retries} attempts failed")
        return None

def main():
    print("=" * 50)
    print("RPC CLIENT - Distributed Computing Lab 1")
    print(f"Server: {SERVER_IP}:{PORT}")
    print(f"Timeout: {TIMEOUT}s | Max retries: {MAX_RETRIES}")
    print("=" * 50)
    
    client = RPCClient(SERVER_IP, PORT, TIMEOUT, MAX_RETRIES)
    
    print("\n" + "=" * 30)
    print("TEST 1: Addition")
    print("=" * 30)
    result = client.call("add", {"a": 5, "b": 7})
    
    print("\n" + "=" * 30)
    print("TEST 2: Get Server Time")
    print("=" * 30)
    result = client.call("get_time", {})
    
    print("\n" + "=" * 30)
    print("TEST 3: Reverse String")
    print("=" * 30)
    result = client.call("reverse", {"s": "hello"})
    
    print("\n" + "=" * 50)
    print("ALL TESTS COMPLETED")
    print("=" * 50)

if __name__ == "__main__":
    main()