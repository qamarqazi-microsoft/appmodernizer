def load_prompt(architecture, domain_models, api_endpoints, logic_summaries, dependencies, entity_name=None):
    prompt = (
        "You are a code generation assistant. Based on the following inputs, generate a complete microservice in Java Spring Boot. "
        "For each resource, output the code as follows: '// FILE: <filename>\\n<code>' (e.g., '// FILE: User.java'). "
        "Generate separate files for Entity, Controller, Service, Repository, application.yml, and Dockerfile. "
        "Place all files for this microservice directly in a folder named after the entity (e.g., 'User/'). "
        "Do NOT use any nested folders, package directories, or src/main/java structure. "
        "All files must be at the top level of the microservice folder. "
        "Do not include any explanations or extra text.\n\n"
    )

    prompt += "## Domain Models:\n"
    for entity, fields in domain_models.items():
        prompt += f"- Entity: {entity}\n"
        for field in fields:
            prompt += f"  - {field['name']} ({field['type']})\n"

    prompt += "\n## API Endpoints:\n"
    for endpoint in api_endpoints:
        prompt += f"- {endpoint['method']} {endpoint['path']} (Controller: {endpoint['controller']})\n"

    prompt += "\n## Business Logic Summaries:\n"
    for class_name, summary in logic_summaries.items():
        prompt += f"- {class_name}: {summary}\n"

    prompt += "\n## Dependencies:\n"
    for class_name, imports in dependencies.items():
        prompt += f"- {class_name} depends on: {', '.join(imports)}\n"

    prompt += "\n## Architecture:\n"
    for key, value in architecture.items():
        prompt += f"- {key}: {value}\n"

    ##prompt += f"\nGenerate all files for the microservice in a folder named '{entity_name}/' (if entity_name is provided). Each file should start with the marker '// FILE: <filename>' and contain only the code. Do not include explanations.\n"
    return prompt