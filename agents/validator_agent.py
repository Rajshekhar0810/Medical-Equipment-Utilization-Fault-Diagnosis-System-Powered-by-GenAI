#BrochureAgent extracts the specs from the brochure,
#the next logical step is to compare those specs with real-time data — that's the job of the ValidatorAgent

# agents/validator_agent.py

import pandas as pd
from utils.file_loader import load_usage_data
from utils.model_loader import ModelLoader
from utils.logger import log


class ValidatorAgent:
    def __call__(self, state: dict) -> dict:
        """
        Compares real-time equipment data with brochure specifications.
        Identifies violations and summarizes them using GPT.

        Args:
            state (dict): Input state containing specs and real-time data path.

        Returns:
            dict: Updated state with 'violations' and GPT summary.
        """
        specs = state.get("extracted_specs")
        data_path = state.get("data_path")

        if not specs or not data_path:
            log("❌ Missing extracted_specs or data_path", level="ERROR")
            state["error"] = "ValidatorAgent needs both specs and data"
            return state

        # Step 1: Load real-time data
        try:
            log(f"📊 Loading usage data from: {data_path}")
            df = load_usage_data(data_path)
        except Exception as e:
            log(f"❌ Failed to load usage data: {e}", level="ERROR")
            state["error"] = f"Data load error: {e}"
            return state

        # Step 2: Compare each row with specs
        violations = []
        for _, row in df.iterrows():
            device_id = row.get("device_id")
            usage = row.get("usage_hours", 0)
            temp = row.get("temperature", 0)
            pressure = row.get("pressure", 0)

            issues = []

            if specs.get("max_usage_hours_per_day") is not None:
                if usage > specs["max_usage_hours_per_day"]:
                    issues.append(f"Exceeded usage hours ({usage} > {specs['max_usage_hours_per_day']})")

            if specs.get("pressure_limit_bar") is not None:
                if pressure > specs["pressure_limit_bar"]:
                    issues.append(f"Exceeded pressure ({pressure} > {specs['pressure_limit_bar']})")

            if specs.get("temperature_range_celsius"):
                if not self._is_temp_within_range(temp, str(specs["temperature_range_celsius"])):
                    issues.append(f"Temperature {temp}°C outside range {specs['temperature_range_celsius']}")

            if issues:
                violations.append({
                    "device_id": device_id,
                    "issues": issues
                })

        state["violations"] = violations

        # Step 3: Ask GPT to summarize the violations
        if violations:
            try:
                prompt = self._build_violation_prompt(violations)
                llm = ModelLoader().load_model()
                summary = llm.invoke(prompt)
                state["violation_summary"] = str(summary)  # Fix: cast to string to avoid `.strip` error
                log("✅ GPT summarized the violations.")
            except Exception as e:
                log(f"⚠️ GPT failed to summarize violations: {e}", level="ERROR")
                state["violation_summary"] = "Summary generation failed."
        else:
            log("✅ No violations found.")
            state["violation_summary"] = "All equipment within safe limits."

        return state

    def _is_temp_within_range(self, temp, range_str):
        """Check if temperature is within the given range like '60–70'."""
        try:
            parts = range_str.replace("–", "-").split("-")
            min_temp = float(parts[0].strip())
            max_temp = float(parts[1].strip())
            return min_temp <= temp <= max_temp
        except Exception:
            return False

    def _build_violation_prompt(self, violations):
        """Create a prompt for GPT to summarize violations."""
        return f"""
You are a hospital device monitoring assistant.

Here is a list of equipment violations. Summarize what went wrong and suggest a general maintenance action:

{violations}

Respond in bullet points, short and actionable.
"""
