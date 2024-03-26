import ast
import os
import sys


def get_imports(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)

    return imports


def is_std_lib(module_name):
    return module_name in sys.builtin_module_names
def is_not_in_exclusion_list(module_name, exclusion_list):
    return module_name not in exclusion_list


def generate_requirements():
    current_dir = os.getcwd()
    os.chdir(r'..')
    project_dir = os.getcwd()
    os.chdir(current_dir)
    python_files = [f for f in os.listdir(project_dir) if f.endswith('.py')]

    all_imports = set()
    for file in python_files:
        file_path = os.path.join(project_dir, file)
        file_imports = get_imports(file_path)
        all_imports.update(file_imports)

    # Filter out standard library modules
    all_imports = {module for module in all_imports if not is_std_lib(module)}
    exclusion_list = ['multiprocessing','os']
    all_imports = {module for module in all_imports if is_not_in_exclusion_list(module, exclusion_list)}

    with open('requirements.txt', 'w') as req_file:
        for module in sorted(all_imports):
            req_file.write(f"{module}\n")

    print("Requirements.txt generated successfully.")


if __name__ == "__main__":
    generate_requirements()
