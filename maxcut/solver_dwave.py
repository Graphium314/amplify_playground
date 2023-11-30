import sys
from amplify import IsingPoly, IsingSymbolGenerator
from amplify import Solver
from amplify.client.ocean import LeapHybridSamplerClient

from dotenv import load_dotenv
load_dotenv()

import os

def main():
    args = sys.argv
    input_path = args[1]

    with open(input_path, 'r') as f:
        lines = f.readlines()

    # v: 頂点数, e: 辺数
    v,e = map(int, lines[0].split())

    # イジング変数の設定
    gen = IsingSymbolGenerator()
    s = gen.array(v)

    # 目的関数の設定
    f = IsingPoly()
    for i in range(1,e+1):
        u,v,c= map(int, lines[i].split())
        f += c*(1-s[u-1]*s[v-1])
    f /= 2
    f *= -1

    # clientの設定
    client = LeapHybridSamplerClient()
    client.solver = "hybrid_binary_quadratic_model_version2"
    client.token = os.getenv('DWAVE_TOKEN')

    # 実行
    solver = Solver(client)
    result = solver.solve(f)

    for sol in result:
        solution = s.decode(sol.values)

    print(-sol.energy)

if __name__ == '__main__':
    main()
