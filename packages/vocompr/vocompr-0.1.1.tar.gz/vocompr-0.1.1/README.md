# VoCompr (status: POC)
[![Actions Status](https://github.com/enzobnl/vocompr/workflows/test/badge.svg)](https://github.com/enzobnl/pycout/actions) [![Actions Status](https://github.com/enzobnl/vocompr/workflows/PyPI/badge.svg)](https://github.com/enzobnl/pycout/actions)

**A VOCabulary-based COMPRession algorithm**

*Specialized in the compression of texts having a small characters set, like DNA sequencies.*

## Install
`pip install vocompr` (or `pip install git+https://github.com/enzobnl/vocompr.git`)
## Usage

```python
from vocompr import vocompr, unvocompr

with open("path/vopress_input.txt", "r") as input_file:
    input_str = input_file.read()

with open("path/vopress_output", "wb") as output_bytes_file:
    output_bytes_file.write(vocompr(input_str))

with open("path/vopress_output", "rb") as input_bytes_file:
    print("original text:", unvocompr(input_bytes_file.read()))
```

## Author
Enzo Bonnal (enzobonnal@gmail.com)