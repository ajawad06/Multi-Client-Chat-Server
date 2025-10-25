# 🗨️ Chat Application

A console-based chat application built in **Python** that allows multiple clients to communicate simultaneously through a central **TCP server**.  

---

## 🚀 Features
- 📡 Multi-threaded server to handle multiple clients concurrently
- 📢 Broadcast messaging
- 💌 Private/unicast messaging using `@username`
- 🔔 Join/leave notifications
- 🔒 Unique usernames (prevents duplicates)    
- 🌈 Color-coded terminal messages:
  - 🟩 Green → user joined  
  - 🔵 Blue → private message  
  - 🔴 Red → user left   

---

## 🛠️ Tech Stack
- Python
- Socket Programming
- TCP
  
---

## 🧩 Files
| File | Description |
|------|--------------|
| `chat_server.py` | Contains the server code that handles clients, broadcasting, and unicast messaging. |
| `chat_client.py` | The client-side script that connects to the server, sends messages, and receives updates. |

---

## ⚙️ How to Run

### Step 1: Start the Server
```bash
python chat_server.py
```
### Step 2: Run Clients
Open multiple terminals and run:
```bash
python chat_client.py
```
