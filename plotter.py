import matplotlib.pyplot as plt


class Plotter:
    """
    The received data should be a list of tuples. Each tuple represent information about each element:
    Example for a tuple:
        (len(PLANT), len(PREY), len(PREDATOR), len(EVOLVED_PREY), len(EVOLVED_PREDATOR), cataclysm_counter, timestamp)
        Each element from this tuple is present in simulation.py
    This class is desired to plot the information as a graph.
    """

    def __init__(self, data: list[tuple]):
        self.data = data

        self.plant = [t[0] for t in data]
        self.prey = [t[1] for t in data]
        self.predator = [t[2] for t in data]
        self.evolved_prey = [t[3] for t in data]
        self.evolved_predator = [t[4] for t in data]
        self.cataclysm = [t[5] for t in data]

    def plot_graph_whole(self):
        # Settings
        # bmh seaborn-v0_8-notebook seaborn-v0_8-darkgrid
        plt.style.use('seaborn-v0_8-darkgrid')

        # Plotting
        plt.plot(self.plant, label="Plant", color='green', linewidth=2)
        plt.plot(self.prey, label="Prey", color='blue', linewidth=2)
        plt.plot(self.predator, label="Predator", color='red', linewidth=2)
        plt.plot(self.evolved_prey, label="Ev. Prey", color='cyan', linewidth=2)
        plt.plot(self.evolved_predator, label="Ev. Predator", color='purple', linewidth=2)
        plt.plot(self.cataclysm, label="Cataclysm", color='orange', linewidth=2)

        # Adding labels and legend
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Number', fontsize=12)
        plt.title('Graphic for Simulation of life', fontsize=16, fontweight='bold')
        plt.legend()
        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

        plt.savefig("full_correlation_graph.png", dpi=300, bbox_inches='tight')
        # Display the plot
        plt.show()

    def plot_graph_plants_prey(self):
        # Settings
        # bmh seaborn-v0_8-notebook seaborn-v0_8-darkgrid
        plt.style.use('seaborn-v0_8-darkgrid')

        # Plotting
        plt.plot(self.plant, label="Plant", color='green', linewidth=2)
        plt.plot(self.prey, label="Prey", color='blue', linewidth=2)

        # Adding labels and legend
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Number', fontsize=12)
        plt.title('Plant vs Prey', fontsize=16, fontweight='bold')
        plt.legend()
        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

        plt.savefig("plant_prey.png", dpi=300, bbox_inches='tight')
        # Display the plot
        plt.show()

    def plot_graph_prey_predator(self):
        # Settings
        # bmh seaborn-v0_8-notebook seaborn-v0_8-darkgrid
        plt.style.use('seaborn-v0_8-darkgrid')

        # Plotting
        plt.plot(self.prey, label="Prey", color='blue', linewidth=2)
        plt.plot(self.predator, label="Predator", color='red', linewidth=2)

        # Adding labels and legend
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Number', fontsize=12)
        plt.title('Prey vs Predator', fontsize=16, fontweight='bold')
        plt.legend()
        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

        plt.savefig("prey_predator.png", dpi=300, bbox_inches='tight')
        # Display the plot
        plt.show()

    def plot_graph_prey_predator_ev_predator(self):
        # Settings
        # bmh seaborn-v0_8-notebook seaborn-v0_8-darkgrid
        plt.style.use('seaborn-v0_8-darkgrid')

        # Plotting
        plt.plot(self.prey, label="Prey", color='blue', linewidth=2)
        plt.plot(self.predator, label="Predator", color='red', linewidth=2)
        plt.plot(self.evolved_predator, label="Ev. Predator", color='purple', linewidth=2)

        # Adding labels and legend
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Number', fontsize=12)
        plt.title('Prey vs Predator vs Ev Predator', fontsize=16, fontweight='bold')
        plt.legend()
        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

        plt.savefig("prey_predator_ev_predator.png", dpi=300, bbox_inches='tight')
        # Display the plot
        plt.show()

    def get_all_plots(self):
        self.plot_graph_whole()
        self.plot_graph_plants_prey()
        self.plot_graph_prey_predator()
        self.plot_graph_prey_predator_ev_predator()