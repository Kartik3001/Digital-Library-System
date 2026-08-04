#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>

using namespace std;

// ---------- PRIME GENERATOR ----------

vector<int> prime_sizes = {29, 53, 101, 211, 431, 863};  // descending
int get_next_size() {
    int val = prime_sizes.back();
    prime_sizes.pop_back();
    return val;
} // for resizing hash tables(for dynamic growth)

// ---------- POLYNOMIAL HASHING UTILS ----------

int get_char_val(char ch) {
    if (ch >= 'a' && ch <= 'z') return ch - 'a';
    if (ch >= 'A' && ch <= 'Z') return ch - 'A' + 26;
    return 0;
}
// converts each char into an index
long long hash_function(const string& key, int z) {
    long long h = 0;
    long long powz = 1;
    for (char c : key) {
        h += get_char_val(c) * powz;
        powz *= z;
    }
    return h ;
} // polynomial rolling hash used for indexing

// ---------- HASH TABLE ----------

class HashTable {
protected:
    string collision_type;
    vector<string> table;  // only for HashSet
    vector<pair<string, string>> table_map; // only for HashMap
    int table_size, elements;
    int z, z1, z2, c2;

public:
    HashTable(string type, vector<int> params, bool is_map=false) {
        collision_type = type;
        if (type == "Double") {
            z1 = params[0];
            z2 = params[1];
            c2 = params[2];
            table_size = params[3];
        } else {
            z = params[0];
            table_size = params[1];
        }
        elements = 0;
        if (is_map)
            table_map = vector<pair<string, string>>(table_size, {"", ""});
        else
            table = vector<string>(table_size, "");
    }

    virtual void insert(const string& key) {}
    virtual string find(const string& key) { return ""; }
    virtual int get_slot(const string& key) { return -1; }
    virtual double get_load() { return double(elements) / table_size; }
};

// ---------- HASHSET CLASS ----------

class HashSet : public HashTable {
    vector<vector<string>> chain_table;

public: 
    HashSet(string type, vector<int> params) : HashTable(type, params, false) {
        if (type == "Chain") chain_table = vector<vector<string>>(table_size);
    }

    void insert(const string& key) override {
        long long h = (collision_type == "Double") ? hash_function(key, z1) : hash_function(key, z);
        int idx = h % table_size;

        if (collision_type == "Chain") {
            for (string& s : chain_table[idx]) {
                if (s == key) return;
            }
            chain_table[idx].push_back(key);
            elements++;
        } 
        else if (collision_type == "Linear") {
            for (int i = 0; i < table_size; ++i) {
                int new_idx = (idx + i) % table_size;
                if (table[new_idx] == "") {
                    table[new_idx] = key;
                    elements++;
                    return;
                } else if (table[new_idx] == key) return;
            }
        } 
        else if (collision_type == "Double") {
            int step = c2 - (hash_function(key, z2) % c2);
            int i = 0;
            while (true) {
                int new_idx = (h + i * step) % table_size;
                if (table[new_idx] == "") {
                    table[new_idx] = key;
                    elements++;
                    return;
                } else if (table[new_idx] == key) return;
                ++i;
            }
        }
    }

    bool find_bool(const string& key) {
        long long h = (collision_type == "Double") ? hash_function(key, z1) : hash_function(key, z);
        int idx = h % table_size;

        if (collision_type == "Chain") {
            for (const string& s : chain_table[idx]) {
                if (s == key) return true;
            }
            return false;
        }
        else if (collision_type == "Linear") {
            for (int i = 0; i < table_size; ++i) {
                int new_idx = (idx + i) % table_size;
                if (table[new_idx] == key) return true;
                if (table[new_idx] == "") return false;
            }
        }
        else if (collision_type == "Double") {
            int step = c2 - (hash_function(key, z2) % c2);
            int i = 0;
            while (true) {
                int new_idx = (h + i * step) % table_size;
                if (table[new_idx] == key) return true;
                if (table[new_idx] == "") return false;
                ++i;
            }
        }
        return false;
    }

    vector<string> get_all_elements() {
        vector<string> result;
        if (collision_type == "Chain") {
            for (auto& bucket : chain_table)
                for (auto& s : bucket)
                    result.push_back(s);
        } else {
            for (auto& s : table)
                if (s != "") result.push_back(s);
        }
        return result;
    }

    int count() { return elements; }

    string to_string_repr() {
        string out = "";
        if (collision_type == "Chain") {
            for (auto& bucket : chain_table) {
                if (bucket.empty()) out += "<EMPTY> | ";
                else {
                    for (auto& s : bucket)
                        out += s + " ; ";
                    out.pop_back(); out.pop_back(); out.pop_back();
                    out += " | ";
                }
            }
        } else {
            for (auto& s : table) {
                if (s == "") out += "<EMPTY> | ";
                else out += s + " | ";
            }
        }
        if (out.size() >= 3) out.erase(out.size() - 3);
        return out;
    }
};
// ---------- HASHMAP CLASS ----------

