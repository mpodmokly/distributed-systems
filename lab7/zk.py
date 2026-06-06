from kazoo.client import KazooClient
import subprocess
import tkinter as tk
from tkinter import messagebox
import sys


NODE = "/a"
application = None
program = sys.argv[1]
zk = KazooClient(hosts="127.0.0.1:2181")

def watch_children(children):
    n = len(children)

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo("Children", f"Number of children of node /a: {n}", parent=root)
    root.destroy()

def watch_node(event):
    global application

    if event.type == "CREATED":
        print("Start application")
        application = subprocess.Popen([program], stdout=subprocess.DEVNULL)
        zk.ChildrenWatch(NODE, watch_children)
    elif event.type == "DELETED":
        print("Close application")
        if application:
            application.terminate()
            application = None
    
    zk.exists(NODE, watch_node)

def print_tree(path):
    if not zk.exists(path):
        print("Empty tree")
        return
    
    node_name = path.split("/")[-1]
    indent = len(path) - len(node_name) - 1
    print(" " * indent + f"/{node_name}")
    children = zk.get_children(path)
    for child in children:
        print_tree(f"{path}/{child}")


zk.start()
print("Client started")
zk.exists(NODE, watch_node)

try:
    while True:
        cmd = input("\nTo get tree type T:\n")
        if cmd == "T":
            print_tree(NODE)
        elif cmd == "STOP":
            print("Client stopped")
            break
        else:
            print("Wrong command")
except KeyboardInterrupt:
    print("Client stopped")
finally:
    zk.stop()
