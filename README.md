# CloakShell

CloakShell is an advanced, modular PowerShell obfuscator and evasive payload generator designed for red teamers and offensive operators. It transforms readable PowerShell scripts into heavily obfuscated payloads capable of bypassing modern EDR solutions.

## Features

- [x] Variable and function name obfuscation
- [x] String obfuscation (splitting, char arrays)
- [x] Multi-layer encoding (Base64)
- [ ] Anti-analysis checks (debugger, sandbox detection)
- [x] Output formats: PS1, one-liner
- [ ] C# EXE output
- [x] Modular plugin architecture

## Installation

1. Clone the repository:
```bash
git clone https://github.com/t3chfalcon/cloakshell.git
cd cloakshell
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python cloakshield.py --input script.ps1 --output obfuscated.ps1
```

Advanced usage:
```bash
python cloakshield.py \
    --input script.ps1 \
    --output obfuscated.ps1 \
    --obfuscation-level high \
    --format ps1-oneliner \
    --encoding base64,xor \
    --junk-code \
    --anti-analysis
```

### Options

- `--input, -i`: Input PowerShell script to obfuscate
- `--output, -o`: Output file path
- `--obfuscation-level, -l`: Level of obfuscation (low/medium/high)
- `--format, -f`: Output format (ps1/ps1-oneliner/csharp-exe)
- `--encoding, -e`: Encoding methods (base64/xor/aes)
- `--junk-code, -j`: Inject junk code and NOPs
- `--anti-analysis, -a`: Add anti-analysis checks

## Project Structure

```
CloakShell/
├── cloakshield.py           # CLI entry point
├── obfuscators/            # Obfuscation plugins
│   ├── base.py
│   ├── variable_renamer.py
│   └── string_obfuscator.py
├── encoders/               # Encoding modules
│   └── base64_encoder.py
├── stubs/                  # Template stubs
│   └── ps_stub.ps1
└── README.md
```

## Security Notice

This tool is designed for authorized red team engagements and security research only. Do not use it for malicious purposes. The authors are not responsible for any misuse of this tool.

## License

MIT License - See LICENSE file for details 