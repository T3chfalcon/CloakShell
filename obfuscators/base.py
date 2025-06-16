from abc import ABC, abstractmethod

class BaseObfuscator:
    """Base class for all obfuscation plugins."""
    
    def __init__(self, level='medium'):
        self.level = level
    
    @abstractmethod
    def apply(self, script_text: str) -> str:
        """
        Apply the obfuscation technique to the script.
        
        Args:
            script_text (str): The PowerShell script text to obfuscate
            
        Returns:
            str: The obfuscated script text
        """
        pass
    
    def _get_level_multiplier(self) -> int:
        """Get a multiplier based on the obfuscation level."""
        return {
            'low': 1,
            'medium': 2,
            'high': 3
        }.get(self.level, 2) 