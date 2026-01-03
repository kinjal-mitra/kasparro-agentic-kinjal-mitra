from graph.graph import build_graph
from graph.state import AgentState


def test_graph_runs_end_to_end(sample_product_data, sample_fictional_product):
    graph = build_graph()

    initial_state = AgentState(
        raw_product_a=sample_product_data,
        raw_product_b=sample_fictional_product,
    )

    final_state = graph.invoke(initial_state)

    # Core outputs exist
    assert final_state["faq_page"] is not None
    assert final_state["product_page"] is not None
    assert final_state["comparison_page"] is not None

    # Execution log exists
    assert "execution_log" in final_state
    assert len(final_state["execution_log"]) > 0
