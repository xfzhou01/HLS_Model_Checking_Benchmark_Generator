# HLS Model Checking Benchmark Generator

## Description

This project generates benchmarks for High-Level Synthesis (HLS) model checking by creating random computation graphs, compiling them to HDL using Vitis HLS, and producing miter circuits for equivalence checking. The tool generates pairs of functionally equivalent but structurally different C++ programs to test HLS optimization and verification tools.

## Features

- **Random Graph Generation**: Creates directed acyclic graphs representing computations with operations, arrays, loops, and branches
- **Pragma Insertion**: Automatically inserts different HLS optimization pragmas to create functionally equivalent but differently optimized designs
- **HLS Compilation**: Compiles C++ code to Verilog using Xilinx Vitis HLS
- **Miter Generation**: Creates miter circuits for equivalence checking between two HLS implementations
- **AIGER Output**: Converts miter circuits to AIGER format for model checking tools
- **Configurable Parameters**: Supports customization of seeds, output directories, clock periods, and more

## Requirements

### Python Dependencies
- Python 3.7+
- `networkx` - For graph data structures and algorithms
- `numpy` - For numerical operations
- `matplotlib` - For graph visualization (optional)

### External Tools
- **Xilinx Vitis HLS** - Required for C++ to HDL synthesis
  - Must be installed and `vitis_hls` command available in PATH
- **Yosys** - Open-source synthesis tool for Verilog processing
  - Used for flattening and AIGER conversion
- **clang-format** (optional) - For C++ code formatting

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd hls_model_checking_benchmark_generator
   ```

2. **Install Python dependencies:**
   ```bash
   pip install networkx numpy matplotlib
   ```

3. **Install external tools:**
   - Install Xilinx Vitis HLS and ensure `vitis_hls` is in your PATH
   - Install Yosys: `sudo apt-get install yosys` (Ubuntu/Debian) or build from source
   - Optional: Install clang-format: `sudo apt-get install clang-format`

## Usage

### Basic Usage

Generate HLS benchmarks with default settings:
```bash
python src/main.py
```

### Command Line Options

```bash
python src/main.py [OPTIONS]
```

**Options:**
- `--seed SEED` - Random seed for graph generation (default: 42)
- `--output-dir DIR` - Output directory for generated files (default: ./output)
- `--cpp-file FILE` - Name of C++ output file (default: benchmark.cpp)
- `--project-name NAME` - HLS project name (default: hls_benchmark)
- `--top-function NAME` - Top-level function name (default: top)
- `--clock-period NS` - Clock period in nanoseconds (default: 10)
- `--skip-compilation` - Skip Vitis HLS compilation step
- `--verbose, -v` - Enable verbose output

### Examples

1. **Generate benchmarks with a specific seed:**
   ```bash
   python src/main.py --seed 123 --verbose
   ```

2. **Generate only C++ files without compilation:**
   ```bash
   python src/main.py --skip-compilation --output-dir ./my_output
   ```

3. **Custom project settings:**
   ```bash
   python src/main.py --project-name my_project --top-function compute --clock-period 5
   ```

## Output Structure

The tool generates the following output structure:

```
output/
├── benchmark_1.cpp          # First C++ implementation
├── benchmark_2.cpp          # Second C++ implementation (with different pragmas)
├── compile_1/               # Vitis HLS compilation results for first implementation
│   ├── hls_script_1.tcl    # HLS synthesis script
│   ├── hls_compile_1.log   # Compilation log
│   └── hls_benchmark_1/    # HLS project directory
│       └── solution1/
│           ├── syn/verilog/ # Generated Verilog files
│           └── ...
├── compile_2/               # Vitis HLS compilation results for second implementation
│   └── ...
└── miter/                   # Miter generation results
    ├── merged_1.v          # Merged Verilog from first implementation
    ├── merged_2.v          # Merged Verilog from second implementation
    ├── miter.v             # Generated miter circuit
    └── miter.aig           # AIGER format output
```

## Workflow

1. **Graph Generation**: Creates a random computation graph with nodes representing operations, arrays, loops, and branches
2. **C++ Generation**: Converts the graph to two functionally equivalent C++ programs with different optimization pragmas
3. **HLS Compilation**: Compiles both C++ programs to Verilog using Vitis HLS
4. **Miter Creation**: Merges the Verilog files and creates a miter circuit for equivalence checking
5. **AIGER Export**: Converts the miter to AIGER format for use with model checking tools

## Architecture

The project consists of several key modules:

- `main.py` - Command-line interface and workflow orchestration
- `random_graph_manager.py` - Random computation graph generation
- `graph_manager.py` - Base graph management and C++ code generation
- `vitis_hls_compiler.py` - Vitis HLS compilation interface
- `miter_generator.py` - Miter circuit creation
- `yosys_compiler.py` - Yosys tool interface for Verilog processing
- `node.py` - Graph node definitions and types
- `verilog_processing.py` - Verilog file manipulation utilities

## Troubleshooting

### Common Issues

1. **Vitis HLS not found:**
   - Ensure Vitis HLS is installed and `vitis_hls` command is in your PATH
   - Check with: `which vitis_hls`

2. **Yosys compilation errors:**
   - Verify Yosys installation: `yosys --version`
   - Check that Verilog files are valid

3. **Python import errors:**
   - Ensure all required packages are installed
   - Verify Python path includes the src directory

### Debug Mode

Enable verbose output for detailed information:
```bash
python src/main.py --verbose
```