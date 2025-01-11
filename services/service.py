import io
from typing import Union
import matplotlib
import matplotlib.pyplot as plt
import control as ctrl
import numpy as np
from PIL import Image
from control import TransferFunction, StateSpace
from flask import send_file, jsonify

from base.base_service import BaseService
from helpers.plotter import Plotter
from helpers.sanitize_data import sanitize_data

# utilise pour utiliser matplotlib seulement pour la generation des images svg
matplotlib.use("SVG")

# Une description de Classe Service est faite dans /docs/service.md

class Service(BaseService):
    def __init__(self):
        super().__init__()
        self.plotter = Plotter()

    # pour generer une map contient la position des poles et des zeros
    def pole_zero(self, system: Union[TransferFunction, StateSpace]):
        plt.figure()
        ctrl.pzmap(system, plot=True, title="Pole-Zero Map")
        plt.grid(True)

        # pour sauvegarder l'image dans un stream , puis dans la reponse de cette fonction (handler)
        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='svg')
        img_stream.seek(0)

        # pour retourner la reponse en format d'image svg
        response = send_file(img_stream, mimetype="image/svg+xml")
        return response

    # pour generer la reponse indicielle
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

    # pour generer la reponse impulsionnel
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

    # pour generer la reponse a une entree rampe
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

    # cette fonction pour avoir diagramme de bode en format svg (non utilise svg est mieux pour les sites web)
    def bode_png(self,system: Union[TransferFunction, StateSpace], x_axis=None, img_format='svg', compress=True):
        if x_axis is None:
            x_axis = [-1, 2]

        omega = np.logspace(x_axis[0], x_axis[1], 1000)
        mag, phase, omega = ctrl.bode(system, omega, plot=False)

        fig, ax = plt.subplots(2, 1, figsize=(8, 6))

        # diagramme d'amplitude
        ax[0].semilogx(omega, 20 * np.log10(mag))
        ax[0].set_title('Bode Plot')
        ax[0].set_ylabel('Magnitude (dB)')
        ax[0].grid(True, which='both', axis='both')
        ax[0].minorticks_on()
        ax[0].set_xscale('log')
        ax[0].set_yscale('linear')

        # diagramme de phase
        ax[1].semilogx(omega, np.degrees(phase))
        ax[1].set_xlabel('Frequency (rad/s)')
        ax[1].set_ylabel('Phase (degrees)')
        ax[1].grid(True, which='both', axis='both')
        ax[1].minorticks_on()
        ax[1].set_xscale('log')
        ax[1].set_yscale('linear')

        plt.tight_layout()

        img = io.BytesIO()
        fig.savefig(img, format=img_format)
        img.seek(0)

        if compress and img_format in ['png', 'jpeg', 'jpg']:
            img_compressed = io.BytesIO()
            pil_img = Image.open(img)
            pil_img.save(img_compressed, format=img_format, optimize=True,
                         quality=85)
            img_compressed.seek(0)
            img = img_compressed

        mime_type = f'image/{img_format}'
        response = send_file(img, mimetype=mime_type)

        return response

    # pour generer diagramme de bode
    def bode(self, system: Union[TransferFunction, StateSpace], x_axis=None):
        if x_axis is None:
            x_axis = [-1, 2]
        omega = np.logspace(x_axis[0], x_axis[1], 1000)
        mag, phase, omega = ctrl.bode(system, omega, plot=False)
        fig, ax = plt.subplots(2, 1, figsize=(8, 6))

        # diagramme d'amplitude
        ax[0].semilogx(omega, 20 * np.log10(mag))
        ax[0].set_title('Bode Plot')
        ax[0].set_ylabel('Magnitude (dB)')
        ax[0].grid(True, which='both', axis='both')
        ax[0].minorticks_on()
        ax[0].set_xscale('log')  # pour avoir un plan logarithmic
        ax[0].set_yscale('linear')

        # diagramme de phase
        ax[1].semilogx(omega, np.degrees(phase))
        ax[1].set_xlabel('Frequency (rad/s)')
        ax[1].set_ylabel('Phase (degrees)')
        ax[1].grid(True, which='both', axis='both')
        ax[1].minorticks_on()
        ax[1].set_xscale('log')  # pour avoir un plan logarithmic
        ax[1].set_yscale('linear')

        img = io.BytesIO()
        fig.savefig(img, format='svg')
        img.seek(0)

        response = send_file(
            img,
            mimetype='image/svg+xml',
        )

        return response

    # pour calculer les caracteristique d'etude frequentielle (marge de phase , marge de gain , marge de stability ...)
    def bode_performance(self,system:Union[TransferFunction|StateSpace]):
        gm,pm,sm,wpc,wgc,wms = ctrl.stability_margins(system)
        print(gm,pm,sm,wpc,wgc,wms)
        response = [
            {"key":"Gain Margin","value":sanitize_data(gm)}, # Marge de gain
            {"key":"Phase Margin","value":sanitize_data(pm)}, # Marge de phase
            {"key":"Stability Margin","value":sanitize_data(sm)}, # Marge de Stabilite
            {"key":"Gain Crossover Frequency", "value": sanitize_data(wgc)},
            {"key":"Phase Crossover Frequency","value":sanitize_data(wpc)},
            {"key":"Stability margin frequency","value":sanitize_data(wms)},
        ]

        return sanitize_data(response)

    # pour generer  diagramme de nyquist
    def nyquist(self,
                system: Union[TransferFunction, StateSpace],
                x_axis,
                y_axis,
                ):

        omega = np.logspace(-100, 100, 10000)

        plt.figure(figsize=(8, 6))

        ctrl.nyquist(system,omega)

        img_stream = io.BytesIO()
        plt.savefig(img_stream, format='svg')
        plt.close()
        img_stream.seek(0)

        response = send_file(
            img_stream,
            mimetype='image/svg+xml',
            # as_attachment=True,
        )

        return response

    # calcule de caracteristique de performance en reponse indicielle
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

    # calcule de boucle fermee
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

    # calcul de temps de stabilisation entre + et - 2% de valeur finale
    def settling(self, time, response, final_value: float):
        tolerance = 0.05 * final_value  # 5% tolerance
        settling_time = None

        for t, y in zip(time, response):
            if np.abs(y - final_value) > tolerance:
                settling_time = t
        return settling_time

    # calcule de depassement
    def calculate_overshoot(self, response, final_value: float):
        peak_value = np.max(response)
        overshoot = (peak_value - final_value) / final_value * 100
        return overshoot

    # calcule de pic et return temps de pic , valeur d'amplitude max
    def calculate_peak(self, time, response):
        return time[np.argmax(response)], np.max(response)

    # calcule de temps de reponse
    def calculate_rise_time(self, time, response, final_value):
        rise_time_start = np.where(response >= 0.1 * final_value)[0][0]
        rise_time_end = np.where(response >= 0.9 * final_value)[0][0]
        return time[rise_time_end] - time[rise_time_start]

    # calcule de temps de stabilisation entre + et - 2% de valeur finale (methode non utilise)
    def calculate_settling_time(self, time, response, final_value):
        return time[np.where(np.abs(response - final_value) <= 0.02 * final_value)[0][0]]

    # calcule d'erreur
    def calculate_steady_error(self, final_value, static_gain):
        return abs(final_value - static_gain)

    # calcule de gain static d'un system
    def calculate_static_gain(self, system: Union[TransferFunction, StateSpace]):
        system_type = self.get_system_type(system)
        if system_type == "tf":
            return system.num[0][0] / system.den[0][0]
        else:
            return np.dot(system.C, np.linalg.inv(system.A).dot(system.B))

    # calcule de valeur final de system
    def calculate_final_value(self, system: Union[TransferFunction | StateSpace]):
        return ctrl.dcgain(system)

    # dans les methode de ce service , les methodes recoit system comme argument ,
    # ce system est de type Union[TransferFunction,StateSpace] , donc il peut etre un model espace d'etat ,
    # ou bien un model fonction transfer , donc on verifi s'il est un instant de class TransferFunction ,
    # sinon il est un instant de StateSpace
    def get_system_type(self, system: Union[TransferFunction, StateSpace]):
        if isinstance(system, TransferFunction):
            return "tf"
        else:
            return "ss"

    # calcule de vecteur du temps
    def generate_time(self, t_end: float):
        return np.arange(0, t_end, 0.01)