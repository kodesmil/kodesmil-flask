import threading
from tkinter import *
from tkinter import simpledialog

import grpc

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

address = 'localhost'
port = 11912


class Client:

    def __init__(self, u: str, window):
        # the frame to put ui components on
        self.window = window
        self.author_id = u
        self.chatroom_id = 'test'
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatServerStub(channel)
        # create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        self.__setup_ui()
        self.window.mainloop()

    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        for message in self.conn.ChatStream(chat.Empty()):  # this line will wait for new messages from the server!
            print("R[{}] {}".format(message.author_id, message.text))  # debugging statement
            self.chat_list.insert(END, "[{}] {}\n".format(message.author_id, message.text))  # add the message to the UI

    def send_message(self, event):
        """
        This method is called when user enters something into the textbox
        """
        text = self.entry_message.get()  # retrieve message from the UI
        if text is not '':
            n = chat.Message()  # create protobug message (called Note)
            n.author_id = self.author_id  # set the username
            n.text = text  # set the actual message of the note
            n.chatroom_id = self.chatroom_id
            print("S[{}] {}".format(n.author_id, n.text))  # debugging statement
            self.conn.SendMessage(n)  # send the Note to the server

    def __setup_ui(self):
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.author_id)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.send_message)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)


if __name__ == '__main__':
    root = Tk()  # I just used a very simple Tk window for the chat UI, this can be replaced by anything
    frame = Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()
    author_id = None
    while author_id is None:
        # retrieve a username so we can distinguish all the different clients
        author_id = simpledialog.askstring("Username", "What's your username?", parent=root)
    root.deiconify()  # don't remember why this was needed anymore...
    c = Client(author_id, frame)  # this starts a client and thus a thread which keeps connection to server open
