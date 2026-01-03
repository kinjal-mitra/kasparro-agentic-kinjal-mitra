from graph.graph import build_graph
from graph.state import AgentState


def test_question_generation_retry_guard(sample_product_data, sample_fictional_product):
    graph = build_graph()

    initial_state = AgentState(
        raw_product_a=sample_product_data,
        raw_product_b=sample_fictional_product,
        max_question_generation_attempts=1,
        min_required_questions=100,
    )

    final_state = graph.invoke(initial_state)

    assert any(
        "Max question generation retries reached" in entry
        for entry in final_state["execution_log"]
    )
