"""
AI Assistant Configuration
Store your API keys and settings here or in environment variables
"""
import os

# AI Provider Configuration
# Options: 'mock' (free, no API key), 'claude', 'openai', 'openrouter'
AI_PROVIDER = os.getenv('AI_PROVIDER', 'mock')  # Default to 'mock' for free testing

# API Keys - IMPORTANT: Store these in environment variables, not in code
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'google/gemma-3-12b-it:free')

# Mock AI is used when no API keys are provided (100% free)
USE_MOCK_AI = AI_PROVIDER == 'mock' or (
    AI_PROVIDER != 'openrouter' and not ANTHROPIC_API_KEY and not OPENAI_API_KEY
)

# Model Configuration
AI_MODELS = {
    'claude': {
        'default': 'claude-3-5-sonnet-20241022',
        'fast': 'claude-3-haiku-20240307',
        'advanced': 'claude-3-opus-20240229'
    },
    'openai': {
        'default': 'gpt-4',
        'fast': 'gpt-3.5-turbo',
        'advanced': 'gpt-4-turbo'
    },
    'openrouter': {
        'default': OPENROUTER_MODEL,
        'fast': 'google/gemma-3-4b-it:free',
        'advanced': 'google/gemma-3-12b-it:free'
    }
}

# Default model to use
if AI_PROVIDER == 'openrouter':
    DEFAULT_MODEL = OPENROUTER_MODEL
else:
    DEFAULT_MODEL = AI_MODELS.get(AI_PROVIDER, {}).get('default', 'claude-3-5-sonnet-20241022')

# API Settings
MAX_TOKENS = 4096
TEMPERATURE = 0.7
TOP_P = 0.9

# Rate Limiting
MAX_REQUESTS_PER_MINUTE = 60
MAX_REQUESTS_PER_DAY = 1000

# Conversation Settings
MAX_CONVERSATION_HISTORY = 20  # Number of messages to keep in context
CONVERSATION_TIMEOUT_HOURS = 24

# Feature Flags
ENABLE_RESUME_ANALYSIS = True
ENABLE_JOB_MATCHING = True
ENABLE_INTERVIEW_PREP = True
ENABLE_SKILL_RECOMMENDATIONS = True

# Analysis Thresholds
MIN_SKILL_MATCH_SCORE = 0.6  # 60% minimum match to recommend a job
HIGH_MATCH_THRESHOLD = 0.8    # 80% for high match
