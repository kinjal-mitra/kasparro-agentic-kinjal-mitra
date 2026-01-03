from langgraph.graph import StateGraph, END

from graph.state import AgentState

from graph.nodes.parse_products import parse_products_node
from graph.nodes.generate_questions import generate_questions_node
from graph.nodes.validate_question_count import validate_question_count_node, route_after_question_validation
from graph.nodes.build_faq_context import build_faq_context_node
from graph.nodes.generate_faq_answers import generate_faq_answers_node
from graph.nodes.assemble_faq_page import assemble_faq_page_node
from graph.nodes.assemble_product_page import assemble_product_page_node
from graph.nodes.generate_comparison import generate_comparison_node
from graph.nodes.validate_final_output import validate_final_output_node


def build_graph():
    """
    Builds and returns the LangGraph execution graph.
    """

    graph = StateGraph(AgentState)

    # --------------------------------------------------
    # Register nodes
    # --------------------------------------------------
    graph.add_node("parse_products", parse_products_node)
    graph.add_node("generate_questions", generate_questions_node)
    graph.add_node("validate_question_count", validate_question_count_node)
    graph.add_node("build_faq_context", build_faq_context_node)
    graph.add_node("generate_faq_answers", generate_faq_answers_node)
    graph.add_node("assemble_faq_page", assemble_faq_page_node)
    graph.add_node("assemble_product_page", assemble_product_page_node)
    graph.add_node("generate_comparison", generate_comparison_node)
    graph.add_node("validate_final_output", validate_final_output_node)

    # --------------------------------------------------
    # Define edges 
    # --------------------------------------------------
    graph.set_entry_point("parse_products")

    graph.add_edge("parse_products", "generate_questions")
    graph.add_edge("generate_questions", "validate_question_count")

    # --------------------------------------------------
    # Conditional edge (FAQ count enforcement)
    # --------------------------------------------------
    graph.add_conditional_edges(
        "validate_question_count",
        route_after_question_validation,  # Added router function
        {
            "retry": "generate_questions",
            "continue": "build_faq_context",
        },
    )

    # --------------------------------------------------
    # Continue after validation
    # --------------------------------------------------
    graph.add_edge("build_faq_context", "generate_faq_answers")
    graph.add_edge("generate_faq_answers", "assemble_faq_page")
    graph.add_edge("assemble_faq_page", "assemble_product_page")
    graph.add_edge("assemble_product_page", "generate_comparison")
    graph.add_edge("generate_comparison", "validate_final_output")

    # --------------------------------------------------
    # Terminal
    # --------------------------------------------------
    graph.add_edge("validate_final_output", END)

    return graph.compile()
