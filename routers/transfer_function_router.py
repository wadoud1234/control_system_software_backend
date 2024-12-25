from flask import request
import control as ctrl
from base.base_router import BaseRouter
from services.service import Service
from validation.transfer_function_validation import TransferFunctionPlotInput, TransferFunctionInput, \
    TransferFunctionPlotInputWithAxis


class TransferFunctionRouter(BaseRouter):
    def __init__(self):
        super().__init__("transfer_function", __name__)
        self.service = Service()
        self.register_routes()

    def register_routes(self):
        self.post("/step", "step", self.step)
        self.post("/impulse", "impulse", self.impulse)
        self.post("/ramp", "ramp", self.ramp)
        self.post("/bode", "bode", self.bode)
        self.post("/nyquist", "nyquist", self.nyquist)
        self.post("/poles_zeros_map","poles_zeros",self.poles_zeros)
        self.post("/step/performance","step_performance",self.step_performance)
        self.post("/bode/performance","bode_performance",self.bode_performance)
        self.post("/close_loop","close_loop",self.close_loop)
        self.post("/tf_to_ss","convert tf form to ss form",self.convert_tf_to_ss)

    def step(self):
        tf_input = TransferFunctionPlotInputWithAxis()
        try:
            data = tf_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        num,den, t_max, x_axis, y_axis = self.extract_input(data)
        system = ctrl.tf(num,den)
        return self.service.step(system, t_max, x_axis, y_axis)

    def step_performance(self):
        tf_input=TransferFunctionInput()
        try:
            data = tf_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        num,den = data["num"],data["den"]
        system = ctrl.tf(num,den)
        return self.service.performance(system)


    def impulse(self):
        tf_input = TransferFunctionPlotInputWithAxis()
        try:
            data = tf_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        num, den, t_max, x_axis, y_axis = self.extract_input(data)
        system = ctrl.tf(num,den)
        return self.service.impulse(system, t_max, x_axis, y_axis)

    def ramp(self):
        tf_input = TransferFunctionPlotInputWithAxis()
        try:
            data = tf_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        num, den, t_max, x_axis, y_axis = self.extract_input(data)
        system = ctrl.tf(num,den)
        return self.service.ramp(system, t_max, x_axis, y_axis)

    def bode(self):
        tf_input = TransferFunctionPlotInput()
        try:
            data = tf_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        num, den, t_max,x_axis = data["num"],data["den"],data["t_max"],data["x_axis"]
        system = ctrl.tf(num,den)
        return self.service.bode(system,x_axis)

    def bode_performance(self):
        tf_input = TransferFunctionInput()
        try:
            data = tf_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        num, den = data["num"], data["den"]
        system = ctrl.tf(num, den)
        return self.service.bode_performance(system)

    def nyquist(self):
        tf_input = TransferFunctionPlotInputWithAxis()
        try:
            data = tf_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        num, den, _, x_axis, y_axis = self.extract_input(data)
        system = ctrl.tf(num,den)
        return self.service.nyquist(system, x_axis, y_axis)

    def poles_zeros(self):
        tf_input = TransferFunctionInput()
        try:
            data = tf_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        num,den = data["num"],data["den"]
        system = ctrl.tf(num,den)
        return self.service.pole_zero(system)

    def close_loop(self):
        tf_input = TransferFunctionInput()
        try:
            data = tf_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        num, den = data["num"], data["den"]
        system = ctrl.tf(num, den)
        ss_system = self.service.closed_loop(system)

        response = {
            "num":ss_system.num[0][0].tolist(),
            "den":ss_system.den[0][0].tolist()
        }
        print(response)
        return response

    def convert_tf_to_ss(self):
        tf_input = TransferFunctionInput()
        try:
            data = tf_input.load(request.get_json())
        except Exception as err:
            print(err)
            return {"error": str(err)}, 400
        num, den = data["num"], data["den"]
        system = ctrl.tf(num, den)
        ss_system = self.service.convert_tf_to_ss(system)
        print(ss_system)
        response = {
            "A":ss_system.A.tolist(),
            "B":ss_system.B.tolist(),
            "C":ss_system.C.tolist(),
            "D":ss_system.D.tolist(),
        }
        return response

    def extract_input(self, data: TransferFunctionPlotInput):
        return data["num"], data["den"], data["t_max"], data["x_axis"], data["y_axis"]


tf_router = TransferFunctionRouter()
