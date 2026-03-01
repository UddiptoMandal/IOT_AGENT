import json

def build_prompt(question, trajectory):

    system_description = """
You are an IoT Monitoring Agent.

You do NOT have direct access to the dataset.
You MUST use tools to retrieve information.

The system uses a CSV dataset with columns:
- timestamp (ISO8601 string)
- site_name (string)
- asset_id (string)
- sensor_name (string)
- value (float)
- unit (string)

AVAILABLE TOOLS (STRICT SCHEMA):

1) sites
   Parameters: {}
   Returns: {"sites": [string]}

2) assets
   Parameters:
   {
     "site_name": string
   }

3) sensors
   Parameters:
   {
     "site_name": string,
     "asset_id": string
   }

4) history
   Parameters:
   {
     "site_name": string,
     "asset_id": string,
     "start": ISO8601 string,
     "final": ISO8601 string,
     "sensor_list": optional list of strings
   }

5) currenttime
   Parameters: {}

STRICT RULES:

- You MUST produce EXACTLY ONE JSON object.
- Do NOT produce text outside JSON.
- Do NOT explain anything.
- Do NOT simulate tool outputs.
- Do NOT invent parameters.
- Use ONLY parameters defined above.
- If parameters are missing, first retrieve required information using tools.
- Continue reasoning step-by-step using tool calls.
-You are NEVER allowed to answer a question without first calling a tool,
unless the question is about currenttime.
-If you return final=true without calling at least one tool,
your response will be rejected.
- When the answer is fully determined, return:

{
  "final": true,
  "answer": "your complete natural language answer"
}

Otherwise return:

{
  "thought": "brief reasoning",
  "action": "tool_name",
  "action_input": {...},
  "final": false
}

You must always include the "final" field.
"""

    few_shot = """
Example 1:

Question: what sites are there

{
  "thought": "I need to retrieve all available sites.",
  "action": "sites",
  "action_input": {},
  "final": false
}

Example 2:

Question: list assets at MAIN

{
  "thought": "I need to retrieve assets for site MAIN.",
  "action": "assets",
  "action_input": {"site_name": "MAIN"},
  "final": false
}

Example 3:

Question: list sensors for Chiller_1 at MAIN

{
  "thought": "I need to retrieve sensors for the specified site and asset.",
  "action": "sensors",
  "action_input": {"site_name": "MAIN", "asset_id": "Chiller_1"},
  "final": false
}

Example 4:

If sufficient information has already been gathered:

{
  "final": true,
  "answer": "MAIN has 2 assets: Chiller_1 and AHU_2."
}
"""

    history_text = ""

    for step in trajectory:
        if "thought" in step:
            history_text += "\nPrevious Step:\n"
            history_text += json.dumps(step, indent=2) + "\n"
        elif "observation" in step:
            history_text += "\nTool Observation:\n"
            history_text += json.dumps(step["observation"], indent=2) + "\n"

    return f"""
{system_description}

{few_shot}

Question:
{question}

{history_text}

Respond with EXACTLY ONE JSON object.
"""