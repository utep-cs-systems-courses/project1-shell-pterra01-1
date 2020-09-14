import os, sys, re

#Taking in input
def main():
    while True:
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
                os.write(2, ("cd: no such file or direcory\n").encode())
        else:
            execute(command)

def execute(command):
    pid = os.getpid()
    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
    
    rc = os.fork()
    args = command.split()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:      #child
        os.write(1, ("This is a child! Child's pid=%d Parent's pid=%d\n" % (os.getpid(),pid)).encode())
        if '>' in command:
            redirect('>', command)
        elif '<' in command:
            redirect('<', command)
        else:
            for dir in re.split(":", os.environ['PATH']): #try each directory in the path
                program = "%s/%s" % (dir, args[0])
                os.write(1, ("Child is trying to exec %s\n" % program).encode())
                try:
                    os.execve(program, args, os.environ) #try to exec program
                except FileNotFoundError:                #this is expected
                    pass                                 #fail quietly
                        
            os.write(2, ("Child was not able to exec %s\n" % args[0]).encode())
            sys.exit(1)                                  #terminate with error
    else:
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %(pid, rc)).encode())
        wait = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %wait).encode())
        
    
    
def redirect(command):
    print("working on it...")
    
    
if '__main__' == __name__:
    main()
       