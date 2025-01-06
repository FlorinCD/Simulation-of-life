# **Simulation of Life**
    This is a simulation made in python using pygame, matplotlib and tkinter. The concept here is simulating life in nature. We have some categories: plants, preys and predators.
    This simulation shows interesting patterns like in real life:
    - when food is plenty and the population is thriving until overpopulation and crisis that appear due to the effects of this phenomenon;
    - you can observe how nature can regulate itself, when there are a lot of predators and food, some of them may evolve into a stronger one which can kill other normal predators;
    - how cataclysms shape the relief and the population and reset the cycle of life to new horizons.

## **Description**
    The parameters that influence the simulation are set in the interface also, please read: SimulationLaws.txt.
    Here is a description of what you need to know:
    predator = RED
    prey = BLUE
    plant = GREEN - spawn randomly

    The prey (BLUE) eats plants (GREEN) and has a range of view ~ if it sees a plant, it will go after it,
    if it doesn't see it stays on the same spot waiting.
    If it's traveling and doesn't have enough energy it dies.
    If it has enough energy it reproduces itself at some point.

    The evolved prey (TURQUOISE) eats plants is pretty slow, has a slow metabolism, it lets a mark behind by destroying the terrain.
    It can't be eaten by predators since it's pretty big. (Probably won't survive to a cataclysm). It reproduces the unevoled one.

    The predator (RED) hunts after prey (BLUE) and has a higher speed and range of view than prey, it also destroys every plant he passes by.
    If it doesn't have enough energy, stays on the ground waiting for regeneration.
    If it has enough energy it reproduces itself or it might evolve into the perfect predator.

    The evolved predator (PURPLE) hunts prey and predator and has a higher speed and range view.
    It reproduces.
    It has a chance of regression - to the species predator (RED).

    The cataclysm (ORANGE) is an event that happens by chance once in a while (meteorite hit), it destroys the whole area nearby.

    The hard terrain (BLACK) is a terrain obstacle.

    The land (WHITE).

## **Installation**
    Steps to install the project:

    1. Open a command line shell such as Powershell (on Windows).

    2. Create a folder to store the project at <storage_folder_path>.

    3. Clone the repository at <storage_folder_path>/ : git clone https://github.com/FlorinCD/Simulation-of-life

    4. At <storage_folder_path>/Simulation-of-life/ create a virtual environment.

    5. Activate the venv : cd <storage_folder_path>/Simulation-of-life/<venv-name-given>/Scripts/activate (now it should have name of the venv in the front in cmd)

    6. Install dependencies: at <storage_folder_path>/Simulation-of-life/ use: pip install -r requirements.txt

## **Usage**
    - Example command: `python main.py` (this will launch the interface where you can set the parameters and run the simulation)
    - Set the parameters accordingly (it will pop some text if it's not correct and use the default value)
    - After the end of the simulation some important graphs will be created to reflect the relations between different species and environment.

## **License**
    This project is not licensed but refer to it when using it somewhere else.

## **Contact**
    Author: Florin Despina
    Email: florin_cosmin77@yahoo.com