from schemas.faq_schema import FAQPageSchema
from schemas.product_schema import ProductPageSchema
from schemas.comparison_schema import ComparisonPageSchema


def test_final_outputs_match_schemas(final_graph_state):
    FAQPageSchema(**final_graph_state["faq_page"])
    ProductPageSchema(**final_graph_state["product_page"])
    ComparisonPageSchema(**final_graph_state["comparison_page"])
