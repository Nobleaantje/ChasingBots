import random
import numpy as np
from ..bot_control import Move

class ChasingBots:

    def __init__(self):
        self.target = None
        self.init = False
        self.hyster = 2
        self.prev_target = 0

    def get_name(self):
        return "ChasingBots"

    def get_contributor(self):
        return "Jerrel"

    def determine_next_move(self, grid, enemies, game_info):
    
        if self.init == False:
            self.takeable_ids = self.ids_to_take(enemies)
            self.init = True
            
        target_id = self.find_best_enemy(grid)
        self.prev_target = target_id
        target_coord = self.find_target_coord(enemies,target_id,grid)
        
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
        best_id = takeable_ids[np.argmax(n_tiles)]
        if self.prev_target == 0:
            return best_id
        if best_id == self.prev_target:
            return best_id
        if np.amax(n_tiles) > n_tiles[np.where(takeable_ids == self.prev_target)] * self.hyster:
            return best_id
        else:
            return self.prev_target
        
    def find_target_coord(self,enemies,target_id,grid):
    
        for x in enemies:
                if x['id'] == target_id:
                    enemy_coords = x['position']
                    break
    
        tile_coords = np.where(grid == target_id)
        if tile_coords[0].size == 0:
            return enemy_coords
            
        best_dist = 9999
        best_coords = [0,0]
        
        for idx, y in enumerate(tile_coords[0]):
            x =  tile_coords[1][idx]
            dist_to_self   = abs(self.position[0] - x) + abs(self.position[1] - y)
            dist_to_enemy = abs(enemy_coords[0] - x) + abs(enemy_coords[1] - y)
            
            tot_dist = 2*dist_to_self + dist_to_enemy
            
            if tot_dist < best_dist:
                best_dist = tot_dist
                best_coords = [x, y]
        return best_coords
        
        
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