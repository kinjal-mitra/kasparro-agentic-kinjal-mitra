import pytest
from agents.content_logic_agent import ContentLogicAgent


@pytest.fixture
def normalized_product():
    return {
        "name": "GlowBoost Vitamin C Serum",
        "concentration": "10% Vitamin C",
        "skin_type": ["Oily", "Combination"],
        "ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "benefits": ["Brightening", "Fades dark spots"],
        "usage": "Apply 2–3 drops in the morning before sunscreen",
        "side_effects": "Mild tingling for sensitive skin",
        "price": 699,
    }


@pytest.fixture
def fictional_product():
    return {
        "name": "RadiantPlus Serum",
        "concentration": "8% Vitamin C",
        "skin_type": ["Dry"],
        "ingredients": ["Vitamin C", "Niacinamide"],
        "benefits": ["Hydration", "Glow"],
        "usage": "Apply at night",
        "price": 799,
    }


@pytest.fixture
def content_logic_agent():
    return ContentLogicAgent()


# -------------------------
# Product Page Tests
# -------------------------
def test_product_page_generation(content_logic_agent, normalized_product):
    result = content_logic_agent.generate(
        content_type="product_page",
        payload=normalized_product,
    )

    assert isinstance(result, dict)
    assert "overview" in result
    assert "ingredients" in result
    assert "benefits" in result
    assert "usage" in result
    assert "pricing" in result
    assert "safety" in result
    assert "skin_type" in result

    assert result["overview"]["title"] == normalized_product["name"]
    assert result["pricing"]["price"] == normalized_product["price"]


# -------------------------
# FAQ Tests
# -------------------------
def test_faq_generation(content_logic_agent, normalized_product):
    questions = [
        {"question": "How do I use this serum?", "category": "Usage"},
        {"question": "Is it safe for sensitive skin?", "category": "Safety"},
        {"question": "What is the price?", "category": "Pricing"},
        {"question": "What are the ingredients?", "category": "Ingredients"},
        {"question": "What does it do?", "category": "General"},
    ]

    payload = {
        "product": normalized_product,
        "questions": questions,
    }

    result = content_logic_agent.generate(
        content_type="faq",
        payload=payload,
    )

    assert "faqs" in result
    assert len(result["faqs"]) == len(questions)

    for faq in result["faqs"]:
        assert "question" in faq
        assert "answer" in faq
        assert isinstance(faq["answer"], str)


# -------------------------
# Comparison Tests
# -------------------------
def test_comparison_generation(
    content_logic_agent, normalized_product, fictional_product
):
    payload = {
        "product_a": normalized_product,
        "product_b": fictional_product,
    }

    result = content_logic_agent.generate(
        content_type="comparison",
        payload=payload,
    )

    assert "products" in result
    assert "price_comparison" in result
    assert "ingredients_comparison" in result
    assert "benefits_comparison" in result
    assert "summary" in result

    assert (
        result["price_comparison"]["cheaper_option"]
        == normalized_product["name"]
    )


# -------------------------
# Edge Case Tests
# -------------------------
def test_missing_side_effects_handled(content_logic_agent):
    product = {
        "name": "Test Serum",
        "concentration": "5%",
        "skin_type": ["Normal"],
        "ingredients": ["Ingredient A"],
        "benefits": ["Test Benefit"],
        "usage": "Test usage",
        "price": 500,
    }

    result = content_logic_agent.generate(
        content_type="product_page",
        payload=product,
    )

    assert "safety" in result
    assert "disclaimer" in result["safety"]


def test_invalid_content_type_raises_error(content_logic_agent):
    with pytest.raises(ValueError):
        content_logic_agent.generate(
            content_type="invalid_type",
            payload={},
        )
