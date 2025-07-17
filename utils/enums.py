from enum import Enum

class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL= "tool"

class AI_Providers(Enum):
    OPENROUTER = "openRouter"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"
    AZURE_OPENAI = "azureOpenAI"
    OPENAI = "openAI"
    LOCAL = "local"

class Numbers(Enum):
    MAX_MESSAGES = 20