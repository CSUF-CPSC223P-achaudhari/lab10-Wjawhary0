import threading
import time
import json

def load_inventory(filename='inventory.dat'):
    with open(filename, 'r') as file:
        inventory = json.load(file)
    return inventory

def bot_fetcher(items, cart, lock, inventory):
    for item in items:
        time.sleep(inventory[item][1]) 
        with lock:
            cart.append([item, inventory[item][0]])

def bot_clerk(items):
    inventory = load_inventory()
    cart = []
    lock = threading.Lock()

    fetcher_lists = [[] for _ in range(3)]
    for i, item in enumerate(items):
        fetcher_lists[i % 3].append(item)

    threads = []
    for fetcher_list in fetcher_lists:
        thread = threading.Thread(target=bot_fetcher, args=(fetcher_list, cart, lock, inventory))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return cart

if __name__ == "__main__":
    items_to_fetch = ['101', '103', '105', '107']
    cart_items = bot_clerk(items_to_fetch)
    print("Cart contains:", cart_items)
