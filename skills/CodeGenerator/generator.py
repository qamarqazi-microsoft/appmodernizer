import os
from openai import AzureOpenAI
from .prompt_loader import load_prompt
import openai
import re
class PromptBasedCodeGenerator:
    def __init__(self, output_dir="generated_microservices"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

 # e.g., "gpt-4"

    def generate_code(self, architecture, domain_models, api_endpoints, logic_summaries, dependencies):
        # Azure OpenAI client setup
        client = openai.AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-12-01-preview",
            azure_endpoint="https://azure-ai-foundry-vijay.openai.azure.com/"
        )

        for entity, fields in domain_models.items():
            microservice_dir = os.path.join(self.output_dir, entity + "-service")
            os.makedirs(microservice_dir, exist_ok=True)

            # Filter relevant data for this entity
            entity_api_endpoints = [ep for ep in api_endpoints if ep.get('controller', '').startswith(entity)]
            entity_logic_summaries = {k: v for k, v in logic_summaries.items() if k.startswith(entity)}
            entity_dependencies = {k: v for k, v in dependencies.items() if k.startswith(entity)}

            prompt = load_prompt(architecture, {entity: fields}, entity_api_endpoints, entity_logic_summaries, entity_dependencies, entity)

            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "You are a helpful software engineer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )

            code = response.choices[0].message.content

            # Split the output by file markers
            file_blocks = re.split(r'// FILE: (.+?)\n', code)
            # file_blocks[0] is any text before the first file marker (usually empty)
            allowed_prefixes = [entity]
            allowed_files = [
                f"{entity}.java",
                f"{entity}Controller.java",
                f"{entity}Service.java",
                f"{entity}Repository.java",
                "application.yml",
                "Dockerfile",
                f"{entity}Application.java"
            ]
            for i in range(1, len(file_blocks), 2):
                rel_path = file_blocks[i].strip()
                # Only save files that match the main entity or are standard config files
                if rel_path in allowed_files:
                    content = file_blocks[i+1].lstrip()
                    file_path = os.path.join(microservice_dir, rel_path)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
            print(f"All files for microservice '{entity}' have been generated in {microservice_dir}")


    def _save_code(self, code_text):
        file_path = os.path.join(self.output_dir, "GeneratedMicroservice.java")
        with open(file_path, "w") as f:
            f.write(code_text)
        print(f"Code saved to {file_path}")