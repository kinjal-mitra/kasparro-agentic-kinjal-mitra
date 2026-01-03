from graph.state import AgentState
from agents.template_agent import TemplateAgent


def assemble_product_page_node(state: AgentState) -> AgentState:
    agent = TemplateAgent()
    state.product_page = agent.build_product_page(
        state.normalized_product_a
    )
    state.execution_log.append("Product page assembled")
    return state
