import random
from typing import List, Dict, Union, Optional
from node import OperationType


class RandomOpTypeGenerator:
    """
    A generator for randomly selecting OperationType values based on given distributions.
    
    This class allows for weighted random selection of operation types, which is useful
    for creating benchmarks with specific operation type distributions.
    Only considers: ADD, SUB, MUL, AND, OR, XOR, NOT, SHL, SHR, EQ, NEQ, LT, GT, LE, GE
    """
    
    def __init__(self, distribution: Union[Dict[OperationType, float], List[float]] = None, seed: Optional[int] = None):
        """
        Initialize the random operation type generator.
        
        Args:
            distribution: Either a dictionary mapping OperationType to weights,
                         or a list of weights in the same order as the supported operations.
                         If None, uses a default distribution favoring arithmetic operations.
            seed: Random seed for reproducible results.
        """
        # Only consider the specified operations
        self.operation_types = [
            OperationType.ADD,
            OperationType.SUB,
            OperationType.MUL,
            OperationType.AND,
            OperationType.OR,
            OperationType.XOR,
            OperationType.NOT,
            OperationType.SHL,
            OperationType.SHR,
            OperationType.EQ,
            OperationType.NEQ,
            OperationType.LT,
            OperationType.GT,
            OperationType.LE,
            OperationType.GE
        ]
        
        if distribution is None:
            # Default distribution favoring arithmetic operations, then logic, then comparison
            self.weights = [
                0.15,  # ADD - common arithmetic
                0.15,  # SUB - common arithmetic
                0.12,  # MUL - less common arithmetic
                0.08,  # AND - logic operation
                0.08,  # OR - logic operation
                0.06,  # XOR - less common logic
                0.04,  # NOT - unary logic
                0.04,  # SHL - shift operation
                0.04,  # SHR - shift operation
                0.06,  # EQ - common comparison
                0.06,  # NEQ - common comparison
                0.04,  # LT - comparison
                0.04,  # GT - comparison
                0.02,  # LE - less common comparison
                0.02   # GE - less common comparison
            ]
        elif isinstance(distribution, dict):
            # Convert dict to list of weights for supported operations only
            self.weights = [distribution.get(op_type, 0.0) for op_type in self.operation_types]
        elif isinstance(distribution, list):
            if len(distribution) != len(self.operation_types):
                raise ValueError(f"Distribution list length ({len(distribution)}) must match "
                               f"number of supported operation types ({len(self.operation_types)})")
            self.weights = distribution.copy()
        else:
            raise TypeError("Distribution must be a dict, list, or None")
        
        # Normalize weights to ensure they sum to 1
        total_weight = sum(self.weights)
        if total_weight == 0:
            raise ValueError("All weights cannot be zero")
        self.weights = [w / total_weight for w in self.weights]
        
        # Set random seed if provided
        if seed is not None:
            random.seed(seed)
    
    def generate(self) -> OperationType:
        """
        Generate a random OperationType based on the configured distribution.
        
        Returns:
            A randomly selected OperationType
        """
        return random.choices(self.operation_types, weights=self.weights)[0]
    
    def generate_multiple(self, count: int) -> List[OperationType]:
        """
        Generate multiple random OperationType values.
        
        Args:
            count: Number of operation types to generate
            
        Returns:
            List of randomly selected OperationType values
        """
        return random.choices(self.operation_types, weights=self.weights, k=count)
    
    def set_distribution(self, distribution: Union[Dict[OperationType, float], List[float]]):
        """
        Update the distribution weights.
        
        Args:
            distribution: New distribution as dict or list
        """
        if isinstance(distribution, dict):
            self.weights = [distribution.get(op_type, 0.0) for op_type in self.operation_types]
        elif isinstance(distribution, list):
            if len(distribution) != len(self.operation_types):
                raise ValueError(f"Distribution list length ({len(distribution)}) must match "
                               f"number of supported operation types ({len(self.operation_types)})")
            self.weights = distribution.copy()
        else:
            raise TypeError("Distribution must be a dict or list")
        
        # Normalize weights
        total_weight = sum(self.weights)
        if total_weight == 0:
            raise ValueError("All weights cannot be zero")
        self.weights = [w / total_weight for w in self.weights]
    
    def get_distribution(self) -> Dict[OperationType, float]:
        """
        Get the current distribution as a dictionary.
        
        Returns:
            Dictionary mapping OperationType to their weights
        """
        return dict(zip(self.operation_types, self.weights))
    
    def set_seed(self, seed: int):
        """
        Set the random seed for reproducible results.
        
        Args:
            seed: Random seed value
        """
        random.seed(seed)


