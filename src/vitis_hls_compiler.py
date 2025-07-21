import shutil
import os
import glob
import subprocess


class VitisHLSCompiler:

    def __init__(self, working_dir = None, hls_script_path = None, log_file_path = None):
        self.vitis_hls_exists = shutil.which("vitis_hls") is not None
        
        if working_dir is None:
            self.working_dir = os.getcwd()
        else:
            if working_dir == "":
                raise ValueError("working_dir cannot be empty")
            self.working_dir = working_dir
            if not os.path.exists(self.working_dir):
                os.makedirs(self.working_dir)

        if hls_script_path is None:
            self.hls_script_path = os.path.join(self.working_dir, "hls_script.tcl")
        else:
            if hls_script_path == "":
                raise ValueError()
            self.hls_script_path = hls_script_path

        if log_file_path is None:
            self.log_file_path = os.path.join(self.working_dir, "hls_compile.log")
        else:
            if log_file_path == "":
                raise ValueError()
            self.log_file_path = log_file_path

    def _collect_generated_verilog(self, project_name="proj"):
        """
        Collect generated Verilog files from the HLS synthesis output.
        
        Args:
            project_name: Name of the HLS project
            
        Returns:
            list: List of paths to generated Verilog files
        """
        verilog_files = []
        
        # Common paths where Vitis HLS generates Verilog files
        synthesis_paths = [
            os.path.join(self.working_dir, project_name, "solution1", "syn", "verilog"),
            # os.path.join(self.working_dir, project_name, "solution1", "impl", "verilog"),
            # os.path.join(self.working_dir, project_name, "solution1", "syn", "vhdl"),
            # os.path.join(self.working_dir, project_name, "solution1", "impl", "vhdl")
        ]
        
        for path in synthesis_paths:
            if os.path.exists(path):
                # Find all Verilog files (.v, .sv) and VHDL files (.vhd, .vhdl)
                v_files = glob.glob(os.path.join(path, "*.v"))
                sv_files = glob.glob(os.path.join(path, "*.sv"))
                vhd_files = glob.glob(os.path.join(path, "*.vhd"))
                vhdl_files = glob.glob(os.path.join(path, "*.vhdl"))
                
                verilog_files.extend(v_files)
                # currently we only support v_files
                # verilog_files.extend(sv_files)
                # verilog_files.extend(vhd_files)
                # verilog_files.extend(vhdl_files)
        
        return verilog_files

    def _launch_hls_script(self):
        """
        Launch the HLS script using vitis_hls command.
        
        Raises:
            RuntimeError: If vitis_hls is not available or compilation fails
        """
        if not self.vitis_hls_exists:
            raise RuntimeError("vitis_hls command not found in PATH")
            
        # Change to working directory to ensure relative paths work correctly
        original_cwd = os.getcwd()
        try:
            os.chdir(self.working_dir)
            cmd_hls = f"vitis_hls -f {os.path.basename(self.hls_script_path)} > {os.path.basename(self.log_file_path)} 2>&1"
            ret = os.system(cmd_hls)
            if ret != 0:
                raise RuntimeError(f"vitis_hls command failed with exit code {ret}")
            else:
                print("[INFO] compile success from C to RTL")
        finally:
            os.chdir(original_cwd)

    def _generate_hls_script(self,
        project_name = "proj", top_name = "", clock_period = 0,
        cpp_file_list = []):
        """
        Generate HLS TCL script for synthesis.
        
        Args:
            project_name: Name of the HLS project
            top_name: Name of the top-level function
            clock_period: Clock period in nanoseconds
            cpp_file_list: List of C++ source files to include
            
        Raises:
            TypeError: If arguments have wrong types
            ValueError: If arguments have invalid values
            FileNotFoundError: If C++ files don't exist
        """
        if not isinstance(project_name,str):
            raise TypeError()
        if not isinstance(top_name,str):
            raise TypeError()
        if not isinstance(clock_period,int):
            raise TypeError()
        if not isinstance(cpp_file_list, list):
            raise TypeError()
        if len(cpp_file_list) == 0:
            raise ValueError("empty cpp file list")

        if project_name == "":
            raise ValueError("empty project name")
        if top_name == "":
            raise ValueError("empty top name")
        if clock_period <= 0:
            raise ValueError(f"illegal cp = {clock_period}")
        
        
        file_list_add_str = ""
        for cpp_file in cpp_file_list:
            if not os.path.exists(cpp_file):
                raise FileNotFoundError(f"cpp file not found: {cpp_file}")
            # Use relative path if file is in working directory, otherwise absolute
            if os.path.dirname(os.path.abspath(cpp_file)) == os.path.abspath(self.working_dir):
                file_path = os.path.basename(cpp_file)
            else:
                file_path = os.path.abspath(cpp_file)
            file_list_add_str += f"add_files {file_path}\n"
            

        script_content = f'''
open_project -reset {project_name}
set_top {top_name}
{file_list_add_str}
open_solution "solution1" -flow_target vivado
set_part {{xc7z020clg484-1}}
create_clock -period {clock_period} -name default
csynth_design
exit
        '''

        with open(self.hls_script_path, "w") as f:
            f.write(script_content)

    def compile(self, project_name="proj", top_name="", clock_period=10, cpp_file_list=[]):
        """
        Complete HLS compilation workflow: generate script, run synthesis, and collect results.
        
        Args:
            project_name: Name of the HLS project (default: "proj")
            top_name: Name of the top-level function
            clock_period: Clock period in nanoseconds (default: 10)
            cpp_file_list: List of C++ source files to compile
            
        Returns:
            dict: Compilation results containing:
                - success: Boolean indicating if compilation succeeded
                - verilog_files: List of generated HDL files
                - log_file: Path to compilation log
                - project_path: Path to generated project directory
                
        Raises:
            RuntimeError: If vitis_hls is not available
            ValueError: If required parameters are invalid
            FileNotFoundError: If source files don't exist
        """
        if not self.vitis_hls_exists:
            raise RuntimeError("vitis_hls is not available. Please install Vitis HLS and ensure it's in your PATH.")
        
        try:
            # Step 1: Generate HLS script
            print(f"[INFO] Generating HLS script for project '{project_name}'")
            self._generate_hls_script(project_name, top_name, clock_period, cpp_file_list)
            
            # Step 2: Launch HLS compilation
            print(f"[INFO] Starting HLS synthesis...")
            self._launch_hls_script()
            
            # Step 3: Collect generated files
            print(f"[INFO] Collecting generated HDL files...")
            verilog_files = self._collect_generated_verilog(project_name)
            
            project_path = os.path.join(self.working_dir, project_name)
            
            result = {
                "success": True,
                "verilog_files": verilog_files,
                "log_file": self.log_file_path,
                "project_path": project_path if os.path.exists(project_path) else None,
                "script_file": self.hls_script_path
            }
            
            print(f"[INFO] Compilation completed successfully. Generated {len(verilog_files)} HDL files.")
            return result
            
        except Exception as e:
            print(f"[ERROR] Compilation failed: {str(e)}")
            result = {
                "success": False,
                "error": str(e),
                "log_file": self.log_file_path if os.path.exists(self.log_file_path) else None,
                "script_file": self.hls_script_path if os.path.exists(self.hls_script_path) else None
            }
            return result

    def check_vitis_hls_availability(self):
        """
        Check if Vitis HLS is available in the system.
        
        Returns:
            bool: True if vitis_hls command is available, False otherwise
        """
        return self.vitis_hls_exists

    def get_synthesis_reports(self, project_name="proj"):
        """
        Get paths to synthesis reports generated by Vitis HLS.
        
        Args:
            project_name: Name of the HLS project
            
        Returns:
            dict: Dictionary containing paths to various report files
        """
        reports = {}
        project_path = os.path.join(self.working_dir, project_name)
        
        if os.path.exists(project_path):
            solution_path = os.path.join(project_path, "solution1")
            
            # Common report files
            report_files = {
                "synthesis_report": os.path.join(solution_path, "syn", "report", f"{project_name}_csynth.rpt"),
                "timing_report": os.path.join(solution_path, "syn", "report", f"{project_name}_timing_report.rpt"),
                "utilization_report": os.path.join(solution_path, "syn", "report", f"{project_name}_utilization_report.rpt")
            }
            
            for report_name, report_path in report_files.items():
                if os.path.exists(report_path):
                    reports[report_name] = report_path
        
        return reports

    def clean_project(self, project_name="proj"):
        """
        Clean up generated project files.
        
        Args:
            project_name: Name of the HLS project to clean
            
        Returns:
            bool: True if cleanup was successful, False otherwise
        """
        try:
            project_path = os.path.join(self.working_dir, project_name)
            if os.path.exists(project_path):
                shutil.rmtree(project_path)
                print(f"[INFO] Cleaned project directory: {project_path}")
            
            # Also clean script and log files if they exist
            files_to_clean = [self.hls_script_path, self.log_file_path]
            for file_path in files_to_clean:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"[INFO] Removed file: {file_path}")
            
            return True
        except Exception as e:
            print(f"[ERROR] Failed to clean project: {str(e)}")
            return False

