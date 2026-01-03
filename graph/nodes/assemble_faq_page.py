from graph.state import AgentState
from agents.template_agent import TemplateAgent


def assemble_faq_page_node(state: AgentState) -> AgentState:
    agent = TemplateAgent()
    state.faq_page = agent.build_faq_page(state.faq_answers)
    state.execution_log.append("FAQ page assembled")
    return state
