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
        
    
    def move_forward(self, obs, action):
    	#Methode qui permet au kart rester au centre de la piste
    	steer = action["steer"]
    	center = obs["paths_end"][2] # center est le noeuds du 2eme segment apres le notre
    	if (center[2] > 20 and abs(obs["center_path_distance"]) < 2):
    	#On verifie que la coordonné z (front) est loin et que  notre kart est a une distance inferieur a 2 du centre de la piste 
    		steer = 0 #on ne bouge pas le volant
    	elif abs(center[0]) > 0.6: 
    	#OU que la valeur absolue de la coordonné x (gauche) est inferieur 0.6
    		steer += 0.5*center[0] #on augmente le steer de la moitié de notre coordonné x  
    	action["steer"] = np.clip(steer, -1, 1) # on restreint le steer entre -1 et 1 par securité
    	return action
    	
    def move_backward(self, obs, action):
    	#Methode qui permet au kart rester au centre de la piste
    	action["acceleration"] = 0
    	action["brake"] = True
    	steer = action["steer"]
    	center = obs["paths_start"][0] # center est le noeuds du segment actuel
    	if (center[2] > 20 and abs(obs["center_path_distance"]) < 2):
    	#On verifie que la coordonné z (front) est loin et que  notre kart est a une distance inferieur a 2 du centre de la piste 
    		steer = 0 #on ne bouge pas le volant
    	elif abs(center[0]) > 0.6: 
    	#OU que la valeur absolue de la coordonné x (gauche) est inferieur 0.6
    		steer += 0.5*center[0] #on augmente le steer de la moitié de notre coordonné x  
    	action["steer"] = np.clip(steer, -1, 1) # on restreint le steer entre -1 et 1 par securité
    	return action
    	    	
    def choose_action(self, obs):
        action = {
            "acceleration": 0.5, # pour que le kart avance a une vitesse constante
            "steer": 0, # pour que des le depart le kart reste droit
            "brake": False, # bool(random.getrandbits(1)),
            "drift": bool(random.getrandbits(1)),
            "nitro": bool(random.getrandbits(1)),
            "rescue":bool(random.getrandbits(1)),
            "fire": bool(random.getrandbits(1)),
        }
        steps = 0
        final_action = self.move_forward(obs, action)
        while steps < 1000:
        #tant que steps < 1000 on augmentes steps de 1
        	steps= steps + 1
        	print(steps,"\n")
        	if steps >= 200:
        	#quand on arrive a 200 step on recule 
        		action["acceleration"] = 0
        		action["brake"] = True
        		steer = action["steer"]
        		center = obs["paths_start"][0]
        		if (center[2] > 20 and abs(obs["center_path_distance"]) < 2):
        			steer = 0 #on ne bouge pas le volant
        		elif abs(center[0]) > 0.6: 
        			steer += 0.5*center[0]
        		action["steer"] = np.clip(steer, -1, 1)
        	else: 
        	#sinon on avance
        		return final_action
