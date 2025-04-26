from langgraph.graph import StateGraph
from agents.research_agent import ResearchAgent
from agents.answer_agent import AnswerAgent
from typing import Dict, List, Any, TypedDict

class GraphState(TypedDict):
    research_data: List[Dict[str, str]] 
    answer: str

def build_graph(question: str):
    researcher = ResearchAgent(query=question, max_results=3)
    
    # Node 1: Collect information
    def collect(state: Dict[str, Any]) -> Dict[str, Any]:
        pages = researcher.gather_information()
        return {"research_data": pages, **state}

    # Node 2: Draft an answer
    def draft(state: Dict[str, Any]) -> Dict[str, Any]:
        answerer = AnswerAgent()
        # Build context from research data
        context = "\n".join([page["text"] for page in state["research_data"]])
        response = answerer.draft_answer(context, question)
        return {"answer": response, **state}

    builder = StateGraph(GraphState)
    builder.add_node("Collect", collect)
    builder.add_node("Draft", draft)

    builder.set_entry_point("Collect")
    builder.add_edge("Collect", "Draft")

    graph = builder.compile()
    return graph
