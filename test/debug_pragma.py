#!/usr/bin/env python3
import sys
import os

# Add the src directory to Python path to import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from random_graph_manager import RandomGraphManager
import random
import networkx as nx

# Create manager and generate a graph
manager = RandomGraphManager(seed=10)
manager.generate_random_graph()
print('Original graph nodes:', manager.program_graph.number_of_nodes())

# Call copy and insert pragmas
manager._copy_graph_and_insert_pragmas()
print('Copy 1 nodes:', manager.program_graph_copy_1.number_of_nodes())
print('Copy 2 nodes:', manager.program_graph_copy_2.number_of_nodes())

# Check if copies are identical
print('Are copies identical?', nx.is_isomorphic(manager.program_graph_copy_1, manager.program_graph_copy_2))

# Check loop nodes and their pragmas
from node import LoopNode
loop_nodes_1 = [n for n in manager.program_graph_copy_1.nodes() if isinstance(n, LoopNode)]
loop_nodes_2 = [n for n in manager.program_graph_copy_2.nodes() if isinstance(n, LoopNode)]
print('Loop nodes in copy 1:', len(loop_nodes_1))
print('Loop nodes in copy 2:', len(loop_nodes_2))

if loop_nodes_1 and loop_nodes_2:
    print('First loop pragma in copy 1:', getattr(loop_nodes_1[0], 'is_pipelined', None))
    print('First loop pragma in copy 2:', getattr(loop_nodes_2[0], 'is_pipelined', None))
    
    # Check all pragmas
    for i, (node1, node2) in enumerate(zip(loop_nodes_1, loop_nodes_2)):
        print(f'Loop {i} copy 1 pipelined:', getattr(node1, 'is_pipelined', None))
        print(f'Loop {i} copy 2 pipelined:', getattr(node2, 'is_pipelined', None))
        print(f'Loop {i} copy 1 unrolled:', getattr(node1, 'is_unrolled', None))
        print(f'Loop {i} copy 2 unrolled:', getattr(node2, 'is_unrolled', None))
        print(f'Loop {i} copy 1 flattened:', getattr(node1, 'is_flattened', None))
        print(f'Loop {i} copy 2 flattened:', getattr(node2, 'is_flattened', None))
        print(f'Loop {i} copy 1 unroll_factor:', getattr(node1, 'unroll_factor', None))
        print(f'Loop {i} copy 2 unroll_factor:', getattr(node2, 'unroll_factor', None))
        print('---')

# Test the clock periods
print('Clock period 1:', getattr(manager, 'cp_1', None))
print('Clock period 2:', getattr(manager, 'cp_2', None))
