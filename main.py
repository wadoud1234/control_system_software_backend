from server import Server
import os

server = Server()

app = server.app
app.run(port=3000)