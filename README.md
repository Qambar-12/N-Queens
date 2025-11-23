# N-Queens Solver & Analyzer

**Project Overview**

This repository provides a solution to the classic N-Queens problem: place N queens on an N×N board so that no two queens threaten each other (no shared row, column, or diagonal).

The project contains:

- `csp.py` — Constraint-satisfaction (CSP) solver
- `local_search.py` — Heuristic / local-search solver
- `board.py` — Board representation, placement, and conflict checks
- `plot.py` — Visualization utilities for board states
- `interface.py` — CLI/runner for experiments
- `test_config.py` — Basic configuration and test helpers
- `N-Queens.ipynb`  — Interactive notebook for exploration

**Features**

- Solve for any `N` (user-configurable)
- Two solver options: CSP (complete) and Local Search (heuristic)
- Performance and scalability comparisons
- Visualize solutions and highlight conflicts
- Modular and easy to extend with new heuristics

## Getting Started

### Prerequisites

Install Python 3.7+ and the main dependencies:

```bash
pip install numpy matplotlib ipython jupyter
```

### Running the project

Clone the repository (if needed):

```bash
git clone https://github.com/Qambar-12/N-Queens.git
cd N-Queens
```

Run the CLI (`interface.py`) to solve with the CSP solver:

```bash
python interface.py --method csp --N 8
```

Run the local-search solver (example for N=50):

```bash
python interface.py --method local_search --N 50
```

Open the interactive notebook:

```bash
jupyter notebook N-Queens.ipynb
```

## File Overview

- `board.py`: Board logic, queen placement, conflict checks
- `csp.py`: Constraint-satisfaction solver implementation
- `local_search.py`: Heuristic solver implementation
- `plot.py`: Visualization utilities for board states
- `interface.py`: CLI/runner for executing experiments
- `test_config.py`: Configurations & basic tests
- `N-Queens.ipynb` : Notebook explaining methods & results

## Interpreting Results

- **CSP**: Deterministic, finds a solution if one exists; scales slower as `N` grows
- **Local Search**: Often fast for large `N`, may require multiple restarts or iterations to reach zero conflicts

## Contributing

Contributions are welcome — add new heuristics, improve efficiency, or enhance visualizations. Please open a PR or an issue.

## License

This project is licensed under the MIT License.

## Author

Muhammad Qambar Hussain — Computer & Information Systems Engineer 

Happy solving! 👑
