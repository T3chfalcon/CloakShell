#!/usr/bin/env python3
import argparse
import os
import sys
import re
from colorama import init, Fore, Style
from obfuscators.variable_renamer import VariableRenamer
from obfuscators.string_obfuscator import StringObfuscator
from encoders.base64_encoder import Base64Encoder

# Initialize colorama
init()

class CloakShell:
    def __init__(self):
        self.parser = self._setup_parser()
        
    def _setup_parser(self):
        parser = argparse.ArgumentParser(
            description='CloakShell - Advanced PowerShell Obfuscator and Evasive Payload Generator',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        parser.add_argument('--input', '-i', required=True,
                          help='Input PowerShell script to obfuscate')
        parser.add_argument('--output', '-o', required=True,
                          help='Output file path for obfuscated script')
        parser.add_argument('--obfuscation-level', '-l', 
                          choices=['low', 'medium', 'high'],
                          default='medium',
                          help='Level of obfuscation to apply')
        parser.add_argument('--format', '-f',
                          choices=['ps1', 'ps1-oneliner', 'csharp-exe'],
                          default='ps1',
                          help='Output format')
        parser.add_argument('--encoding', '-e',
                          nargs='+',
                          choices=['base64', 'xor', 'aes'],
                          default=['base64'],
                          help='Encoding methods to apply')
        parser.add_argument('--junk-code', '-j',
                          action='store_true',
                          help='Inject junk code and NOPs')
        parser.add_argument('--anti-analysis', '-a',
                          action='store_true',
                          help='Add anti-analysis checks')
        
        return parser

    def validate_input(self, args):
        if not os.path.exists(args.input):
            print(f"{Fore.RED}Error: Input file '{args.input}' does not exist{Style.RESET_ALL}")
            sys.exit(1)
            
        if not args.input.endswith('.ps1'):
            print(f"{Fore.YELLOW}Warning: Input file does not have .ps1 extension{Style.RESET_ALL}")

    def _read_script(self, input_file):
        """Read the input PowerShell script."""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"{Fore.RED}Error reading input file: {str(e)}{Style.RESET_ALL}")
            sys.exit(1)

    def _write_script(self, output_file, content):
        """Write the obfuscated script to file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"{Fore.RED}Error writing output file: {str(e)}{Style.RESET_ALL}")
            sys.exit(1)

    def _split_script(self, script_text):
        """Split script into sections for obfuscation."""
        sections = []
        current_section = []
        in_function = False
        brace_count = 0
        
        for line in script_text.split('\n'):
            # Check for function start
            if line.strip().startswith('function '):
                if current_section:
                    sections.append(('\n'.join(current_section), in_function))
                current_section = [line]
                in_function = True
                brace_count = 0
            # Count braces to properly handle nested blocks
            elif in_function:
                brace_count += line.count('{')
                brace_count -= line.count('}')
                current_section.append(line)
                # Only end function when we've matched all braces
                if brace_count == 0 and line.strip() == '}':
                    sections.append(('\n'.join(current_section), in_function))
                    current_section = []
                    in_function = False
            else:
                current_section.append(line)
        
        if current_section:
            sections.append(('\n'.join(current_section), in_function))
            
        return sections

    def _apply_obfuscation(self, script_text, args):
        """Apply obfuscation techniques to the script."""
        print(f"{Fore.CYAN}Applying obfuscation techniques...{Style.RESET_ALL}")
        
        # Initialize obfuscators
        obfuscators = [
            VariableRenamer(level=args.obfuscation_level),
            StringObfuscator(level=args.obfuscation_level)
        ]
        
        # Split script into sections
        sections = self._split_script(script_text)
        obfuscated_sections = []
        
        # Process each section
        for section, is_function in sections:
            if is_function:
                # For functions, only obfuscate the body, not the definition
                lines = section.split('\n')
                function_def = lines[0]  # First line is function definition
                function_body = '\n'.join(lines[1:])  # Rest is function body
                
                # Apply obfuscation to function body
                for obfuscator in obfuscators:
                    print(f"  - Applying {obfuscator.__class__.__name__}...")
                    function_body = obfuscator.apply(function_body)
                
                # Combine function definition with obfuscated body
                obfuscated_sections.append(function_def + '\n' + function_body)
            else:
                # Apply obfuscation to non-function sections
                for obfuscator in obfuscators:
                    print(f"  - Applying {obfuscator.__class__.__name__}...")
                    section = obfuscator.apply(section)
                obfuscated_sections.append(section)
        
        return '\n'.join(obfuscated_sections)

    def _apply_encoding(self, script_text, args):
        """Apply encoding to the script."""
        print(f"{Fore.CYAN}Applying encoding...{Style.RESET_ALL}")
        
        # Currently only supporting base64
        if 'base64' in args.encoding:
            print("  - Applying Base64 encoding...")
            encoded, decoder = Base64Encoder.encode(script_text, compression=True)
            
            # Read the stub template
            try:
                with open('stubs/ps_stub.ps1', 'r') as f:
                    stub = f.read()
            except Exception as e:
                print(f"{Fore.RED}Error reading stub template: {str(e)}{Style.RESET_ALL}")
                sys.exit(1)
            
            # Replace the placeholder with the encoded payload
            stub = stub.replace('PAYLOAD_PLACEHOLDER', encoded)
            return stub
        
        return script_text

    def run(self):
        args = self.parser.parse_args()
        self.validate_input(args)
        
        print(f"{Fore.GREEN}CloakShell - Starting obfuscation process{Style.RESET_ALL}")
        print(f"Input: {args.input}")
        print(f"Output: {args.output}")
        print(f"Obfuscation Level: {args.obfuscation_level}")
        print(f"Format: {args.format}")
        print(f"Encoding: {', '.join(args.encoding)}")
        
        # Read the input script
        script_text = self._read_script(args.input)
        
        # Apply obfuscation
        script_text = self._apply_obfuscation(script_text, args)
        
        # Apply encoding
        script_text = self._apply_encoding(script_text, args)
        
        # Write the output
        self._write_script(args.output, script_text)
        
        print(f"{Fore.GREEN}Obfuscation completed successfully!{Style.RESET_ALL}")
        print(f"Output written to: {args.output}")

def main():
    try:
        cloak = CloakShell()
        cloak.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == '__main__':
    main() 