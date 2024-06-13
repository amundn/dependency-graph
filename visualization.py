import networkx as nx
import matplotlib.pyplot as plt
from tabulate import tabulate

def visualize_graph(solution_projects, project_dependencies):
    G = nx.DiGraph()

    # Add nodes for each project and solution
    for solution, projects in solution_projects.items():
        G.add_node(solution, subset='solution', color='lightblue')
        for project in projects:
            G.add_node(project, subset='project', color='lightgreen')

    # Add edges based on cross-solution dependencies
    color_map = ['red', 'blue', 'green', 'purple', 'orange']
    solution_colors = {solution: color_map[idx % len(color_map)] for idx, solution in enumerate(solution_projects.keys())}

    edge_list = []
    edge_labels = {}
    color_list = []
    for project, solutions in project_dependencies.items():
        for solution, version in solutions:
            edge_color = solution_colors[solution]
            for other_solution, other_projects in solution_projects.items():
                if project in other_projects:
                    G.add_edge(solution, project, color=edge_color)
                    edge_list.append((solution, project))
                    color_list.append(edge_color)
                    edge_labels[(solution, project)] = f'{solution} -> {project}'

    # Get positions for nodes in graph using multipartite layout
    pos = nx.multipartite_layout(G, subset_key='subset')

    # Separate solutions and projects for vertical spacing
    solutions = [node for node in G.nodes if G.nodes[node]['subset'] == 'solution']
    projects = [node for node in G.nodes if G.nodes[node]['subset'] == 'project']

    # Adjust vertical spacing
    total_solutions = len(solutions)
    total_projects = len(projects)

    solution_y_positions = {node: 1 - i * (2 / (total_solutions - 1)) for i, node in enumerate(solutions)}
    project_y_positions = {node: -1 + i * (2 / (total_projects - 1)) for i, node in enumerate(projects)}

    for node in G.nodes:
        x, _ = pos[node]
        if node in solution_y_positions:
            pos[node] = (x, solution_y_positions[node])
        elif node in project_y_positions:
            pos[node] = (x, project_y_positions[node])

    # Draw the graph
    node_colors = [G.nodes[n]['color'] for n in G.nodes]
    plt.figure(figsize=(20, 20))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=color_list, edgelist=edge_list, node_shape='s', node_size=3000, font_size=8, font_weight='bold', arrowsize=20, bbox=dict(facecolor="white", edgecolor='black', boxstyle='round,pad=0.3'))

    # Save the SVG file
    plt.savefig('project_dependencies.svg', format='svg')
    plt.show()

    # Return the graph and edge labels for further processing
    return G, edge_labels

def display_dependency_table(project_dependencies, project_versions, output_file="dependency_table.txt"):
    table_data = []
    for project, solutions in project_dependencies.items():
        for solution, version in solutions:
            table_data.append([project, solution, project_versions[project][solution]])

    headers = ["Project name", "Solution Name", "Version"]
    table = tabulate(table_data, headers, tablefmt="pretty")
    
    # Print the table to console
    print(table)
    
    # Save the table to a text file
    with open(output_file, 'w') as f:
        f.write(table)
