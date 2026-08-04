import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass



def merge_sort(arr):
    if len(arr) == 1:
        return arr
    
    mid = len(arr)//2
    left = arr[:mid]
    right = arr[mid:]
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)

def merge(left, right):
    merged_lst = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged_lst.append(left[i])
            i += 1
        elif left[i] == right[j]:
            merged_lst.append(left[i])
            i += 1
            j += 1
        else:
            merged_lst.append(right[j])
            j += 1
    
    while i < len(left):
        merged_lst.append(left[i])
        i += 1
    while j < len(right):
        merged_lst.append(right[j])
        j += 1
    return merged_lst

def merge_sort_pairs(arr):
    if len(arr) == 1:
        return arr
    
    mid = len(arr)//2
    left = arr[:mid]
    right = arr[mid:]
    left = merge_sort_pairs(left)
    right = merge_sort_pairs(right)
    return merge_pairs(left, right)

def merge_pairs(left, right):
    merged_lst = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][0] < right[j][0]:
            merged_lst.append(left[i])
            i += 1
        elif left[i][0] == right[j][0]:
            merged_lst.append(left[i])
            i += 1
            j += 1
        else:
            merged_lst.append(right[j])
            j += 1
    
    while i < len(left):
        merged_lst.append(left[i])
        i += 1
    while j < len(right):
        merged_lst.append(right[j])
        j += 1
    return merged_lst


class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        self.musk_books = []

        for i in range(len(book_titles)):
            self.musk_books.append([book_titles[i], merge_sort(texts[i])])
        self.musk_books = merge_sort_pairs(self.musk_books)

        pass
    
    def find_book(self, book_title, low = 0, high = None):
        if high is None:
            high = len(self.musk_books)-1
        if low > high:
            return -1
        mid = (low+high)//2
        mid_book = self.musk_books[mid][0]
        if mid_book == book_title:
            return mid
        elif mid_book < book_title:
            return self.find_book(book_title, mid+1, high)
        else:
            return self.find_book(book_title, low, mid-1)
        
    def find_word(self, text, word, low = 0, high = None):
        if high is None:
            high = len(text)-1
        if low > high:
            return -1
        mid = (low+high)//2
        mid_word = text[mid]
        if mid_word == word:
            return mid
        elif mid_word < word:
            return self.find_word(text, word, mid+1, high)
        else:
            return self.find_word(text, word, low, mid-1)

    def distinct_words(self, book_title):
        
        book_index = self.find_book(book_title)
        return self.musk_books[book_index][1]
        pass
    
    def count_distinct_words(self, book_title):
        book_index = self.find_book(book_title)
        return len(self.musk_books[book_index][1])
        pass
    
    def search_keyword(self, keyword):
        keyword_books = []
        for book, text in self.musk_books:
            word_index = self.find_word(text, keyword)
            if word_index != -1:
                keyword_books.append(book)
        return keyword_books
        pass
    
    def print_books(self):
        final_output = ""
        for book, text in self.musk_books:
            final_output += book + ": "
            for word in text:
                final_output += word + " | "
            final_output = final_output[:-3] + "\n"
        print(final_output[:-1])
        pass


class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        self.name = name
        self.params = params
        if self.name =="Jobs":
            hash_list = ht.HashMap("Chain", self.params)
        elif self.name == "Gates":
            hash_list = ht.HashMap("Linear", self.params)
        else:
            hash_list = ht.HashMap("Double", self.params)
        self.hash_list = hash_list
        pass
        
    def add_book(self, book_title, text):
        if self.name == "Jobs":
            text_hash_list = ht.HashSet("Chain", self.params)
        elif self.name == "Gates":
            text_hash_list = ht.HashSet("Linear", self.params)
        else:
            text_hash_list = ht.HashSet("Double", self.params)
        for i in text:
            text_hash_list.insert(i)
        self.hash_list.insert((book_title, text_hash_list))
        pass
    
    def distinct_words(self, book_title):
        texts = self.hash_list.find(book_title)
        if texts is None:
            return []
        dist_words = []
        
        for i in texts.table:
            if i is not None:
                if self.name == "Jobs":
                    for _ in i:
                        dist_words.append(_)
                else:
                    dist_words.append(i)
        
        return dist_words
        pass
    
    def count_distinct_words(self, book_title):
        texts = self.hash_list.find(book_title)
        if texts is None:
            return 0
        return texts.elements
        pass
    
    def search_keyword(self, keyword):
        keyword_books = []
        for i in self.hash_list.table:
            if i is not None:
                if self.name == "Jobs":
                    for j in i:
                        word_present = j[1].find(keyword)
                        if word_present:
                            keyword_books.append(j[0])
                else:
                    word_present = i[1].find(keyword)
                    if word_present:
                        keyword_books.append(i[0])
        return keyword_books
        pass
    
    def print_books(self):
        final_output = ""
        for i in self.hash_list.table:
            if i is not None:
                if self.name == "Jobs":
                    for _ in i:
                        final_output += _[0] + ": "
                        final_output += _[1].__str__() + "\n"
                else:
                    final_output += i[0] + ": "
                    final_output += i[1].__str__() + "\n"
        print(final_output[:-1])
        pass