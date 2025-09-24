import os
from skills.GitHubReader.reader import clone_repo
from skills.CodeParser.parser import CodeParser
from skills.ApiEndpointExtractor.extractor import ApiEndpointExtractor
from skills.DomainModelExtractor.domain_model_extractor import DomainModelExtractor
from skills.DependencyGraph.dependency_graph import DependencyGraph
from skills.BusinessLogicSummarizer.summarizer import BusinessLogicSummarizer
from skills.ArchitectureDesigner.designer import ArchitectureDesigner
from skills.CodeGenerator.generator import PromptBasedCodeGenerator
from skills.GitHubWriter.github_writer import GitHubWriter
from dotenv import load_dotenv

def run():
    load_dotenv()  # Load environment variables from .env file
    repo_url = "https://github.com/Jonahida/java-spring-monolithic-ecommerce-application"
    repo_path = clone_repo(repo_url)

    parser = CodeParser()
    code_structure = parser.parse_code(repo_path)

    endpoint_extractor = ApiEndpointExtractor()
    api_endpoints = endpoint_extractor.extract_api_endpoints(repo_path)

    domain_extractor = DomainModelExtractor()
    domain_models = domain_extractor.extract_domain_models(repo_path)

    dependency_tool = DependencyGraph()
    dependencies = dependency_tool.build_dependency_graph(repo_path)

    summarizer = BusinessLogicSummarizer()
    # Provide both file path and content to the summarizer
    code_files = []
    for f in code_structure:
        file_path = f["file"]
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
        except Exception:
            content = ""
        code_files.append({"path": file_path, "content": content})
    logic_summaries = summarizer.summarize_business_logic(code_files)

    designer = ArchitectureDesigner()
    # Aggregate entities and controllers for architecture input
    entities = []
    controllers = []
    for f in code_structure:
        entities.extend(f.get("classes", []))
        controllers.extend([c for c in f.get("classes", []) if "Controller" in c])
    architecture_input = {
        "entities": entities,
        "controllers": controllers
    }
    architecture = designer.design_architecture(architecture_input)

    generator = PromptBasedCodeGenerator()
    generator.generate_code(architecture, domain_models, api_endpoints, logic_summaries, dependencies)

    
    # === Call GitHubWriter at the end ===
    github_writer = GitHubWriter(
        local_folder="generated_microservices",
        github_url=os.getenv("TARGET_REPO_URL"),
        branch="main",
        commit_message="Add generated microservices"
    )
    github_writer.write_to_github()


if __name__ == "__main__":
    run()
