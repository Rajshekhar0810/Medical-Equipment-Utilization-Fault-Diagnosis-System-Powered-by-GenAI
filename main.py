# main.py

from agents.agent_workflow import build_agent_workflow
from utils.logger import log
from langchain_openai import ChatOpenAI

def main():
    # 1. Build the full agent graph
    graph = build_agent_workflow()

    # 2. Define initial input state
    initial_state = {
        "brochure_path": r"docs\MRI_brochure.pdf",
        "data_path":  r"data\live_equipment_data.csv",
        "user_query": "Which devices are at high risk and what actions should be taken?"
    }

    log("🚀 Starting Smart Equipment Diagnosis Workflow...\n")
    
    # 3. Run the graph
    final_state = graph.invoke(initial_state)

    # 4. Output results
    print("\n🔍 Final Outputs")
    print("----------------------------")
    print("🛠 Violation Summary:\n", final_state.get("violation_summary", "No summary"))
    print("\n📋 Risk Report:\n", final_state.get("risk_report", "N/A"))
    print("\n🧰 Maintenance Plan:\n", final_state.get("maintenance_plan", "N/A"))
    print("\n💬 Chat Response:\n", final_state.get("chat_response", "No response"))
    print("----------------------------")

    if final_state.get("error"):
        log(f"⚠️ Error encountered: {final_state['error']}", level="ERROR")

if __name__ == "__main__":
    main()
