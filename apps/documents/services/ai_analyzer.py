import json
import os
import google.generativeai as genai


class AIService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and api_key != "your_gemini_api_key_here":
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    def analyze_document(self,text_context:str)-> dict:
        # Fallback if no API key is configured yet (ensures offline dev works)
        if not self.model:
            return {
                "executive_summary": "Invoice processed in offline fallback mode.",
                "key_takeaways": ["Add GEMINI_API_KEY to .env to enable real AI summarization."],
                "topics": ["Invoicing", "Cloud Services"],
                "sentiment": "NEUTRAL",
                "tokens_used": 0
            }

        prompt = f"""
You are an executive document analyst. Read the document text below and return ONLY a valid JSON object matching this schema:
{{
  "executive_summary": "A concise 2-3 sentence summary of the document.",
  "key_takeaways": ["Key point 1", "Key point 2", "Key point 3"],
  "topics": ["Topic1", "Topic2"],
  "sentiment": "POSITIVE" | "NEGATIVE" | "NEUTRAL"
}}


Do NOT wrap the output in markdown fences. Return raw JSON text only.


Document Text:
{text_content[:10000]}
"""

        response = self.model.generate_content(prompt)
        raw_text = response.text.strip()

        # Clean accidental markdown fences if returned
        if raw_text.startswith("```json"):
            raw_text =raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]


        parsed = json.loads(raw_text.strip())
        parsed["tokens_used"] = getattr(response.usage_metadata, "total_token_count", 0)
        return parsed
    