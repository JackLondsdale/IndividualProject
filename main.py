import tkinter as tk
from tkinter import ttk, messagebox
import math
import subprocess
import os

# Define a class for the Equation Solver application, inheriting from tk.Tk
class EquationSolverApp(tk.Tk):
    def __init__(self):
        
        # Initialize the parent class (tk.Tk)
        super().__init__()
        
        # Set the title of the application window
        self.title("Equation Solver")
        
        # Set the dimensions of the application window
        self.geometry("400x600")
        
        self.scripts = {
           "Ideal Gas Law": "idealgas.py",
           "First Order Rate Law": "ratelaw.py"
           "Clausius Clapeyron Equation" "clausius.py"
           "Heisenberg Uncertainty Principle" "heisen.py"
       }
        
        # Define a dictionary to store equations
        self.equations = {

        # (Further initialization and GUI components would be added here)
            "Thermodynamics (Gibbs Free Energy)": ("G = H - T*S", ["G", "H", "T", "S"]),
            "Ideal Gas Law": ("P*V = n*R*T", ["P", "V", "n", "R", "T"]),
            "Arrhenius Equation": ("k = A*exp(-Ea/(R*T))", ["k", "A", "Ea", "R", "T"]),
            "Nernst Equation": ("E = E0 - (R*T)/(n*F) * ln(Q)", ["E", "E0", "R", "T", "n", "F", "Q"]),
            "Rate Law (First Order)": ("ln([A]_t) = -k*t + ln([A]_0)", ["[A]_t", "k", "t", "[A]_0"]),
            "Clausius Equation (Entropy Change)": ("ΔS = q_rev / T", ["ΔS", "q_rev", "T"]),
            "Beer-Lambert Law": ("A = epsilon * c * l", ["A", "epsilon", "c", "l"]),
            "Gibbs Free Energy for Electrochemical Cells": ("ΔG = -n*F*E", ["ΔG", "n", "F", "E"]),
            "Debye-Hückel Equation": ("gamma_pm = exp(-A * sqrt(I) / (1 + B * a * sqrt(I)))", ["gamma_pm", "A", "I", "B", "a"]),
            "Schrödinger Equation": ("H * Psi = E * Psi", ["H", "Psi", "E"]),
            "Heisenberg Uncertainty Principle": ("Δx * Δp >= h_bar / 2", ["Δx", "Δp", "h_bar"]),
            "Bragg's Law": ("n*lambda = 2*d*sin(theta)", ["n", "lambda", "d", "theta"]),
            "Clausius-Clapeyron Equation": ("ln(P2/P1) = (ΔHvap/R) * (1/T1 - 1/T2)", ["P1", "P2", "ΔHvap", "R", "T1", "T2"]),
            "First Law of Thermodynamics": ("ΔU = q + W", ["ΔU", "q", "W"]),
            "Van der Waals Equation": ("(P + a*n^2/V^2) * (V - n*b) = n*R*T", ["P", "V", "n", "a", "b", "R", "T"]),
            "Raoult's Law": ("P_solution = X_solvent * P0_solvent", ["P_solution", "X_solvent", "P0_solvent"]),
            "Hess's Law": ("ΔH_reaction = sum(ΔH_products) - sum(ΔH_reactants)", ["ΔH_reaction", "ΔH_products", "ΔH_reactants"]),
            "Coulomb's Law": ("F = k_e * (q1 * q2) / r^2", ["F", "k_e", "q1", "q2", "r"]),
            "Michaelis-Menten Equation": ("v = (Vmax * [S]) / (Km + [S])", ["v", "Vmax", "[S]", "Km"]),
            "Henderson-Hasselbalch Equation": ("pH = pKa + log([A-]/[HA])", ["pH", "pKa", "[A-]", "[HA]"]),
            "Avogadro's Law": ("V1/n1 = V2/n2", ["V1", "n1", "V2", "n2"]),
            "Faraday's Law of Electrolysis": ("m = (Q * M) / (n * F)", ["m", "Q", "M", "n", "F"])
        }

        self.create_widgets()

    def create_widgets(self):

        
        self.equation_label = ttk.Label(self, text="Select Simulation:", style='Custom.TLabel')
        self.equation_label.pack(pady=(20, 5), padx=20)
        
        
    # Dropdown for simulations
        self.simulation_var = tk.StringVar()
        self.simulation_dropdown = ttk.Combobox(self, textvariable=self.simulation_var)
        self.simulation_dropdown['values'] = ("Ideal Gas Simulation", "First Order Rate Law Simulation", "Clausius Clapeyron Simulation", "Heisenberg Simulation")
        self.simulation_dropdown.pack(pady=10)
    
        # Run button
        self.run_button = ttk.Button(self, text="Run Simulation", command=self.run_selected_simulation)
        self.run_button.pack(pady=10)
        
        # Equation Label
        self.equation_label = ttk.Label(self, text="Select Equation:", style='Custom.TLabel')
        self.equation_label.pack(pady=(20, 5), padx=20)

        # Equation Combobox
        self.equation_combobox = ttk.Combobox(self, values=list(self.equations.keys()), style='Custom.TCombobox')
        self.equation_combobox.pack(pady=5, padx=20)
        self.equation_combobox.bind("<<ComboboxSelected>>", self.display_inputs)

        # Input Frame
        self.input_frame = ttk.Frame(self, style='Custom.TFrame')
        self.input_frame.pack(pady=(20, 10), padx=20, fill='x')

        # Calculate Button
        self.calculate_button = ttk.Button(self, text="Calculate", command=self.calculate, style='Custom.TButton')
        self.calculate_button.pack(pady=10)

        # Result Frame
        self.result_frame = ttk.Frame(self, style='Custom.TFrame', borderwidth=2, relief="solid")
        self.result_frame.pack(pady=20, padx=20, fill='both', expand=True)

        # Result Label
        self.result_label = ttk.Label(self.result_frame, text="Result: ", style='Custom.TLabel')
        self.result_label.pack(padx=10, pady=5)

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('Custom.TCombobox', padding=5, width=30, background="#E0E0E0", foreground="#00796B")
        self.style.configure('Custom.TButton', padding=10, background="#00796B", foreground="#00796B", font=('TkDefaultFont', 10, 'bold'))
        self.style.map('Custom.TButton', background=[('active', '#005a52')])
        self.style.configure('Custom.TLabel', padding=5, background="#E0E0E0", foreground="#00796B", font=('TkDefaultFont', 10, 'bold'))
        self.style.configure('Custom.TFrame', background="#E0E0E0", borderwidth=2, relief="solid", bordercolor="#2E363D")
    def run_selected_simulation(self):
        selected_simulation = self.simulation_var.get()
        if selected_simulation == "Ideal Gas Simulation":
            self.open_idealgas()
        elif selected_simulation == "First Order Rate Law Simulation":
            self.open_ratelaw()  
        elif selected_simulation == "Clausius Clapeyron Simulation":
            self.open_clausius()
        elif selected_simulation == "Heisenberg Simulation":
            self.open_heisen()
    def open_idealgas(self):
            try:
                subprocess.Popen(['python', 'idealgas.py'])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open idealgas.py: {e}")
                
    def open_ratelaw(self):
            try:
                subprocess.Popen(['python', 'ratelaw.py'])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open ratelaw.py: {e}")
                
    def open_clausius(self):
            try:
                subprocess.Popen(['python', 'clausius.py'])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open clausius.py: {e}")
                
    def open_heisen(self):
            try:
                subprocess.Popen(['python', 'heisen.py'])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open heisen.py: {e}")
            
    def display_inputs(self, event):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        self.inputs = {}
        equation = self.equation_combobox.get()
        _, variables = self.equations[equation]

        for i, var in enumerate(variables):
            label = ttk.Label(self.input_frame, text=var)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(self.input_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.inputs[var] = entry


    def calculate(self):
        # Get the selected equation from the combobox
        equation = self.equation_combobox.get()
        
        # Retrieve the formula and variables associated with the selected equation
        formula, variables = self.equations[equation]
        
        # Dictionary to store variable values entered by the user
        values = {}
        
        # Variable to keep track of which variable is missing (if any)
        missing_var = None
        
        try:
            # Iterate through each variable required by the equation
            for var in variables:
                # Get the input entry field for the current variable
                entry = self.inputs[var]
                
                # Get the value entered by the user in the entry field
                value = entry.get()
                
                # Check if the entry field is empty
                if value == "":
                    # If this is the first missing variable encountered, store it
                    if missing_var is None:
                        missing_var = var
                    else:
                        # If more than one variable is missing, show an error message
                        messagebox.showerror("Error", "More than one variable is missing.")
                        return
                else:
                    # If the entry field is not empty, convert the value to float and store it in the dictionary
                    values[var] = float(value)
            
            # If no variable is missing, show an error message
            if missing_var is None:
                messagebox.showerror("Error", "No variable is missing.")
                return
    
            # Calculate the missing variable based on the selected equation
            if equation == "Thermodynamics (Gibbs Free Energy)":
                # Calculate the missing variable based on the Gibbs Free Energy equation
                if missing_var == "G":
                    result = values["H"] - values["T"] * values["S"]
                elif missing_var == "H":
                    result = values["G"] + values["T"] * values["S"]
                elif missing_var == "T":
                    result = (values["H"] - values["G"]) / values["S"]
                elif missing_var == "S":
                    result = (values["H"] - values["G"]) / values["T"]


            elif equation == "Ideal Gas Law":
                if missing_var == "P":
                    result = (values["n"] * values["R"] * values["T"]) / values["V"]
                elif missing_var == "V":
                    result = (values["n"] * values["R"] * values["T"]) / values["P"]
                elif missing_var == "n":
                    result = (values["P"] * values["V"]) / (values["R"] * values["T"])
                elif missing_var == "R":
                    result = (values["P"] * values["V"]) / (values["n"] * values["T"])
                elif missing_var == "T":
                    result = (values["P"] * values["V"]) / (values["n"] * values["R"])

            elif equation == "Arrhenius Equation":
                if missing_var == "k":
                    result = values["A"] * math.exp(-values["Ea"] / (values["R"] * values["T"]))
                elif missing_var == "A":
                    result = values["k"] / math.exp(-values["Ea"] / (values["R"] * values["T"]))
                elif missing_var == "Ea":
                    result = -values["R"] * values["T"] * math.log(values["k"] / values["A"])
                elif missing_var == "R":
                    result = -values["Ea"] / (values["T"] * math.log(values["k"] / values["A"]))
                elif missing_var == "T":
                    result = -values["Ea"] / (values["R"] * math.log(values["k"] / values["A"]))

            elif equation == "Nernst Equation":
                if missing_var == "E":
                    result = values["E0"] - (values["R"] * values["T"]) / (values["n"] * values["F"]) * math.log(values["Q"])
                elif missing_var == "E0":
                    result = values["E"] + (values["R"] * values["T"]) / (values["n"] * values["F"]) * math.log(values["Q"])
                elif missing_var == "R":
                    result = (values["E0"] - values["E"]) * (values["n"] * values["F"]) / (values["T"] * math.log(values["Q"]))
                elif missing_var == "T":
                    result = (values["E0"] - values["E"]) * (values["n"] * values["F"]) / (values["R"] * math.log(values["Q"]))
                elif missing_var == "n":
                    result = (values["R"] * values["T"] * math.log(values["Q"])) / (values["F"] * (values["E0"] - values["E"]))
                elif missing_var == "F":
                    result = (values["R"] * values["T"] * math.log(values["Q"])) / (values["n"] * (values["E0"] - values["E"]))
                elif missing_var == "Q":
                    result = math.exp((values["E0"] - values["E"]) * (values["n"] * values["F"]) / (values["R"] * values["T"]))
                    
            elif equation == "Michaelis-Menten Equation":
                if missing_var == "v":
                    result = (values["Vmax"] * values["[S]"]) / (values["Km"] + values["[S]"])
                elif missing_var == "Vmax":
                    result = (values["v"] * (values["Km"] + values["[S]"])) / values["[S]"]
                elif missing_var == "[S]":
                    result = (values["v"] * values["Km"]) / (values["Vmax"] - values["v"])
                elif missing_var == "Km":
                    result = (values["Vmax"] * values["[S]"]) / values["v"] - values["[S]"]
            
            elif equation == "Henderson-Hasselbalch Equation":
                if missing_var == "pH":
                    result = values["pKa"] + math.log10(values["[A-]"] / values["[HA]"])
                elif missing_var == "pKa":
                    result = values["pH"] - math.log10(values["[A-]"] / values["[HA]"])
                elif missing_var == "[A-]":
                    result = 10**(values["pH"] - values["pKa"]) * values["[HA]"]
                elif missing_var == "[HA]":
                    result = values["[A-]"] / 10**(values["pH"] - values["pKa"])
                    
            elif equation == "Faraday's Law of Electrolysis":
                if missing_var == "m":
                    result = (values["Q"] * values["M"]) / (values["n"] * values["F"])
                elif missing_var == "Q":
                    result = (values["m"] * values["n"] * values["F"]) / values["M"]
                elif missing_var == "M":
                    result = (values["m"] * values["n"] * values["F"]) / values["Q"]
                elif missing_var == "n":
                    result = (values["m"] * values["F"]) / (values["Q"] * values["M"])
                elif missing_var == "F":
                    result = (values["m"] * values["n"]) / (values["Q"] * values["M"])
                    
            elif equation == "Avogadro's Law":
                if missing_var == "V1":
                    result = (values["n1"] * values["V2"]) / values["n2"]
                elif missing_var == "n1":
                    result = (values["V1"] * values["n2"]) / values["V2"]
                elif missing_var == "V2":
                    result = (values["V1"] * values["n2"]) / values["n1"]
                elif missing_var == "n2":
                    result = (values["V2"] * values["n1"]) / values["V1"]   
                    
            elif equation == "Rate Law (First Order)":
                if missing_var == "[A]_t":
                    result = math.exp(-values["k"] * values["t"] + math.log(values["[A]_0"]))
                elif missing_var == "k":
                    result = -(math.log(values["[A]_t"]) - math.log(values["[A]_0"])) / values["t"]
                elif missing_var == "t":
                    result = -(math.log(values["[A]_t"]) - math.log(values["[A]_0"])) / values["k"]
                elif missing_var == "[A]_0":
                    result = math.exp(math.log(values["[A]_t"]) + values["k"] * values["t"])
            
            elif equation == "Clausius Equation (Entropy Change)":
                if missing_var == "ΔS":
                    result = values["q_rev"] / values["T"]
                elif missing_var == "q_rev":
                    result = values["ΔS"] * values["T"]
                elif missing_var == "T":
                    result = values["q_rev"] / values["ΔS"]
            
            elif equation == "Beer-Lambert Law":
                if missing_var == "A":
                    result = values["epsilon"] * values["c"] * values["l"]
                elif missing_var == "epsilon":
                    result = values["A"] / (values["c"] * values["l"])
                elif missing_var == "c":
                    result = values["A"] / (values["epsilon"] * values["l"])
                elif missing_var == "l":
                    result = values["A"] / (values["epsilon"] * values["c"])
            
            elif equation == "Gibbs Free Energy for Electrochemical Cells":
                if missing_var == "ΔG":
                    result = -values["n"] * values["F"] * values["E"]
                elif missing_var == "n":
                    result = -values["ΔG"] / (values["F"] * values["E"])
                elif missing_var == "F":
                    result = -values["ΔG"] / (values["n"] * values["E"])
                elif missing_var == "E":
                    result = -values["ΔG"] / (values["n"] * values["F"])
            
            elif equation == "Debye-Hückel Equation":
                if missing_var == "gamma_pm":
                    result = math.exp(-values["A"] * math.sqrt(values["I"]) / (1 + values["B"] * values["a"] * math.sqrt(values["I"])))
                elif missing_var == "A":
                    result = -math.log(values["gamma_pm"]) * (1 + values["B"] * values["a"] * math.sqrt(values["I"])) / math.sqrt(values["I"])
                elif missing_var == "I":
                    result = (math.log(values["gamma_pm"]) * (1 + values["B"] * values["a"]) / values["A"]) ** 2
                elif missing_var == "B":
                    result = (-math.log(values["gamma_pm"]) - values["A"] * math.sqrt(values["I"])) / (values["a"] * math.sqrt(values["I"]))
                elif missing_var == "a":
                    result = (-math.log(values["gamma_pm"]) - values["A"] * math.sqrt(values["I"])) / (values["B"] * math.sqrt(values["I"]))
            
            elif equation == "Schrödinger Equation":
                if missing_var == "H":
                    result = values["E"] * values["Psi"] / values["Psi"]
                elif missing_var == "Psi":
                    result = values["E"] * values["H"] / values["E"]
                elif missing_var == "E":
                    result = values["H"] * values["Psi"] / values["Psi"]
            
            elif equation == "Heisenberg Uncertainty Principle":
                if missing_var == "Δx":
                    result = values["h_bar"] / (2 * values["Δp"])
                elif missing_var == "Δp":
                    result = values["h_bar"] / (2 * values["Δx"])
                elif missing_var == "h_bar":
                    result = 2 * values["Δx"] * values["Δp"]
            
            elif equation == "Bragg's Law":
                if missing_var == "n":
                    result = 2 * values["d"] * math.sin(math.radians(values["theta"])) / values["lambda"]
                elif missing_var == "lambda":
                    result = 2 * values["d"] * math.sin(math.radians(values["theta"])) / values["n"]
                elif missing_var == "d":
                    result = values["n"] * values["lambda"] / (2 * math.sin(math.radians(values["theta"])))
                elif missing_var == "theta":
                    result = math.degrees(math.asin(values["n"] * values["lambda"] / (2 * values["d"])))
            
            elif equation == "Clausius-Clapeyron Equation":
                if missing_var == "P1":
                    result = values["P2"] * math.exp((values["ΔHvap"] / values["R"]) * (1 / values["T1"] - 1 / values["T2"]))
                elif missing_var == "P2":
                    result = values["P1"] * math.exp(-(values["ΔHvap"] / values["R"]) * (1 / values["T1"] - 1 / values["T2"]))
                elif missing_var == "ΔHvap":
                    result = values["R"] * math.log(values["P2"] / values["P1"]) / (1 / values["T1"] - 1 / values["T2"])
                elif missing_var == "R":
                    result = values["ΔHvap"] / (math.log(values["P2"] / values["P1"]) * (1 / values["T1"] - 1 / values["T2"]))
                elif missing_var == "T1":
                    result = 1 / ((math.log(values["P2"] / values["P1"]) * values["R"] / values["ΔHvap"]) + (1 / values["T2"]))
                elif missing_var == "T2":
                    result = 1 / (1 / values["T1"] - (math.log(values["P2"] / values["P1"]) * values["R"] / values["ΔHvap"]))
            
            elif equation == "First Law of Thermodynamics":
                if missing_var == "ΔU":
                    result = values["q"] + values["W"]
                elif missing_var == "q":
                    result = values["ΔU"] - values["W"]
                elif missing_var == "W":
                    result = values["ΔU"] - values["q"]
            
            elif equation == "Van der Waals Equation":
                if missing_var == "P":
                    result = (values["n"] * values["R"] * values["T"] / (values["V"] - values["n"] * values["b"])) - (values["a"] * values["n"]**2 / values["V"]**2)
                elif missing_var == "V":
                    result = values["n"] * values["R"] * values["T"] / (values["P"] + values["a"] * values["n"]**2 / values["V"]**2) + values["n"] * values["b"]
                elif missing_var == "n":
                    result = (values["P"] + values["a"] * values["n"]**2 / values["V"]**2) * (values["V"] - values["n"] * values["b"]) / (values["R"] * values["T"])
                elif missing_var == "a":
                    result = (values["P"] + values["n"] * values["R"] * values["T"] / (values["V"] - values["n"] * values["b"])) * values["V"]**2 / values["n"]**2
                elif missing_var == "b":
                    result = (values["V"] - values["n"] * values["R"] * values["T"] / (values["P"] + values["a"] * values["n"]**2 / values["V"]**2)) / values["n"]
                elif missing_var == "R":
                    result = (values["P"] + values["a"] * values["n"]**2 / values["V"]**2) * (values["V"] - values["n"] * values["b"]) / (values["n"] * values["T"])
                elif missing_var == "T":
                    result = (values["P"] + values["a"] * values["n"]**2 / values["V"]**2) * (values["V"] - values["n"] * values["b"]) / (values["n"] * values["R"])
            
            elif equation == "Raoult's Law":
                if missing_var == "P_solution":
                    result = values["X_solvent"] * values["P0_solvent"]
                elif missing_var == "X_solvent":
                    result = values["P_solution"] / values["P0_solvent"]
                elif missing_var == "P0_solvent":
                    result = values["P_solution"] / values["X_solvent"]
            
            elif equation == "Hess's Law":
                if missing_var == "ΔH_reaction":
                    result = sum(values["ΔH_products"]) - sum(values["ΔH_reactants"])
                elif missing_var == "ΔH_products":
                    result = values["ΔH_reaction"] + sum(values["ΔH_reactants"])
                elif missing_var == "ΔH_reactants":
                    result = sum(values["ΔH_products"]) - values["ΔH_reaction"]
            
            elif equation == "Coulomb's Law":
                if missing_var == "F":
                    result = values["k_e"] * (values["q1"] * values["q2"]) / values["r"]**2
                elif missing_var == "k_e":
                    result = values["F"] * values["r"]**2 / (values["q1"] * values["q2"])
                elif missing_var == "q1":
                    result = values["F"] * values["r"]**2 / (values["k_e"] * values["q2"])
                elif missing_var == "q2":
                    result = values["F"] * values["r"]**2 / (values["k_e"] * values["q1"])
                elif missing_var == "r":
                    result = math.sqrt(values["k_e"] * values["q1"] * values["q2"] / values["F"])

            self.result_label.config(text=f"Result: {missing_var} = {result}")

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

if __name__ == "__main__":
    app = EquationSolverApp()
    app.mainloop()