# Predefined distributions for common use cases
class PredefinedDistributions:
    """
    Collection of predefined operation type distributions for common scenarios.
    Only includes supported operations: ADD, SUB, MUL, AND, OR, XOR, NOT, SHL, SHR, EQ, NEQ, LT, GT, LE, GE
    """
    
    @staticmethod
    def arithmetic_heavy() -> Dict[OperationType, float]:
        """Distribution favoring arithmetic operations."""
        return {
            OperationType.ADD: 0.35,
            OperationType.SUB: 0.35,
            OperationType.MUL: 0.20,
            OperationType.AND: 0.02,
            OperationType.OR: 0.02,
            OperationType.XOR: 0.02,
            OperationType.NOT: 0.01,
            OperationType.SHL: 0.01,
            OperationType.SHR: 0.01,
            OperationType.EQ: 0.003,
            OperationType.NEQ: 0.003,
            OperationType.LT: 0.002,
            OperationType.GT: 0.002,
            OperationType.LE: 0.001,
            OperationType.GE: 0.001
        }
    
    @staticmethod
    def logical_heavy() -> Dict[OperationType, float]:
        """Distribution favoring logical operations."""
        return {
            OperationType.ADD: 0.10,
            OperationType.SUB: 0.10,
            OperationType.MUL: 0.05,
            OperationType.AND: 0.25,
            OperationType.OR: 0.25,
            OperationType.XOR: 0.15,
            OperationType.NOT: 0.05,
            OperationType.SHL: 0.02,
            OperationType.SHR: 0.02,
            OperationType.EQ: 0.003,
            OperationType.NEQ: 0.003,
            OperationType.LT: 0.002,
            OperationType.GT: 0.002,
            OperationType.LE: 0.001,
            OperationType.GE: 0.001
        }
    
    @staticmethod
    def comparison_heavy() -> Dict[OperationType, float]:
        """Distribution favoring comparison operations."""
        return {
            OperationType.ADD: 0.15,
            OperationType.SUB: 0.15,
            OperationType.MUL: 0.05,
            OperationType.AND: 0.05,
            OperationType.OR: 0.05,
            OperationType.XOR: 0.03,
            OperationType.NOT: 0.02,
            OperationType.SHL: 0.02,
            OperationType.SHR: 0.02,
            OperationType.EQ: 0.16,
            OperationType.NEQ: 0.16,
            OperationType.LT: 0.06,
            OperationType.GT: 0.06,
            OperationType.LE: 0.02,
            OperationType.GE: 0.02
        }
    
    @staticmethod
    def uniform() -> Dict[OperationType, float]:
        """Uniform distribution across all supported operation types."""
        supported_ops = [
            OperationType.ADD, OperationType.SUB, OperationType.MUL,
            OperationType.AND, OperationType.OR, OperationType.XOR, OperationType.NOT,
            OperationType.SHL, OperationType.SHR,
            OperationType.EQ, OperationType.NEQ, OperationType.LT, OperationType.GT,
            OperationType.LE, OperationType.GE
        ]
        weight = 1.0 / len(supported_ops)
        return {op_type: weight for op_type in supported_ops}


# Example usage
if __name__ == "__main__":
    # Example 1: Using default distribution (favors arithmetic operations)
    generator = RandomOpTypeGenerator()
    print("Default distribution (arithmetic-heavy):")
    ops = generator.generate_multiple(10)
    print([op.value for op in ops])
    
    # Example 2: Using predefined logical-heavy distribution
    generator = RandomOpTypeGenerator(PredefinedDistributions.logical_heavy())
    print("\nLogical-heavy distribution:")
    ops = generator.generate_multiple(10)
    print([op.value for op in ops])
    
    # Example 3: Using custom distribution as list (15 values for 15 supported operations)
    custom_weights = [0.2, 0.2, 0.15, 0.1, 0.1, 0.08, 0.05, 0.04, 0.04, 0.02, 0.01, 0.005, 0.005, 0.0025, 0.0025]
    generator.set_distribution(custom_weights)
    print("\nCustom distribution:")
    ops = generator.generate_multiple(10)
    print([op.value for op in ops])
    
    # Example 4: Using uniform distribution
    generator = RandomOpTypeGenerator(PredefinedDistributions.uniform())
    print("\nUniform distribution:")
    ops = generator.generate_multiple(10)
    print([op.value for op in ops])
    
    # Example 5: Show current distribution
    print("\nCurrent distribution weights:")
    dist = generator.get_distribution()
    for op_type, weight in dist.items():
        print(f"{op_type.value}: {weight:.4f}")