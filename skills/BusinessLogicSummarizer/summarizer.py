import os
import re
from openai import AzureOpenAI
from dotenv import load_dotenv

class BusinessLogicSummarizer:
    def __init__(self):
        load_dotenv()  # Ensure .env variables are loaded
        # Azure OpenAI client setup


    def summarize_business_logic(self, code_files):
        summaries = {}

        for file in code_files:
            content = file["content"]
            class_match = re.search(r'class\s+(\w+)', content)
            class_name = class_match.group(1) if class_match else "UnknownClass"

            prompt = f"""
                You are a software analyst. Summarize the business logic of the following C# .net class in clear, concise language.
                Focus on what the class does, its responsibilities, and how it interacts with other components.

                C# Class:
                {content}
                """
            client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version="2024-12-01-preview",
                azure_endpoint="https://azure-ai-foundry-vijay.openai.azure.com/"
            )
            response =  client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "You are a helpful software analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )

            summary = response.choices[0].message.content
            summaries[class_name] = summary

        return summaries

# Example usage
if __name__ == "__main__":
    tool = BusinessLogicSummarizer()
    sample_code_files = [{"path": "UserService.cs", "content": "public class UserService { ... }"}]
    result = tool.summarize_business_logic(sample_code_files)
    print(result)
