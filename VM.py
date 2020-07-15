import re

labelpattern = re.compile(r".*:")
stmtpattern = re.compile(r"    .*")

functions = {
        "cp": (1, lambda x: [x, x]),
        "out": (1, lambda x: print(x)),
        "call": (1, lambda x: x.execute())
}

class Function:
    def __init__(self, source):
        self.source = source
    
    def execute(self, machine, env={}):
        machine.execute(self.source, env)

class Machine:
    def __init__(self):
        self.stack = []
    
    def doins(self, ins, env={}):
        if ins in functions.keys():
            argnum = functions[ins][0]
            args = []
            while argnum != 0:
                args.append(self.stack.pop())
                argnum -= 1
            self.stack += functions[ins][1](*args)

        elif ins in env.keys():
            self.stack.append(env[ins])
        else:
            self.stack.append(ins)

    def execute(self, instructions, env={}):
        for i in instructions:
            self.doins(i, env)

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

def makeEnv(c):
    ans = {}
    for key in c:
        ans[key] = Function(c[key])
    return ans

if __name__ == "__main__":
    with open("test.vm") as f:
        m = Machine()
        env = makeEnv(parsenames(f.read()))
        env['_start'].execute(m, env)
