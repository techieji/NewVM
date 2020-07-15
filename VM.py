import re

labelpattern = re.compile(r".*:")
stmtpattern = re.compile(r"    .*")

variables = {
        "ENV": None,
}

functions = {
        "cp": (1, lambda x: [x, x]),
        "out": (1, lambda x: print(x)),
        "call": (1, lambda x: x.execute(env=variables["ENV"]))
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
            x = functions[ins][1](*args)
            # print(f"{ins}: {args}")
            if x != None:
                self.stack += list(x)

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

def makeEnv(c, m):
    ans = {}
    for key in c:
        ans[key] = Function(c[key], m)
    variables["ENV"] = ans
    return ans

if __name__ == "__main__":
    with open("test.vm") as f:
        m = Machine()
        env = makeEnv(parsenames(f.read()), m)
        env['_start'].execute(env=env)
