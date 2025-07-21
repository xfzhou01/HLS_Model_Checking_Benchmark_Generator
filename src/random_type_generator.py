from node import ResultDataType
from random_width_generator import RandomWidthGenerator, RandomLinearWidthGenerator
from enum import Enum
import random
from typing import Union, Tuple
from node import QuantizationMode, OverflowMode

class RandomApFixQuantGenerator:

    def __init__(self, quant_distribution = None):
        self.quant_type_list = [
            QuantizationMode.AP_RND,
            QuantizationMode.AP_RND_ZERO,
            QuantizationMode.AP_RND_MIN_INF,
            QuantizationMode.AP_RND_INF,
            QuantizationMode.AP_RND_CONV,
            QuantizationMode.AP_TRN,
            QuantizationMode.AP_TRN_ZERO
        ]

        if quant_distribution is None:
            self.quant_distribution = [1.0 / float(len(self.quant_type_list)) \
                                  for _ in range(len(self.quant_type_list))]
        else:
            self.quant_distribution = quant_distribution
        
    def generate(self):
        """
        Generate a random quantization mode based on the defined distribution.
        """
        return random.choices(self.quant_type_list, 
                              weights=self.quant_distribution)[0]
    
class RandomApFixOverflowGenerator:

    def __init__(self, overflow_distribution = None):
        self.overflow_type_list = [
            OverflowMode.AP_SAT,
            OverflowMode.AP_SAT_ZERO,
            OverflowMode.AP_SAT_SYM,
            OverflowMode.AP_WRAP,
            OverflowMode.AP_WRAP_SM
        ]

        if overflow_distribution is None:
            self.overflow_distribution = [1.0 / float(len(self.overflow_type_list)) \
                                  for _ in range(len(self.overflow_type_list))]
        else:
            self.overflow_distribution = overflow_distribution
        
    def generate(self):
        """
        Generate a random overflow mode based on the defined distribution.
        """
        return random.choices(self.overflow_type_list, 
                              weights=self.overflow_distribution)[0]


class RandomTypeGenerator:
    """
    A class to generate random types for nodes in a graph.
    """
    def __init__(self, result_type_distribution=None,
                 result_width_distribution=None,result_width_list=None):
        """
        Initialize the generator with a list of result types and their distribution.
        """
        result_type_list = [ResultDataType.AP_INT, ResultDataType.AP_FIXED, ResultDataType.AP_UINT]
        
        if result_type_distribution is None:
            result_type_distribution = [0.4, 0.4, 0.2]  # Default distribution

        self.result_width_list = result_width_list or [1, 2, 4, 8, 16, 32]
        self.result_width_distribution = result_width_distribution or [0.1, 0.2, 0.3, 0.2, 0.1, 0.1]

        self.result_type_list = result_type_list
        self.result_type_distribution = result_type_distribution

        if len(result_type_list) != len(result_type_distribution):
            raise ValueError("Result type list and distribution must have the same length.")
        
        # Normalize the distribution if sum is not 1
        total = sum(result_type_distribution)
        if total != 1:
            self.result_type_distribution = [x / total for x in result_type_distribution]


    def generate(self) -> Union[Tuple[ResultDataType, int], Tuple[ResultDataType, int, int, str, str]]:
        """
        Generate a random ResultDataType based on the defined distribution.
        """
        ap_type = random.choices(self.result_type_list, weights=self.result_type_distribution)[0].value
        ap_width = RandomWidthGenerator(self.result_width_list, self.result_width_distribution).generate()

        if ap_type == ResultDataType.AP_FIXED.value:
            # For AP_FIXED, we also need to generate the integer width
            r_linear_width_gen = RandomLinearWidthGenerator(min_width=1, max_width=ap_width)
            q_gen = RandomApFixQuantGenerator()
            o_gen = RandomApFixOverflowGenerator()
            quantization_mode = q_gen.generate()
            overflow_mode = o_gen.generate()

            result_int_width_ap_fixed = r_linear_width_gen.generate()
            return ap_type, ap_width, result_int_width_ap_fixed, quantization_mode, overflow_mode
        else:
            # For AP_INT and AP_UINT, we do not need the integer width
            return ap_type, ap_width