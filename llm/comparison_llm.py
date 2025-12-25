# llm/groq_client.py
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

class ComparisonClient:
    """
    Wrapper around Groq API for fast LLM inference.
    """
    def __init__(
        self,
        model: str = "llama-3.3-70b-versatile",  # Best model
        temperature: float = 0.3
    ):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        self.model_name = model
        self.temperature = temperature
        self.client = Groq(api_key=api_key)
    
    def generate(self, prompt: str) -> str:
        """
        Sends a prompt to Groq and returns raw text output.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}") from e