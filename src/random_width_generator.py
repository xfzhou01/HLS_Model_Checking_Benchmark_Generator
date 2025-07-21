import random
class RandomWidthGenerator:
    """
    A class to generate random widths for nodes in a graph.
    """
    def __init__(self, width_list = [1,2,4,8,16,32],
                 width_distribution = [0.1, 0.2, 0.3, 0.2, 0.1, 0.1]):
        """
        Initialize the generator 
        """
        self.width_list = width_list
        self.width_distribution = width_distribution

        if len(width_list) != len(width_distribution):
            raise ValueError("Width list and distribution must have the same length.")
        # normalize the distribution if sum is not 1
        total = sum(width_distribution)
        if total != 1:
            self.width_distribution = [x / total for x in width_distribution]

    def generate(self) -> int:
        """
        Generate a random width based on the defined distribution.
        """
        
        return random.choices(self.width_list, weights=self.width_distribution)[0]
    
class RandomLinearWidthGenerator:
    """
    A class to generate random linear widths for nodes in a graph.
    """
    def __init__(self, min_width=1, max_width=32):
        """
        Initialize the generator with a minimum and maximum width.
        """
        self.min_width = min_width
        self.max_width = max_width

    def generate(self) -> int:
        """
        Generate a random width within the specified range.
        """
        return random.randint(self.min_width, self.max_width)