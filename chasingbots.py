import random
import numpy as np
from ..bot_control import Move

class ChasingBots:

    def __init__(self):
        self.target = None
        self.init = False

    def get_name(self):
        return "ChasingBots"

    def get_contributor(self):
        return "Jerrel"

    def determine_next_move(self, grid, enemies, game_info):
    
        if self.init == False:
            self.takeable_ids = self.ids_to_take(enemies)
            self.init = True
            
        target_id = self.find_best_enemy(grid)
        target_coord = self.find_enemy_coord(enemies, target_id)
        print(target_id)
        
        return self.move_to_target(target_coord)
        
    def ids_to_take(self, enemies):
        n_enemies = len(enemies)
        ids = np.zeros(n_enemies,dtype=int)
        for idx, x in enumerate(enemies):
            ids[idx] = x['id']   
        ids = np.delete(ids,np.where(ids == self.id))
        
        for idx, x in enumerate(ids):
            new_color = [x, 0, self.id][(self.id - x) % 3]
            if new_color != self.id:
                ids[idx] = 0
        ids = np.delete(ids,np.where(ids == 0))
        return ids
        
    def find_best_enemy(self,grid):
        takeable_ids = self.takeable_ids
        n_tiles = np.zeros(len(takeable_ids),dtype=int)
        for idx, x in enumerate(takeable_ids):
            n_tiles[idx] = np.count_nonzero(grid == x)
        return takeable_ids[np.argmax(n_tiles)]
        
    def find_enemy_coord(self,enemies,target_id):
        for x in enemies:
            if x['id'] == target_id:
                return x['position']
        
        
    def move_to_target(self, target):
        # Move in direction of target
        dx = abs(target[0] - self.position[0])
        dy = abs(target[1] - self.position[1])
        
        if dx > dy:
            if target[0] > self.position[0]:
                return Move.RIGHT
            else:
                return Move.LEFT
        else:
            if target[1] > self.position[1]:
                return Move.UP
            else:
                return Move.DOWN