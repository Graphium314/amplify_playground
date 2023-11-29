import sys
from amplify import IsingPoly, IsingSymbolGenerator
from amplify import Solver
from amplify.client import FixstarsClient
from dotenv import load_dotenv
load_dotenv()

import os

def main():
    args = sys.argv
    input_path = args[1]

    with open(input_path, 'r') as f:
        lines = f.readlines()

    v,e = map(int, lines[0].split())

    gen = IsingSymbolGenerator()
    s = gen.array(v)
    f = IsingPoly()
    for i in range(1,e+1):
        u,v,c= map(int, lines[i].split())
        f += c*(1-s[u-1]*s[v-1])
    f /= 2
    f *= -1

    client = FixstarsClient()
    client.parameters.timeout = 10000
    client.token = os.getenv('FIXSTARS_AE_TOKEN')

    solver = Solver(client)

    result = solver.solve(f)

    for sol in result:
        solution = s.decode(sol.values)

    print(-sol.energy)

if __name__ == '__main__':
    main()
