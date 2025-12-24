# llm/llm_client.py

from typing import Optional
import os

import anthropic
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class LLMClient:
    """
    Thin wrapper around Anthropic Claude.
    Responsible ONLY for:
    - Sending prompts
    - Returning raw text output
    """

    def __init__(
        self,
        model: str = "claude-3-5-haiku-20241022",
        temperature: float = 0.3,
        max_tokens: int = 500
    ):
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY not found. "
                "Make sure it is set in your .env file."
            )

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, prompt: str) -> str:
        """
        Sends a prompt to Claude and returns raw text output.

        Parameters:
        - prompt (str): The prompt to send to the LLM

        Returns:
        - str: Raw response text
        """

        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Claude responses are returned as content blocks
        return message.content[0].text.strip()
