from data_collection import find_sln_files, build_dependency_graph
from visualization import visualize_graph, display_dependency_table

# Define the base directory to search for .sln files
base_directory = 'C:/solutions'

# Find all .sln files in the base directory and subdirectories
solutions = find_sln_files(base_directory)

# Build the dependency graph
solution_projects, project_dependencies, project_versions = build_dependency_graph(solutions)
# Export to json
#export_graph_to_json(solution_projects, project_dependencies)
# Visualize the graph and generate SVG
visualize_graph(solution_projects, project_dependencies)

display_dependency_table(project_dependencies, project_versions)