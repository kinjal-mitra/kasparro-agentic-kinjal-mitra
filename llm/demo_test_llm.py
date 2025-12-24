# llm/demo_test_llm.py

from llm_client import LLMClient


def main():
    """
    Simple sanity check for LLMClient.
    This script verifies:
    - .env loading
    - Anthropic API connectivity
    - Proper response extraction
    """

    llm = LLMClient(
        model="claude-3-5-haiku-20241022",
        temperature=0.2,
        max_tokens=150
    )

    prompt = """
        Generate exactly three short questions a user might ask
        about a generic skincare product.
        Return them as a numbered list.
    """

    response = llm.generate(prompt)

    print("\n=== LLM RESPONSE START ===\n")
    print(response)
    print("\n=== LLM RESPONSE END ===\n")


if __name__ == "__main__":
    main()
