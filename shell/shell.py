#! /usr/bin/env python3

import os, sys, re

#Taking in input
def main():
    while True:
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())

        command = input("$ ")
            
        if command == "exit":
            sys.exit(1)
            
        elif command == "help":
            print("note: help was selected")
            
        elif 'cd' in command:
            if '..' in command:
                cd_change = '..'
            else:
                cd_change = command.split('cd')[1].strip()
            try:
                os.chdir(cd_change)
            except FileNotFoundError:
                os.write(1, ("cd %s: No such file or directory\n" % cd_change).encode())
                pass
            continue
        
        else:
            execute(command)
            
def path(args):

    for dir in re.split(":", os.environ['PATH']): # try each directory in the path
        program = "%s/%s" % (dir, args[0])
        os.write(1, ("Child is trying to exec %s\n" % program).encode())
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:                # ...expected
            pass                                    # ...fail quietly
                        
    os.write(2, ("Child was not able to exec %s\n" % args[0]).encode())
    sys.exit(1)                                  #terminate with error

def execute(command):
    pid = os.getpid()
    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
    
    rc = os.fork()
    args = command.split()
    if rc < 0:
        os.write(2, ("Fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
   
    elif rc == 0:      #child
        os.write(1, ("Child: Child's pid=%d Parent's pid=%d\n" % (os.getpid(),pid)).encode())
        
        if '>' in command:
             os.close(1)
             sys.stdout = open(command[1].strip(), "w")
             os.set_inheritable(1, True)
             path(command[0].split())
            
        elif '<' in command:
            os.close(0)
            sys.stdin = open(command[1].strip(), 'r')
            os.set_inheritable(0, True)
            path(command[0].split())
        
        elif '|' in command: # piping
            command, command2 = command.split('|')
            command = command.split()
            command2 = command2.split()
    
            r, w = os.pipe()
            for f in (r, w):
                os.set_inheritable(f, True)
    
            pid = os.fork()
    
            if pid == 0:
                os.close(1)
                os.dup(w)
                os.set_inheritable(1, True)
                for fd in (r, w):
                   os.close(fd)
                   path(command)
            elif pid > 0:
                os.close(0)
                os.dup(r)
                os.set_inheritable(0, True) 
                for fd in (w, r):
                    os.close(fd)
                    path(command2)
            else:
                os.write(2, ('Fork failed').encode())
                sys.exit(1)
            
        else:
            path(args)                                  
    else:
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %(pid, rc)).encode())
        wait = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %wait).encode())
    