import json
from llm import llama_call
from promt_template import build_prompt
from tools import IOTTools
from datetime import datetime
import os
from registry import build_registry, SCHEMA_REGISTRY


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
import re
import json

class IOTAgent:
    def __init__(self, csv_path):
        self.tools = IOTTools(csv_path)
        self.registry = build_registry(csv_path)

    def run(self, question):
        trajectory = []
        final_answer = None

        prompt = build_prompt(question, [])  # No trajectory feedback
        response = llama_call(prompt)

        print("\nRAW LLM RESPONSE:\n", response)

        parsed = json.loads(response)

        if not parsed:
            print("No JSON found.")
            return None
        if parsed.get("final") is True:
            # Only allow final if at least one tool was called
            if not trajectory:
                print("Model attempted premature final. Forcing tool usage.")
                return {"error": "Model attempted premature final without tool call."}
            
            return parsed.get("answer")

        thought = parsed.get("thought")
        action = parsed.get("action")
        action_input = parsed.get("action_input", {})

        print("\nSELECTED ACTION:", action)
        print("ACTION INPUT:", action_input)

        trajectory.append({
            "thought": thought,
            "action": action,
            "action_input": action_input
        })
        
        tool_function = self.registry.get(action)

        if not tool_function:
            observation = {"error": "Invalid tool"}
        else:
            try:
                schema = SCHEMA_REGISTRY[action]
                validated = schema(**action_input)
                observation = tool_function(**validated.dict())
            except Exception as e:
                observation = {"error": str(e)}

        print("\nTOOL OUTPUT:\n", json.dumps(observation, indent=2))

        trajectory.append({"observation": observation})

        final_answer = observation

        log = {
            "question": question,
            "trajectory": trajectory,
            "final_answer": final_answer,
            "timestamp": datetime.now().isoformat()
        }

        log_path = os.path.join(LOG_DIR, f"log_{datetime.now().timestamp()}.json")
        with open(log_path, "w") as f:
            json.dump(log, f, indent=2)

        return final_answer
            
