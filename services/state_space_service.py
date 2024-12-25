import io
import json

import control as ctrl
from flask import send_file, Response, jsonify
from scipy import signal
import numpy as np
from scipy.signal import bode
import matplotlib.pyplot as plt
from base.base_service import BaseService
from helpers.plotter import Plotter
from models.state_space_model import StateSpaceModel

class StateSpaceService(BaseService):
    def __init__(self):
        super().__init__()
        self.plotter = Plotter()


    def step(self,
             A: np.ndarray,
             B: np.ndarray,
             C: np.ndarray,
             D: np.ndarray,
             t_max: float,
             num_points: int,
             x_axis,
             y_axis
        ):

        # Generate the time vector from 0 to t_max
        t = self.generate_time(t_max,num_points)

        # Define the state-space system
        system = StateSpaceModel(A, B, C, D).gen()

        # Calculate the step response
        _, y = signal.step(system, T=t)

        # Create the plot
        # Save the plot to a BytesIO object as SVG
        img_stream = self.plotter.plot(
             t,y,
             title="State Space Step Response",
             grid=True,
             legend="Response",
             xlim=x_axis,
             ylim=y_axis
        )
        # img_stream = self.plotter.save_svg()

        # Return the image as a StreamingResponse
        return send_file(img_stream, mimetype="image/svg+xml")

    def impulse(self,
                A: np.ndarray,
                B: np.ndarray,
                C: np.ndarray,
                D: np.ndarray,
                t_max: float,
                num_points: int,
                x_axis,
                y_axis
                ):
        # Generate the time vector from 0 to t_max
        t = self.generate_time(t_max, num_points)

        # Define the state-space system
        system = StateSpaceModel(A, B, C, D).gen()

        # Calculate the step response
        _, y = signal.impulse(system, T=t)

        # Create the plot
        # Save the plot to a BytesIO object as SVG
        img_stream = self.plotter.plot(
            t, y,
            title="State Space Impulse Response",
            grid=True,
            legend="Response",
            xlim=x_axis,
            ylim=y_axis
        )
        # img_stream = self.plotter.save_svg()

        # Return the image as a StreamingResponse
        return send_file(img_stream, mimetype="image/svg+xml")

    def ramp(self,
             A: np.ndarray,
             B: np.ndarray,
             C: np.ndarray,
             D: np.ndarray,
             t_max: float,
             num_points: int,
             x_axis,
             y_axis
             ):
        # Generate the time vector from 0 to t_max
        t = self.generate_time(t_max, num_points)

        # Define the state-space system
        system = StateSpaceModel(A, B, C, D).gen()

        ramp_input = t

        # Calculate the step response
        time, y, _ = signal.lsim(system, ramp_input, t)

        # Create the plot
        # Save the plot to a BytesIO object as SVG
        img_stream = self.plotter.plot(
            t, y,
            title="State Space Ramp Response",
            grid=True,
            legend="Response",
            xlim=x_axis,
            ylim=y_axis
        )
        # img_stream = self.plotter.save_svg()

        # Return the image as a StreamingResponse
        return send_file(img_stream, mimetype="image/svg+xml")

    def bode(self,
             A: np.ndarray,
             B: np.ndarray,
             C: np.ndarray,
             D: np.ndarray,
             t_max: float,
             num_points: int,
             x_axis,
             y_axis
             ):
        sys = ctrl.ss(A, B, C, D)

        # Generate the Bode plot using control library (or custom logic)
        omega = np.logspace(-1, 2, num_points)
        mag, phase, omega = ctrl.bode(sys, omega, plot=False)  # Bode plot data without plotting

        # If you need to use the x_axis and y_axis for plotting, ensure they are handled in the logic.
        # For now, we will plot mag vs omega.

        fig, ax = plt.subplots(2, 1, figsize=(8, 6))

        # Plot magnitude
        ax[0].semilogx(omega, 20 * np.log10(mag))
        ax[0].set_title('Bode Plot')
        ax[0].set_ylabel('Magnitude (dB)')

        # Plot phase
        ax[1].semilogx(omega, np.degrees(phase))
        ax[1].set_xlabel('Frequency (rad/s)')
        ax[1].set_ylabel('Phase (degrees)')

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        fig.savefig(img, format='svg')
        img.seek(0)  # Reset pointer to the start of the BytesIO object

        margins = ctrl.stability_margins(sys)

        # Extract specific values
        gm = margins[0]  # Gain margin
        pm = margins[1]  # Phase margin
        wg = margins[2]  # Gain crossover frequency
        wp = margins[3]  # Phase crossover frequency

        stability_data = {
            "gm": gm,  # Gain margin
            "pm": pm,  # Phase margin
            "wg": wg,  # Gain crossover frequency
            "wp": wp  # Phase crossover frequency
        }

        stability_data_json = json.dumps(stability_data)

        # Prepare response with both the SVG image and the stability data as JSON
        response = send_file(
            img,
            mimetype='image/svg+xml',
            # as_attachment=True,
            # download_name='nyquist_plot.svg'
        )

        # Add the stability data as a custom header (ensure no newlines in the header)
        response.headers['X-Stability-Data'] = stability_data_json

        return response

    def nyquist(self,
             A: np.ndarray,
             B: np.ndarray,
             C: np.ndarray,
             D: np.ndarray,
             t_max: float,
             num_points: int,
             x_axis,
             y_axis
             ):
        sys = ctrl.ss(A, B, C, D)

        # Create a larger figure
        plt.figure(figsize=(8, 6))  # Adjust the size (width, height)

        # Generate Nyquist plot
        ctrl.nyquist(sys, omega_limits=[0.1, 10])

        # Calculate stability margins (gain margin, phase margin, and crossover frequencies)
        margins = ctrl.stability_margins(sys)

        # Extract specific values
        gm = margins[0]  # Gain margin
        pm = margins[1]  # Phase margin
        wg = margins[2]  # Gain crossover frequency
        wp = margins[3]  # Phase crossover frequency

        # Print and return stability margins as part of the response
        stability_data = {
            "gm": gm,  # Gain margin
            "pm": pm,  # Phase margin
            "wg": wg,  # Gain crossover frequency
            "wp": wp  # Phase crossover frequency
        }

        # Save the plot to a BytesIO object
        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='svg')
        plt.close()
        img_stream.seek(0)  # Rewind the stream to the beginnin

        stability_data_json = json.dumps(stability_data)

        # Prepare response with both the SVG image and the stability data as JSON
        response = send_file(
            img_stream,
            mimetype='image/svg+xml',
            # as_attachment=True,
            # download_name='nyquist_plot.svg'
        )

        # Add the stability data as a custom header (ensure no newlines in the header)
        response.headers['X-Stability-Data'] = stability_data_json

        return response

    def generate_time(self, t_max:float, num_points:int):
        return np.linspace(0, t_max, num_points)
