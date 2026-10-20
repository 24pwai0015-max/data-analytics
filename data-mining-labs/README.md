# Data Mining Labs

University coursework and laboratory notebooks for the Data Mining curriculum.

## Environment & Kernel
- **Jupyter Kernel:** `data-analytics`
- **Python Version:** Python 3.12 (via root `venv`)

## Running Labs
You can launch Jupyter from the project root using:
```powershell
.\run.ps1 jupyter
```
Or in VS Code, open any `.ipynb` file and select the **Python (data-analytics)** kernel from the top-right kernel picker.

## Dataset Access
Datasets are centralized in `..\data\` relative to this folder, or `data\` from the project root.
```python
from pathlib import Path
DATA_DIR = Path.cwd().parent / "data"  # when running inside this folder
```
