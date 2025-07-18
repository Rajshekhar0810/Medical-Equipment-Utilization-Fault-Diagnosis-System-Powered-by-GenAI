#Let technicians, admins, or users ask questions like: 1) “Which devices have exceeded pressure limits?”
# 2) “When should calibration be scheduled?” , 3) “Summarize risks found so far.” and return intelligent answers using context (e.g., violations, extracted specs, etc.).
# agents/chat_agent.py

from utils.model_loader import ModelLoader
from utils.logger import log


class ChatAgent:
    def __call__(self, state: dict) -> dict:
        """
        Handles user queries based on available extracted specs and violations.

        Args:
            state (dict): Should contain 'user_query', may include 'violations', 'extracted_specs', etc.

        Returns:
            dict: Updated state with 'chat_response'
        """
        query = state.get("user_query")
        if not query:
            log("⚠️ No user_query found in state.", level="WARNING")
            state["chat_response"] = "No question received."
            return state

        # Compose context from previous outputs
        context = self._build_context(state)
        prompt = self._build_prompt(query, context)

        try:
            llm = ModelLoader().load_model()
            log("💬 Sending technician query to GPT...")
            response = llm.invoke(prompt)
            state["chat_response"] = str(response).strip()
        except Exception as e:
            log(f"❌ ChatAgent failed: {e}", level="ERROR")
            state["chat_response"] = f"ChatAgent error: {e}"

        return state

    def _build_context(self, state):
        """Builds the text context from prior agents."""
        parts = []
        if state.get("extracted_specs"):
            parts.append(f"Equipment Specs:\n{state['extracted_specs']}")
        if state.get("violations"):
            parts.append(f"Violations:\n{state['violations']}")
        if state.get("violation_summary"):
            parts.append(f"Summary:\n{state['violation_summary']}")
        return "\n\n".join(parts)

    def _build_prompt(self, question, context):
        """Final GPT prompt with user query and available context."""
        return f"""
You are a smart hospital assistant helping technicians.

Based on the following data, answer the user's question clearly.

{context}

User's Question:
{question}
"""







