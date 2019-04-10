# Simple Group Talk
A simple group voice chat service implemented over TCP sockets.

### How to use
Make sure you have pyaudio installed on your system. Run the server.py to start the server and then run as many client.py as you want. To by typing in 1 in the client terminal, the client will start broadcasting the microphone input data.

### Packet Design

`Handshake Packet`
```
# sent from the client to the server after connection
| 4 bytes username length | username encoded string |
```

`Streaming`
```
# sent from the client to server during streaming
| 1024 bytes of audio data in Portaudio paInt16 format |
```

`Receiving Stream`
```
# sent from server to clients during broadcast
| 4 bytes username length | username (broadcaster) encoded string | 1024 byte audio data in Portaudio paInt16 format |
```

### Todo
[ ] Move from TCP to UDP sockets.
[ ] Implement end ot end encryption.
[ ] Implement UDP hole punching for peer to peer connections.

Note that this service is nowhere near production level, hell, it probably has quite a lot of bugs haha. It is implemented as a reference and practice for future projects.