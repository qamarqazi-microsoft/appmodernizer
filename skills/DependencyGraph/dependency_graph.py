import os
import re

class DependencyGraph:
    def __init__(self):
        pass

    def build_dependency_graph(self, repo_path):
        graph = {}

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".cs"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # Find all classes in the file
                    classes = re.findall(r'class\s+(\w+)', content)
                    # Find all types used as fields, properties, method parameters, or base classes/interfaces
                    # Simplified: we look for capitalized identifiers which are common for class/type names
                    # This regex captures identifiers used after access modifiers or in inheritance
                    used_types = set(re.findall(r'(?:public|private|protected|internal)\s+([\w<>]+)\s+\w+\s*[;=\(]', content))
                    inherits = []
                    for match in re.findall(r'class\s+\w+\s*:\s*([\w, ]+)', content):
                        inherits.extend([x.strip() for x in match.split(",")])

                    # Combine all dependencies for this file
                    dependencies = set()
                    dependencies.update(used_types)
                    dependencies.update(inherits)

                    for cls in classes:
                        graph[cls] = list(dependencies)

        return graph

# Example usage
if __name__ == "__main__":
    tool = DependencyGraph()
    repo_path = "/path/to/cloned/repo"
    graph = tool.build_dependency_graph(repo_path)
    print(graph)
