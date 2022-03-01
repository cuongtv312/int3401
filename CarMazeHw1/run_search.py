
from PIL import Image, ImageDraw
import time
import sys
from environment import CarMazeEnv
from solver import Solver
import argparse
import os


def trace_back(solver, x, y, d, v, image):
    path = [(x, y, d, v)]
    draw = ImageDraw.Draw(image)
    scale_factor = solver.env.scale_factor
    prev_state = solver.path[path[-1]]
    while prev_state != None:
        path.append(prev_state)
        draw.line([((x+0.5) * scale_factor, (y+0.5) * scale_factor),
                    ((prev_state[0] + 0.5) * scale_factor, (prev_state[1] + 0.5) * scale_factor)], 
                    fill='red', width=4)
        x, y, d, v = prev_state
        prev_state = solver.path[prev_state]
    return path


#%%
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_file', type=str, default='input.txt',
                        help='Input file')
    parser.add_argument('--method', type=str, default='bfs',
                        help='The searching algorithm')
    parser.add_argument('--output_folder', type=str, default='./images',
                        help='Base input folder')

    args = parser.parse_args()
    method = args.method
    inputmap = args.input_file
    output_folder = args.output_folder

    assert method in ('bfs')
    # inputmap='car_large'
    env = CarMazeEnv()
    env.read_map(inputmap)
    env.image.show()
    env.image.save(os.path.join(output_folder, 'env_' + inputmap.split('/')[-1].split('.')[0] + '.png'))
    solver = Solver(env)

    print("solving ...")
    start = time.time()
    ans, last_state = solver.solve_bfs()
    print('Min cost', ans, 'Done in', time.time() - start)
    print('Tracing...')
    path = trace_back(solver, *last_state, env.image)
    print('Num step:', len(path) - 1)
    print('Found path:')
    for s in reversed(path):
        print('->',s)
    print('Showing map and path') 
    env.image.show()
    env.image.save(os.path.join(output_folder, f'{method}_' + inputmap.split('/')[-1].split('.')[0] + '.png'))
# %%
