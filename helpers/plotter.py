from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from flask import render_template
import matplotlib

matplotlib.use("SVG")

class Plotter:
    def __init__(self):
        pass

    def plot(self,
             t:np.ndarray,
             y:np.ndarray,
             title:str="State-Space Step Response",
             xlabel:str="Time (seconds)",
             ylabel:str="Response",
             grid:bool=True,
             legend:str="Response",
             xlim=[0,10],
             ylim=[-5,5]
             ):
        plt.figure(figsize=(8,6))
        plt.plot(t, y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.grid(grid)
        if legend: plt.legend([legend])

        img_stream = BytesIO()
        plt.savefig(img_stream, format='svg')
        img_stream.seek(0)

        return img_stream

    # def save_svg(self):
    #       # Rewind to the start of the stream
    #     return img_stream
