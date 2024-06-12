from data_collection import find_sln_files, build_dependency_graph, export_graph_to_json
from visualization import visualize_graph

# Define the base directory to search for .sln files
base_directory = 'C:/solutions'

# Find all .sln files in the base directory and subdirectories
solutions = find_sln_files(base_directory)

# Build the dependency graph
solution_projects, project_dependencies = build_dependency_graph(solutions)

# Call this function with your data
export_graph_to_json(solution_projects, project_dependencies)

# Visualize the graph and generate SVG
visualize_graph(solution_projects, project_dependencies)