class HashMap : public HashTable {
    vector<vector<pair<string, string>>> chain_map;

public:
    HashMap(string type, vector<int> params) : HashTable(type, params, true) {
        if (type == "Chain") {
            chain_map = vector<vector<pair<string, string>>>(table_size);
        }
    }

    void insert(const pair<string, string>& entry) {
        string key = entry.first;
        long long h = (collision_type == "Double") ? hash_function(key, z1) : hash_function(key, z);
        int idx = h % table_size;

        if (collision_type == "Chain") {
            for (auto& p : chain_map[idx]) {
                if (p.first == key) return;
            }
            chain_map[idx].push_back(entry);
            elements++;
        }
        else if (collision_type == "Linear") {
            for (int i = 0; i < table_size; ++i) {
                int new_idx = (idx + i) % table_size;
                if (table_map[new_idx].first == "" || table_map[new_idx].first == key) {
                    table_map[new_idx] = entry;
                    elements++;
                    return;
                }
            }
        }
        else if (collision_type == "Double") {
            int step = c2 - (hash_function(key, z2) % c2);
            int i = 0;
            while (true) {
                int new_idx = (h + i * step) % table_size;
                if (table_map[new_idx].first == "" || table_map[new_idx].first == key) {
                    table_map[new_idx] = entry;
                    elements++;
                    return;
                }
                ++i;
            }
        }
    }

    string find(const string& key) override {
        long long h = (collision_type == "Double") ? hash_function(key, z1) : hash_function(key, z);
        int idx = h % table_size;

        if (collision_type == "Chain") {
            for (auto& p : chain_map[idx]) {
                if (p.first == key) return p.second;
            }
            return "";
        }
        else if (collision_type == "Linear") {
            for (int i = 0; i < table_size; ++i) {
                int new_idx = (idx + i) % table_size;
                if (table_map[new_idx].first == key)
                    return table_map[new_idx].second;
                if (table_map[new_idx].first == "")
                    return "";
            }
        }
        else if (collision_type == "Double") {
            int step = c2 - (hash_function(key, z2) % c2);
            int i = 0;
            while (true) {
                int new_idx = (h + i * step) % table_size;
                if (table_map[new_idx].first == key)
                    return table_map[new_idx].second;
                if (table_map[new_idx].first == "")
                    return "";
                ++i;
            }
        }
        return "";
    }

    vector<pair<string, string>> get_all_entries() {
        vector<pair<string, string>> result;
        if (collision_type == "Chain") {
            for (auto& bucket : chain_map)
                for (auto& p : bucket)
                    result.push_back(p);
        } else {
            for (auto& p : table_map)
                if (p.first != "") result.push_back(p);
        }
        return result;
    }

    string to_string_repr() {
        string out = "";
        if (collision_type == "Chain") {
            for (auto& bucket : chain_map) {
                if (bucket.empty()) out += "<EMPTY> | ";
                else {
                    for (auto& p : bucket)
                        out += "(" + p.first + ", " + p.second + ") ; ";
                    out.pop_back(); out.pop_back(); out.pop_back();
                    out += " | ";
                }
            }
        } else {
            for (auto& p : table_map) {
                if (p.first == "") out += "<EMPTY> | ";
                else out += "(" + p.first + ", " + p.second + ") | ";
            }
        }
        if (out.size() >= 3) out.erase(out.size() - 3);
        return out;
    }
};
// ---------- DYNAMIC HASHSET ----------

class DynamicHashSet : public HashSet {
public:
    DynamicHashSet(string type, vector<int> params) : HashSet(type, params) {}

    void insert(const string& key) {
        HashSet::insert(key);
        if (get_load() >= 0.5)
            rehash();
    }

    void rehash() {
        vector<string> all_words = get_all_elements();
        int new_size = get_next_size();

        vector<int> new_params;
        if (collision_type == "Double")
            new_params = {z1, z2, c2, new_size};
        else
            new_params = {z, new_size};

        // Recreate HashSet
        HashSet new_table(collision_type, new_params);
        for (const string& w : all_words)
            new_table.insert(w);

        // Copy updated data
        *this = DynamicHashSet(collision_type, new_params);
        for (const string& w : all_words)
            HashSet::insert(w);
    }
};
// ---------- DYNAMIC HASHMAP ----------
/*Automatically rehashes (resizes) when load factor ≥ 0.5.

rehash():

Gets next prime size.

Recreates a new table.

Re-inserts all elements.*/
class DynamicHashMap : public HashMap {
public:
    DynamicHashMap(string type, vector<int> params) : HashMap(type, params) {}

    void insert(const pair<string, string>& entry) {
        HashMap::insert(entry);
        if (get_load() >= 0.5)
            rehash();
    }

