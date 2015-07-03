from Tkinter import *
import threading
import Queue
from Client import ChatClient


def send(message, instance):
    msg = "[Me]: " + message + "\n"
    ChatClient.send_message(message + "\n")
    instance.text_input.delete(0, END)
    instance.queue.put(msg)

def exit_chat():
    ChatClient.exit()
    client.endApplication()
    sys.exit()


class GuiPart:
    def __init__(self, master, queue, endCommand):
        self.queue = queue
        self.bottom_frame = Frame(master, width=80, bg='#c9daf8')
        self.bottom_frame.pack(side=BOTTOM, fill="both", expand=True)

        self.member_frame = Frame(master)
        self.member_frame.pack(side=LEFT)

        self.member_list = Text(self.member_frame, width=30, height=30, bg='#d9ead3', fg='#999999')
        self.member_list.configure(state="disabled")
        self.member_list.pack()

        # Set up the GUI
        self.quit_button = Button(self.bottom_frame, text='Quit', command=endCommand)
        self.quit_button.pack(side=LEFT, anchor='w')

        self.scrollbar = Scrollbar(master)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.log = Text(master, width=50, height=30, takefocus=0, bg='#fff2cc', fg='#999999')
        self.log.configure(state="disabled")
        self.log.pack()

        # attach text box to scrollbar
        self.log.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.log.yview)

        self.text_input = Entry(self.bottom_frame, width=35)
        self.text_input.bind("<Return>",(lambda event: send(self.text_input.get(), self)))
        self.text_input.pack(side=BOTTOM, anchor=CENTER)

        self.send_button = Button(self.bottom_frame, text="Send Message")
        self.send_button.pack(side=RIGHT, anchor='se', fill=Y)

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                # As a test, we simply print it
                print msg
                if msg[:5] == 'query':
                    msg = "Online Users:\n" + msg[5:len(msg)-1]
                    self.member_list.configure(state="normal")
                    self.member_list.delete("1.0", END)
                    self.member_list.insert(END, msg)
                    self.member_list.configure(state="disable")
                else:
                    self.log.configure(state="normal")
                    self.log.insert(END, str(msg))
                    self.log.configure(state="disable")
                    # to prevent user from typing in window

            except Queue.Empty:
                pass


class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        # Create the queue
        self.queue = Queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        ChatClient.connect()

        while self.running:

            message = ChatClient.listener()
            if message is not None and len(message) > 1:
                self.queue.put(message)

    def endApplication(self):
        self.running = 0
        self.thread1.join()
        self.thread1 = None


root = Tk()
root.wm_title("Chat Room")
root.configure(bg='#999999')
#root.update()
client = ThreadedClient(root)
root.mainloop()
