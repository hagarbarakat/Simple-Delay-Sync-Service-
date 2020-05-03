# Simple-Delay-Sync-Service-  

## Requirements:  
  **Operating System:** Linux  
## Checklist:  
- Part 1: 
  - [x] Run every function that ends with _thread in its own thread
  - [x] Setup the TCP socket and start accepting clients (tcp_server_thread)
  - [x] Setup the UDP socket and send broadcasts (send_broadcast_thread) 
  - [x] Parse received broadcasts (receive_broadcast_thread) 
- Part 2:
  - [x] Accept TCP clients and send them the node's timestamp (tcp_server_thread)
  - [x] Initiate TCP connection to newly discovered nodes and exchange timestamps (exchange_timestamps_thread)
  - [x] Refresh neighbor information every 10 broadcasts
