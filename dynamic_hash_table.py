from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        old_table = self.table
        old_size = self.table_size

        new_table_size = get_next_size()
        # self.table_size = new_table_size
        # self.table = [None] * new_table_size
        # self.elements = 0

        # if self.collision_type == "Chain" or self.collision_type == "Linear":
        #     self.params[1] = self.table_size
        # else:
        #     self.params[3] = self.table_size
        if self.collision_type == "Chain" or self.collision_type == "Linear":
            new_hash_set = HashSet(self.collision_type, (self.z, new_table_size))
        else:
            new_hash_set = HashSet(self.collision_type, (self.z1, self.z2, self.c2, new_table_size))
        
        self.table = new_hash_set.table
        self.table_size = new_table_size
        self.elements = new_hash_set.elements
        self.params = new_hash_set.params

        for i in old_table:
            if i is not None:
                if self.collision_type == "Chain":
                    for j in i:
                        self.insert(j)
                else:
                    self.insert(i)
        

        pass
        
    def insert(self, x):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(x)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        old_table = self.table
        new_table_size = get_next_size()
        # self.table_size = new_table_size
        # self.table = [None] * new_table_size
        # self.elements = 0

        # if self.collision_type == "Chain" or self.collision_type == "Linear":
        #     self.params[1] = self.table_size
        # else:
        #     self.params[3] = self.table_size

        if self.collision_type == "Chain" or self.collision_type == "Linear":
            new_hash_map = HashMap(self.collision_type, (self.z, new_table_size))
        else:
            new_hash_map = HashMap(self.collision_type, (self.z1, self.z2, self.c2, new_table_size))
        
        self.table = new_hash_map.table
        self.table_size = new_table_size
        self.elements = new_hash_map.elements
        self.params = new_hash_map.params


        for i in old_table:
            if i is not None:
                if self.collision_type == "Chain":
                    for j in i:
                        self.insert(j)
                else:
                    self.insert(i)
        

        pass
        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()