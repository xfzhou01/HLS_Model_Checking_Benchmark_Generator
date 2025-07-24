import os
from verilog_processing import kairos_preprocess
from kairos_pre_processor import KairosPreprocessor
import re
class MiterGenerator:
    def __init__(self, verilog_file_path_list_1:list[str],
                 verilog_file_path_list_2:list[str],
                 merged_verilog_folder_path:str,
                 top_name:str):
        if not isinstance(verilog_file_path_list_1, list):
            raise TypeError()
        if not isinstance(verilog_file_path_list_2, list):
            raise TypeError()
        for verilog_file_path in verilog_file_path_list_1:
            if not isinstance(verilog_file_path, str):
                raise TypeError()
            if not os.path.exists(verilog_file_path):
                raise FileNotFoundError()
        for verilog_file_path in verilog_file_path_list_2:
            if not isinstance(verilog_file_path, str):
                raise TypeError()
            if not os.path.exists(verilog_file_path):
                raise FileNotFoundError()
        if not os.path.isdir(merged_verilog_folder_path):
            raise FileNotFoundError()
        if not isinstance(top_name, str):
            raise TypeError()
        if top_name == "":
            raise ValueError()
        
        self.verilog_file_path_list_1 = verilog_file_path_list_1
        self.verilog_file_path_list_2 = verilog_file_path_list_2

        self.merged_verilog_file_path_1 = os.path.join(merged_verilog_folder_path,"merged_1.v")
        self.merged_verilog_file_path_2 = os.path.join(merged_verilog_folder_path,"merged_2.v")
        self.merged_verilog_file_path_1_proc = os.path.join(merged_verilog_folder_path,"merged_1_proc.v")
        self.merged_verilog_file_path_2_proc = os.path.join(merged_verilog_folder_path,"merged_2_proc.v")
        self.miter_verilog_file_path = os.path.join(merged_verilog_folder_path, "miter.v")
        self.working_dir = merged_verilog_folder_path
        self.top_name = top_name
        self.kpp1 = None
        self.kpp2 = None

    def _merge_verilog(self):
        print("[INFO] start merge verilog")
        with open(self.merged_verilog_file_path_1, 'w') as outfile1:
            for fname in self.verilog_file_path_list_1:
                with open(fname) as infile:
                    outfile1.write(infile.read())
                    outfile1.write('\n')

        with open(self.merged_verilog_file_path_2, 'w') as outfile2:
            for fname in self.verilog_file_path_list_2:
                with open(fname) as infile:
                    outfile2.write(infile.read())
                    outfile2.write('\n')
        print("[INFO] finisihed merge verilog")

    def _generate_miter(self, insert_assertions=False):
        print("[INFO] start generate miter")
        self._merge_verilog()

        self.kpp1 = KairosPreprocessor(
            working_dir=self.working_dir,
            top_name=self.top_name,
            verilog_file_path_before_preprocess=self.merged_verilog_file_path_1,
            verilog_file_path_after_preprocess=self.merged_verilog_file_path_1_proc
        )
        self.kpp1.process()
        self.kpp2 = KairosPreprocessor(
            working_dir=self.working_dir,
            top_name=self.top_name,
            verilog_file_path_before_preprocess=self.merged_verilog_file_path_2,
            verilog_file_path_after_preprocess=self.merged_verilog_file_path_2_proc
        )
        self.kpp2.process()

        if not os.path.exists(self.merged_verilog_file_path_1):
            raise FileNotFoundError()
        if not os.path.exists(self.merged_verilog_file_path_2):
            raise FileNotFoundError()
        try:
            kairos_top = kairos_preprocess(
                src_file_1=self.merged_verilog_file_path_1_proc,
                src_file_2=self.merged_verilog_file_path_2_proc,
                dst_file=self.miter_verilog_file_path,
                fast_slow_mode=True
            )
        except Exception as e:
            print(f"[ERROR] src_file_1 = {self.merged_verilog_file_path_1_proc}")
            print(f"[ERROR] src_file_2 = {self.merged_verilog_file_path_2_proc}")
            raise e
        if insert_assertions:
            self._insert_assertion(kairos_top=kairos_top)
        return kairos_top
    
    def _insert_assertion(self, kairos_top):
        print("[INFO] insert assertion to unsafe signal")
        if not os.path.exists(self.miter_verilog_file_path):
            raise FileNotFoundError()
        miter_file = open(self.miter_verilog_file_path)
        miter_file_l = miter_file.readlines()
        new_miter_file_l = []
        pattern = f"module\s+{kairos_top}"
        entering_top = False
        for ml in miter_file_l:
            ml = ml.strip()
            if re.match(pattern, ml):
                entering_top = True
            if entering_top and ml == "endmodule":
                new_miter_file_l.append(
                    "assert property (@(posedge ap_clk) unsafe_signal);"
                )
            new_miter_file_l.append(ml)
        new_miter_file_s = "\n".join(new_miter_file_l)
        with open(self.miter_verilog_file_path, 'w') as f:
            f.write(new_miter_file_s)
        print("[INFO] finish insert assertion to unsafe signal")


    def generate_miter(self, insert_assertions=False):
        return self._generate_miter(insert_assertions=insert_assertions)