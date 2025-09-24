import os
import re

class ApiEndpointExtractor:
    def __init__(self):
        pass

    def extract_api_endpoints(self, repo_path):
        endpoints = []

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".cs"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    if '[ApiController]' in content or 'Controller' in file:
                        class_name_match = re.search(r'class\s+(\w+)', content)
                        class_name = class_name_match.group(1) if class_name_match else "Unknown"

                        base_route_match = re.search(r'\[Route\("([^"]*)"\)\]', content)
                        base_route = base_route_match.group(1) if base_route_match else ""

                        # Extract methods with inline routes: [HttpGet("path")]
                        method_matches = re.findall(r'\[(HttpGet|HttpPost|HttpPut|HttpDelete)\s*\(\s*"(.*?)"\s*\)\]', content)
                        for method, path in method_matches:
                            full_path = self._combine_paths(base_route, path)
                            endpoints.append({
                                "controller": class_name,
                                "method": method,
                                "path": full_path
                            })

                        # Extract methods with no route: [HttpGet]
                        simple_method_matches = re.findall(r'\[(HttpGet|HttpPost|HttpPut|HttpDelete)\]', content)
                        for method in simple_method_matches:
                            # fallback to base route only
                            full_path = self._combine_paths(base_route, "")
                            endpoints.append({
                                "controller": class_name,
                                "method": method,
                                "path": full_path
                            })

        return endpoints

    def _combine_paths(self, base, sub):
        path_parts = []
        if base:
            path_parts.append(base.strip("/"))
        if sub:
            path_parts.append(sub.strip("/"))
        return "/" + "/".join(path_parts)

# Example usage
if __name__ == "__main__":
    extractor = ApiEndpointExtractor()
    repo_path = "/path/to/cloned/repo"
    endpoints = extractor.extract_api_endpoints(repo_path)
    for ep in endpoints:
        print(ep)
