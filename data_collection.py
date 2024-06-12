import xml.etree.ElementTree as ET
import os
import re
from collections import defaultdict

def parse_packages_props(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        dependencies = []
        for package in root.findall(".//PackageVersion"):
            name = package.get('Include')
            version = package.get('Version')
            dependencies.append((name, version))
        return dependencies
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return []

def parse_sln(file_path):
    project_pattern = re.compile(r'Project\("{.*}"\) = "(.*)", "(.*)", "{.*}"')
    projects = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = project_pattern.match(line)
                if match:
                    project_name = match.group(1)
                    project_path = os.path.join(os.path.dirname(file_path), match.group(2).replace("\\", "/"))
                    projects.append((project_name, project_path))
        # print(f"Parsed projects from {file_path}: {projects}")
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    return projects

def find_csproj_files(base_directory):
    csproj_files = []
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.csproj'):
                csproj_files.append(os.path.join(root, file))
    return csproj_files

def parse_assembly_name(csproj_file):
    if not os.path.exists(csproj_file):
        print(f"CSProj file not found: {csproj_file}")
        return None
    try:
        tree = ET.parse(csproj_file)
        root = tree.getroot()
        assembly_name = None
        for elem in root.iter('AssemblyName'):
            assembly_name = elem.text
            break
        if not assembly_name:
            assembly_name = os.path.splitext(os.path.basename(csproj_file))[0]
        return assembly_name
    except Exception as e:
        print(f"Error parsing {csproj_file}: {e}")
        return None

def find_sln_files(base_directory):
    sln_files = []
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.sln'):
                sln_files.append(os.path.join(root, file))
    # print(f"Found solution files: {sln_files}")
    return sln_files

# Build dependency graph code remains the same - ensure paths are properly constructed and checked before use

def build_dependency_graph(solutions):
    solution_projects = {}
    project_dependencies = defaultdict(list)
    all_dependencies = set()
    project_assembly_names = {}
    project_versions = defaultdict(dict)

    # First pass: Collect all projects from all solutions
    for solution in solutions:
        projects = parse_sln(solution)
        solution_name = os.path.basename(solution)
        solution_projects[solution_name] = projects

    # Collect all .csproj files and parse their assembly names
    base_directory = os.path.commonpath(solutions)
    csproj_files = find_csproj_files(base_directory)
    for csproj_file in csproj_files:
        assembly_name = parse_assembly_name(csproj_file)
        if assembly_name:
            project_assembly_names[assembly_name] = csproj_file

    # print(f"Project assembly names: {project_assembly_names}")

    # Second pass: Collect all dependencies
    for solution in solutions:
        solution_name = os.path.basename(solution)
        solution_dir = os.path.dirname(solution)
        props_path = os.path.join(solution_dir, 'Directory.Packages.props')

        if os.path.exists(props_path):
            dependencies = parse_packages_props(props_path)
            for dep, version in dependencies:
                all_dependencies.add(dep)
                project_versions[dep][solution_name] = version
                if dep in project_assembly_names:
                    for other_solution, other_projects in solution_projects.items():
                        if other_solution != solution_name:
                            for project_name, project_path in other_projects:
                                project_csproj_path = os.path.abspath(os.path.join(solution_dir, project_path))
                                if project_csproj_path == project_assembly_names[dep]:
                                    project_dependencies[dep].append((solution_name, version))
                                    # print(f"Added dependency: {solution_name} -> {dep}")
                                # else:
                                #     print(f"No match for {project_csproj_path} and {project_assembly_names[dep]}")

    # Filter out projects that are not in the list of dependencies
    filtered_solution_projects = {}
    for sol, projs in solution_projects.items():
        filtered_projects = []
        for proj_name, proj_path in projs:
            csproj_file = os.path.join(os.path.dirname(solutions[0]), proj_path)
            assembly_name = parse_assembly_name(csproj_file)
            if assembly_name in all_dependencies:
                filtered_projects.append(assembly_name)
        filtered_solution_projects[sol] = filtered_projects

    project_dependencies = {proj: sols for proj, sols in project_dependencies.items() if proj in all_dependencies}

    print("Filtered Solution Projects:", filtered_solution_projects)
    print("Filtered Project Dependencies:", project_dependencies)

    return filtered_solution_projects, project_dependencies, project_versions

def export_graph_to_json(solution_projects, project_dependencies):
    nodes = [{'id': proj, 'group': 'solution' if proj in solution_projects else 'project'} for proj in set(solution_projects.keys()).union(project_dependencies.keys())]
    links = [{'source': sol, 'target': proj, 'value': 1} for proj, sols in project_dependencies.items() for sol in sols]
    
    graph = {
        'nodes': nodes,
        'links': links
    }
    
    with open('graph_data.json', 'w') as f:
        json.dump(graph, f, indent=4)