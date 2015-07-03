import sys
import socket
import select


class ChatClient:
    s = None
    socket = None
    host = '127.0.0.1'
    port = 9009
    nickname = 'Andrew'

    def __init__(self, nickname):
        ChatClient.nickname = nickname

    @staticmethod
    def connect():
        ChatClient.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ChatClient.socket.settimeout(2)
        try:
            ChatClient.socket.connect((ChatClient.host, ChatClient.port))
        except:
            print 'Unable to connect'
            sys.exit()
        ChatClient.nickname = raw_input("Enter a nickname: ")
        ChatClient.socket.send(ChatClient.nickname + ": is trying to connect.\n")
        sys.stdout.write('[Me] ');
        sys.stdout.flush()

    @staticmethod
    def listener():
        socket_list = [sys.stdin, ChatClient.socket]

        # Get the list sockets which are readable
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

        for sock in ready_to_read:
            if sock == ChatClient.socket:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data:
                    print '\nDisconnected from chat server'
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write('\r' + data)
                    sys.stdout.write('[Me] ');
                    sys.stdout.flush()
                    return data

    @staticmethod
    def send_message(msg):

        if msg[0].lower() == 'q' and len(msg) < 3:
            sys.exit()

        else:
            ChatClient.socket.send(ChatClient.nickname + ": " + msg)
            sys.stdout.write('[Me] ');
            sys.stdout.flush()

    @staticmethod
    def exit():
        sys.exit()
