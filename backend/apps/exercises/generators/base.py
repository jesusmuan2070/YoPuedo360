"""
Base Exercise Generator
"""
from abc import ABC, abstractmethod


class ExerciseGeneratorBase(ABC):
    """
    Abstract base for all exercise generators.
    """
    
    @abstractmethod
    def generate(self, **kwargs):
        """
        Generate exercise(s).
        Returns: Exercise instance or list of exercises
        """
        pass
    
    @abstractmethod
    def generate_bulk(self, count, **kwargs):
        """
        Generate multiple exercises.
        """
        pass
