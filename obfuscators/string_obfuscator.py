import re
import random
import string
from .base import BaseObfuscator

class StringObfuscator(BaseObfuscator):
    """Obfuscates string literals in PowerShell scripts."""
    
    def __init__(self, level='medium'):
        super().__init__(level)
        self.string_pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')
        self.function_pattern = re.compile(r'function\s+[\w-]+\s*{')
        self.param_pattern = re.compile(r'param\s*\(')
        self.format_pattern = re.compile(r'\[string\]::Format\s*\(')
        self.system_cmd_pattern = re.compile(r'(Get-Process|Get-Service|Get-Item|Set-Item|Remove-Item|Copy-Item|Move-Item|Out-File|Get-Content|Set-Content|Add-Content)')
        self.file_path_pattern = re.compile(r'[A-Za-z]:\\|\\\\|/')
        self.hash_table_pattern = re.compile(r'@\s*{')
        self.hash_table_key_pattern = re.compile(r'"([^"]+)"\s*=\s*')
        self.wmi_pattern = re.compile(r'(Get-WmiObject|Get-CimInstance)\s+(\w+)')
        self.env_pattern = re.compile(r'\$env:')
        self.output_pattern = re.compile(r'(Write-Host|Write-Output|Write-Error|Write-Warning)')
        self.property_access_pattern = re.compile(r'\.\s*(\w+)\s*$')
        self.date_conversion_pattern = re.compile(r'\[Management\.ManagementDateTimeConverter\]::ToDateTime')
        self.math_pattern = re.compile(r'\[math\]::')
        self.wmi_property_pattern = re.compile(r'\$\(([^)]+)\)')
        self.network_pattern = re.compile(r'(New-Object\s+System\.Net\.Sockets\.TcpClient|BeginConnect|EndConnect|Connect|ConnectAsync|WaitOne|Disconnect)')
        self.file_content_pattern = re.compile(r'Out-File|Get-Content|Set-Content|Add-Content')
        self.method_call_pattern = re.compile(r'\.\s*(\w+)\s*\(')
        
    def _should_obfuscate(self, match, script_text, pos):
        """Determine if a string should be obfuscated based on its context."""
        # Get the string and its position
        string_value = match.group(1)
        start_pos = match.start()
        
        # Get the line containing this string
        line_start = script_text.rfind('\n', 0, start_pos) + 1
        line_end = script_text.find('\n', start_pos)
        if line_end == -1:
            line_end = len(script_text)
        line = script_text[line_start:line_end]
        
        # For low level, only obfuscate non-critical strings
        if self.level == 'low':
            # Don't obfuscate any strings in low level
            return False
            
        # For medium and high levels, apply more aggressive obfuscation
        if self.level in ['medium', 'high']:
            # Don't obfuscate strings in function definitions
            if self.function_pattern.search(line):
                return False
                
            # Don't obfuscate strings in parameter blocks
            if self.param_pattern.search(line):
                return False
                
            # Don't obfuscate strings that are part of file paths
            if self.file_path_pattern.search(line):
                return False
                
            # Don't obfuscate strings in WMI calls
            if self.wmi_pattern.search(line):
                return False
                
            # Don't obfuscate strings in environment variable access
            if self.env_pattern.search(line):
                return False
                
            # Don't obfuscate strings in system commands
            if self.system_cmd_pattern.search(line):
                return False
                
            # Don't obfuscate strings in output commands
            if self.output_pattern.search(line):
                return False
                
            # Don't obfuscate strings that are part of type definitions
            if '[' in line and ']' in line:
                return False
                
            # Don't obfuscate strings that are part of variable assignments with type constraints
            if '[' in line and ']' in line and '=' in line:
                return False
                
            # Don't obfuscate strings that are part of function calls with type parameters
            if '(' in line and ')' in line and '[' in line and ']' in line:
                return False
                
            # Don't obfuscate strings in string.Format calls
            if self.format_pattern.search(line):
                return False
                
            # Don't obfuscate strings that contain PowerShell variables
            if '$' in string_value:
                return False
                
            # Don't obfuscate strings that contain PowerShell expressions
            if '$(' in string_value:
                return False
                
            # Don't obfuscate strings that are part of Out-File or Get-Content
            if 'Out-File' in line or 'Get-Content' in line:
                return False
                
            # Don't obfuscate strings in hash table declarations
            if self.hash_table_pattern.search(line):
                return False
                
            # Don't obfuscate strings that are hash table keys
            if self.hash_table_key_pattern.search(line):
                return False
                
            # Don't obfuscate strings that are hash table values
            if '=' in line and '}' in line:
                return False
                
            # Don't obfuscate strings that are property access
            if self.property_access_pattern.search(line):
                return False
                
            # Don't obfuscate strings in date conversions
            if self.date_conversion_pattern.search(line):
                return False
                
            # Don't obfuscate strings in math operations
            if self.math_pattern.search(line):
                return False
                
            # Don't obfuscate strings in WMI property access
            if self.wmi_property_pattern.search(line):
                return False
                
            # Don't obfuscate strings in network operations
            if self.network_pattern.search(line):
                return False
                
            # Don't obfuscate strings in file content operations
            if self.file_content_pattern.search(line):
                return False
                
            # Don't obfuscate strings in method calls
            if self.method_call_pattern.search(line):
                return False
                
            # Don't obfuscate strings that are part of network addresses
            if any(addr in string_value for addr in ['.com', '.org', '.net', '.io', '.co', '.gov', '.edu']):
                return False
                
            # Don't obfuscate strings that are port numbers
            if string_value.isdigit() and 0 <= int(string_value) <= 65535:
                return False
                
            # For high level, obfuscate more aggressively
            if self.level == 'high':
                # Add more aggressive obfuscation rules here
                pass
                
        return True

    def _split_string(self, string_value):
        """Split a string into random parts for obfuscation."""
        if len(string_value) <= 3:
            return [string_value]
            
        parts = []
        remaining = string_value
        
        while remaining:
            if len(remaining) <= 3:
                parts.append(remaining)
                break
                
            # Randomly choose split point
            split_point = random.randint(1, min(3, len(remaining) - 1))
            parts.append(remaining[:split_point])
            remaining = remaining[split_point:]
            
        return parts

    def _generate_concatenation(self, parts):
        """Generate a concatenation expression for the string parts."""
        if len(parts) == 1:
            return f'"{parts[0]}"'
            
        # For high level, use more complex concatenation
        if self.level == 'high':
            # Use string concatenation with random variables
            var_name = ''.join(random.choices(string.ascii_lowercase, k=8))
            parts_str = ' + '.join(f'"{p}"' for p in parts)
            return f'${{{var_name} = {parts_str}}}'
        else:
            # For medium level, use simple concatenation
            return ' + '.join(f'"{part}"' for part in parts)

    def apply(self, script_text):
        """Apply string obfuscation to the script."""
        if self.level == 'low':
            return script_text
            
        def replace_string(match):
            string_value = match.group(1)
            
            # Skip if we shouldn't obfuscate this string
            if not self._should_obfuscate(match, script_text, match.start()):
                return f'"{string_value}"'
                
            # Split the string and generate concatenation
            parts = self._split_string(string_value)
            return self._generate_concatenation(parts)
            
        # Apply the obfuscation
        return self.string_pattern.sub(replace_string, script_text) 