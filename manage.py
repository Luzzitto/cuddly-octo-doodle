import os
import sys

def register():
    pass

def main():
    try:
        subcommand = sys.argv[1]
    except Exception:
        print("Usage: py manage.py [subcommand]")
    
    if subcommand in ["register"]:
        globals()[subcommand]()
    
if __name__ == "__main__":
    main()
