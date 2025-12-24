from agents.question_generation_agent import QuestionGenerationAgent

# -------------------------
# Mock normalized product
# -------------------------
normalized_product = {
    "name": "GlowBoost Vitamin C Serum",
    "concentration": "10% Vitamin C",
    "skin_type": ["Oily", "Combination"],
    "ingredients": ["Vitamin C", "Hyaluronic Acid"],
    "benefits": ["Brightening", "Fades dark spots"],
    "usage": "Apply 2–3 drops in the morning before sunscreen",
    "side_effects": "Mild tingling for sensitive skin",
    "price": "₹699"
}


def test_rule_only_mode():
    print("\n=== RULE-ONLY MODE TEST ===\n")

    agent = QuestionGenerationAgent(llm_client=None)
    questions = agent.generate(normalized_product)

    for category, qs in questions.items():
        print(f"{category.upper()} ({len(qs)})")
        for q in qs:
            print(f"  - {q}")

    print("\n✔ Rule-only test passed\n")


if __name__ == "__main__":
    test_rule_only_mode()
