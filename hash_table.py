from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.collision_type = collision_type
        self.params = params
        if self.collision_type == "Chain" or self.collision_type == "Linear":
            self.z = params[0]
            self.table_size = params[1]
        else:
            self.z1 = params[0]
            self.z2 = params[1]
            self.c2 = params[2]
            self.table_size = params[3]
        
        self.table = [None] * self.table_size
        self.elements = 0

    def get_val(self, key):
        if key >= 'a' and key <= 'z':
            return ord(key) - ord('a') + 0
        elif key >= 'A' and key <= 'Z':
            return ord(key) - ord('A') + 26
        else:
            return 0
        

    def hash_function(self, key, z):
        hash_val = 0
        for i in range(len(key)):
            hash_val += self.get_val(key[i]) *z**i
        return hash_val
        


    def insert(self, x):
        y = x
        if isinstance(y, tuple):
            x = x[0]
        ori_hash_x = self.hash_function(x, self.params[0])
        hash_x = ori_hash_x % self.table_size
        if self.table[hash_x] is None:
            if self.collision_type == "Chain":
                self.table[hash_x] = [y]
            else:
                self.table[hash_x] = y
            self.elements += 1
        else:
            if self.collision_type == "Chain":
                if y not in self.table[hash_x]:
                    self.table[hash_x].append(y)
                    self.elements += 1

            elif self.collision_type == "Linear":
                for i in range(0, self.table_size):
                    new_hash = (hash_x + i) % self.table_size
                    if self.table[new_hash] is None:
                        self.table[new_hash] = y
                        self.elements += 1
                        break
                    elif self.table[new_hash] == y:
                        break
            else:
                h2 = self.c2 - (self.hash_function(x, self.z2)%self.c2)
                multi = 0
                while True:
                    new_hash = (ori_hash_x + multi*h2) % self.table_size
                    if self.table[new_hash] is None:
                        self.table[new_hash] = y
                        self.elements += 1
                        break
                    elif self.table[new_hash] == y:
                        break
                    multi += 1
        
        pass
    
    def find(self, key):
        ori_hash_key = self.hash_function(key, self.params[0])
        hash_key = ori_hash_key % self.table_size
        if self.table[hash_key] is None:
            return False
        elif self.collision_type == "Chain":
            count = 0
            for i in self.table[hash_key]:
                if isinstance(i, tuple):
                    if i[0] == key:
                        count = 1
                        return i[1]
                else:
                    if i == key:
                        return True
            if count == 0:
                return False
            else:
                return None

        elif self.collision_type == "Linear":
            count = 0
            for i in range(0, self.table_size):
                new_hash = (hash_key + i) % self.table_size
                if isinstance(self.table[new_hash], tuple):
                    if self.table[new_hash][0] == key:
                        count = 1
                        return self.table[new_hash][1]
                else:
                    if self.table[new_hash] == key:
                        return True
                    elif self.table[new_hash] is None:
                        if count == 0:
                            return False
                        else:
                            return None
                        
            if count == 0:
                return False
            else:
                return None
        
        else:
            h2 = self.c2 - self.hash_function(key, self.z2)%self.c2
            multi = 0
            count = 0
            while True:
                new_hash = (ori_hash_key + multi*h2) % self.table_size
                if isinstance(self.table[new_hash], tuple):
                    if self.table[new_hash][0] == key:
                        count = 1
                        return self.table[new_hash][1]
                else:
                    if self.table[new_hash] == key:
                        return True
                    elif self.table[new_hash] is None:
                        if count == 0:
                            return False
                        else:
                            return None
                        
                multi += 1
        pass
    

    def get_slot(self, key):
        ori_hash_key = self.hash_function(key, self.params[0])
        hash_key = ori_hash_key % self.table_size
        if self.table[hash_key] is None:
            return None
        elif self.collision_type == "Chain":
            for i in self.table[hash_key]:
                if isinstance(i, tuple):
                    if i[0] == key:
                        return hash_key
                else:
                    if i == key:
                        return hash_key
            return None
            
        elif self.collision_type == "Linear":
            for i in range(0, self.table_size):
                new_hash = (hash_key + i) % self.table_size
                if isinstance(self.table[new_hash], tuple):
                    if self.table[new_hash][0] == key:
                        return new_hash
                else:
                    if self.table[new_hash] == key:
                        return new_hash
                    elif self.table[new_hash] is None:
                        return None
            return None
        
        else:
            h2 = self.c2 - self.hash_function(key, self.z2)%self.c2
            multi = 0
            while True:
                new_hash = (ori_hash_key + multi*h2) % self.table_size
                if isinstance(self.table[new_hash], tuple):
                    if self.table[new_hash][0] == key:
                        return new_hash
                else:
                    if self.table[new_hash] == key:
                        return new_hash
                    elif self.table[new_hash] is None:
                        return None
                multi += 1
        pass
    
    def get_load(self):
        return self.elements/self.table_size
        pass
    
    def __str__(self):
        final_output = ""
        for i in range(self.table_size):
            if self.table[i] is None:
                final_output += '<EMPTY> | '
            else:
                if self.collision_type == "Chain":
                    for x in self.table[i]:
                        if isinstance(x, tuple):
                            final_output += f'({x[0]}, {x[1]}) ; '
                        else:
                            final_output += f'{x} ; '
                    final_output = final_output[:-3] + " | "
                else:
                    if isinstance(self.table[i], tuple):
                        final_output += f'({self.table[i][0]}, {self.table[i][1]}) | '
                    else:
                        final_output += f'{self.table[i]} | '
        return final_output[:-3]
        pass
    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass
    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF,
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        pass
    
    def insert(self, key):
        super().insert(key)
        pass
    
    def find(self, key):
        return super().find(key)
        pass
    
    def get_slot(self, key):
        return super().get_slot(key)
        pass
    
    def get_load(self):
        return super().get_load()
        pass
    
    def __str__(self):
        return super().__str__()
        pass
    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        pass
    
    def insert(self, x):
        # x = (key, value)
        super().insert(x)
        pass
    
    def find(self, key):
        return super().find(key)
        pass
    
    def get_slot(self, key):
        return super().get_slot(key)
        pass
    
    def get_load(self):
        return super().get_load()
        pass
    
    def __str__(self):
        return super().__str__()
        pass