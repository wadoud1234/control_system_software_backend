from flask import request
from base.base_router import BaseRouter
from services.service import Service
from validation.state_space_validation import StateSpacePlotInput, StateSpaceInput, StateSpacePlotInputWithAxis
import control as ctrl

# Une description est faite dans /docs/routers.md

class StateSpaceRouter(BaseRouter):
    def __init__(self):
        super().__init__("state_space",__name__)
        self.service = Service()
        self.register_routes()

    def register_routes(self):
        self.post("/step","step",self.step)
        self.post("/impulse", "impulse", self.impulse)
        self.post("/ramp","ramp",self.ramp)
        self.post("/bode", "bode", self.bode)
        self.post("/bode/opt","opt bode",self.bode_opt)
        self.post("/nyquist", "nyquist", self.nyquist)
        self.post("/poles_zeros_map","poles_zeros",self.poles_zeros)
        self.post("/step/performance","step_performance",self.step_performance)
        self.post("/bode/performance","bode_performance",self.bode_performance)
        self.post("/close_loop","closed_loop",self.closed_loop)
        self.post("/ss_to_tf","convert ss form to tf form",self.convert_ss_to_tf)

    def step(self):
        ss_step_input = StateSpacePlotInputWithAxis()
        try:
            data = ss_step_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error":str(err)},400
        A,B,C,D,t_max,x_axis,y_axis =self.extract_input(data)
        system = ctrl.ss(A,B,C,D)
        return self.service.step(system,t_max,x_axis, y_axis)

    def step_performance(self):
        ss_input=StateSpaceInput()
        try:
            data = ss_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        A, B, C, D = data["A"],data["B"],data["C"],data["D"]
        system = ctrl.ss(A,B,C,D)
        return self.service.performance(system)

    def impulse(self):
        ss_step_input = StateSpacePlotInputWithAxis()
        try:
            data = ss_step_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        A, B, C, D, t_max,x_axis,y_axis = self.extract_input(data)
        system = ctrl.ss(A,B,C,D)
        return self.service.impulse(system, t_max,x_axis,y_axis)

    def ramp(self):
        ss_step_input = StateSpacePlotInputWithAxis()
        try:
            data = ss_step_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        A, B, C, D, t_max,x_axis,y_axis = self.extract_input(data)
        system = ctrl.ss(A,B,C,D)
        return self.service.ramp(system, t_max,x_axis,y_axis)

    def bode_opt(self):
        ss_step_input = StateSpacePlotInput()
        try:
            data = ss_step_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        A, B, C, D,x_axis= data["A"],data["B"],data["C"],data["D"],data["x_axis"]
        system = ctrl.ss(A,B,C,D)
        return self.service.bode_png(system,x_axis,img_format="jpeg")


    def bode(self):
        ss_step_input = StateSpacePlotInput()
        try:
            data = ss_step_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        A, B, C, D,x_axis= data["A"],data["B"],data["C"],data["D"],data["x_axis"]
        system = ctrl.ss(A,B,C,D)
        return self.service.bode(system,x_axis)

    def bode_performance(self):
        ss_input = StateSpaceInput()
        try:
            data = ss_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        A, B, C, D = data["A"],data["B"],data["C"],data["D"]
        system = ctrl.ss(A,B,C,D)
        return self.service.bode_performance(system)

    def nyquist(self):
        ss_step_input = StateSpacePlotInput()
        try:
            data = ss_step_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        A, B, C, D, _, x_axis, y_axis = self.extract_input(data)
        system = ctrl.ss(A,B,C,D)
        return self.service.nyquist(system, x_axis,y_axis)

    def poles_zeros(self):
        ss_input = StateSpaceInput()
        try:
            data = ss_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        A, B, C, D = data["A"],data["B"],data["C"],data["D"]
        system = ctrl.ss(A,B,C,D)
        return self.service.pole_zero(system)

    def closed_loop(self):
        ss_input = StateSpaceInput()
        try:
            data = ss_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        A, B, C, D = data["A"],data["B"],data["C"],data["D"]
        system = ctrl.ss(A,B,C,D)
        tf_system = self.service.closed_loop(system)
        response =  {
            "A": tf_system.A.tolist(),
            "B": tf_system.B.tolist(),
            "C":tf_system.C.tolist(),
            "D":tf_system.D.tolist()
        }
        return response

    def convert_ss_to_tf(self):
        ss_input = StateSpaceInput()
        try:
            data = ss_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        A, B, C, D = data["A"], data["B"], data["C"], data["D"]
        system = ctrl.ss(A, B, C, D)
        tf_system = self.service.convert_ss_to_tf(system)

        response = {
            "num": tf_system.num[0][0].tolist(),
            "den": tf_system.den[0][0].tolist(),
        }

        return response

    def extract_input(self,data:StateSpacePlotInput):
        return data["A"], data["B"], data["C"], data["D"], data["t_max"], data["x_axis"], data["y_axis"]

ss_router = StateSpaceRouter()