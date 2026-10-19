# Graph Theory Project (Dijkstra's Algorithm)

This project is the result of our work on directed and weighted graphs. The goal was to code a module capable of calculating the shortest path between two geographical points using Dijkstra's famous algorithm.

*(The formatting of certain lines might look unusual; this is due to adhering to Pylint conventions to write cleaner code).*

---

## How to Run the Program?

We provided two ways to use it, depending on whether you prefer a pure command line interface or a more interactive module.

> **!!! WARNING !!!**
> In both of the following cases, **store the CSV and GraphML files in the `donnees/` folder**.

### Option A: Command Mode (required by the assignment)

Use the `main.py` file. It takes specific arguments and gives you the direct output

**Command:**

```bash
python main.py --fichier toulouse.csv --source 625236 --cible 2493904512 

```

*(Optional: add `--graphml toulouse.graphml` at the end)*

### Option B: Demo Mode (more user-friendly)

Run the `demonstration.py` file. The script will guide you and ask you, after specifying the CSV and GraphML files, to enter the start and destination directly in the console using a map showing the coordinates of the various destinations (if the CSV file is small).

---

## Data Format

The program reads CSV files (encoded in UTF-8). Each line represents a trip (an edge) between two cities along with their coordinates.
**Format:** `depart, x_depart, y_depart, arrivee, x_arrivee, y_arrivee`

**Note:** Since the file does not directly provide trip weights, we calculate them ourselves using the Euclidean distance between the two points. Because of this, edge weights will never be negative, making exceptions or tests for negative weights superfluous or even impossible.

A `.graphml` file can also be added for a more detailed path visualization.

---

## Code Organization

We split the project into several files to keep it organized:

* **`classes.py`**: The core engine. Contains the definitions of Nodes, Edges, and all Dijkstra logic.
* **`fonctions.py`**: Handles administrative tasks (loading the CSV and formatting outputs nicely).
* **`main.py`**: CLI tool for running the program.
* **`demonstration.py`**: Our script for the interactive presentation.
* **`static_methods.py`**: Contains static methods (`@staticmethod`) that would have cluttered `classes.py`.
* **`test_projet.py`**: All our test cases to ensure nothing breaks (using `pytest`).

---

## Technical Choices

* **For the Graph:** We store vertices in a list and edges in a dictionary. Why a dictionary? Because it allows retrieving edge weights extremely quickly, with $O(1)$ complexity.
* **For Dijkstra:** We also use dictionaries to track distances and parent nodes for each point, making updates very efficient.

**Important:** A path from A to B is not necessarily the same as B to A (it is a directed graph). We also ensure all weights are positive, as this is a golden rule for Dijkstra.

---

## Why No Negative Weights?

It comes down to logic: Dijkstra is a greedy algorithm. It assumes that as soon as it finds a path to a node, it is guaranteed to be the shortest. If there were negative weights, you could keep reducing the distance indefinitely by revisiting certain paths, causing the algorithm to produce incorrect results or run indefinitely.

> **Minimal Counterexample:**
> Given a graph with three nodes A, B, C and three edges:
> * A -> B (weight 10)
> * A -> C (weight 5)
> * B -> C (weight -7)
> 
> 
> If we look for the shortest path from A to C:
> At initialization, A is 0. Neighbors are B (10) and C (5).
> **ERROR:** Since C is the smallest, Dijkstra "locks" it and considers 5 as the shortest distance to C.
> It then moves to B (distance 10). It sees edge B -> C with a weight of -7. The calculation would be $10 + (-7) = 3$. But since C is already marked as "visited/finished", standard Dijkstra will not go back to correct it.
> **Result:** Dijkstra will report the path as A -> C (cost 5), whereas the actual shortest path is A -> B -> C (cost 3).

---

## Test Suite (Edge Case Coverage)

To test the program without manually creating files or typing inputs each time, we used fixtures from `pytest` ([documentation](https://docs.pytest.org/en/7.1.x/reference/reference.html?highlight=tmp_path#fixtures)):

* **`tmp_path`**: Creates a temporary workspace to test file reading without cluttering the disk.
* **`monkeypatch`**: Simulates user input by automatically mocking answers to `input()` calls so navigation can be tested headlessly.
* **`capsys`**: Captures console output (`print`), enabling us to verify that the final display matches expected specifications.
* **`sys`** (via `monkeypatch`): Simulates CLI arguments like `--source` or `--cible` to validate `main.py` without human intervention.

### Coverage Includes:

* **CSV Loading:** Tests valid files, malformed formats (`ValueError` caught), and non-existent files (`FileNotFoundError` caught).
* **Path Calculation and Unreachability:** Tests nominal paths, start vertex equal to target vertex (cost 0), and isolated targets (returns an empty list and +inf).
* **Minimum Condition:** Isolated mathematical verification proving the algorithm updates a distance only if the relaxation condition $C(j) > C(i) + c_{ij}$ is strictly met.
* **Negative Weight Error:** Simulates forcible modification of the edge dictionary with a negative value. The test asserts that `plus_court_chemin` immediately raises a `ValueError`, validating code robustness.

---

## Algorithmic Optimizations and Performance

Standard Dijkstra was refactored to efficiently process large-scale graphs (such as the Toulouse road network).

> **PERFORMANCE**
> Execution time on the full dataset went from several minutes to a fraction of a second.

* **Binary Heap (Priority Queue)**
Linear search for the nearest vertex was replaced using the built-in `heapq` module. This structure keeps the vertex with the minimum distance at index 0, reducing extraction complexity from $O(V)$ to $O(\log V)$. The algorithm handles `(distance, label)` tuples to leverage Python's native sorting.
* **Precomputation via Adjacency Dictionary**
The main bottleneck was dynamic neighbor lookup. Now, during graph initialization, a `self.adjacence` dictionary is generated. It stores the target label and precomputed weight for each vertex, reducing neighbor access to $O(1)$ complexity and avoiding full graph traversals.
* **Elimination of Loop Instantiations**
Inside the innermost loop, iterative object creation (such as `Arc` instances) and type conversions (like `list()`) were entirely removed. Data is handled using tuples, significantly reducing CPU overhead.
* **Early Exit Condition**
The algorithm does not explore the entire graph unless necessary. The main loop incorporates a `break` condition that triggers as soon as the target node's label is finalized (extracted from the binary heap).
