# Simple-Delay-Sync-Service-  

## Requirements:  
  **Operating System:** Linux  
## Checklist:  
- Part 1: 
  - [ ] Run every function in the skeleton that ends with _thread in its own thread
  - [ ] Setup the TCP socket and start accepting clients (tcp_server_thread)
  - [ ] Setup the UDP socket and send broadcasts (send_broadcast_thread) 
  - [ ] Parse received broadcasts (receive_broadcast_thread) 
- Part 2:
  - [ ] Accept TCP clients and send them the node's timestamp (tcp_server_thread)
  - [ ] Initiate TCP connection to newly discovered nodes and exchange timestamps (exchange_timestamps_thread)
  - [ ] Refresh neighbor information every 10 broadcasts
