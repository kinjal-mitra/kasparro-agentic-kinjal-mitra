from graph.state import AgentState
from agents.question_generation_agent import QuestionGenerationAgent


def generate_questions_node(state: AgentState) -> AgentState:
    agent = QuestionGenerationAgent()

    questions = agent.generate(state.normalized_product_a)

    state.generated_questions = questions
    state.question_count = len(questions)
    state.question_generation_attempts += 1

    state.execution_log.append(
        f"Generated {state.question_count} questions "
        f"(attempt {state.question_generation_attempts})"
    )

    return state
