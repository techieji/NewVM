import re
import sys
from pprint import pprint

labelpattern = re.compile(r".*:")
stmtpattern = re.compile(r"    .*")

variables = {
        "ENV": None,
        "STACK": None
}

def setvar(varname, value):
    variables[varname] = value

functions = {
        "int": (1, lambda x: int(x)),
        "bool": (1, lambda x: bool(x)),
        "str": (1, lambda x: str(x)),
        "float": (1, lambda x: float(x)),
        "pair": (2, lambda x, y: (y, x)),
        "add": (2, lambda x, y: x + y),
        "sub": (2, lambda x, y: y - x),
        "dec": (1, lambda x: x - 1),
        "cp": (1, lambda x: [x, x]),
        "out": (1, lambda x: print(x)),
        "inp": (0, lambda x: input()),
        "call": (1, lambda x: x.execute(env=variables["ENV"])),
        "swp": (2, lambda x, y: [x, y]),
        "eq?": (2, lambda x, y: y == x),
        "set": (2, lambda x, y: setvar(x, y)),
        "get": (1, lambda x: variables[x]),
        "rm": (1, lambda x: None),
        "if": (3, lambda x, y, z: y if x else z)
}

class Function:
    def __init__(self, source, machine):
        self.source = source
        self.machine = machine

    def execute(self, env={}):
        self.machine.execute(self.source, env)

class Machine:
    def __init__(self):
        self.stack = []
    
    def doins(self, ins, env={}):
        if ins in functions.keys():
            argnum = functions[ins][0]
            args = []
            for x in range(argnum):
                args.append(self.stack.pop())
#            print(f"{ins}: {args}")
            x = functions[ins][1](*args)
            if x != None:
                if type(x) == list:
                    self.stack += x
                else:
                    self.stack.append(x)

        elif ins in env.keys():
            self.stack.append(env[ins])
        else:
            self.stack.append(ins)

        variables["STACK"] = tuple(self.stack)

    def oldexec(self, instructions, env):
        for ins in instructions:
            self.doins(ins, env)

    def execute(self, instructions, env={}):
        i = 0
        while i < len(instructions):
            ins = instructions[i]
            if ins == "jmp":
                i = self.stack.pop()
            else:
                self.doins(ins, env)
                i += 1

def parsenames(doc):
    ans = {}
    curref = ""
    lines = doc.split("\n")
    for line in lines:
        if labelpattern.match(line):
            curref = line[:-1]
            ans[curref] = []
        elif stmtpattern.match(line):
            ans[curref].append(line[4:])
    return ans

def makeEnv(c, m):
    ans = {}
    for key in c:
        ans[key] = Function(c[key], m)
    variables["ENV"] = ans
    return ans

def runFiles(f1, *fs):
    text = ""
    for x in fs:
        with open(x) as f:
            text += f.read()
            text += "\n"

    m = Machine()
    env = makeEnv(parsenames(text), m)
    env['_start'].execute(env=env)
#    print("Env: ", end="")
#    pprint(variables["ENV"])
#    print(f"_start: {variables['ENV']['_start'].source}")
#    print(f"Stack at end: {variables['STACK']}")

if __name__ == "__main__":
    args = sys.argv
    runFiles(*args)
