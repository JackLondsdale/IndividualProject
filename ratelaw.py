import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class FirstOrderRateLawSimulationApp:
    def __init__(self, master):
        # Initialize the First Order Rate Law Simulation App with a master window.
        self.master = master
        self.master.title("First Order Rate Law Simulation")

        # Initialize variables for rate constant and initial concentration of A.
        self.k = tk.DoubleVar(value=1.0)
        self.concentration_a = tk.DoubleVar(value=1.0)

        # Create the user interface components.
        self.create_ui()

    def create_ui(self):
        # Create sliders for adjusting rate constant and initial concentration.
        self.create_sliders()
        # Create the plot area.
        self.create_plot()

    def create_sliders(self):
        # Create a frame to hold the sliders.
        frame = ttk.Frame(self.master)
        frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Slider for adjusting the rate constant.
        ttk.Label(frame, text="Rate Constant (k):").grid(row=0, column=0, sticky=tk.W)
        self.k_slider = ttk.Scale(frame, from_=0.1, to=10, variable=self.k, orient=tk.HORIZONTAL, command=self.update_plot)
        self.k_slider.grid(row=0, column=1, sticky=tk.EW)

        # Slider for adjusting the initial concentration of A.
        ttk.Label(frame, text="Initial Concentration [A]:").grid(row=1, column=0, sticky=tk.W)
        self.concentration_a_slider = ttk.Scale(frame, from_=0.1, to=10, variable=self.concentration_a, orient=tk.HORIZONTAL, command=self.update_plot)
        self.concentration_a_slider.grid(row=1, column=1, sticky=tk.EW)

        frame.columnconfigure(1, weight=1)

    def create_plot(self):
        # Create a plot area.
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.update_plot()

    def update_plot(self, *args):
        # Update the plot with current slider values.
        k = self.k.get()
        concentration_a = self.concentration_a.get()

        time = np.linspace(0, 10, 500)
        concentration = concentration_a * np.exp(-k * time)

        self.ax.clear()
        self.ax.plot(time, concentration, label=f"[A](t) with k={k:.2f}, [A]_0={concentration_a:.2f}")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Concentration [A]")
        self.ax.legend()
        self.ax.set_title("First Order Rate Law: [A] = [A]_0 * exp(-kt)")
        self.canvas.draw()

if __name__ == "__main__":
    # Create the Tkinter root window and initialize the simulation app.
    root = tk.Tk()
    app = FirstOrderRateLawSimulationApp(root)
    root.mainloop()
