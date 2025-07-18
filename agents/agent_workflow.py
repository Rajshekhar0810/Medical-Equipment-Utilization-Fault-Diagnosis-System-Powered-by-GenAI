# Agents:
# 📄 BrochureAgent → Extracts specs from brochure PDF

# 📊 ValidatorAgent → Validates live data against those specs

# 📝 SummaryAgent → Writes risk report & maintenance plan

# 💬 ChatAgent → Answers technician’s queries

from typing import TypedDict, Optional, Dict, List  
from langgraph.graph import StateGraph, END, START
from agents.brochure_agent import BrochureAgent
from agents.validator_agent import ValidatorAgent
from agents.summary_agent import SummaryAgent
from agents.chat_agent import ChatAgent

# ✅ Define your state schema
class AgentState(TypedDict, total=False):
    brochure_path: str
    extracted_specs: Dict[str, str]
    data_path: str
    violations: List[str]
    violation_summary: str
    risk_report: str
    maintenance_plan: str
    user_query: str
    chat_response: str
    error: str

def build_agent_workflow():
    # ✅ Use the schema here, NOT a dict
    builder = StateGraph(AgentState)

    # Add your agents
    builder.add_node("BrochureAgent", BrochureAgent())
    builder.add_node("ValidatorAgent", ValidatorAgent())
    builder.add_node("SummaryAgent", SummaryAgent())
    builder.add_node("ChatAgent", ChatAgent())

    # Define edges
    builder.add_edge(START, "BrochureAgent")
    builder.add_edge("BrochureAgent", "ValidatorAgent")
    builder.add_edge("ValidatorAgent", "SummaryAgent")
    builder.add_edge("SummaryAgent", "ChatAgent")
    builder.add_edge("ChatAgent", END)

    return builder.compile()
