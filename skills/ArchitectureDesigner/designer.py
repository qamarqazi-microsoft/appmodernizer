class ArchitectureDesigner:
    def __init__(self):
        pass

    def design_architecture(self, code_structure):
        """
        Accepts parsed code structure and returns a microservices architecture plan.
        """

        # Extract entities and controllers from parsed code
        entities = code_structure.get("entities", [])
        controllers = code_structure.get("controllers", [])

        # Define services based on entities
        services = [f"{entity}Service" for entity in entities]

        # Communication strategy
        communication = "REST"

        # Database strategy
        database = {
            "type": "PostgreSQL",
            "strategy": "One database per service (schema separation)"
        }

        # API Gateway and Security
        gateway = {
            "enabled": True,
            "tool": "Azure API Management",
            "auth": "OAuth2 / JWT"
        }

        # Observability
        observability = {
            "logging": "Azure Monitor",
            "tracing": "OpenTelemetry",
            "metrics": "Prometheus (optional)"
        }

        # Deployment
        deployment = {
            "containerization": "Docker",
            "orchestration": "Azure Kubernetes Service (AKS)",
            "CI/CD": "GitHub Actions"
        }

        return {
            "services": services,
            "communication": communication,
            "database": database,
            "gateway": gateway,
            "observability": observability,
            "deployment": deployment
        }

# Example usage
if __name__ == "__main__":
    designer = ArchitectureDesigner()
    sample_structure = {
        "entities": ["User", "Product", "Order"],
        "controllers": ["UserController", "ProductController", "OrderController"]
    }
    architecture = designer.design_architecture(sample_structure)
    print(architecture)