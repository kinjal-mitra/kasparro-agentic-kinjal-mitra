import pytest
from agents.template_agent import TemplateAgent


@pytest.fixture
def template_agent():
    return TemplateAgent()


@pytest.fixture
def product_page_blocks():
    return {
        "overview": {"title": "GlowBoost", "summary": "Test summary"},
        "ingredients": {"key_ingredients": ["A", "B"], "ingredient_count": 2},
        "benefits": {"primary_benefits": ["X"], "benefit_count": 1},
        "usage": {"how_to_use": "Apply daily", "recommended_time": "Morning"},
        "pricing": {"price": 699, "currency": "INR"},
        "safety": {"side_effects": "None", "disclaimer": "Patch test"},
        "skin_type": {"suitable_for": ["Oily"], "not_recommended_for": []},
    }


@pytest.fixture
def faq_blocks():
    return {
        "faq_count": 2,
        "faqs": [
            {
                "question": "How to use?",
                "category": "Usage",
                "answer": "Apply daily",
            },
            {
                "question": "Is it safe?",
                "category": "Safety",
                "answer": "Patch test recommended",
            },
        ],
    }


@pytest.fixture
def comparison_blocks():
    return {
        "products": {
            "product_a": "GlowBoost",
            "product_b": "RadiantPlus",
        },
        "price_comparison": {
            "GlowBoost": 699,
            "RadiantPlus": 799,
            "cheaper_option": "GlowBoost",
        },
        "ingredients_comparison": {
            "GlowBoost": ["A", "B"],
            "RadiantPlus": ["A", "C"],
            "common_ingredients": ["A"],
        },
        "benefits_comparison": {
            "GlowBoost": ["Brightening"],
            "RadiantPlus": ["Hydration"],
        },
        "summary": "Comparison summary",
    }


# -------------------------
# Product Page Tests
# -------------------------
def test_render_product_page(template_agent, product_page_blocks):
    result = template_agent.render(
        content_type="product_page",
        structured_blocks=product_page_blocks,
    )

    assert result["page_type"] == "product_page"
    assert "product_overview" in result
    assert "ingredients_section" in result
    assert "benefits_section" in result
    assert "usage_section" in result
    assert "pricing_section" in result
    assert "safety_section" in result
    assert "skin_type_section" in result


# -------------------------
# FAQ Page Tests
# -------------------------
def test_render_faq_page(template_agent, faq_blocks):
    result = template_agent.render(
        content_type="faq",
        structured_blocks=faq_blocks,
    )

    assert result["page_type"] == "faq"
    assert result["total_questions"] == faq_blocks["faq_count"]
    assert len(result["questions"]) == faq_blocks["faq_count"]


# -------------------------
# Comparison Page Tests
# -------------------------
def test_render_comparison_page(template_agent, comparison_blocks):
    result = template_agent.render(
        content_type="comparison",
        structured_blocks=comparison_blocks,
    )

    assert result["page_type"] == "comparison"
    assert "products_compared" in result
    assert "price_comparison" in result
    assert "ingredients_comparison" in result
    assert "benefits_comparison" in result
    assert "summary" in result


# -------------------------
# Error Handling Tests
# -------------------------
def test_invalid_content_type_raises_error(template_agent):
    with pytest.raises(ValueError):
        template_agent.render(
            content_type="invalid_type",
            structured_blocks={},
        )
