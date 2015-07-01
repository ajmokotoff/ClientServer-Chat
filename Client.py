from Tkinter import *
import sys
import socket
import select


def chat_client():


    '''
    window = Tk()
    label = Label(window, text='our label widget')
    entry = Entry(window)
    label.pack(side=TOP)
    entry.pack()
    window.mainloop()
    '''

    if len(sys.argv) < 4:
        print 'Usage : python chat_client.py hostname port nickname'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    nickname = sys.argv[3]

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
                    # print data
                    sys.stdout.write('\r' + data)
                    sys.stdout.write('[Me] ');
                    sys.stdout.flush()
            
            else:
                # user entered a message
                msg = sys.stdin.readline()


                if msg[0] == 'q' or msg[0] == 'Q':
                    sys.exit()

                else:
                    s.send(nickname + ": " + msg)
                    sys.stdout.write('[Me] ');
                    sys.stdout.flush()

if __name__ == "__main__":
    sys.exit(chat_client())