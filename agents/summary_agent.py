# agents/summary_agent.py

import os
from utils.model_loader import ModelLoader
from utils.logger import log


class SummaryAgent:
    def __call__(self, state: dict) -> dict:
        """
        Generates a final risk report and maintenance plan using GPT.
        Saves the results in /reports/ folder and updates the state.

        Args:
            state (dict): Must contain 'violations'

        Returns:
            dict: Updated state with 'risk_report' and 'maintenance_plan'
        """
        violations = state.get("violations", [])
        if not violations:
            log("✅ No violations detected. SummaryAgent will skip.", level="INFO")
            state["risk_report"] = "No risk found. All equipment operating within limits."
            state["maintenance_plan"] = "Routine maintenance as per standard schedule."
            return state

        try:
            log("📝 Generating risk report and maintenance plan using GPT...")
            llm = ModelLoader().load_model()

            # Build the prompt
            prompt = self._build_summary_prompt(violations)
            response = llm.invoke(prompt)

            # Optional: split response into sections
            risk_section, plan_section = self._split_sections(response)

            state["risk_report"] = risk_section
            state["maintenance_plan"] = plan_section

            # Save to files
            os.makedirs("reports", exist_ok=True)
            with open("reports/risk_report.txt", "w") as f:
                f.write(risk_section)
            with open("reports/maintenance_plan.txt", "w") as f:
                f.write(plan_section)

            log("✅ Summary and maintenance plan saved to /reports/")
        except Exception as e:
            log(f"❌ SummaryAgent failed: {e}", level="ERROR")
            state["error"] = f"SummaryAgent error: {e}"

        return state

    def _build_summary_prompt(self, violations):
        """Prompt for GPT to write both sections."""
        return f"""
You are a hospital device monitoring AI.

Based on the following violation records, write:
1. A short **Risk Summary Report**
2. A suggested **Maintenance Plan**

Format:
### Risk Summary
...

### Maintenance Plan
...

Violation Data:
{violations}
"""

    def _split_sections(self, response: str):
        """Split GPT response into two sections based on headers."""
        try:
            parts = response.content.split("### Maintenance Plan")
            risk = parts[0].replace("### Risk Summary", "").strip()
            plan = parts[1].content.strip() if len(parts) > 1 else "Could not extract plan."
            return risk, plan
        except Exception:
            return response.content.strip(), "Plan section missing."
