class Masheen():
    validCommands = '+-><[].,'
    
    def __init__(self, prog, dataIn=[0], dataN=10, debuggering=False):
        self.maxValue = 256
        self.dataIn = dataIn
        self.pointIn = 0
        self.dataN = dataN
        self.dataProg = [0]*self.dataN
        if hasattr(prog, 'read'):
            progS = prog.read()
        else:
            progS = prog
        self.dataCode = [di for di in progS if di in self.validCommands]
        self.maxStep = 1000
        self.pointData = 0
        self.pointCode = 0
        self.pointJumps = []
        self.point_r_braces = []
        self.outs = []
        self.iteration = 0
        self.out_code = 'not started'
        self.out_of_code = False
        self.strict_r_brace = True
        self.debuggering = debuggering
        if self.debuggering:
            print(self.dataCode)
    def run(self, steps=None):
        if len(self.dataCode)==0:
            return
        run_iteration = 0
        while True:
            if self.pointCode >= len(self.dataCode):
                self.out_of_code = True
                self.out_code = 'out of code'
                break
            if steps:
                if steps <= 0:
                    self.out_code = '0 steps input'
                    break
                if run_iteration >= steps:
                    self.out_code = 'reached run max iterations'
                    break
            if not steps and self.iteration >= self.maxStep:
                self.out_code = 'reached global max iterations'
                break
            run_iteration += 1
            self.iteration += 1
        #for i in range(self.maxStep):
            if self.debuggering:
                print(f'iter {i}, code {self.dataCode[self.pointCode]}')
            if self.dataCode[self.pointCode] == '+':
                self.dataProg[self.pointData] += 1
            elif self.dataCode[self.pointCode] == '-':
                self.dataProg[self.pointData] -= 1
            elif self.dataCode[self.pointCode] == '>':
                self.pointData += 1
            elif self.dataCode[self.pointCode] == '<':
                self.pointData -= 1
            elif self.dataCode[self.pointCode] == '[':
                
                #print('?')
                deep = 0
                rbrace = None
                for di, d in enumerate(self.dataCode[self.pointCode+1:]):
                    #print(d)
                    #print(deep)
                    #print(di)
                    if d == ']' and deep == 0:
                        rbrace = di + self.pointCode + 1
                        break
                    elif d == ']' and deep > 0:
                        deep -= 1
                    if d == '[':
                        deep += 1
                if rbrace is None:
                    raise ValueError("Can't find proper matching ']'.")
                if self.dataProg[self.pointData] == 0:
                    self.pointCode = rbrace
                else:
                    self.pointJumps.append(self.pointCode)
                    self.point_r_braces.append(rbrace)
            elif self.dataCode[self.pointCode] == ']':
                if len(self.pointJumps) == 0:
                    if self.strict_r_brace:
                        raise ValueError("Can't find proper matching '['.")
                    else:
                        self.pointJumps.append(0)
                if self.dataProg[self.pointData] != 0:
                    self.pointCode = self.pointJumps[-1]
                else:
                    del self.pointJumps[-1]
                    del self.point_r_braces[-1]

            elif self.dataCode[self.pointCode] == '.':
                self.outs.append(self.dataProg[self.pointData])
            elif self.dataCode[self.pointCode] == ',':
                self.dataProg[self.pointData] = self.dataIn[self.pointIn]
                self.pointIn += 1
                self.pointIn = self.pointIn % len(self.dataIn)
            
            self.pointCode +=1
            self.pointData = self.pointData % self.dataN
            self.dataProg = [d % self.maxValue for d in self.dataProg]
            if self.debuggering:
                print(''.join([f'*{d}*' if di==self.pointData else f' {d} ' for di, d in enumerate(self.dataProg)]))
            if self.debuggering:
                print(self.dataProg)
                print(f'pointData {self.pointData} \npointCode {self.pointCode}')


def Mash(prog):
    m = Masheen(prog)
    m.run()
    return ''.join([chr(mi) for mi in m.outs])