import os
import http.server
import threading
# import signal

import logging

logger = logging.getLogger(__name__)

class DisplayServer:
	def __init__(self, wd, port, log=logger):
		self.wd = wd
		self.port = port
		self.log = log
		self.server = None

	def create_server(self):
		'''
		Create a server that will display the slides
		'''
		os.makedirs(self.wd, exist_ok=True)

		# Pass the path to server working sirectory by variable
		# instead of using self (crash)
		wd = self.wd

		class Handler(http.server.SimpleHTTPRequestHandler):
			def __init__(self, *args, **kwargs):
				super().__init__(*args, directory=wd, **kwargs)

		_ , addr = http.server._get_best_family(None, self.port)
		serv = http.server.HTTPServer(addr, Handler)

		self.log.info(f"Created the server {serv}")

		self.server = serv

	def start_server(self):
		self.create_server()

		def serve_forever(httpd):
			'''
			Threaded function to start a server
			'''
			with httpd as server:
				server.serve_forever()

		# Kill the server if the program is stopped
		def signal_term_handler(signal, frame):
			print('got SIGTERM')
			self.stop_server()

		self.log.debug(f"Starting server {self.server}")
		self.server_thread = threading.Thread(target=serve_forever, args=(self.server, ))

		# Starting as deamon wil end the thread when the program stops
		self.server_thread.setDaemon(True)

		# Starting the thread
		self.server_thread.start()
		self.log.info(f"Server {self.server} started")

		# Assign the function to call if the signal SIGTERM is received
#		signal.signal(signal.SIGTERM, signal_term_handler)

	def stop_server(self):
		if self.server is None:
			self.log.error(f"Server not started")

		self.log.debug(f"Stopping server {self.server}")
		self.server.shutdown()
		self.server_thread._stop()
		self.log.info(f"Server {self.server} stopped")
