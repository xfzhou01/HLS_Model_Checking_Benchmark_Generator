import os
import subprocess

class YosysCompiler:

    def __init__(self):
        self.yosys_script_path = ""
        self.aiger_file_path = ""
        self.verilog_output_file_path = ""

    def _generate_script_content_flatten(self,
        working_dir:str = "",
        verilog_file_path:str = "",
        top_name:str = "",
        flattened_file_path:str= ""):
        if not os.path.isdir(working_dir):
            raise FileNotFoundError()
        if not os.path.exists(verilog_file_path):
            raise FileNotFoundError()
        if top_name == "":
            raise ValueError()
        if flattened_file_path == "":
            raise ValueError()
        
        yosys_script = [
            f"read -sv {verilog_file_path}",
            f"prep -top {top_name}",
            "flatten",
            f"write_verilog -noattr -noparallelcase -simple-lhs {flattened_file_path}"
        ]

        yosys_script_content = "\n".join(yosys_script)
        
        self.yosys_script_path = os.path.join(working_dir, "flatten_verilog.ys")
        with open(self.yosys_script_path, "w") as f:
            f.write(yosys_script_content)

    def _generate_script_content_to_aiger(self, 
        working_dir:str = "",
        verilog_file_path:str = "",
        top_name:str = "",
        is_ascii:bool = True,
        has_symbol:bool = True,
        aiger_file_path = ""):
        if not os.path.isdir(working_dir):
            raise FileNotFoundError()
        if not os.path.exists(verilog_file_path):
            raise FileNotFoundError()
        if top_name == "":
            raise ValueError()
        
        if is_ascii:
            if not self.aiger_file_path.endswith(".aag"):
                raise ValueError(f"ascii aiger should ends with .aag"+\
                    f" but got {self.aiger_file_path}")
        else:
            if not self.aiger_file_path.endswith(".aig"):
                raise ValueError(f"binary aiger should ends with .aig"+\
                    f" but got {self.aiger_file_path}")
        
        write_aiger_ascii_option = " -ascii " if is_ascii else ""
        symbol_option = " -symbols " if has_symbol else ""


        yosys_script = [
            f"read -sv {verilog_file_path}",
            f"prep -top {top_name}",
            "flatten",
            "memory -nordff",
            "setundef -undriven -init -expose",
            # f"sim -clock ap_clk -reset _setup -rstlen 1 -n 1 -w {top_name}",
            # f"sim -clock ap_clk -n 1 -w {top_name}",
            # "delete -output",
            "techmap",
            "abc -fast -g AND",
            f"write_aiger -zinit {symbol_option} {write_aiger_ascii_option} {aiger_file_path}"
        ]

        yosys_script_content = "\n".join(yosys_script)
        
        self.yosys_script_path = os.path.join(working_dir, "miter_to_aiger.ys")
        with open(self.yosys_script_path, "w") as f:
            f.write(yosys_script_content)

    def _generate_script_content_to_aiger_liyou(self, 
        working_dir:str = "",
        verilog_file_path:str = "",
        top_name:str = "",
        is_ascii:bool = True,
        has_symbol:bool = True,
        aiger_file_path = ""):
        if not os.path.isdir(working_dir):
            raise FileNotFoundError()
        if not os.path.exists(verilog_file_path):
            raise FileNotFoundError()
        if top_name == "":
            raise ValueError()
        
        if is_ascii:
            if not self.aiger_file_path.endswith(".aag"):
                raise ValueError(f"ascii aiger should ends with .aag"+\
                    f" but got {self.aiger_file_path}")
        else:
            if not self.aiger_file_path.endswith(".aig"):
                raise ValueError(f"binary aiger should ends with .aig"+\
                    f" but got {self.aiger_file_path}")
        
        write_aiger_ascii_option = " -ascii " if is_ascii else ""
        symbol_option = " -symbols " if has_symbol else ""


        yosys_script = [
            f"read_verilog {verilog_file_path}",
            f"synth -top {top_name}",
            "flatten",
            "memory -nordff",
            "aigmap",
            "abc -fast -g AND",
            f"write_aiger -zinit {symbol_option} {write_aiger_ascii_option} {aiger_file_path}"
        ]

        yosys_script_content = "\n".join(yosys_script)
        
        self.yosys_script_path = os.path.join(working_dir, "miter_to_aiger.ys")
        with open(self.yosys_script_path, "w") as f:
            f.write(yosys_script_content)

    def _execute_compile(self, yosys_path = ""):
        if self.yosys_script_path == "":
            raise ValueError("yosys script path is empty")
        if not os.path.exists(self.yosys_script_path):
            raise FileNotFoundError()
        print(f"[INFO] run yosys which script {self.yosys_script_path}")
        yosys_call = "yosys"
        if yosys_path != "":
            yosys_call = yosys_path
        try:
            result = subprocess.run(
            [yosys_call, "-S", self.yosys_script_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )
        except subprocess.CalledProcessError as e: 
            raise RuntimeError(f"Yosys compilation failed:\n{e.stderr}") from e
        
        # check output aiger exists
        # if not os.path.exists(self.aiger_file_path):
        #     raise FileNotFoundError()
        print("[INFO] compile success, generated")

    def execute_flatten(self, verilog_file_path:str, 
                working_dir:str,
                verilog_output_file_path:str,
                top_name:str = "top"):
        self.verilog_output_file_path = verilog_output_file_path
        self._generate_script_content_flatten(
            working_dir=working_dir,
            top_name=top_name,
            verilog_file_path=verilog_file_path,
            flattened_file_path=verilog_output_file_path
        )
        print(f"[INFO] generated script at {self.yosys_script_path}")
        self._execute_compile(yosys_path="/home/x/xiaofeng-zhou/oss_cad/oss_cad_2025/oss-cad-suite/bin/yosys")
        
    def execute(self, verilog_file_path:str, 
                working_dir:str,
                aiger_file_path:str,
                top_name:str = "top"):
        self.aiger_file_path = aiger_file_path
        self._generate_script_content_to_aiger(
            verilog_file_path=verilog_file_path,
            working_dir=working_dir,
            top_name=top_name,
            is_ascii=False, has_symbol=False,
            aiger_file_path=aiger_file_path
        )
        print(f"[INFO] generated script at {self.yosys_script_path}")
        self._execute_compile()

    def execute_liyou(self, verilog_file_path:str, 
                working_dir:str,
                aiger_file_path:str,
                top_name:str = "top"):
        self.aiger_file_path = aiger_file_path
        self._generate_script_content_to_aiger_liyou(
            verilog_file_path=verilog_file_path,
            working_dir=working_dir,
            top_name=top_name,
            is_ascii=False, has_symbol=False,
            aiger_file_path=aiger_file_path
        )
        print(f"[INFO] generated script at {self.yosys_script_path}")
        self._execute_compile()
        
        
    
    