    void rehash() {
        vector<pair<string, string>> all_entries = get_all_entries();
        int new_size = get_next_size();

        vector<int> new_params;
        if (collision_type == "Double")
            new_params = {z1, z2, c2, new_size};
        else
            new_params = {z, new_size};

        // Recreate HashMap
        HashMap new_table(collision_type, new_params);
        for (const auto& p : all_entries)
            new_table.insert(p);

        // Copy updated data
        *this = DynamicHashMap(collision_type, new_params);
        for (const auto& p : all_entries)
            HashMap::insert(p);
    }
};
// ---------- MERGESORT UTILS ----------

vector<string> merge_sort(vector<string> arr) {
    if (arr.size() <= 1) return arr;
    int mid = arr.size() / 2;
    vector<string> left(arr.begin(), arr.begin() + mid);
    vector<string> right(arr.begin() + mid, arr.end());
    left = merge_sort(left);
    right = merge_sort(right);
    vector<string> merged;
    int i = 0, j = 0;
    while (i < left.size() && j < right.size()) {
        if (left[i] < right[j]) merged.push_back(left[i++]);
        else if (left[i] == right[j]) { merged.push_back(left[i++]); j++; } // skip duplicates
        else merged.push_back(right[j++]);
    }
    while (i < left.size()) merged.push_back(left[i++]);
    while (j < right.size()) merged.push_back(right[j++]);
    return merged;
}

bool binary_search_word(const vector<string>& vec, const string& word) {
    int l = 0, r = vec.size() - 1;
    while (l <= r) {
        int mid = (l + r) / 2;
        if (vec[mid] == word) return true;
        else if (vec[mid] < word) l = mid + 1;
        else r = mid - 1;
    }
    return false;
}

int binary_search_book(const vector<pair<string, vector<string>>>& books, const string& title) {
    int l = 0, r = books.size() - 1;
    while (l <= r) {
        int mid = (l + r) / 2;
        if (books[mid].first == title) return mid;
        else if (books[mid].first < title) l = mid + 1;
        else r = mid - 1;
    }
    return -1;
}

// ---------- MUSK LIBRARY ----------

class MuskLibrary {
    vector<pair<string, vector<string>>> books;

public:
    MuskLibrary(vector<string>& titles, vector<vector<string>>& texts) {
        for (int i = 0; i < titles.size(); ++i) {
            vector<string> sorted_words = merge_sort(texts[i]);
            books.push_back({titles[i], sorted_words});
        }
        sort(books.begin(), books.end());
    }

    vector<string> distinct_words(const string& book_title) {
        int idx = binary_search_book(books, book_title);
        if (idx == -1) return {};
        return books[idx].second;
    }

    int count_distinct_words(const string& book_title) {
        int idx = binary_search_book(books, book_title);
        if (idx == -1) return 0;
        return books[idx].second.size();
    }

    vector<string> search_keyword(const string& keyword) {
        vector<string> result;
        for (auto& book : books) {
            if (binary_search_word(book.second, keyword))
                result.push_back(book.first);
        }
        return result;
    }

    void print_books() {
        for (auto& book : books) {
            cout << book.first << ": ";
            for (int i = 0; i < book.second.size(); ++i) {
                cout << book.second[i];
                if (i != book.second.size() - 1) cout << " | ";
            }
            cout << endl;
        }
    }
};
// ---------- JGB LIBRARY (SAFE VERSION) ----------

class JGBLibrary {
    string name;
    vector<int> params;
    vector<pair<string, DynamicHashSet*>> books;

public:
    // Constructor: Set hashing strategy and parameters
    JGBLibrary(string dev_name, vector<int> hash_params) {
        name = dev_name;
        params = hash_params;
    }

    // Add a book with its word list
    void add_book(const string& book_title, const vector<string>& text) {
        DynamicHashSet* word_set;

        if (name == "Jobs")
            word_set = new DynamicHashSet("Chain", params);
        else if (name == "Gates")
            word_set = new DynamicHashSet("Linear", params);
        else
            word_set = new DynamicHashSet("Double", params);

        for (const string& word : text) {
            word_set->insert(word);
        }

        books.push_back({book_title, word_set});
    }

    // Return distinct words in a book
    vector<string> distinct_words(const string& book_title) {
        for (auto& entry : books) {
            if (entry.first == book_title) {
                return entry.second->get_all_elements();
            }
        }
        return {};
    }

    // Return count of distinct words in a book
    int count_distinct_words(const string& book_title) {
        for (auto& entry : books) {
            if (entry.first == book_title) {
                return entry.second->count();
            }
        }
        return 0;
    }

    // Return list of book titles that contain the keyword
    vector<string> search_keyword(const string& keyword) {
        vector<string> result;
        for (auto& entry : books) {
            if (entry.second->find_bool(keyword)) {
                result.push_back(entry.first);
            }
        }
        return result;
    }

    // Print all books in required format
    void print_books() {
        for (auto& entry : books) {
            cout << entry.first << ": " << entry.second->to_string_repr() << endl;
        }
    }
};
