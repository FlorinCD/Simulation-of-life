This is a simulation made in python using pygame. The concept here is simulating life in nature. We have some categories: plants, preys and predators.
This simulation shows interesting patterns like in real life when food is plenty and the population is thriving until overpopulation and crisis that appear due to the effects of this phenomenon.
Each group starts with a specific number where you can play to observe different things. The current numbers are pretty good since the simulation can run without having an extinct species for hours at least in the most runs.

Here is a description of what you need to know:
predator = RED
prey = BLUE
plant = GREEN - spawn randomly

The prey (BLUE) eats plants (GREEN) and has a range of view ~ if it sees a plant, it will go after it,
if it doesn't see it stays on the same spot waiting.
If it's traveling and doesn't have enough energy it dies. 
If it has enough energy it reproduces itself at some point.

The evolved prey (TURQUOISE) eats plants is pretty slow, has a slow metabolism, it lets a mark behind by destroying the terrain.
It can't be eaten by predators since it's pretty big. (Probably wont survive to a cataclysm). It reproduces the unevoled one.

The predator (RED) hunts after prey (BLUE) and has a higher speed and range of view than prey, it also destroys every plant he passes by.
If it doesn't have enough energy, stays on the ground waiting for regeneration.
If it has enough energy it reproduce itself or it might evolve into the perfect predator.

The evolved predator (PURPLE) hunts prey and predator and has a higher speed and range view. 
It reproduces.
It has a chance of regression - to the species predator (RED).

The cataclysm (ORANGE) is an event that happens by chance once in a while (meteorite hit), it destroys the whole area nearby.

The hard terrain (BLACK) is an terrain obstacle.

The land (WHITE).

