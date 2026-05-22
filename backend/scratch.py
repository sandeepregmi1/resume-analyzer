import os
import ast

def get_imports_from_file(filepath):
    imports = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    if module:
                        imports.add(f"{module}.{alias.name}")
                    else:
                        imports.add(alias.name)
    except Exception as e:
        pass
    return imports

def find_unused_files(directory):
    all_files = set()
    all_imports = set()
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                filepath = os.path.join(root, file)
                module_path = os.path.relpath(filepath, directory).replace('/', '.').replace('.py', '')
                all_files.add(f"app.{module_path}")
                
                imports = get_imports_from_file(filepath)
                all_imports.update(imports)

    print("Checking unused files...")
    for f in sorted(all_files):
        # f is like 'app.models.user_model'
        # A file is used if 'app.models.user_model' is in imports or if 'app.models.user_model.Something' is in imports.
        # Alternatively, 'app.models' is imported and 'user_model' is accessed, which is harder to track but usually it's explicitly imported.
        is_used = False
        if f == 'app.main':
            continue
        for imp in all_imports:
            if f in imp or imp.startswith(f):
                is_used = True
                break
        if not is_used:
            print(f"Potentially unused: {f}")

if __name__ == '__main__':
    find_unused_files('app')
