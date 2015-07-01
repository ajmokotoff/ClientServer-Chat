# ClientServer-Chat

## Project Specifications:

The model used for this project is the single server - multiple client model, and python was used to perform socket commands. The following general specifications will be implemented:

1. Multiple client functionality
2. A GUI will be created for the Client program
4. Clients will be able to “whisper” or send private messages to each other
5. Clients will be able to choose a nickname and that nickname will be attached to their messages


## The Server

A single server program will handle all requests from the clients. The client will implement a multi-service solution for the server. The following will be implemented for the server application:

1. Server operations (such as connect requests and disconnect requests) will be printed out by the server.
2. The server will handle connections / disconnections without disruption of other services.
3. Clients will have unique nicknames, duplicates must be resolved before allowing a client to be connected.
4. All clients must be informed of changes in the list of connected users.

## The Client(s)

The following will be implemented in the client application:

1. A list of online users must be displayed (via GUI or command).
2. Connection / disconnection actions of users will be displayed.
3. Messages from the originating user and other users will be displayed
4. Still able to receive messages / actions even if typing a message.
5. Clients will be able to disconnect without disrupting the server.
