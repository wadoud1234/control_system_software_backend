from flask import Flask, Config
from flask_cors import CORS

from routers.state_space_router import ss_router
from routers.transfer_function_router import tf_router


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)

        CORS(self.app)  # This will allow all origins by default
        self.register_routes()
        self.app.add_url_rule("/","home",self.hello,methods=["GET"])

    def hello(self):
        return "HELLO"

    def register_routes(self):
        self.app.register_blueprint(ss_router.router, url_prefix='/ss')
        self.app.register_blueprint(tf_router.router, url_prefix='/tf')

    def run(self):
        self.app.run(debug=True)

