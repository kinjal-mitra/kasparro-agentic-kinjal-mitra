from graph.state import AgentState
from schemas.faq_schema import FAQPageSchema
from schemas.product_schema import ProductPageSchema
from schemas.comparison_schema import ComparisonPageSchema
from pydantic import ValidationError


def validate_final_output_node(state: AgentState) -> AgentState:
    errors = {}

    # -------------------------
    # FAQ validation
    # -------------------------
    try:
        FAQPageSchema(**state.faq_page)
    except ValidationError as e:
        errors["faq"] = e.errors()

    # -------------------------
    # Product page validation
    # -------------------------
    try:
        ProductPageSchema(**state.product_page)
    except ValidationError as e:
        errors["product"] = e.errors()

    # -------------------------
    # Comparison page validation
    # -------------------------
    try:
        ComparisonPageSchema(**state.comparison_page)
    except ValidationError as e:
        errors["comparison"] = e.errors()

    state.schema_validation_errors = errors

    if errors:
        state.execution_log.append(
            f"Schema validation failed: {list(errors.keys())}"
        )
    else:
        state.execution_log.append("All output schemas validated successfully")

    return state
