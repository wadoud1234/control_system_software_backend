from server import Server
import os

server = Server()

app = server.app
app.run(host="0.0.0.0",port=3000)