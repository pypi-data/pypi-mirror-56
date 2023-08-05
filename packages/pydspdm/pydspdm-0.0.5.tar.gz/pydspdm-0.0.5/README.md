# Pydspdm Manual

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)


---

## Installation

```python
# Install a pip package in the current Jupyter kernel
import sys
!{sys.executable} -m pip install numpy
```

---

## Usage

This util contains two separated package, dspdmapi which is aiming gettting data from dspdm service, and dspdmutil is a toolset for pre-defined calculation

example of using dspdmapi
```python
import dspdmapi
well = dspdmapi.getWellData()
```

example of using dspdmutil, well is retrived by previous operation

```python
import dspdmutil
output_well = dspdmutil.countActiveWell(well)
```