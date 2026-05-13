import os
import json
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console

from tools.web_search import web_search
from tools.fetch_url import fetch_url
from tools.calculator import calculate
from schemas.tool_schemas import TOOL_SCHEMAS

load_dotenv()
console = Console()

class ResearchAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        # Load system prompt
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "system_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()
            
        self.tool_dispatcher = {
            "web_search": web_search,
            "fetch_url": fetch_url,
            "calculator": calculate
        }
        
        self.history = [
            {"role": "system", "content": self.system_prompt}
        ]
        self.max_iterations = 10
        self.model = "llama-3.1-8b-instant"

    def dispatch_tool(self, tool_name: str, tool_input: dict) -> str:
        if tool_name not in self.tool_dispatcher:
            return json.dumps({"error": f"Tool {tool_name} not found"})
            
        tool_func = self.tool_dispatcher[tool_name]
        try:
            result = tool_func(**tool_input)
            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})

    def run(self, query: str) -> str:
        self.history.append({"role": "user", "content": query})
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
                max_tokens=4096
            )
            
            response_message = response.choices[0].message
            
            # If there's content but no tool calls, it's the final answer
            if not response_message.tool_calls:
                # Add it to history
                self.history.append({
                    "role": "assistant",
                    "content": response_message.content
                })
                return response_message.content
                
            # If there are tool calls, we process them
            # Groq/OpenAI expects the assistant message containing tool calls to be added first
            self.history.append(response_message)
            
            for tool_call in response_message.tool_calls:
                tool_name = tool_call.function.name
                
                try:
                    tool_input = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    tool_input = {}
                    
                console.log(f"[yellow]Tool called:[/yellow] {tool_name} with input {str(tool_input)[:100]}...")
                
                result_str = self.dispatch_tool(tool_name, tool_input)
                
                # Append tool results
                self.history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": result_str
                })
                
        return "Error: Max iterations reached before completing the research."
