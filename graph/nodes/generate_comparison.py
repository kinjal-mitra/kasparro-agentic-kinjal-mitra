from graph.state import AgentState
from agents.comparison_agent import ComparisonAgent
from agents.template_agent import TemplateAgent


def generate_comparison_node(state: AgentState) -> AgentState:
    comparison_agent = ComparisonAgent()
    template_agent = TemplateAgent()

    comparison_blocks = comparison_agent.compare(
        state.normalized_product_a,
        state.normalized_product_b
    )

    state.comparison_page = template_agent.build_comparison_page(
        comparison_blocks
    )

    state.execution_log.append("Comparison page generated")
    return state
