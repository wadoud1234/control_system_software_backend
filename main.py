from server import Server
import os

server = Server()

if __name__ == "__main__":
    # Get the port from the environment variable or use 5000 as a fallback
    port = int(os.environ.get("PORT", 5000))
    server.app.run(host="0.0.0.0", port=port)