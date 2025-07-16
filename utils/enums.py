from enum import Enum

class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class AI_Providers(Enum):
    OPENROUTER = "openRouter"
    ANTHROPIC = "anthropic"
    AZURE_OPENAI = "azureOpenAI"
    OPENAI = "openAI"
    LOCAL = "local"