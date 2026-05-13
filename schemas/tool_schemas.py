TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information on a topic. Use this when you need facts, recent events, or information you don't already know. Returns a list of results with titles, URLs, and snippets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query. Be specific and use keywords. Example: 'latest developments quantum computing 2025'"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Number of results to return. Default 5, max 10."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_url",
            "description": "Fetch and read the full content of a webpage. Use this after web_search when you need more detail from a specific URL. Returns cleaned text content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The full URL to fetch. Must start with http:// or https://"
                    },
                    "max_chars": {
                        "type": "integer",
                        "description": "Maximum characters to return. Default 4000."
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate a mathematical expression. Use for any numeric calculations needed in your research — statistics, comparisons, unit conversions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A math expression as a string. Example: '(42 * 1.15) / 100'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]
