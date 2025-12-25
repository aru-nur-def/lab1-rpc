# Lab 1: RPC Implementation on AWS EC2
## Video link: [https://docs.google.com/videos/d/1tuga3L940IQUg5qWzP_Fqjq-oMsgaqiCVLdov2XUPQc/edit?usp=sharing](https://docs.google.com/videos/d/1G_KkebVBt8KijHSq4DjAxU_JCAPOH3O9g0Y_oJ2_4jo/edit?usp=sharing)
## Project Overview
Simple RPC system on two AWS EC2 instances.

## Architecture
- **Server:** rpc-server-node (18.206.165.165:5000)
- **Client:** rpc-client-node (54.91.160.213)
- **Protocol:** TCP with JSON

## RPC Methods
- `add(a, b)` - Sum two numbers
- `get_time()` - Current server time
- `reverse(s)` - Reverse string

## Setup
### Server:
```bash
ssh -i "rpc-key.pem" ubuntu@18.206.165.165
python3 server.py
```

### Client:
```bash
ssh -i "rpc-key.pem" ubuntu@54.91.160.213
```
Edit `SERVER_IP` in `client.py` to `"18.206.165.165"`
```bash
python3 client.py
```

## Demo
- **Normal:** RPC calls work
- **Error demo:** Server delay=5s, client timeout=2s
- **Result:** 3 timeout attempts (shows retry logic)

## Files
- `client.py` - RPC client
- `server.py` - RPC server
- `requirements.txt` - Python dependencies

