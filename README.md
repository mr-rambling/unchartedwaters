# Current Status
This has spiraled rapidly out of control. What began as a simple text adventure with a basic interaction tree suddenly possesses a GUI sailing interface, inventory and placeholder character screen. I will submit the current workable state despite the bugs and continue it as a WIP. 

# Goal
This has instead turned into me attempting to replicate the entire MMO Uncharted Waters Online as a single player experience. At least the gameplay, the art is beyond me. For now it shall remain a 2D game of basic polgons.

~~This will be an attempt to reproduce some of the trading functionality of the MMO Uncharted Waters Online for my Boot.dev personal project.~~

1. ~~Establish five fictional cities with semi-unique goods. Categorise these goods into general archtypes~~
 - This spiraled. A City() class has been built to easily add additional cities.
2. ~~Create a trading platform to buy and sell in each city~~
3. ~~Establish distances of each city from one another~~
 - Also spiraled. Have instead got a complete world map with each city having its own coordinates to designate location
4. Create favoured goods for each city based on the distance travelled from point of origin
5. Introduce variability to pricing based on recently bought/sold goods
6. Introduce a degree of randomness to product demand in each city
7. ~~Add travel time and costs to trading between cities~~
 - While it isnt fully complete, the sailing gameplay element covers this
8. ~~Add player functionality. Restrict cargo space and starting capital~~
9. Add player upgrades.
10. ~~Welcome message to each city~~
11. AI generated talk from your ships crew each day at sea
12. PvE events while travelling
13. Add save and load game functionality. Placeholder buttons currently exist.

# How to Use
1. Clone the repository:

```
git clone https://github.com/mr-rambling/unchartedwaters.git
```

2. Navigate to the project directory:

```
cd unchartedwaters
```

3. Run your application:

```
python main.py
```