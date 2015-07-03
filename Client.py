import sys
import socket
import select


class ChatClient:
    s = None
    socket = None
    host = '127.0.0.1'
    port = 9009
    nickname = 'Mok'
    members = []

    def __init__(self, host, nickname):
        ChatClient.host = host
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
        ChatClient.socket.send(ChatClient.nickname + ": Has joined the channel\n")
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
            '''
            else:
                # user entered a message
                msg = sys.stdin.readline()

                if msg[0] == 'q' or msg[0] == 'Q':
                    sys.exit()

                else:
                    ChatClient.socket.send(ChatClient.nickname + ": " + msg)
                    sys.stdout.write('[Me] ');
                    sys.stdout.flush()
            '''

    @staticmethod
    def send_message(msg):
        #msg = sys.stdin.readline()

        if msg[0].lower() == 'q' and len(msg) < 3:
            sys.exit()

        else:
            ChatClient.socket.send(ChatClient.nickname + ": " + msg)
            sys.stdout.write('[Me] ');
            sys.stdout.flush()

    @staticmethod
    def exit():
        sys.exit()



def chat_client():
    '''
    if len(sys.argv) < 4:
        print 'Usage : python chat_client.py hostname port nickname'
        sys.exit()
    '''

    host = '127.0.0.1'
    port = int(9009)
    nickname = "joddsh"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print 'Unable to connect'
        sys.exit()
    s.send(nickname + ": Has joined the channel\n")

    print 'Connected to remote host. You can start sending messages'
    sys.stdout.write('[Me] ');
    sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

        for sock in ready_to_read:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data:
                    print '\nDisconnected from chat server'
                    sys.exit()
                else:
                    if data[:5] == 'query':
                        data = data[5:len(data)-1]
                        print data
                    else:
                        sys.stdout.write('\r' + data)
                        sys.stdout.write('[Me] ');
                        sys.stdout.flush()

            else:
                # user entered a message
                msg = sys.stdin.readline()

                if msg[0].lower() == 'q' and len(msg) < 3:
                    sys.exit()

                else:
                    s.send(nickname + ": " + msg)
                    sys.stdout.write('[Me] ');
                    sys.stdout.flush()


if __name__ == "__main__":
    sys.exit(chat_client())
