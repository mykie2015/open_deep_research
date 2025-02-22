import os
import ast
from enum import Enum
from dataclasses import dataclass, fields
from typing import Any, Optional, Dict

from langchain_core.runnables import RunnableConfig

DEFAULT_REPORT_STRUCTURE = """Use this structure to create a report on the user-provided topic:

1. Introduction (no research needed)
   - Brief overview of the topic area

2. Main Body Sections:
   - Each section should focus on a sub-topic of the user-provided topic
   
3. Conclusion
   - Aim for 1 structural element (either a list of table) that distills the main body sections 
   - Provide a concise summary of the report"""

class SearchAPI(Enum):
    PERPLEXITY = "perplexity"
    TAVILY = "tavily"

class PlannerProvider(Enum):
    OPENAI = "openai"
    GROQ = "groq"

class WriterProvider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GROQ = "groq"

def load_config(file_path):
    with open(file_path, 'r') as file:
        config_content = file.read()
        config_dictionary = ast.literal_eval(config_content)
        return config_dictionary

# Usage
config_file_path = 'config.ini'
config = load_config(config_file_path)

@dataclass(kw_only=True)
class Configuration:
    """Configuration including API keys and base URLs."""
    # API Keys and URLs
    openai_api_key: str = os.getenv('OPENAI_API_KEY', '')
    openai_base_url: str = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    anthropic_api_key: str = os.getenv('ANTHROPIC_API_KEY', '')
    groq_api_key: str = os.getenv('GROQ_API_KEY', '')
    tavily_api_key: str = os.getenv('TAVILY_API_KEY', '')
    perplexity_api_key: str = os.getenv('PERPLEXITY_API_KEY', '')

    # The configurable fields for the chatbot.
    report_structure: str = DEFAULT_REPORT_STRUCTURE # Defaults to the default report structure
    number_of_queries: int = 2 # Number of search queries to generate per iteration
    max_search_depth: int = 2 # Maximum number of reflection + search iterations
    planner_provider: PlannerProvider = PlannerProvider.OPENAI  # Defaults to OpenAI as provider
    planner_model: str = "o3-mini" # Defaults to OpenAI o3-mini as planner model
    writer_provider: WriterProvider = WriterProvider.ANTHROPIC # Defaults to Anthropic as provider
    writer_model: str = "claude-3-5-sonnet-latest" # Defaults to Anthropic as provider
    search_api: SearchAPI = SearchAPI.TAVILY # Default to TAVILY

    @classmethod
    def from_runnable_config(cls, config: Optional[Dict] = None) -> "Configuration":
        """Create Configuration instance with validation."""
        configurable = config.get("configurable", {}) if config else {}
        
        # Load all environment variables and config values
        values: Dict[str, Any] = {
            f.name: os.getenv(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }

        # Validate required keys
        if not values.get('openai_api_key'):
            raise ValueError("OPENAI_API_KEY is required in environment variables")

        return cls(**{k: v for k, v in values.items() if v is not None})
