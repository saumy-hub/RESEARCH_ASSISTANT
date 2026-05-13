# Smart Research Assistant

A CLI-based Smart Research Assistant powered by the Groq API that autonomously decides which tools to call, loops through tool calls to gather information, and returns a clean, structured markdown research report.

## Features
- **Autonomous Tool Usage**: Chooses between web search, URL fetching, and a calculator based on the research query.
- **Agentic Loop**: Continues reasoning and calling tools until it has sufficient information.
- **Structured Outputs**: Produces a rigorous research report in a consistent Markdown format.
- **Rich CLI**: Beautiful terminal UI showing real-time tool usage and formatted reports.

## Setup Instructions

1. Clone this repository (or copy the files).
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Setup API Keys in `.env`:
   Create a `.env` file in the root directory and add your keys:
   ```
   GROQ_API_KEY=your_anthropic_key_here
   TAVILY_API_KEY=your_tavily_key_here
   ```

## Usage
Run the main script:
```bash
python main.py
```

### Sample Queries
- "What are the latest breakthroughs in solid-state batteries in 2025?"
- "Compare the energy density of Li-ion vs solid-state batteries in Wh/kg"
- "How does RISC-V compare to ARM for embedded systems?"
- "What is the current state of neuromorphic computing?"

## Architecture Diagram

```
User Query → Groq API → tool_use? → Dispatch Tool → Append Result → Loop
                  ↓
              end_turn → Return Report
```

