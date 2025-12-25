
from comparison_llm import ComparisonClient


def run_test():
    print("Initializing GeminiClient...")

    client = ComparisonClient()

    prompt = "Explain what an AI agent is in one sentence."

    print("\nSending prompt to Gemini...")
    response = client.generate(prompt)

    print("\n--- Gemini Response ---")
    print(response)
    print("----------------------")

    if isinstance(response, str) and len(response.strip()) > 0:
        print("\n✅ TEST PASSED: GeminiClient returned text successfully.")
    else:
        print("\n❌ TEST FAILED: No valid text returned.")


if __name__ == "__main__":
    run_test()
