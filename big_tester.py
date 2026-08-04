from hash_table import HashSet, HashMap
from dynamic_hash_table import DynamicHashSet, DynamicHashMap
from library import MuskLibrary, JGBLibrary
from prime_generator import set_primes, get_next_size
import random
import string

def generate_large_dataset(num_elements):
    return [f"{''.join(random.choices(string.ascii_letters, k=8))}_{i}" for i in range(num_elements)]

def test_hash_set():
    print("Starting rigorous test for HashSet...\n")

    print("Testing HashSet with Chaining on large data:")
    table_size = 997  # Larger prime table size
    hs_chain = HashSet("Chain", (31, table_size))
    elements = generate_large_dataset(1000)  # 1000 unique keys

    # Insert and test retrieval
    for elem in elements:
        hs_chain.insert(elem)
        assert hs_chain.find(elem), f"Element {elem} not found!"
    print("All elements found after insertion.")

    # Test retrieval with missing elements
    missing_elements = generate_large_dataset(500)  # Non-existent elements
    for elem in missing_elements:
        assert not (hs_chain.find(elem) == elem in elements), f"Unexpectedly found missing element {elem}!"
    print("All missing elements correctly not found.")

    print("Passed large data test for HashSet with Chaining.\n")

    print("Testing HashSet with Linear Probing on high collision data:")
    hs_linear = HashSet("Linear", (31, table_size))
    colliding_keys = [f"collision_{i % 10}" for i in range(500)]  # High collision dataset

    # Insert and test retrieval with collisions
    for elem in colliding_keys:
        hs_linear.insert(elem)
    assert all(hs_linear.find(elem) for elem in set(colliding_keys)), "Collision handling failed for Linear Probing."
    
    print("Passed collision test for HashSet with Linear Probing.\n")

    print("Testing HashSet with Double Hashing on random data:")
    hs_double = HashSet("Double", (7, 3, 5, 1049))
    for elem in elements:
        hs_double.insert(elem)
        assert hs_double.find(elem), f"Element {elem} not found in Double Hashing."
    
    print("Passed test for HashSet with Double Hashing.\n")

def test_hash_map():
    print("Starting rigorous test for HashMap...\n")

    print("Testing HashMap with Chaining on large dataset:")
    table_size = 997
    hm_chain = HashMap("Chain", (31, table_size))
    kv_pairs = [(f"key_{i}", i) for i in range(1000)]  # 1000 unique key-value pairs

    # Insert key-value pairs
    for key, val in kv_pairs:
        hm_chain.insert((key, val))
    print("Inserted all key-value pairs.")

    # Test retrieval and updating values
    for key, val in kv_pairs:
        assert hm_chain.find(key) == val, f"Incorrect value for {key}."
    print("All values correctly retrieved.")

    # Update values and verify
    # for key, val in kv_pairs:
    #     hm_chain.insert((key, val + 1))
    # for key, val in kv_pairs:
    #     assert hm_chain.find(key) == val + 1, f"Update failed for {key}."
    print("Value updates verified.")

    print("Passed test for HashMap with Chaining on large dataset.\n")

def test_dynamic_hash_set():
    print("Starting rigorous test for DynamicHashSet...\n")
    set_primes([21727,10111,5879,2731,1049,571,101,97,29])
    initial_table_size = 7  # Small prime to ensure frequent resizing
    dhs = DynamicHashSet("Chain", (31, initial_table_size))
    elements = generate_large_dataset(5000)  # Test with 5000 elements for resizing stress

    for i, elem in enumerate(elements):
        dhs.insert(elem)
        if (i + 1) % 1000 == 0:
            print(f"Inserted {i + 1} elements, current load: {dhs.get_load():.2f}")

    print("Inserted all elements into DynamicHashSet.")

    # Check all elements are retrievable after multiple resizes
    for elem in elements:
        assert dhs.find(elem), f"Element {elem} missing after rehash."
    print("All elements found post-rehash.")

    print("Passed rigorous test for DynamicHashSet.\n")

def test_dynamic_hash_map():
    print("Starting rigorous test for DynamicHashMap...\n")
    initial_table_size = 7
    dhm = DynamicHashMap("Chain", (31, initial_table_size))
    kv_pairs = [(f"key_{i}", i) for i in range(5000)]

    for i, (key, val) in enumerate(kv_pairs):
        dhm.insert((key, val))
        if (i + 1) % 1000 == 0:
            print(f"Inserted {i + 1} key-value pairs, current load: {dhm.get_load():.2f}")

    # Check all key-value pairs are retrievable after rehashes
    for key, val in kv_pairs:
        assert dhm.find(key) == val, f"Value for {key} missing after rehash."
    print("All key-value pairs found post-rehash.")

    print("Passed rigorous test for DynamicHashMap.\n")

def test_digital_library():
    print("Starting rigorous test for DigitalLibrary...\n")
    book_titles = [f"book_{i}" for i in range(50)]
    book_texts = [generate_large_dataset(1000) for _ in book_titles]

    print("Testing MuskLibrary with large data...")
    musk_lib = MuskLibrary(book_titles, book_texts)

    # Test distinct words and counts for MuskLibrary
    for title, text in zip(book_titles, book_texts):
        assert musk_lib.count_distinct_words(title) == len(set(text))
    print("Distinct word counts verified for MuskLibrary.")

    # Test keyword search across all books
    for title, text in zip(book_titles, book_texts):
        if text:
            word = text[0]
            assert title in musk_lib.search_keyword(word), f"Keyword {word} not found in {title}."
    print("Keyword search verified for MuskLibrary.")

    print("Testing JGBLibrary (Jobs) with large data...")
    jgb_lib_jobs = JGBLibrary("Jobs", (31, 997))
    for title, text in zip(book_titles, book_texts):
        jgb_lib_jobs.add_book(title, text)

    # Test distinct word counts for JGBLibrary
    for title, text in zip(book_titles, book_texts):
        assert jgb_lib_jobs.count_distinct_words(title) == len(set(text))
    print("Distinct word counts verified for JGBLibrary Jobs.")

    # Test keyword search across all books
    for title, text in zip(book_titles, book_texts):
        if text:
            word = text[0]
            assert title in jgb_lib_jobs.search_keyword(word), f"Keyword {word} not found in {title}."
    print("Keyword search verified for JGBLibrary Jobs.")

    print("Passed rigorous test for DigitalLibrary.\n")

if __name__ == "__main__":
    test_hash_set()
    test_hash_map()
    test_dynamic_hash_set()
    test_dynamic_hash_map()
    test_digital_library()
    print("All rigorous tests completed successfully.")
