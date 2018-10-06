import gamelib
import random
import math
import warnings
from sys import maxsize

"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

Additional functions are made available by importing the AdvancedGameState 
class from gamelib/advanced.py as a replcement for the regular GameState class 
in game.py.

You can analyze action frames by modifying algocore.py.

The GameState.map object can be manually manipulated to create hypothetical 
board states. Though, we recommended making a copy of the map to preserve 
the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy 2...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER, RIGHT_SIDE_EMERGENCY
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]
        RIGHT_SIDE_EMERGENCY = 0

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.AdvancedGameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy2'.format(game_state.turn_number))
        #game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.

        self.start_strategy(game_state)

        game_state.submit_turn()

    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safey be replaced for your custom algo.
    """
    def start_strategy(self, game_state):
        """
            Build the main wall for defense and add encryprors for the first attacs.
        """
        self.build_main_wall(game_state)

        """
        Then build additional defenses.
        """
        self.build_defences(game_state)

        """
        Finally deploy our information units to attack.
        """
        self.deploy_attackers(game_state)


    def build_main_wall(self, game_state):
        """
        use Filter firewalls to build main wall
        """
        
        for x in range(7,21):
            if game_state.can_spawn(FILTER, [x, 13]) and not game_state.contains_stationary_unit([x,14]):
                game_state.attempt_spawn(FILTER, [x,13])
                if game_state.turn_number != 0 and x > 17:
                    RIGHT_SIDE_EMERGENCY = 1
    
    def build_defences(self, game_state):
        #Add some detrructors l and r
        destr = [[5,12],[23,12]]
        destr2 = [[4,12],[24,12]]
        for ix in range(0,len(destr)):
            if game_state.can_spawn(DESTRUCTOR, destr[ix]):
                game_state.attempt_spawn(DESTRUCTOR, destr[ix])
                if game_state.turn_number > 0:
                    if game_state.can_spawn(DESTRUCTOR, destr2[ix]):
                        game_state.attempt_spawn(DESTRUCTOR, destr2[ix])

        #fixme: rigt coords
        if RIGHT_SIDE_EMERGENCY:
            if game_state.can_spawn(DESTRUCTOR, [23,11]):
                game_state.attempt_spawn(DESTRUCTOR, [23,11])
                                    
#if game_state.turn_number >= 3 and game_state.enemy_health == 30 :
        #algo not effective enough.. try sth. else
        
        #fixme: rigt coords
        if len(game_state.get_attackers([2,13], 0)) > 1 and game_state.can_spawn(EMP, [3,10]):
                game_state.attempt_spawn(EMP, [3,10])

        firewall_locations = [[5, 11],[6,11]]
        for location in firewall_locations:
            if game_state.can_spawn(ENCRYPTOR, location):
                game_state.attempt_spawn(ENCRYPTOR, location)

        for x in range(27,5,-1):
            #gamelib.debug_write('that one strange for loop...')
            if game_state.can_spawn(FILTER, [x,13]) and not game_state.contains_stationary_unit([x,14]):
                game_state.attempt_spawn(FILTER, [x,13])
        x = 6
        y = 10
	
        while game_state.get_resource(game_state.CORES) >= game_state.type_cost(ENCRYPTOR) and y > 6:
            #gamelib.debug_write('resources for ENCRYPRORS...')
            if game_state.can_spawn(ENCRYPTOR, [x,y]):
                game_state.attempt_spawn(ENCRYPTOR, [x,y])
            x += 1
            if game_state.can_spawn(ENCRYPTOR,[x,y]):
                game_state.attempt_spawn(ENCRYPTOR,[x,y])
            y -= 1
                
                
    def deploy_attackers(self, game_state):
        
        if (game_state.turn_number == 0 and game_state.can_spawn(SCRAMBLER, [25, 11])) or RIGHT_SIDE_EMERGENCY:
            game_state.attempt_spawn(SCRAMBLER, [25, 11])
        
        
        
        if game_state.number_affordable(PING) > 4 and game_state.can_spawn(SCRAMBLER, [14,0]):
	        game_state.attempt_spawn(SCRAMBLER,[14,0])
            
        while game_state.get_resource(game_state.BITS) >= game_state.type_cost(PING):
            #gamelib.debug_write('resources for PINGS...')
            if game_state.can_spawn(PING, [14, 0]):
        	    game_state.attempt_spawn(PING, [14,0])
            else:
                gamelib.debug_write('{} Bits cant spawn PINGS at [14,0]'.format(game_state.turn_number))
                return
        
    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
