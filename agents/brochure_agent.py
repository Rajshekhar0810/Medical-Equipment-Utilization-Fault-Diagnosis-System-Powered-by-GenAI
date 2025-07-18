# agents/brochure_agent.py

"""
Goal:
-----
The purpose of BrochureAgent is to extract key technical specifications from a medical equipment brochure.
These include:
- Maximum usage hours per day
- Temperature range (in Celsius)
- Pressure limits (in bar)
- Calibration interval (in days)

Steps Performed:
----------------
1. Load and extract text content from the brochure PDF
2. Construct a prompt for GPT
3. Call a language model using ModelLoader
4. Parse and return structured specifications in the LangGraph state
"""

import json
from utils.brochure_parser import extract_text_from_pdf
from utils.model_loader import ModelLoader
from utils.logger import log


class BrochureAgent:
    def __call__(self, state: dict) -> dict:
        """
        Extracts technical specifications from a medical equipment brochure using GPT.

        Args:
            state (dict): Contains 'brochure_path'

        Returns:
            dict: Updated state with 'extracted_specs' or error information
        """
        brochure_path = state.get("brochure_path")
        if not brochure_path:
            log("❌ 'brochure_path' not found in state.", level="ERROR")
            state["error"] = "Missing brochure_path"
            return state

        # Step 1: Extract brochure text from PDF
        try:
            log(f"📄 Extracting text from brochure: {brochure_path}")
            brochure_text = extract_text_from_pdf(brochure_path)
        except Exception as e:
            log(f"❌ Failed to read brochure: {e}", level="ERROR")
            state["error"] = f"PDF extract error: {e}"
            return state

        # Step 2: Build prompt from extracted text
        prompt = self._build_prompt(brochure_text)

        # Step 3: Send prompt to language model
        try:
            log("🤖 Sending prompt to GPT model...")
            llm = ModelLoader().load_model()
            response = llm.invoke(prompt)

            if not response:
                raise ValueError("No response from GPT model")

            # If it's a LangChain AIMessage object
            if hasattr(response, "content"):
                response_content = response.content
            else:
                response_content = str(response)

            log(f"🧾 GPT raw response: {response_content}")

            # Clean up response for valid JSON
            cleaned_response = (
                response_content.strip()
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            try:
                extracted_specs = json.loads(cleaned_response)
                log("✅ Specs extracted successfully from brochure.")
                state["extracted_specs"] = extracted_specs

            except Exception as e:
                raise ValueError(f"Invalid JSON format from GPT: {e} | Raw: {cleaned_response}")

        except Exception as e:
            log(f"⚠️ GPT parsing failed: {e}", level="ERROR")
            state["error"] = f"GPT error: {e}"

        return state

    def _build_prompt(self, brochure_text: str) -> str:
        """
        Creates a structured prompt for GPT to extract specifications.

        Args:
            brochure_text (str): The text extracted from the brochure PDF

        Returns:
            str: A formatted prompt for the language model
        """
        return f"""
You are an expert medical equipment analyst.

Below is a brochure for a hospital device. Extract the key specifications in **valid JSON** format with these keys:
- max_usage_hours_per_day (integer)
- temperature_range_celsius (string, like "60–70")
- pressure_limit_bar (float)
- calibration_interval_days (integer)

Respond with **JSON only**. Do not include any explanation or comments.

---
Brochure Text:
\"\"\"
{brochure_text}
\"\"\"
"""
