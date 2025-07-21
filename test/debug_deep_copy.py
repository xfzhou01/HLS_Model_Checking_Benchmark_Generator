#!/usr/bin/env python3
import sys
import os

# Add the src directory to Python path to import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from random_graph_manager import RandomGraphManager
import random
import networkx as nx
from node import LoopNode

# Create manager and generate a small graph
manager = RandomGraphManager(seed=10)
manager.generate_random_graph()

print('Original graph nodes:', manager.program_graph.number_of_nodes())

# Call copy and insert pragmas
manager._copy_graph_and_insert_pragmas()
print('Copy 1 nodes:', manager.program_graph_copy_1.number_of_nodes())
print('Copy 2 nodes:', manager.program_graph_copy_2.number_of_nodes())

# Check loop nodes and their object IDs
loop_nodes_1 = [n for n in manager.program_graph_copy_1.nodes() if isinstance(n, LoopNode)]
loop_nodes_2 = [n for n in manager.program_graph_copy_2.nodes() if isinstance(n, LoopNode)]

print('Loop nodes in copy 1:', len(loop_nodes_1))
print('Loop nodes in copy 2:', len(loop_nodes_2))

if loop_nodes_1 and loop_nodes_2:
    print(f'First loop node ID copy 1: {id(loop_nodes_1[0])}')
    print(f'First loop node ID copy 2: {id(loop_nodes_2[0])}')
    print(f'Are they the same object? {loop_nodes_1[0] is loop_nodes_2[0]}')
    
    # Check first few loops for pragma differences
    for i in range(min(3, len(loop_nodes_1), len(loop_nodes_2))):
        node1 = loop_nodes_1[i]
        node2 = loop_nodes_2[i]
        print(f'Loop {i}:')
        print(f'  Copy 1 - pipelined: {getattr(node1, "is_pipelined", None)}, unrolled: {getattr(node1, "is_unrolled", None)}, factor: {getattr(node1, "unroll_factor", None)}')
        print(f'  Copy 2 - pipelined: {getattr(node2, "is_pipelined", None)}, unrolled: {getattr(node2, "is_unrolled", None)}, factor: {getattr(node2, "unroll_factor", None)}')
        same_pragmas = (getattr(node1, "is_pipelined", None) == getattr(node2, "is_pipelined", None) and 
                       getattr(node1, "is_unrolled", None) == getattr(node2, "is_unrolled", None) and
                       getattr(node1, "unroll_factor", None) == getattr(node2, "unroll_factor", None))
        print(f'  Same pragmas? {same_pragmas}')

print('Clock period 1:', getattr(manager, 'cp_1', None))
print('Clock period 2:', getattr(manager, 'cp_2', None))
