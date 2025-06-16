import re
import random
import string
from .base import BaseObfuscator

class VariableRenamer(BaseObfuscator):
    """Renames variables in PowerShell scripts."""
    
    def __init__(self, level='medium'):
        super().__init__(level)
        # List of variable names to protect (do not rename)
        self.protected_vars = set([
            # Network
            'targetHost', 'port', 'timeout', 'tcpClient', 'connection', 'wait', 'hostname', 'connectionResult',
            # File
            'tempFile', 'content',
            # System info
            'systemInfo', 'info', 'key', 'Detailed', 'result',
            # Array/Hash
            'ports', 'services',
            # PowerShell special
            '_', '?', 'true', 'false', 'null', 'args', 'env',
            # Common
            'i', 'j', 'k', 'n', 'count', 'index',
        ])
        self.var_pattern = re.compile(r'\$(\w+)')
        self.hash_key_pattern = re.compile(r'"([^"]+)"\s*=')
        self.function_pattern = re.compile(r'function\s+[\w-]+\s*{')
        self.param_pattern = re.compile(r'param\s*\(')
        self.file_path_pattern = re.compile(r'[A-Za-z]:\\|\\\\|/')
        self.hash_table_pattern = re.compile(r'@\s*{')
        self.hash_table_key_pattern = re.compile(r'"([^"]+)"\s*=\s*')
        self.network_pattern = re.compile(r'(Test-NetworkConnection|New-Object\s+System\.Net\.Sockets\.TcpClient)')
        self.assignment_pattern = re.compile(r'\$([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*')
        
    def _should_rename(self, var_name, line):
        # Never rename protected variables
        if var_name in self.protected_vars:
            return False
        # Never rename variables used as hash keys
        if self.hash_key_pattern.search(line):
            return False
        # Never rename variables in param blocks
        if 'param(' in line or 'param (' in line:
            return False
        # Never rename variables in function definitions
        if 'function' in line:
            return False
        # Never rename variables in foreach/for loops
        if 'foreach' in line or 'for(' in line or 'for (' in line:
            return False
        # Never rename variables in file/network/system commands
        if any(cmd in line for cmd in [
            'New-Object System.Net.Sockets.TcpClient', 'BeginConnect', 'ConnectAsync', 'WaitOne',
            'Out-File', 'Get-Content', 'Remove-Item', 'Get-WmiObject', 'Get-Process', 'Get-Service',
            'Get-PSDrive', 'Write-Host', 'Write-Output', 'Write-Error', 'Write-Warning',
            'System.IO.Path', 'Start-Sleep', 'Add', 'Count', 'env:',
        ]):
            return False
        return True
        
    def _generate_name(self, length=8):
        return ''.join(random.choices(string.ascii_letters, k=length))
        
    def apply(self, script_text):
        """Apply variable renaming to the script."""
        if self.level == 'low':
            return script_text
            
        # Track variable mappings
        var_map = {}
        
        def replace_var(match):
            var_name = match.group(1)
            
            # Skip if we shouldn't rename this variable
            if not self._should_rename(var_name, match.string):
                return match.group(0)
                
            # Use existing mapping or create new one
            if var_name not in var_map:
                var_map[var_name] = self._generate_name()
                
            return f'${var_map[var_name]}'
            
        # Apply the renaming
        return self.var_pattern.sub(replace_var, script_text) 