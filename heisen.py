import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class HeisenbergUncertaintyApp:
    def __init__(self, root):
        # Initialize the Heisenberg Uncertainty App with a root window.
        self.root = root
        self.root.title("Heisenberg Uncertainty Principle Visualization")

        # Create a frame to hold the widgets.
        self.frame = ttk.Frame(root)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        # Create widgets and plot.
        self.create_widgets()
        self.create_plot()

    def create_widgets(self):
        # Create a label for displaying the uncertainty in position.
        ttk.Label(self.frame, text="Uncertainty in Position (Δx):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        
        # Create a slider to control the uncertainty in position.
        self.dx_var = tk.DoubleVar(value=1.0)
        self.dx_scale = ttk.Scale(self.frame, variable=self.dx_var, from_=0.1, to_=5.0, orient='horizontal', command=self.update_plot)
        self.dx_scale.grid(row=0, column=1, padx=5, pady=5)

        # Create a button to reset the sliders.
        self.reset_button = ttk.Button(self.frame, text="Reset", command=self.reset_sliders)
        self.reset_button.grid(row=0, column=2, padx=5, pady=5)

        # Create a figure and axis for plotting.
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        # Create a canvas to display the plot within the frame.
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=3)

        # Set plotting to True and update the plot.
        self.plotting = True
        self.update_plot()

    def create_plot(self):
        self.update_plot()
        self.root.after(100, self.update_plot)

    def update_plot(self, event=None):
        if self.plotting:
            dx = self.dx_var.get()
            hbar = 1.0  # Reduced Planck constant in normalized units
            dp = hbar / (2 * dx)  # Uncertainty in momentum due to the uncertainty principle

            # Clear the previous plot
            self.ax.clear()

            # Generate data for position and momentum uncertainties
            x = np.linspace(-10, 10, 100)
            p = np.linspace(-10, 10, 100)

            # Gaussian distribution in position space
            pos_distribution = (1 / (dx * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (x / dx) ** 2)
            pos_particles = np.random.normal(0, dx, 1000)

            # Gaussian distribution in momentum space
            mom_distribution = (1 / (dp * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (p / dp) ** 2)
            mom_particles = np.random.normal(0, dp, 1000)

            # Plotting position uncertainty
            self.ax.hist(pos_particles, bins=50, density=True, alpha=0.6, color='blue', label='Position')
            self.ax.plot(x, pos_distribution, color='blue', linestyle='--')

            # Plotting momentum uncertainty
            self.ax.hist(mom_particles, bins=50, density=True, alpha=0.6, color='red', label='Momentum')
            self.ax.plot(p, mom_distribution, color='red', linestyle='--')

            # Adding text annotations
            self.ax.text(0.95, 0.95, f"Δx = {dx:.2f}\nΔp = {dp:.2f}\nΔx * Δp = {dx * dp:.2f}",
                         verticalalignment='top', horizontalalignment='right', transform=self.ax.transAxes,
                         color='black', fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))

            # Move the legend to the upper left corner to avoid overlap
            self.ax.legend(loc='upper left')

            self.ax.set_title("Heisenberg Uncertainty Principle")
            self.ax.set_xlabel("Value")
            self.ax.set_ylabel("Probability Density")
            self.ax.grid(True)

            # Set fixed axes limits
            self.ax.set_xlim(-10, 10)
            self.ax.set_ylim(0, 1.2)

            # Redraw the canvas
            self.canvas.draw()

    def reset_sliders(self):
        self.dx_var.set(1.0)
        self.update_plot()

    def start_plotting(self):
        self.plotting = True

    def stop_plotting(self):
        self.plotting = False

if __name__ == "__main__":
    root = tk.Tk()
    app = HeisenbergUncertaintyApp(root)
    root.mainloop()
