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

### Catalog Class methods
request(): Reads the catalog database and returns the contents

### Message class methods
- \_\_init__(source, dest): Initializes the message object with the source and destination IPs. Also initializes headers and sets timestamp
- generateheader(): Returns a string of bits derived from the headers json object
- setheaderparam(param, value): Sets the header parameter to the corresponding value.
- setsongid(songid): Sets the song ID of the message.
- setbody(body): Sets the body of the message.
- generatepacket(): Generates a packet in the form of a string that can be transmitted over sockets

### Playlist class methods
- append(id): append song with the supplied ID to the playlist
- reportqueue(): returns the contents of the playlist
- remove(id): removes the song with the supplied ID from the playlist
- findbyid(id): checks if the song with the supplied ID exists in the playlist
- setdefault(): sets the playmode to default
- setshuffle(): sets the playmode to shuffle
- setloop(): sets the playmode to loop
- play(): sets the mode to play
- playnext(): plays the next song in the queue
- goback(): play the last played song
- quit(): Quit

### Client.py Methods
- decodeinput(text, msg): parses user input and sets the corresponding header in the message
- \_\_main__(): Takes user input, generates packet, sends it, receives server's response and displays it

### Server.py Methods
- decodeheader(header): returns a base 16 hexadecimal integer corresponding to the supplied bit string
- recievepacket(): listens for an incoming packets from the client, interprets it and returns the constructed Message object.
- sendpacket(body, source, dest): generates a packet string that can be transmitted to the client over the socket
- requesthandler(header, songid): interprets the client's packet information and performs the corresponding action. Returns the body of the response header
- main(): Starts the socket server, listens for client requests and serves the correct response.
