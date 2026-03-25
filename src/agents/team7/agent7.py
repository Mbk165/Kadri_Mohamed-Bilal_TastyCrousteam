import numpy as np
import random

from utils.track_utils import compute_curvature, compute_slope
from agents.kart_agent import KartAgent

class Agent7(KartAgent):
    def __init__(self, env, path_lookahead=3):
        super().__init__(env)
        self.path_lookahead = path_lookahead
        self.agent_positions = []
        self.obs = None
        self.isEnd = False
        self.name = "Kadri Mohamed-Bilal" # replace with your chosen name

    def reset(self):
        self.obs, _ = self.env.reset()
        self.agent_positions = []

    def endOfTrack(self):
        return self.isEnd
        
    
    def moove_forward(self, obs, action):
    	steer = action["steer"]
    	center = obs["paths_end"][2]
    	if (center[2] > 30 and abs(obs["center_path_distance"]) < 3):
    		steer = 0
    	elif abs(center[0]) > 0.6:
    		steer += 0.6*center[0]
    	action["steer"] = np.clip(steer, -1, 1)
    	return action
    	    	
    def choose_action(self, obs):
        action = {
            "acceleration": 0.5,
            "steer": 0,
            "brake": False, # bool(random.getrandbits(1)),
            "drift": bool(random.getrandbits(1)),
            "nitro": bool(random.getrandbits(1)),
            "rescue":bool(random.getrandbits(1)),
            "fire": bool(random.getrandbits(1)),
        }
        moove_action = self.moove_forward(obs, action)
        return moove_action
