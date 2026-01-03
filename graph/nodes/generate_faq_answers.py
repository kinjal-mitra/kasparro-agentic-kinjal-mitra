from graph.state import AgentState
from agents.answer_generation_agent import AnswerGenerationAgent
from llm.llm_client import LLMClient


def generate_faq_answers_node(state: AgentState) -> AgentState:
    llm = LLMClient()
    agent = AnswerGenerationAgent(llm)

    answers = []

    for idx, q in enumerate(state.generated_questions):
        try:
            result = agent.generate_answer(
                product=state.normalized_product_a,
                category=q["category"],
                question=q["question"],
                supporting_context=state.faq_context_map.get(idx, {})
            )

            
            answers.append({
                "category": q["category"],
                "question": result["question"],
                "answer": result["answer"],
            })

        except Exception as e:
            state.faq_answer_errors.append(str(e))

    state.faq_answers = answers
    state.execution_log.append("FAQ answers generated")

    return state
