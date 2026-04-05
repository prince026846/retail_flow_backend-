import os
import json
from openai import OpenAI
from typing import List, Dict, Any

class AIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and "your_openai_api_key_here" not in api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None

    def generate_strategic_insights(self, business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not self.client:
            print("❌ AI Client not initialized.")
            return []
        
        print(f"🧠 Generating AI insights for data: {json.dumps(business_data)[:200]}...")

        prompt = f"""
        As a world-class retail strategic advisor for RetailFlow, analyze the following business data and provide 5 highly actionable strategic insights.
        Data: {json.dumps(business_data)}
        
        Format your response as a JSON list of objects:
        [
          {{
            "id": "unique_string",
            "title": "Clear Actionable Title",
            "content": "Detailed strategic recommendation (2 sentences max)",
            "type": "success|warning|info|danger",
            "impact": "HIGH|MEDIUM|LOW|STRATEGIC"
          }}
        ]
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a retail business analyst specializing in inventory and sales optimization."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            
            print("✅ AI Response received successfully.")
            content = response.choices[0].message.content
            insights_data = json.loads(content)
            
            # Extract list from the JSON object if it's wrapped
            if isinstance(insights_data, dict):
                for key in ["insights", "data", "list"]:
                    if key in insights_data and isinstance(insights_data[key], list):
                        return insights_data[key]
                # If no key found, check if values are a list
                for val in insights_data.values():
                    if isinstance(val, list):
                        return val
            
            return insights_data if isinstance(insights_data, list) else []
            
        except Exception as e:
            print(f"AI insight generation failed: {e}")
            return []

ai_service = AIService()
