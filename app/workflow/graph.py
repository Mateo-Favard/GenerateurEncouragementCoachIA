from langgraph.graph import END, StateGraph

from app.models.workflow import CoachingWorkflowState
from app.services.llm.base import LLMProvider
from app.services.tts.base import TTSProvider
from app.workflow.nodes import make_generate_text_node, make_synthesize_audio_node


def should_continue(state: CoachingWorkflowState) -> str:
    if state.get("error"):
        return "end"
    return "synthesize_audio"


def build_coaching_graph(
    llm: LLMProvider,
    tts: TTSProvider,
    max_tokens: int = 2048,
) -> StateGraph:
    graph = StateGraph(CoachingWorkflowState)

    graph.add_node("generate_text", make_generate_text_node(llm, max_tokens))
    graph.add_node("synthesize_audio", make_synthesize_audio_node(tts))

    graph.set_entry_point("generate_text")
    graph.add_conditional_edges("generate_text", should_continue, {
        "synthesize_audio": "synthesize_audio",
        "end": END,
    })
    graph.add_edge("synthesize_audio", END)

    return graph.compile()
