import io
from typing import Union
import matplotlib
import matplotlib.pyplot as plt
import control as ctrl
import numpy as np
from control import TransferFunction, StateSpace
from flask import send_file, Response, jsonify
import json
from base.base_service import BaseService
from helpers.plotter import Plotter
from helpers.sanitize_data import sanitize_data

matplotlib.use("SVG")


class Service(BaseService):
    def __init__(self):
        self.plotter = Plotter()

    def pole_zero(self, system: Union[TransferFunction, StateSpace]):
        plt.figure()
        ctrl.pzmap(system, plot=True, title="Pole-Zero Map")
        plt.grid(True)
        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='svg')
        img_stream.seek(0)

        response = send_file(img_stream, mimetype="image/svg+xml")
        poles_zeros = {
            "poles": ctrl.poles(system),
            "zeros": ctrl.zeros(system),
        }
        response.headers['X-Poles-Zeros'] = poles_zeros
        return response

    def step(self,
             system: Union[TransferFunction, StateSpace],
             t_max: float,
             x_axis,
             y_axis
             ):
        time = self.generate_time(t_max)

        _, response = ctrl.step_response(system, T=time)

        system_type = "Transfer Function" if self.get_system_type(system) == "tf" else "State Space"

        img_stream = self.plotter.plot(
            time, response,
            title=f"{system_type} Step Response",
            grid=True,
            legend="Response",
            xlim=x_axis,
            ylim=y_axis
        )

        return send_file(img_stream, mimetype="image/svg+xml")

    def impulse(self,
                system: Union[TransferFunction, StateSpace],
                t_max: float,
                x_axis,
                y_axis
                ):
        time = self.generate_time(t_max)

        _, response = ctrl.impulse_response(system, T=time)

        system_type = "Transfer Function" if self.get_system_type(system) == "tf" else "State Space"

        img_stream = self.plotter.plot(
            time, response,
            title=f"{system_type} Impulse Response",
            grid=True,
            legend="Response",
            xlim=x_axis,
            ylim=y_axis
        )

        return send_file(img_stream, mimetype="image/svg+xml")

    def ramp(self,
             system: Union[TransferFunction, StateSpace],
             t_max: float,
             x_axis,
             y_axis
             ):
        time = self.generate_time(t_max)
        ramp_input = time
        _, response = ctrl.forced_response(system, T=time, U=ramp_input)

        system_type = "Transfer Function" if self.get_system_type(system) == "tf" else "State Space"

        img_stream = self.plotter.plot(
            time, response,
            title=f"{system_type} Ramp Response",
            grid=True,
            legend="Response",
            xlim=x_axis,
            ylim=y_axis
        )

        return send_file(img_stream, mimetype="image/svg+xml")

    def bode(self, system: Union[TransferFunction, StateSpace], x_axis=None):
        if x_axis is None:
            x_axis = [-1, 2]
        omega = np.logspace(x_axis[0], x_axis[1], 1000)
        mag, phase, omega = ctrl.bode(system, omega, plot=False)
        fig, ax = plt.subplots(2, 1, figsize=(8, 6))

        # Plot magnitude
        ax[0].semilogx(omega, 20 * np.log10(mag))
        ax[0].set_title('Bode Plot')
        ax[0].set_ylabel('Magnitude (dB)')
        ax[0].grid(True, which='both', axis='both')  # Add grid to magnitude plot (major and minor)
        ax[0].minorticks_on()  # Enable minor ticks for finer granularity
        ax[0].set_xscale('log')  # Ensure the x-axis is logarithmic
        ax[0].set_yscale('linear')

        # Plot phase
        ax[1].semilogx(omega, np.degrees(phase))
        ax[1].set_xlabel('Frequency (rad/s)')
        ax[1].set_ylabel('Phase (degrees)')
        ax[1].grid(True, which='both', axis='both')  # Add grid to magnitude plot (major and minor)
        ax[1].minorticks_on()  # Enable minor ticks for finer granularity
        ax[1].set_xscale('log')  # Ensure the x-axis is logarithmic
        ax[1].set_yscale('linear')
        # Save the plot to a BytesIO object
        img = io.BytesIO()
        fig.savefig(img, format='svg')
        img.seek(0)  # Reset pointer to the start of the BytesIO object

        # Prepare response with both the SVG image and the stability data as JSON
        response = send_file(
            img,
            mimetype='image/svg+xml',
        )

        return response

    def bode_performance(self,system:Union[TransferFunction|StateSpace]):
        gm,pm,sm,wpc,wgc,wms = ctrl.stability_margins(system)

        response = [
            {"key":"Gain Margin","value":gm},
            {"key":"Phase Margin","value":pm},
            {"key":"Stability Margin","value":sm},
            {"key":"Gain Crossover Frequency", "value": wgc},
            {"key":"Phase Crossover Frequency","value":wpc},
            {"key":"Stability margin frequency","value":wms},
        ]

        return sanitize_data(response)

    def nyquist(self,
                system: Union[TransferFunction, StateSpace],
                x_axis,
                y_axis,
                ):

        omega = np.logspace(-200, 200, 10000)

        # Create a larger figure
        plt.figure(figsize=(8, 6))  # Adjust the size (width, height)

        # Generate Nyquist plot
        ctrl.nyquist(system,omega)

        # Save the plot to a BytesIO object
        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='svg')
        plt.close()
        img_stream.seek(0)  # Rewind the stream to the beginnin

        # Prepare response with both the SVG image and the stability data as JSON
        response = send_file(
            img_stream,
            mimetype='image/svg+xml',
            # as_attachment=True,
            # download_name='nyquist_plot.svg'
        )

        return response

    def performance(self, system: Union[TransferFunction, StateSpace]):
        time, response = ctrl.step_response(system)
        # static_gain = self.calculate_static_gain(system)
        final_value = self.calculate_final_value(system)
        overshoot = self.calculate_overshoot(response, final_value)
        peak_time, peak_amplitude = self.calculate_peak(time, response)
        rise_time = self.calculate_rise_time(time, response, final_value)
        # settling_time = self.calculate_settling_time(time,response,final_value)
        settling_time = self.settling(time, response, final_value)
        # steady_error = self.calculate_steady_error(final_value)
        response = [
            # "static_gain":static_gain.tolist()[0][0],
            {"key":"Final Value","value": float(final_value)},
            {"key":"Overshoot","value": float(overshoot)},
            {"key":"Peak Time","value": float(peak_time)},
            {"key":"Peak Amplitude","value": float(peak_amplitude)},
            {"key":"Rise Time","value": float(rise_time)},
            {"key":"Settling Time","value": float(settling_time)},
            # "steady_error":self.steady_error(final_value)
        ]
        print(response)
        return jsonify(response), 200

    def closed_loop(self,system:Union[TransferFunction,StateSpace]):
        sys = ctrl.feedback(system,1)
        print(sys)
        return sys

    def convert_tf_to_ss(self,system:TransferFunction):
        return ctrl.tf2ss(system)

    def convert_ss_to_tf(self,system:StateSpace):
        return ctrl.ss2tf(system)

    def steady_error(self, final_value):
        return 1 / (final_value + 1)

    def settling(self, time, response, final_value: float):
        tolerance = 0.05 * final_value  # 2% tolerance
        settling_time = None

        # Find the time when the response stays within 2% of the steady-state value
        for t, y in zip(time, response):
            if np.abs(y - final_value) > tolerance:
                settling_time = t
        return settling_time

    def calculate_overshoot(self, response, final_value: float):
        peak_value = np.max(response)
        overshoot = (peak_value - final_value) / final_value * 100
        return overshoot

    def calculate_peak(self, time, response):
        return time[np.argmax(response)], np.max(response)

    def calculate_rise_time(self, time, response, final_value):
        rise_time_start = np.where(response >= 0.1 * final_value)[0][0]
        rise_time_end = np.where(response >= 0.9 * final_value)[0][0]
        return time[rise_time_end] - time[rise_time_start]

    def calculate_settling_time(self, time, response, final_value):
        return time[np.where(np.abs(response - final_value) <= 0.02 * final_value)[0][0]]

    def calculate_steady_error(self, final_value, static_gain):
        return abs(final_value - static_gain)

    def calculate_static_gain(self, system: Union[TransferFunction, StateSpace]):
        system_type = self.get_system_type(system)
        if system_type == "tf":
            return system.num[0][0] / system.den[0][0]
        else:
            return np.dot(system.C, np.linalg.inv(system.A).dot(system.B))

    def calculate_final_value(self, system: Union[TransferFunction | StateSpace]):
        return ctrl.dcgain(system)

    def get_system_type(self, system: Union[TransferFunction, StateSpace]):
        if isinstance(system, TransferFunction):
            return "tf"
        else:
            return "ss"

    def generate_time(self, t_end: float):
        return np.arange(0, t_end, 0.01)
