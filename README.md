# Audio Streaming Protocol
## To demo
1. ```git clone https://github.com/viny1ic/audio_streaming_protocol && cd audio_streaming_protocol```
2. In terminal 1: ```cd server && python3 server.py```
3. In terminal 2: ```cd client && python3 client.py```
4. Enter your choice as prompted by the client script into the terminal.

## Protocol Specification:
- The protocol is built on TCP
- The protocol follows a simple client-server architecture.
- The client sends a request for which the server sends an appropriate response
- The service runs on port 12000 of the server
### Packet Structure
![image](https://github.com/user-attachments/assets/0052eb3e-715c-4d1e-bf2b-f21f00292c02)
- header: Contains configuration and control information encoded into bits
- song ID: refers to the ID associated with a song in catalog.json
- Body: Contains the response sent by the server

### Header Structure
The Header contains 16 bits. Its structure is as shown below. The server will execute the action corresponding to the bit set in the header.
![image](https://github.com/user-attachments/assets/26d5742d-3511-48dc-a767-c6b463559436)
- The server has no need for setting headers so it sends a default header.
- The header bits are encoded into a base 16 hexadecimal integer before being transmitted. It is then decoded on the other side and interpreted.

## Code Documentation
### Project Structure
![image](https://github.com/user-attachments/assets/9b479498-803c-47bc-bd32-18d9b6e7bdea)


