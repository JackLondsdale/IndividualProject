import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

class ClausiusClapeyronApp:
    def __init__(self, root):
        # Initialize the Clausius-Clapeyron App with a root window.
        self.root = root
        self.root.title("Clausius-Clapeyron Equation Visualization")
        
        # Create a frame to hold the widgets.
        self.frame = ttk.Frame(root)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        # Create widgets and plot.
        self.create_widgets()
        self.plot()

    def create_widgets(self):
        # Create labels and scales for user input parameters.
        ttk.Label(self.frame, text="Latent Heat (L, J/mol):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.l_var = tk.DoubleVar(value=40000)
        ttk.Scale(self.frame, variable=self.l_var, from_=20000, to_=80000, orient='horizontal').grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Initial Temperature (T1, K):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.t1_var = tk.DoubleVar(value=298)
        ttk.Scale(self.frame, variable=self.t1_var, from_=250, to_=350, orient='horizontal').grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Initial Pressure (P1, Pa):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.p1_var = tk.DoubleVar(value=101325)
        ttk.Scale(self.frame, variable=self.p1_var, from_=50000, to_=200000, orient='horizontal').grid(row=2, column=1, padx=5, pady=5)

        # Create a button to update the plot.
        ttk.Button(self.frame, text="Update Plot", command=self.plot).grid(row=3, column=0, columnspan=2, pady=10)

    def plot(self):
        # Retrieve user input values.
        L = self.l_var.get()
        T1 = self.t1_var.get()
        P1 = self.p1_var.get()
        R = 8.314  # J/(mol K)

        # Calculate corresponding temperatures and pressures using the Clausius-Clapeyron equation.
        T2 = np.linspace(250, 400, 500)
        P2 = P1 * np.exp(-L/R * (1/T2 - 1/T1)) / 1000  # Convert Pa to kPa

        # Create a plot.
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        norm = Normalize(vmin=min(T2), vmax=max(T2))
        sm = ScalarMappable(cmap='viridis', norm=norm)
        sm.set_array([])

        # Plot the data points and color them based on temperature.
        for i in range(len(T2)-1):
            ax.plot(T2[i:i+2], P2[i:i+2], color=sm.to_rgba(T2[i]))

        # Add a color bar to the plot.
        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label('Temperature (K)')

        
        # Adding annotations
        step = len(T2) // 10
        for i in range(0, len(T2), step):
            ax.annotate(f'{P2[i]:.2f} kPa', (T2[i], P2[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color='blue')

        ax.set_title("Clausius-Clapeyron Equation: Vapor Pressure vs. Temperature")
        ax.set_xlabel("Temperature (K)")
        ax.set_ylabel("Vapor Pressure (kPa)")
        ax.grid(True)

        # Adjusting y-axis intervals
        max_pressure = max(P2)
        interval = max_pressure / 10
        ax.set_yticks(np.arange(0, max_pressure + interval, interval))

        # Make plot interactive
        plt.subplots_adjust(left=0.1, bottom=0.2)
        plt.xticks(np.arange(min(T2), max(T2)+1, 10))
        plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment='right')

        for widget in self.frame.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClausiusClapeyronApp(root)
    root.mainloop()
