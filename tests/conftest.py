import pytest
import json
from pathlib import Path
from graph.graph import build_graph
from graph.state import AgentState


@pytest.fixture
def sample_product_data():
    return {
        "product_name": "GlowBoost Vitamin C Serum",
        "concentration": "10% Vitamin C",
        "skin_type": ["Oily", "Combination"],
        "key_ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "benefits": ["Brightening", "Fades dark spots"],
        "how_to_use": "Apply 2–3 drops in the morning before sunscreen",
        "side_effects": "Mild tingling for sensitive skin",
        "price": "₹699",
    }


@pytest.fixture
def sample_fictional_product():
    return {
        "product_name": "RadiantPlus Serum",
        "concentration": "8% Vitamin C",
        "skin_type": ["Dry"],
        "key_ingredients": ["Vitamin C", "Niacinamide"],
        "benefits": ["Hydration", "Glow"],
        "how_to_use": "Apply at night",
        "side_effects": "None",
        "price": "₹799",
    }


@pytest.fixture
def final_graph_state(sample_product_data, sample_fictional_product):
    graph = build_graph()
    state = AgentState(
        raw_product_a=sample_product_data,
        raw_product_b=sample_fictional_product,
    )
    return graph.invoke(state)
