import os
from verilog_post_processor import VerilogPostProcessor
from yosys_compiler import YosysCompiler
class KairosPreprocessor:

    def __init__(self, verilog_file_path_before_preprocess:str,
                 verilog_file_path_after_preprocess:str,
                 working_dir:str,
                 top_name:str):
        if not isinstance(verilog_file_path_before_preprocess, str):
            raise TypeError()
        if not isinstance(verilog_file_path_after_preprocess, str):
            raise TypeError()
        if verilog_file_path_after_preprocess == "":
            raise ValueError()
        if not isinstance(top_name,str):
            raise TypeError()
        if not os.path.isdir(working_dir):
            raise FileNotFoundError()
        if working_dir == "":
            raise ValueError()
        if not os.path.exists(verilog_file_path_before_preprocess):
            raise FileNotFoundError()
        
        self.verilog_file_path_before = verilog_file_path_before_preprocess
        self.verilog_file_path_after = verilog_file_path_after_preprocess

        verilog_file_path_before_base = os.path.basename(
            self.verilog_file_path_before
        ).split(".")[0]
        self.working_dir = working_dir
        self.verilog_file_path_mid = os.path.join(self.working_dir, 
            f"{verilog_file_path_before_base}_flatten.v")
        
        self.top_name = top_name

        self.yosys_compiler_instance = YosysCompiler()
        self.vpp_instance = None

    def process(self):
        self.yosys_compiler_instance.execute_flatten(
            verilog_file_path=self.verilog_file_path_before,
            working_dir=self.working_dir,
            verilog_output_file_path=self.verilog_file_path_mid,
            top_name=self.top_name
        )
        self.vpp_instance = VerilogPostProcessor(
            flattened_verilog_file_path=self.verilog_file_path_mid,
            processed_verilog_file_path=self.verilog_file_path_after
        )
        self.vpp_instance.process()