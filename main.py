from server import Server
import os

# Fichier main.py , creer une instance de classs Server et demarrer le backend

server = Server()

app = server.app
app.run(debug=True)