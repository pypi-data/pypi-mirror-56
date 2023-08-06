import argparse

import Masheen

p = argparse.ArgumentParser()

p.add_argument('file', type=str, default='')
p.add_argument('--hello', action='store_true')

a = p.parse_args()
#import code;code.interact(local=locals())
if a.hello:
    c = '+>++<-'
    c = '++++[><-]'

    hello = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'
    m = Masheen.Masheen(hello)

    m.run()

    print(''.join([chr(mi) for mi in m.outs]))
    exit()

if a.file:
    with open(a.file, 'r') as f:
        prog = f.read()
    data = [ord(c) for c in 'a42a \n']
    m = Masheen.Masheen(prog, debuggering=False, dataN=1000, dataIn=data)
    m.maxStep = 500000
    m.run()
    print(m.dataProg)
    print(m.outs)
    print(m.iteration)
    print(''.join([chr(mi) for mi in m.outs]))
else:
    print('Provide filename to run program.')