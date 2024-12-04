import tkinter as tk
import logging
import simulation

from tkinter import Text, messagebox, Canvas



class Menu:

    def __init__(self):
        self.root = tk.Tk()
        self.frame = None
        self.run_button = None

        self.title_label = None
        self.prey_number_label = None
        self.predator_number_label = None
        self.prey_chance_evolve_label = None
        self.predator_chance_evolve_label = None
        self.evolved_predator_regression_label = None
        self.cataclysm_chance_label = None

        self.prey_number_text = None
        self.predator_number_text = None
        self.prey_chance_evolve_text = None
        self.predator_chance_evolve_text = None
        self.evolved_predator_regression_text = None
        self.cataclysm_chance_text = None

        self.prey_number_value = None
        self.predator_number_value = None
        self.prey_chance_evolve_value = None
        self.predator_chance_evolve_value = None
        self.evolved_predator_regression_value = None
        self.cataclysm_chance_value = None

        self.bg_img_reference = None
        self.canvas_main_menu = None

        self.decorate_menu()

        self.root.mainloop()

    """Decorate the tkinter interface with all the widgets"""
    def decorate_menu(self):
        self.root.title("Simulation of life")
        self.root.geometry("600x600")
        self.root.iconbitmap(r"static/icons/simulation_of_life.ico")
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, bg="lightblue", padx=0, pady=0)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self.frame, text="Configuration of simulation:", anchor="w", bg='#3b3642', fg='#ffffff',
                                          font=("Arial", 11))
        self.title_label.place(x=200, y=5)

        # Load the background image
        self.bg_img_reference = tk.PhotoImage(file=r"static/images/image_1.png")

        # Create Canvas
        self.canvas_main_menu = Canvas(self.frame, width=600, height=600)
        self.canvas_main_menu.pack()

        # Display image
        self.canvas_main_menu.create_image((0, 0), image=self.bg_img_reference, anchor="nw")

        self.prey_number_label = tk.Label(self.frame, text="The number of preys:", anchor="w", bg='#3b3642', fg='#ffffff',
                                          font=("Arial", 11))
        self.prey_number_label.place(x=20, y=50)

        self.prey_number_text = Text(self.frame, height=1, width=10)
        self.prey_number_text.place(x=200, y=53)

        self.predator_number_label = tk.Label(self.frame, text="The number of predators:", anchor="w", bg='#3b3642', fg='#ffffff',
                                          font=("Arial", 11))
        self.predator_number_label.place(x=20, y=100)

        self.predator_number_text = Text(self.frame, height=1, width=10)
        self.predator_number_text.place(x=200, y=100)

        self.prey_chance_evolve_label = tk.Label(self.frame, text="The chance of the prey to evolve:", anchor="w", bg='#3b3642', fg='#ffffff',
                                          font=("Arial", 11))
        self.prey_chance_evolve_label.place(x=20, y=150)

        self.prey_chance_evolve_text = Text(self.frame, height=1, width=10)
        self.prey_chance_evolve_text.place(x=280, y=150)

        self.predator_chance_evolve_label = tk.Label(self.frame, text="The chance of the predator to evolve:", anchor="w",
                                                 bg='#3b3642', fg='#ffffff',
                                                 font=("Arial", 11))
        self.predator_chance_evolve_label.place(x=20, y=200)

        self.predator_chance_evolve_text = Text(self.frame, height=1, width=10)
        self.predator_chance_evolve_text.place(x=280, y=200)

        self.evolved_predator_regression_label = tk.Label(self.frame, text="The chance of the evolved predator to regress:", anchor="w",
                                                 bg='#3b3642', fg='#ffffff',
                                                 font=("Arial", 11))
        self.evolved_predator_regression_label.place(x=20, y=250)

        self.evolved_predator_regression_text = Text(self.frame, height=1, width=10)
        self.evolved_predator_regression_text.place(x=340, y=250)

        self.cataclysm_chance_label = tk.Label(self.frame,
                                                          text="The chance of a cataclysm to happen:",
                                                          anchor="w",
                                                          bg='#3b3642', fg='#ffffff',
                                                          font=("Arial", 11))
        self.cataclysm_chance_label.place(x=20, y=300)

        self.cataclysm_chance_text = Text(self.frame, height=1, width=10)
        self.cataclysm_chance_text.place(x=340, y=300)

        self.run_button = tk.Button(self.frame, text="Run Simulation", command=self.run_simulation_button, font=("Arial", 11), bg='green', fg='#ffffff')
        self.run_button.place(x=230, y=500)



    """Run the simulation with the given parameters"""
    def run_simulation_button(self):
        self.prey_number_value = self.get_prey_value()
        self.predator_number_value = self.get_predator_value()

        # set the parameters for the simulation
        simulation.PREY_NUMBER = self.prey_number_value
        simulation.PREDATOR_NUMBER = self.predator_number_value
        simulation.PREY_CHANCE_EVOLVE = self.get_prey_chance_evolve()
        simulation.PREDATOR_CHANCE_EVOLVE = self.get_predator_chance_evolve()
        simulation.EVOLVED_PREDATOR_CHANCE_REGRESSION = self.get_evolved_predator_chance_regression()
        simulation.CATACLYSM_CHANCE = self.get_cataclysm_chance()

        simulation.run_simulation()


    def get_prey_value(self) -> int:
        raw_value = self.prey_number_text.get("1.0", "end-1c")

        try:
            formatted_value = int(raw_value)
            assert formatted_value <= 50
            return formatted_value
        except Exception as e:
            logging.warning(f"The input value for prey was not given or is not correct!{e}")
            # run the default one
            messagebox.showinfo("Warning", "The value for the number of preys should be an integer <= 50! The default value will be used.")
            return simulation.PREY_NUMBER

    def get_predator_value(self) -> int:
        raw_value = self.predator_number_text.get("1.0", "end-1c")

        try:
            formatted_value = int(raw_value)
            assert formatted_value <= 50
            return formatted_value
        except Exception as e:
            logging.warning(f"The input value for predator was not given or is not correct!{e}")
            # run the default one
            messagebox.showinfo("Warning", "The value for the number of predators should be an integer <= 50! The default value will be used.")
            return simulation.PREDATOR_NUMBER

    def get_prey_chance_evolve(self) -> float:
        raw_value = self.prey_chance_evolve_text.get("1.0", "end-1c")

        try:
            formatted_value = float(raw_value)  # to use it later in the simulation
            assert formatted_value <= 1
            return formatted_value
        except Exception as e:
            logging.warning(f"The input value as chance for prey to evolve is not correct!{e}")
            # run the default one
            messagebox.showinfo("Warning", "The value for the prey's chance to evolve should be a float <= 1! The default value will be used.")
            return simulation.PREY_CHANCE_EVOLVE

    def get_predator_chance_evolve(self) -> float:
        raw_value = self.predator_chance_evolve_text.get("1.0", "end-1c")

        try:
            formatted_value = float(raw_value)  # to use it later in the simulation
            assert formatted_value <= 1
            return formatted_value
        except Exception as e:
            logging.warning(f"The input value as chance for predator to evolve is not correct!{e}")
            # run the default one
            messagebox.showinfo("Warning",
                                "The value for the predator's chance to evolve should be a float <= 1! The default value will be used.")
            return simulation.PREDATOR_CHANCE_EVOLVE

    def get_evolved_predator_chance_regression(self) -> float:
        raw_value = self.evolved_predator_regression_text.get("1.0", "end-1c")

        try:
            formatted_value = float(raw_value)  # to use it later in the simulation
            assert formatted_value <= 1
            return formatted_value
        except Exception as e:
            logging.warning(f"The input value as chance for predator to regress is not correct!{e}")
            # run the default one
            messagebox.showinfo("Warning",
                                "The value for the predator's chance to regress should be a float <= 1! The default value will be used.")
            return simulation.EVOLVED_PREDATOR_CHANCE_REGRESSION

    def get_cataclysm_chance(self) -> float:
        raw_value = self.cataclysm_chance_text.get("1.0", "end-1c")

        try:
            formatted_value = float(raw_value)  # to use it later in the simulation
            assert formatted_value <= 0.01
            return formatted_value
        except Exception as e:
            logging.warning(f"The input value as chance for a cataclysm to happen is not correct!{e}")
            # run the default one
            messagebox.showinfo("Warning",
                                "The value for the cataclysm's chance to happen should be a float <= 0.01! The default value will be used.")
            return simulation.CATACLYSM_CHANCE