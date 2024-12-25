from flask import Blueprint


class BaseRouter:
    def __init__(self,name:str,file_name):
        self.router = Blueprint(name,file_name)

    def get(self,path:str,name:str,command):
        self.router.add_url_rule(path,name,command,methods=["GET"])

    def post(self,path:str,name:str,command):
        self.router.add_url_rule(path,name,command,methods=["POST"])

    def patch(self,path:str,name:str,command):
        self.router.add_url_rule(path,name,command,methods=["PATCH"])

    def put(self,path:str,name:str,command):
        self.router.add_url_rule(path,name,command,methods=["PUT"])

    def delete(self,path:str,name:str,command):
        self.router.add_url_rule(path,name,command,methods=["DELETE"])