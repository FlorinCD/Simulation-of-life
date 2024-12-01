import tkinter as tk
import logging
import simulation

from tkinter import Text, messagebox



class Menu:

    def __init__(self):
        self.root = tk.Tk()
        self.frame = None
        self.run_button = None

        self.prey_number_label = None
        self.predator_number_label = None

        self.prey_number_text = None
        self.predator_number_text = None

        self.prey_number_value = None
        self.predator_number_value = None

        self.decorate_menu()

        self.root.mainloop()

    """Decorate the tkinter interface with all the widgets"""
    def decorate_menu(self):
        self.root.title("Simulation of life")
        self.root.geometry("600x600")
        self.root.iconbitmap(r"static/icons/simulation_of_life.ico")
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, bg="lightblue", padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.prey_number_label = tk.Label(self.frame, text="The number of preys:", anchor="w", bg='lightblue',
                                          font=("Arial", 11))
        self.prey_number_label.place(x=20, y=50)

        self.prey_number_text = Text(self.frame, height=1, width=20)
        self.prey_number_text.place(x=200, y=53)

        self.predator_number_label = tk.Label(self.frame, text="The number of predators:", anchor="w", bg='lightblue',
                                          font=("Arial", 11))
        self.predator_number_label.place(x=20, y=100)

        self.predator_number_text = Text(self.frame, height=1, width=20)
        self.predator_number_text.place(x=200, y=100)

        self.run_button = tk.Button(self.frame, text="Run Simulation", command=self.run_simulation_button, font=("Arial", 11), bg='green')
        self.run_button.place(x=230, y=500)



    """Run the simulation with the given parameters"""
    def run_simulation_button(self):
        self.prey_number_value = self.get_prey_value()
        self.predator_number_value = self.get_predator_value()

        simulation.PREY_NUMBER = self.prey_number_value
        simulation.PREDATOR_NUMBER = self.predator_number_value
        simulation.run_simulation()


    def get_prey_value(self) -> int:
        raw_value = self.prey_number_text.get("1.0", "end-1c")

        try:
            formatted_value = int(raw_value)
            return formatted_value
        except Exception as e:
            logging.warning(f"The input value for prey was not given or is not correct!{e}")
            # run the default one
            messagebox.showinfo("Warning", "The value for the number of preys should be an integer!")
            return simulation.PREY_NUMBER

    def get_predator_value(self) -> int:
        raw_value = self.predator_number_text.get("1.0", "end-1c")

        try:
            formatted_value = int(raw_value)
            return formatted_value
        except Exception as e:
            logging.warning(f"The input value for predator was not given or is not correct!{e}")
            # run the default one
            messagebox.showinfo("Warning", "The value for the number of predators should be an integer!")
            return simulation.PREDATOR_NUMBER
