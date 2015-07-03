import sys
import socket
import select
import re

HOST = '' 
SOCKET_LIST = []
MEMBERS = dict()
RECV_BUFFER = 4096 
PORT = 9009


def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)

    print "Chat server started on port " + str(PORT)
 
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        memberList=""
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr

                broadcast(server_socket, sockfd, "[%s:%s] is attempting to enter our chatting room\n" % addr)
             
            # a message from a client, not a new connection
            else:
                for name in MEMBERS:
                    memberList += name + "\n"
                broadcast(server_socket, sock, "query"+memberList)
                memberList = ""

                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if len(data) > 0:
                        # there is something in the socket
                        # broadcast(server_socket, sock,
                        #  "\r" + '[' + str(sock.getpeername()) + '] ' + data)
                        message = data.split(": ")
                        nick = message[0]
                        msg = message[1]

                        if nick not in MEMBERS:
                            MEMBERS[nick] = sock
                            for name in MEMBERS:
                                memberList += name + "\n"
                            #MEMBERS[message[0]].send("query"+memberList)
                            broadcast(server_socket, sock, "query"+memberList)
                            memberList = ""

                        else:
                            if msg == "is trying to connect.\n":
                                sock.send("Sorry, that name has been taken! You have been removed!\n")
                                broadcast(server_socket, sockfd, "[%s:%s] has been removed from the chat!\n" % addr)
                                SOCKET_LIST.remove(sockfd)
                                sockfd.close()

                        m = re.match('\/([A-Za-z0-9]+) (.+)', msg)

                        if m:
                            print "Private message"
                            target = m.group(1)
                            print m.group(2)

                            try:
                                if target in MEMBERS:
                                    MEMBERS[target].send("Private message from "+message[0] + ": " + m.group(2) + "\n")
                                else:
                                    print "No target"
                            except Exception as e:
                                print e.message
                                MEMBERS[target].close()
                            pass

                        elif msg[:len(msg)-1] == "queryusers":
                            for name in MEMBERS:
                                memberList += name + "\n"
                            #MEMBERS[message[0]].send("query"+memberList)
                            broadcast(server_socket, sock, "query"+memberList)
                            memberList = ""

                        else:
                            if msg != "is trying to connect.\n":
                                broadcast(server_socket, sock, data)
                    else:
                        # remove the socket that's broken
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        print 'Socket that\'s broken'
                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                        for name in MEMBERS:
                            memberList += name + "\n"
                        #MEMBERS[message[0]].send("query"+memberList)
                        broadcast(server_socket, sock, "query"+memberList)
                        memberList = ""

                # exception

                except Exception as e:
                    print e
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue


    server_socket.close()


# broadcast chat messages to all connected clients
def broadcast(server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":
    sys.exit(chat_server())