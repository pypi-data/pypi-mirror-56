class Masheen():
    validCommands = '+-><[].,'
    
    def __init__(self, prog, dataIn=[0], debuggering=False):
        self.maxValue = 256
        self.dataIn = dataIn
        self.pointIn = 0
        self.dataN = 10
        self.dataProg = [0]*self.dataN
        self.dataCode = [di for di in prog if di in self.validCommands]
        self.maxStep = 1000
        self.pointData = 0
        self.pointCode = 0
        self.pointJumps = []
        self.outs = []
        self.debuggering = debuggering
        if self.debuggering:
            print(self.dataCode)
    def run(self):
        if len(self.dataCode)==0:
            return
        for i in range(self.maxStep):
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
                if self.dataProg[self.pointData] == 0:
                    #print('?')
                    deep = 0
                    newpointCode = None
                    for di, d in enumerate(self.dataCode[self.pointCode+1:]):
                        #print(d)
                        #print(deep)
                        #print(di)
                        if d == ']' and deep == 0:
                            newpointCode = di + self.pointCode + 1
                        elif d == ']' and deep > 0:
                            deep -= 1
                        if d == '[':
                            deep += 1
                    if newpointCode is None:
                        raise ValueError("Can't find proper matching ']'.")
                    self.pointCode = newpointCode
                else:
                    self.pointJumps.append(self.pointCode)
            elif self.dataCode[self.pointCode] == ']':
                if len(self.pointJumps) == 0:
                    self.pointJumps.append(0)
                if self.dataProg[self.pointData] != 0:
                    self.pointCode = self.pointJumps[-1]
                else:
                    del self.pointJumps[-1]
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
            if self.pointCode >= len(self.dataCode):
                break

def Mash(prog):
    m = Masheen(prog)
    m.run()
    return ''.join([chr(mi) for mi in m.outs])

if __name__ == '__main__':            
    c = '+>++<-'
    c = '++++[><-]'

    hello = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'
    m = Masheen(hello)


    m.run()

    print(''.join([chr(mi) for mi in m.outs]))