from concurrent import futures

import grpc
import time
import json
import datetime as dt

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

from models import ChatRoomMessageSchema

from db import db_conn


class ChatServer(rpc.ChatServerServicer):  # inheriting here from the protobuf rpc file which is generated

	def __init__(self):
		# List with all the chat history
		self.chats = []
		self.db = db_conn()

	# The stream which will be used to send new messages to clients
	def ChatStream(self, request_iterator, context):
		print(request_iterator)
		print('-------')
		print(context)

		"""
		This is a response-stream type call. This means the server can keep sending messages
		Every client opens this connection and waits for server to send new messages
	
		:param request_iterator:
		:param context:
		:return:
		"""
		lastindex = 0
		# For every client a infinite loop starts (in gRPC's own managed thread)
		#while True:

	# Check if there are any new messages in chatroom

	# This method is called when a clients sends a Note to the server.
	def SendMessage(self, request: chat.Message, context):

		# only for the server console
		print("[{}] [{}] {}".format(request.author_id, request.chatroom_id, request.text))

		# Add message to database

		raw_data = {
			'author_id': request.author_id,
			'text': request.text,
			'chatroom_id': request.chatroom_id
		}
		print(raw_data)

		# wtf it's not working with marshmallow?
		# instance = ChatRoomMessageSchema().load(raw_data)

		self.db[request.chatroom_id].insert_one(raw_data)

		return chat.Empty()  # return an empty msg, needed by protobuf


if __name__ == '__main__':
	port = 11912
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))  # create a gRPC server, clients limited to 2
	rpc.add_ChatServerServicer_to_server(ChatServer(), server)  # register the server to gRPC
	print('Starting server. Listening...')
	server.add_insecure_port('[::]:' + str(port))
	server.start()
	while True:
		time.sleep(64 * 64 * 100)
