# Integer Linear Programming Implementation for Packing and Coloring in Graphs
[![DOI](https://zenodo.org/badge/968210406.svg)](https://doi.org/10.5281/zenodo.15975207)

This code uses the formulation from Shao & Vesel’s 2015 work, *Modeling the packing coloring problem of graphs*[^1].

## Setup Instructions

Follow these steps to set up the project on your local machine:

### Prerequisites

Ensure you have the following installed:

- Python 3.10 or higher
- `pip` (Python package manager)

### Installation

1. **Create a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Notes

- Ensure `CPLEX` is installed and configured. [Setting up the CPLEX Python API](https://www.ibm.com/docs/en/icos/22.1.2?topic=cplex-setting-up-python-api)

### Usage

1. **Run the main script**:
   ```bash
   python main.py
   ```

2. **View generated graphs**:
    - Graph files will be saved in the `graphs` directory.

3. **Modify parameters**:
    - Update `P_n`, `B_n`, or `K_n` values in `main.py` to customize the graph generation.

## References

[^1]: Z. Shao and A. Vesel, “Modeling the packing coloring problem of graphs,” *Applied Mathematical Modelling*, vol. 39, no. 13, pp. 3588–3595, 2015. DOI: [10.1016/j.apm.2014.11.060](https://doi.org/10.1016/j.apm.2014.11.060).