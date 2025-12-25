from agents.comparison_agent import ComparisonAgent

agent = ComparisonAgent()

out = agent.compare(
    product_a={
        "product_name": "A",
        "key_ingredients": ["X"],
        "benefits": ["Y"],
        "price": 100
    },
    product_b={
        "product_name": "B",
        "key_ingredients": ["Z"],
        "benefits": ["W"],
        "price": 200
    }
)

print(out)
