# Setup Instructions

Follow these steps to set up the project on your local machine:

## Prerequisites

Ensure you have the following installed:

- Python 3.10 or higher
- `pip` (Python package manager)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gulmelih/ILP_Packing_Coloring.git
   cd ILP_Packing_Coloring
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Notes

- Ensure `CPLEX` is installed and configured. [Setting up the CPLEX Python API](https://www.ibm.com/docs/en/icos/22.1.2?topic=cplex-setting-up-python-api)

## Usage

1. **Run the main script**:
   ```bash
   python main.py
   ```

2. **View generated graphs**:
    - Graph files will be saved in the `graphs` directory.

3. **Modify parameters**:
    - Update `P_n`, `B_n`, or `K_n` values in `main.py` to customize the graph generation.

