import os, sys, re

#Taking in input
def main():
    while True:
        command = input("$ ")
        if command == "exit":
            break
        elif command == "help":
            print("note: help was selected")
        elif command[:3] == "cd ":
            cd(command[3:])
        else:
            execute(command)



def execute(command):
    print("working on it...")
    

def cd(command):
    print("working on it...")
    
    
if '__main__' == __name__:
    main()
       