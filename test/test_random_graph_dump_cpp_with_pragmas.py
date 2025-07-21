#!/usr/bin/env python3
"""
Test script for random graph generation with C++ output.
This test generates different random graphs using different seeds and outputs
them as C++ code files for HLS model checking benchmarks.
"""

import sys
import os
import shutil

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


def validate_cpp_file(file_path):
    """
    Validate the generated C++ file by checking if it exists and has content.
    
    Args:
        file_path: Path to the C++ file to validate
    
    Returns:
        bool: True if file is valid, False otherwise
    """
    if not os.path.exists(file_path):
        print(f"ERROR: C++ file {file_path} was not created")
        return False
    
    # Check if file has content
    with open(file_path, 'r') as f:
        content = f.read().strip()
        if not content:
            print(f"ERROR: C++ file {file_path} is empty")
            return False
    
    print(f"  ✓ C++ file {file_path} created successfully")
    print(f"  File size: {len(content)} characters")
    
    # Check for basic C++ structure
    if '#include' in content and 'int main' in content:
        print(f"  ✓ C++ file contains basic structure (includes and main function)")
    else:
        print(f"  ⚠ C++ file may not contain standard structure")
    
    return True


def compare_file_contents(file_path_1, file_path_2):
    """
    Compare the contents of two files to check if they are identical.
    
    Args:
        file_path_1: Path to the first file
        file_path_2: Path to the second file
    
    Returns:
        bool: True if files have identical content, False otherwise
    """
    try:
        with open(file_path_1, 'r') as f1, open(file_path_2, 'r') as f2:
            content_1 = f1.read()
            content_2 = f2.read()
            return content_1 == content_2
    except FileNotFoundError as e:
        print(f"ERROR: File not found when comparing: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to compare files {file_path_1} and {file_path_2}: {e}")
        return False


def test_cpp_output_generation():
    """
    Test that generates random graphs and outputs them as C++ files.
    Each graph should be generated with different seeds and produce valid C++ code.
    """
    print("\n" + "="*60)
    print("Testing Random Graph Generation with C++ Output")
    print("="*60)
    
    seeds = [10]  # Only generate output_seed_42.cpp
    generated_files = []
    
    for i, seed in enumerate(seeds, 1):
        print(f"\n--- Generating Graph {i} with seed {seed} ---")
        
        # Create a new RandomGraphManager instance with the current seed
        graph_manager = RandomGraphManager(seed=seed)
        
        # Generate the random graph
        success = graph_manager.generate_random_graph()
        success_1 = graph_manager.generate_cmp_graphs()
        
        # Check that graph generation was successful
        if not success:
            print(f"ERROR: Failed to generate graph with seed {seed}")
            return False
        if not success_1:
            print(f"ERROR: Failed to generate cmp graphs with seed {seed}")
            return False
        
        # Print basic statistics about the generated graph
        print_graph_statistics(graph_manager, seed)
        
        # Generate C++ output file
        cpp_file_path = f"output_seed_{seed}.cpp"
        print(f"  Generating C++ output to {cpp_file_path}")
        
        try:
            graph_manager.dump_cpp_std(cpp_file_path)
            
            # Validate the generated C++ file
            if validate_cpp_file(cpp_file_path):
                generated_files.append({
                    'seed': seed,
                    'file_path': cpp_file_path,
                    'manager': graph_manager
                })
            else:
                print(f"ERROR: C++ file validation failed for seed {seed}")
                return False
                
        except Exception as e:
            print(f"ERROR: Failed to generate C++ output for seed {seed}: {e}")
            raise e
        

        cpp_file_path_1 = f"output_seed_{seed}_1.cpp"
        cpp_file_path_2 = f"output_seed_{seed}_2.cpp"
        try:
            graph_manager.dump_cpp_comparsion(
                file_path_1=cpp_file_path_1,
                file_path_2=cpp_file_path_2
            )

            # Check whether cpp_file_path_1 and cpp_file_path_2 have the same content
            if compare_file_contents(cpp_file_path_1, cpp_file_path_2):
                raise ValueError(f"Comparison files {cpp_file_path_1} and {cpp_file_path_2} have the same content")

            
            # Validate the generated C++ file
            if validate_cpp_file(cpp_file_path_1):
                generated_files.append({
                    'seed': seed,
                    'file_path': cpp_file_path_1,
                    'manager': graph_manager
                })
            else:
                print(f"ERROR: C++ file validation failed for seed {seed}")
                return False
            if validate_cpp_file(cpp_file_path_2):
                generated_files.append({
                    'seed': seed,
                    'file_path': cpp_file_path_2,
                    'manager': graph_manager
                })
            else:
                print(f"ERROR: C++ file validation failed for seed {seed}")
                return False
                
        except Exception as e:
            print(f"ERROR: Failed to generate C++ output for seed {seed}: {e}")
            raise e
    
    print(f"\n--- Summary ---")
    print(f"Successfully generated {len(generated_files)} C++ files:")
    for file_info in generated_files:
        print(f"  - {file_info['file_path']} (seed: {file_info['seed']})")
    
    return True





def cleanup_generated_files():
    """
    Clean up generated C++ files after testing.
    """
    print("\n--- Cleaning up generated files ---")
    
    files_to_remove = []
    for file in os.listdir('.'):
        if file.startswith('output_seed_') and file.endswith('.cpp'):
            files_to_remove.append(file)
    
    for file in files_to_remove:
        try:
            os.remove(file)
            print(f"  Removed {file}")
        except Exception as e:
            print(f"  Failed to remove {file}: {e}")


def main():
    """
    Main function to run the tests.
    """
    print("Starting Random Graph C++ Output Tests")
    print("="*60)
    
    # Change to the test directory to avoid cluttering the workspace
    original_dir = os.getcwd()
    test_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(test_dir)
    
    try:
        # Run the main test to generate C++ files
        success1 = test_cpp_output_generation()
        
        # Print final results
        print("\n" + "="*60)
        print("Test Results Summary")
        print("="*60)
        
        if success1:
            print("✓ C++ output generation test: PASSED")
        else:
            print("✗ C++ output generation test: FAILED")
        
        # Clean up generated files
        # cleanup_generated_files()
        
        # Return success code
        return 0 if success1 else 1
        
    finally:
        # Restore original directory
        os.chdir(original_dir)


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)