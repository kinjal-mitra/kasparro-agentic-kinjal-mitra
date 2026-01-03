from graph.state import AgentState


def validate_question_count_node(state: AgentState) -> AgentState:
    if state.question_count < state.min_required_questions:
        if state.question_generation_attempts >= state.max_question_generation_attempts:
            state.retry_flags["questions"] = False
            state.schema_validation_errors["questions"] = (
                f"Failed to generate >=15 questions after "
                f"{state.question_generation_attempts} attempts"
            )
            state.execution_log.append(
                "Max question generation retries reached — aborting retry"
            )
        else:
            state.retry_flags["questions"] = True
            state.execution_log.append(
                f"FAQ count < 15, retrying "
                f"(attempt {state.question_generation_attempts})"
            )
    else:
        state.retry_flags["questions"] = False
        state.execution_log.append("FAQ count validated")

    return state


def route_after_question_validation(state: AgentState) -> str:
    """
    LangGraph router:
    - retry only if allowed
    - otherwise continue forward
    """
    if state.retry_flags.get("questions"):
        return "retry"
    return "continue"
