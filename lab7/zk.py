from kazoo.client import KazooClient
import subprocess
import tkinter as tk
from tkinter import messagebox
import sys
from functools import partial
import threading


NODE = "/a"
application = None
zk = KazooClient(hosts="127.0.0.1:2181")

watched_paths = set()
last_count = -1


def show_popup(n):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo(
        "Children",
        f"Number of descendants of node {NODE}: {n}",
        parent=root
    )
    root.destroy()

def dfs_nodes(path):
    paths = []
    try:
        children = zk.get_children(path)
    except Exception:
        return paths

    if not children:
        return paths

    for child in children:
        child_path = f"{path}/{child}"
        paths.append(child_path)
        paths.extend(dfs_nodes(child_path))
    
    return paths

def watch_children(_):
    global last_count

    if not zk.exists(NODE):
        return

    descendants = dfs_nodes(NODE)
    n = len(descendants)

    current_paths = set(descendants)
    for path in list(watched_paths):
        if path not in current_paths:
            watched_paths.remove(path)

    if n != last_count:
        last_count = n
        threading.Thread(target=show_popup, args=(n,)).start()

    for child_path in descendants:
        if child_path not in watched_paths:
            watched_paths.add(child_path)
            zk.ChildrenWatch(child_path, watch_children)

def watch_node(program, event):
    global application
    global last_count

    if event.type == "CREATED":
        print("Start application")
        last_count = -1
        application = subprocess.Popen([program], stdout=subprocess.DEVNULL)
        zk.ChildrenWatch(NODE, watch_children)
    elif event.type == "DELETED":
        print("Close application")
        if application:
            application.terminate()
            application = None
        
        watched_paths.clear()
    
    zk.exists(NODE, partial(watch_node, program))

def print_tree(path):
    if not zk.exists(path):
        print("Empty tree")
        return
    
    node_name = path.split("/")[-1]
    indent = len(path) - len(node_name) - 1
    print(" " * indent + f"/{node_name}")
    children = zk.get_children(path)

    if not children:
        return

    for child in children:
        print_tree(f"{path}/{child}")

def main():
    if len(sys.argv) != 2:
        return

    program = sys.argv[1]
    zk.start()
    print("Client started")
    zk.exists(NODE, partial(watch_node, program))

    try:
        while True:
            cmd = input("\nTo get tree type T:\n")
            if cmd.upper() == "T":
                print_tree(NODE)
            elif cmd.upper() == "S":
                break
            else:
                print("Wrong command")
    except KeyboardInterrupt:
        pass
    finally:
        print("Client stopped")
        zk.stop()


if __name__ == "__main__":
    main()
