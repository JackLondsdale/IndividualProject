import tkinter as tk
from tkinter import ttk
import random
import math

class IdealGasSimulationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ideal Gas Simulation")

        # Style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Button style
        self.style.configure("TButton", 
                             foreground="white", 
                             background="darkgreen", 
                             font=("Arial", 12, "bold"),
                             padding=6)
        self.style.map("TButton", 
                       background=[("active", "forestgreen"), ("disabled", "gray")])
        
        # Label style
        self.style.configure("TLabel", 
                             foreground="black", 
                             background="#f0f0f0", 
                             font=("Arial", 12, "bold"))
        
        # Scale style
        self.style.configure("TScale",
                             troughcolor="darkgray", 
                             background="lightgray", 
                             foreground="black", 
                             font=("Arial", 10), 
                             sliderlength=20)
        
        # Frame background color
        self.master.configure(background="#f8f8f8")
        
        # Parameters
        self.temperature = tk.DoubleVar()
        self.pressure = tk.DoubleVar()
        self.volume = tk.DoubleVar()
        
        # Default values
        self.temperature.set(300)  # Kelvin
        self.pressure.set(101325)  # Pascals
        self.volume.set(0.01)      # m^3
        
        # Canvas
        self.canvas = tk.Canvas(master, width=350, height=350, bg="#e0e0e0", borderwidth=0, relief="flat")
        self.canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Labels and sliders
        self.create_label_and_scale(master, "Temperature (K):", self.temperature, 100, 1500, 10).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.create_label_and_scale(master, "Pressure (Pa):", self.pressure, 10000, 200000, 1000).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.create_label_and_scale(master, "Volume (m^3):", self.volume, 0.001, 50, 0.001).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        # Start and stop buttons
        self.start_button = ttk.Button(master, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.stop_button = ttk.Button(master, text="Stop Simulation", command=self.stop_simulation, state=tk.DISABLED)
        self.stop_button.grid(row=5, column=0, columnspan=2, pady=5)

    def create_label_and_scale(self, master, text, variable, min_val, max_val, resolution):
        frame = ttk.Frame(master)
        
        label = ttk.Label(frame, text=text)
        label.pack(side=tk.TOP, anchor=tk.W)
        
        value_label = ttk.Label(frame, text=f"{variable.get():.2f}")
        value_label.pack(side=tk.RIGHT, padx=5)
        
        scale = ttk.Scale(frame, variable=variable, orient=tk.HORIZONTAL, length=400,
                          from_=min_val, to=max_val, command=lambda v, var=variable: self.update_value_label(var, value_label))
        scale.pack(side=tk.LEFT, padx=5, pady=5)
        
        min_max_label = ttk.Label(frame, text=f"Min: {min_val}, Max: {max_val}")
        min_max_label.pack(side=tk.BOTTOM, anchor=tk.W)
        
        return frame
    
    def update_value_label(self, variable, label):
        label.config(text=f"{variable.get():.2f}")



    def create_float_scale(self, master, variable, from_, to, resolution):
        scale = ttk.Scale(master, from_=from_, to=to, variable=variable, orient=tk.HORIZONTAL, style="Horizontal.TScale")
        scale.set(variable.get())
        scale.bind("<Motion>", lambda event: self.update_float_scale_label(variable, resolution))
        return scale

    def update_float_scale_label(self, variable, resolution):
        value = round(variable.get() / resolution) * resolution
        variable.set(value)

    def start_simulation(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
    
        gas_constant = 8.314  # J/(mol*K)
        num_particles = 80
    
        # Calculate the mean speed of the particles
        # The formula is sqrt((3 * R * T) / (V * P * constant_factor))
        temperature = self.temperature.get()
        volume = self.volume.get()
        pressure = self.pressure.get()
        constant_factor = 0.1  # Adjust this factor to match your desired behavior
    
        speed = math.sqrt((3 * gas_constant * temperature) / (volume * pressure * constant_factor))
    
        self.particles = []
        for _ in range(num_particles):
            x = random.randint(50, 450)
            y = random.randint(50, 450)
            vx = random.uniform(-speed, speed)
            vy = random.uniform(-speed, speed)
            particle = self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="red", outline="black", width=1, tags="particle")
            self.particles.append([particle, vx, vy])
    
        self.move_particles()




    def move_particles(self):
        for particle_info in self.particles:
            particle, vx, vy = particle_info
            self.canvas.move(particle, vx, vy)
            pos = self.canvas.coords(particle)
            if pos[0] <= 0 or pos[2] >= 350:
                vx = -vx
            if pos[1] <= 0 or pos[3] >= 350:
                vy = -vy
            particle_info[1] = vx
            particle_info[2] = vy
        self.canvas.update()
        self.master.after(20, self.move_particles)  # Update every 20 milliseconds

    def stop_simulation(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        for particle_info in self.particles:
            particle, _, _ = particle_info
            self.canvas.delete(particle)
        self.particles = []

if __name__ == "__main__":
    root = tk.Tk()
    app = IdealGasSimulationApp(root)
    root.mainloop()
