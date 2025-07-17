TOOL_REGISTRY = {
    "weather_tool": {
        "name": "weather",
        "description": "Get current weather information for a specified location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location to get the weather for."
                }
            },
            "required": ["location"]
        }
    },
}