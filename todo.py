#!/usr/bin/env python3
"""Simple command-line Todo List."""

import json
import os
from pathlib import Path

TODO_FILE = Path(__file__).parent / "todos.json"

def load_todos():
    if TODO_FILE.exists():
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)

def show_todos(todos):
    if not todos:
        print("  (no todos yet)")
        return
    for i, t in enumerate(todos, 1):
        status = "[x]" if t["done"] else "[ ]"
        print(f"  {i}. {status} {t['text']}")

def main():
    print("=== Simple Todo List ===")
    print("Commands: add <text> | done <num> | delete <num> | list | quit\n")

    todos = load_todos()

    while True:
        try:
            cmd = input("> ").strip()
            if not cmd:
                continue

            parts = cmd.split(maxsplit=1)
            action = parts[0].lower()

            if action in ("quit", "exit", "q"):
                print("Bye!")
                break

            elif action == "list" or action == "ls":
                show_todos(todos)

            elif action == "add" and len(parts) > 1:
                todos.append({"text": parts[1], "done": False})
                save_todos(todos)
                print(f"Added: {parts[1]}")

            elif action == "done" and len(parts) > 1:
                try:
                    idx = int(parts[1]) - 1
                    if 0 <= idx < len(todos):
                        todos[idx]["done"] = True
                        save_todos(todos)
                        print(f"Marked done: {todos[idx]['text']}")
                    else:
                        print("Invalid number")
                except ValueError:
                    print("Please give a number")

            elif action == "delete" and len(parts) > 1:
                try:
                    idx = int(parts[1]) - 1
                    if 0 <= idx < len(todos):
                        removed = todos.pop(idx)
                        save_todos(todos)
                        print(f"Deleted: {removed['text']}")
                    else:
                        print("Invalid number")
                except ValueError:
                    print("Please give a number")

            else:
                print("Unknown command. Try: add <text> | done <num> | delete <num> | list | quit")

        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break

if __name__ == "__main__":
    main()
