from graph.state import AgentState
from agents.parser_agent import ParserAgent


def parse_products_node(state: AgentState) -> AgentState:
    parser = ParserAgent()

    try:
        state.normalized_product_a = parser.parse(state.raw_product_a)
        state.normalized_product_b = parser.parse(state.raw_product_b)
        state.execution_log.append("Products parsed successfully")
    except Exception as e:
        state.parse_errors.append(str(e))
        state.execution_log.append("Parsing failed")

    return state
