#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import urllib.request

file_url = 'https://www.cs.princeton.edu/~appel/graphdata/graphs.txt.Z'
graph_filename = 'graphs.txt'
data_dirname = ''

def flush(edges, fileno):

    if len(edges) == 0:
        return False

    # rename vertices
    vs = set()
    for e in edges:
        vs.add(e[0])
        vs.add(e[1])

    vdict = {}
    n = 1
    for v in sorted(vs):
        vdict[v] = n
        n += 1

    new_edges = []
    for e in edges:
        v1 = vdict[e[0]]
        v2 = vdict[e[1]]
        new_edges.append((min(v1, v2), max(v1, v2)))

    
    with open(os.path.join(data_dirname, 'register{}.txt'.format(fileno)), 'w') as fout:
        print('p {} {}'.format(len(vs), len(new_edges)), file = fout)
        for e in sorted(new_edges, key = lambda x: 1000000 * x[0] + x[1]):
            print('e {} {}'.format(e[0], e[1]), file = fout)

    return True

def parse(filename, num_files):
    with open(filename) as f:
        edges = []
        fileno = 1
        for line in f:
            if line.startswith('Graph'):
                if flush(edges, fileno):
                    fileno += 1
                    if fileno > num_files:
                        return
                    edges = []
            elif line.startswith('K='):
                pass # ignore
            elif line.find('-->') >= 0:
                ar = line.strip().split(' --> ')
                src = int(ar[0])
                dests = ar[1].split(' ')
                for d in dests:
                    edges.append((src, int(d)))
            elif line.find('<->'):
                ar = line.strip().split(' ')
                for a in ar:
                    es = a.split('<->')
                    edges.append((int(es[0]), int(es[1])))
        flush(edges, fileno)

def main():

    if len(sys.argv) >= 2:
        if sys.argv[1] == 'all':
            n = 9999999999
        else:
            n = len(sys.argv[1])
    else:
        n = 100

    comp_filename = os.path.basename(file_url)
    if not os.path.exists(comp_filename) and not os.path.exists(graph_filename):
        with urllib.request.urlopen(file_url) as web:
            with open(comp_filename, 'wb') as f:
                f.write(web.read())

    if not os.path.exists(comp_filename):
        subprocess.run(['gunzip', '-k', comp_filename])

    #if not os.path.exists(data_dirname):
    #    os.mkdir(data_dirname)

    parse(graph_filename, n)

if __name__ == '__main__':
    main()
