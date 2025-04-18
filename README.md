# InSpice

This repository has been forked from it's original repository PySpice.

## About

InSpice is a Python interface to the Ngspice and Xyce circuit simulators. It provides a Python API to describe electronic circuits and to run analog simulations.

## Installation

You can install InSpice from PyPI:

```bash
pip install inspice
```

For development installation:

```bash
git clone https://github.com/Innovoltive/InSpice.git
cd InSpice
pip install -e .
```

## Dependencies

- Python 3.x
- Ngspice (as shared library)
- matplotlib (for plotting)
- numpy (for numerical computation)
- lit (for testing)

To install lit (LLVM Integrated Tester):

```bash
pip install lit
```

## Usage

See the `examples` directory for various examples of using InSpice.

Basic example:

```python
import InSpice
from InSpice.Unit import *

circuit = InSpice.Circuit('Simple RC Circuit')
circuit.R('1', 'input', 'output', 1@kΩ)
circuit.C('1', 'output', circuit.gnd, 1@µF)
```

## Documentation

For detailed documentation, please refer to the examples and docstrings.

## License

InSpice is licensed under the GNU General Public License v3.0 (GPL-3.0), the same license as the original InSpice project.

### GNU GPL v3.0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Acknowledgments

Original project (PySpice) by Fabrice Salvaire
# Copyright (C) 2025 Innovoltive
# Modified by Innovoltive on April 18, 2025.
