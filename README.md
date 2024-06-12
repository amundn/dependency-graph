# Solution and Project Dependency Visualizer

This project is designed to visualize dependencies between solutions and assemblies generated from other solutions in a .NET environment. It processes solution files (`.sln`) and project files (`.csproj`) to build a dependency graph and generates a visualization of these dependencies. Additionally, it outputs a neatly formatted table showing each project, its dependent solutions, and the version used for each solution.

## Features

- **Dependency Graph Generation**: Parses solution and project files to determine dependencies.
- **Visualization**: Creates a visual representation of the dependency graph.
- **Formatted Table Output**: Displays a table listing projects, dependent solutions, and versions.

## Project Structure

- `main.py`: The main script to run the entire process.
- `data_collection.py`: Contains functions for parsing solution files, project files, and extracting dependency information.
- `visualization.py`: Contains functions to visualize the dependency graph using NetworkX and Matplotlib.
- `requirements.txt`: Lists the required Python packages for the project.

## How to Use

1. **Install Dependencies**:
   Ensure you have Python installed. Then, install the required Python packages using:

   ```sh
   pip install -r requirements.txt
   ```

2. **Set Base Directory**:
   In `main.py`, set the `base_directory` variable to the root directory containing your solution files.

   ```python
   base_directory = 'C:/Solutions'
   ```

3. **Run the Script**:
   Execute the main script:

   ```sh
   python main.py
   ```

4. **View the Outputs**:
   - **SVG Visualization**: The dependency graph will be saved as `project_dependencies.svg` in the current directory.
   - **Formatted Table**: The script will print a table to the console showing the projects, their dependent solutions, and the versions used.

## Example Output

### Graph Visualization

An SVG file (`project_dependencies.svg`) will be generated, showing nodes representing solutions and projects, with edges indicating dependencies.

### Formatted Table

The script will print a table similar to the one below:

```
┌──────────────┬───────────────┬─────────┐
│ Project name │ Solution Name │ Version │
├──────────────┼───────────────┼─────────┤
│ Project A    │ Solution 1    │   1.23  │
│ Project A    │ Solution 2    │   1.24  │
│ Project B    │ Solution 1    │   1.00  │
│ Project B    │ Solution 2    │   1.01  │
└──────────────┴───────────────┴─────────┘
```

## File Descriptions

- **`main.py`**: The entry point of the application. It orchestrates the collection of solution files, building the dependency graph, visualizing the graph, and displaying the formatted table.
- **`data_collection.py`**: This module includes functions to:
  - Parse `.sln` files to extract projects.
  - Find and parse `.csproj` files to get assembly names.
  - Extract dependency information from `Directory.Packages.props` files.
  - Build a dependency graph from the collected data.
- **`visualization.py`**: Contains the `visualize_graph` function which:
  - Uses NetworkX to create a directed graph.
  - Positions nodes and edges for clear visualization.
  - Saves the graph as an SVG file.
- **`requirements.txt`**: Lists the Python dependencies:
  - `networkx`
  - `matplotlib`
  - `tabulate`

## Contributing

If you'd like to contribute to this project, please fork the repository and use a feature branch. Pull requests are welcome.

## License

This project is licensed under the MIT License.

## Contact

For any questions or comments, please reach out to the project maintainer.

---

Happy Coding!
