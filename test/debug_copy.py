#!/usr/bin/env python3
import sys
import os

# Add the src directory to Python path to import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from random_graph_manager import RandomGraphManager
import random
import networkx as nx
from node import LoopNode

# Create manager and generate a graph
manager = RandomGraphManager(seed=10)
manager.generate_random_graph()

# Get original loop nodes
original_loop_nodes = [n for n in manager.program_graph.nodes() if isinstance(n, LoopNode)]

# Create copies
copy1 = manager.program_graph.copy()
copy2 = manager.program_graph.copy()

# Get loop nodes from copies
copy1_loop_nodes = [n for n in copy1.nodes() if isinstance(n, LoopNode)]
copy2_loop_nodes = [n for n in copy2.nodes() if isinstance(n, LoopNode)]

print("Original loop nodes:")
for i, node in enumerate(original_loop_nodes[:3]):
    print(f"  {i}: {id(node)} - {node.name}")

print("\nCopy 1 loop nodes:")
for i, node in enumerate(copy1_loop_nodes[:3]):
    print(f"  {i}: {id(node)} - {node.name}")

print("\nCopy 2 loop nodes:")
for i, node in enumerate(copy2_loop_nodes[:3]):
    print(f"  {i}: {id(node)} - {node.name}")

# Check if they are the same objects
print(f"\nAre first loop nodes the same object? Original vs Copy1: {original_loop_nodes[0] is copy1_loop_nodes[0]}")
print(f"Are first loop nodes the same object? Copy1 vs Copy2: {copy1_loop_nodes[0] is copy2_loop_nodes[0]}")

# Test setting an attribute
copy1_loop_nodes[0].test_attr = "copy1"
copy2_loop_nodes[0].test_attr = "copy2"

print(f"\nAfter setting different attributes:")
print(f"Original loop node test_attr: {getattr(original_loop_nodes[0], 'test_attr', 'None')}")
print(f"Copy1 loop node test_attr: {getattr(copy1_loop_nodes[0], 'test_attr', 'None')}")
print(f"Copy2 loop node test_attr: {getattr(copy2_loop_nodes[0], 'test_attr', 'None')}")
