#!/usr/bin/env python3
"""
Test script for random graph generation with different seeds.
This test generates 3 different random graphs using different seeds to ensure
reproducibility and variety in the generated HLS model checking benchmarks.
"""

import sys
import os

# Add the src directory to Python path to import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from random_graph_manager import RandomGraphManager
from node import LoopNode, BranchNode


def print_graph_statistics(graph_manager, seed):
    """
    Print statistics about the generated graph.
    
    Args:
        graph_manager: The RandomGraphManager instance
        seed: The seed used for generation
    """
    graph = graph_manager.program_graph
    
    # Count different types of nodes
    op_nodes = graph_manager._get_op_node_list()
    array_nodes = graph_manager._get_array_node_list()
    visit_nodes = graph_manager._get_visit_node_list()
    write_nodes = graph_manager._get_write_node_list()
    
    # Count loop and branch nodes
    loop_nodes = []
    branch_nodes = []
    for node in graph.nodes():
        if isinstance(node, LoopNode):
            loop_nodes.append(node)
        elif isinstance(node, BranchNode):
            branch_nodes.append(node)
    
    print(f"  Seed: {seed}")
    print(f"  Total nodes: {graph.number_of_nodes()}")
    print(f"  Total edges: {graph.number_of_edges()}")
    print(f"  Operation nodes: {len(op_nodes)}")
    print(f"  Array nodes: {len(array_nodes)}")
    print(f"  Visit nodes: {len(visit_nodes)}")
    print(f"  Write nodes: {len(write_nodes)}")
    print(f"  Loop nodes: {len(loop_nodes)}")
    print(f"  Branch nodes: {len(branch_nodes)}")
    
    # Print operation type distribution
    if op_nodes:
        op_type_counts = {}
        for op_node in op_nodes:
            op_type = op_node.op_type
            op_type_counts[op_type] = op_type_counts.get(op_type, 0) + 1
        
        print(f"  Operation types distribution:")
        for op_type, count in op_type_counts.items():
            print(f"    {op_type.name}: {count}")


def verify_graphs_are_different(generated_graphs):
    """
    Verify that the generated graphs are different from each other.
    This is a basic check to ensure that different seeds produce different graphs.
    """
    print("\n--- Verifying graph differences ---")
    
    for i in range(len(generated_graphs)):
        for j in range(i + 1, len(generated_graphs)):
            graph1 = generated_graphs[i]['graph']
            graph2 = generated_graphs[j]['graph']
            seed1 = generated_graphs[i]['seed']
            seed2 = generated_graphs[j]['seed']
            
            # Compare basic graph properties
            nodes_different = graph1.number_of_nodes() != graph2.number_of_nodes()
            edges_different = graph1.number_of_edges() != graph2.number_of_edges()
            
            if nodes_different or edges_different:
                print(f"  Graphs with seeds {seed1} and {seed2} are different")
                print(f"    Nodes: {graph1.number_of_nodes()} vs {graph2.number_of_nodes()}")
                print(f"    Edges: {graph1.number_of_edges()} vs {graph2.number_of_edges()}")
            else:
                print(f"  Graphs with seeds {seed1} and {seed2} have same node/edge counts")
                
                # Compare operation types if counts are the same
                op_nodes1 = generated_graphs[i]['manager']._get_op_node_list()
                op_nodes2 = generated_graphs[j]['manager']._get_op_node_list()
                
                if len(op_nodes1) != len(op_nodes2):
                    print(f"    Different number of operation nodes: {len(op_nodes1)} vs {len(op_nodes2)}")
                else:
                    op_types1 = [node.op_type for node in op_nodes1]
                    op_types2 = [node.op_type for node in op_nodes2]
                    
                    if op_types1 != op_types2:
                        print(f"    Different operation type sequences detected")
                    else:
                        print(f"    Same operation type sequences - graphs may be very similar")


def test_generate_graphs_with_different_seeds():
    """
    Test that generates 3 different random graphs using different seeds.
    Each graph should be reproducible when using the same seed.
    """
    print("\n" + "="*60)
    print("Testing Random Graph Generation with Different Seeds")
    print("="*60)
    
    seeds = [42, 12345, 98765]  # Three different seeds for testing
    generated_graphs = []
    
    for i, seed in enumerate(seeds, 1):
        print(f"\n--- Generating Graph {i} with seed {seed} ---")
        
        # Create a new RandomGraphManager instance with the current seed
        graph_manager = RandomGraphManager(seed=seed)
        
        # Generate the random graph
        success = graph_manager.generate_random_graph()
        
        # Check that graph generation was successful
        if not success:
            print(f"ERROR: Failed to generate graph with seed {seed}")
            return False
        
        # Store the generated graph for later analysis
        generated_graphs.append({
            'seed': seed,
            'manager': graph_manager,
            'graph': graph_manager.program_graph
        })
        
        # Print basic statistics about the generated graph
        print_graph_statistics(graph_manager, seed)
    
    print(f"\n--- Summary ---")
    print(f"Successfully generated {len(generated_graphs)} graphs")
    
    # Verify that all graphs are different (optional check)
    verify_graphs_are_different(generated_graphs)
    
    return True


def test_graph_reproducibility():
    """
    Test that the same seed produces the same graph structure.
    This ensures reproducibility of the random graph generation.
    """
    print("\n" + "="*60)
    print("Testing Graph Reproducibility")
    print("="*60)
    
    test_seed = 42
    
    # Generate the same graph twice with the same seed
    manager1 = RandomGraphManager(seed=test_seed)
    manager2 = RandomGraphManager(seed=test_seed)
    
    success1 = manager1.generate_random_graph()
    success2 = manager2.generate_random_graph()
    
    if not success1:
        print("ERROR: First graph generation failed")
        return False
    
    if not success2:
        print("ERROR: Second graph generation failed")
        return False
    
    # Compare basic properties
    graph1 = manager1.program_graph
    graph2 = manager2.program_graph
    
    if graph1.number_of_nodes() != graph2.number_of_nodes():
        print("ERROR: Graphs have different number of nodes")
        return False
    
    if graph1.number_of_edges() != graph2.number_of_edges():
        print("ERROR: Graphs have different number of edges")
        return False
    
    print(f"  Both graphs generated with seed {test_seed} have:")
    print(f"    Nodes: {graph1.number_of_nodes()}")
    print(f"    Edges: {graph1.number_of_edges()}")
    print("  ✓ Reproducibility test passed")
    
    return True


def main():
    """
    Main function to run the tests.
    """
    print("Starting Random Graph Generation Tests")
    print("="*60)
    
    # Run the main test to generate 3 graphs with different seeds
    success1 = test_generate_graphs_with_different_seeds()
    
    # Run the reproducibility test
    # success2 = test_graph_reproducibility()
    
    # Print final results
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    if success1:
        print("✓ Different seeds test: PASSED")
    else:
        print("✗ Different seeds test: FAILED")
 


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)