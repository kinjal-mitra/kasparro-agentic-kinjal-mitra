from graph.state import AgentState
from agents.content_logic_agent import ContentLogicAgent


def build_faq_context_node(state: AgentState) -> AgentState:
    agent = ContentLogicAgent()

    context_map = {}

    for idx, q in enumerate(state.generated_questions):
        context_map[idx] = agent.build_context(
            product_data=state.normalized_product_a,
            category=q["category"]
        )

    state.faq_context_map = context_map
    state.execution_log.append("FAQ context built")

    return state
