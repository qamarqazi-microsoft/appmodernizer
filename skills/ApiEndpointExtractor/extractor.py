import os
import re

class ApiEndpointExtractor:
    def __init__(self):
        pass

    def extract_api_endpoints(self, repo_path):
        endpoints = []

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    if '@RestController' in content or '@Controller' in content:
                        class_name = re.search(r'class\s+(\w+)', content)
                        base_path = re.search(r'@RequestMapping\("(.*?)"\)', content)
                        base = base_path.group(1) if base_path else ""

                        method_matches = re.findall(r'@(GetMapping|PostMapping|PutMapping|DeleteMapping)\("(.*?)"\)', content)
                        for method, path in method_matches:
                            endpoints.append({
                                "controller": class_name.group(1) if class_name else "Unknown",
                                "method": method,
                                "path": f"/api{base}{path}"
                            })

        return endpoints

# Example usage
if __name__ == "__main__":
    extractor = ApiEndpointExtractor()
    repo_path = "/path/to/cloned/repo"
    endpoints = extractor.extract_api_endpoints(repo_path)
    for ep in endpoints:
        print(ep)