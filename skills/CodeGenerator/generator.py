import os
import re
import openai
from dotenv import load_dotenv
from .prompt_loader import load_prompt

load_dotenv()  # Load env vars once

class PromptBasedCodeGenerator:
    def __init__(self, output_dir="generated_microservices"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_code(self, architecture, domain_models, api_endpoints, logic_summaries, dependencies):
        # Azure OpenAI client setup
        client = openai.AzureOpenAI(
            api_key="92oJ2DZjEvYMOCdmXCCPy9H7irVtX6NRWjwQjqKVMQNZ54UPNiYXJQQJ99BIACYeBjFXJ3w3AAAAACOGHoZ4",
            api_version="2024-12-01-preview",
            azure_endpoint="https://msfoundry.openai.azure.com/"  # use env var for endpoint
        )

        for entity, fields in domain_models.items():
            microservice_dir = os.path.join(self.output_dir, f"{entity}-service")
            os.makedirs(microservice_dir, exist_ok=True)

            # Filter relevant data for this entity (case-sensitive prefix match)
            entity_api_endpoints = [
                ep for ep in api_endpoints if ep.get('controller', '').startswith(entity)
            ]
            entity_logic_summaries = {
                k: v for k, v in logic_summaries.items() if k.startswith(entity)
            }
            entity_dependencies = {
                k: v for k, v in dependencies.items() if k.startswith(entity)
            }

            # Load the prompt, adapted for C# .NET microservices
            prompt = load_prompt(
                architecture,
                {entity: fields},
                entity_api_endpoints,
                entity_logic_summaries,
                entity_dependencies,
                entity
            )

            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "You are a helpful software engineer generating C# .NET microservices."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )

            code = response.choices[0].message.content

            # Split output by file markers (expecting "// FILE: filename")
            file_blocks = re.split(r'// FILE: (.+?)\n', code)

            # Allowed C# microservice files - add more if your project needs them
            allowed_files = [
                f"{entity}.csproj",
                f"{entity}Controller.cs",
                f"{entity}Service.cs",
                f"{entity}Repository.cs",
                "application.yml",   # Optional config
                "Dockerfile",
                f"{entity}Application.cs",
                "Startup.cs",        # Common for .NET projects
                "Program.cs"         # Entry point in modern .NET apps
            ]

            # Save only allowed files to disk
            for i in range(1, len(file_blocks), 2):
                filename = file_blocks[i].strip()
                if filename in allowed_files:
                    content = file_blocks[i + 1].lstrip()
                    file_path = os.path.join(microservice_dir, filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)

            print(f"All files for microservice '{entity}' generated in {microservice_dir}")

    def _save_code(self, code_text):
        file_path = os.path.join(self.output_dir, "GeneratedMicroservice.cs")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code_text)
        print(f"Code saved to {file_path}")

