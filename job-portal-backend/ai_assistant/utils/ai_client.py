"""
AI Client for interacting with AI APIs (Claude, GPT, etc.)
Automatically uses mock AI when no API key is available (100% free)
"""
import time
from typing import List, Dict, Optional
from django.conf import settings
from ..config import (
    AI_PROVIDER,
    ANTHROPIC_API_KEY,
    OPENAI_API_KEY,
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    DEFAULT_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    USE_MOCK_AI
)


class AIClient:
    """
    Unified client for AI API interactions
    Supports multiple providers (Claude, OpenAI, etc.)
    """

    def __init__(self, provider: str = AI_PROVIDER):
        self.provider = provider
        self.model = DEFAULT_MODEL
        self.use_mock = USE_MOCK_AI

        # Use mock AI if no API keys are configured (free mode)
        if self.use_mock or provider == 'mock':
            self.provider = 'mock'
            self.use_mock = True
            print("[INFO] Using FREE Mock AI (no API key required)")
            return

        # Initialize the appropriate client
        if provider == 'claude':
            self._init_claude_client()
        elif provider == 'openai':
            self._init_openai_client()
        elif provider == 'openrouter':
            self._init_openrouter_client()
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")

    def _init_claude_client(self):
        """Initialize Anthropic Claude client"""
        if not ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. "
                "Please set it in your environment variables or config.py"
            )

        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        except ImportError:
            raise ImportError(
                "anthropic package not installed. "
                "Install it with: pip install anthropic"
            )

    def _init_openai_client(self):
        """Initialize OpenAI client"""
        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY not found. "
                "Please set it in your environment variables or config.py"
            )

        try:
            import openai
            self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        except ImportError:
            raise ImportError(
                "openai package not installed. "
                "Install it with: pip install openai"
            )

    def _init_openrouter_client(self):
        """Initialize OpenRouter client (uses OpenAI SDK with custom base URL)"""
        if not OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY not found. "
                "Please set it in your environment variables or .env file"
            )

        try:
            import openai
            self.client = openai.OpenAI(
                api_key=OPENROUTER_API_KEY,
                base_url="https://openrouter.ai/api/v1"
            )
            self.model = OPENROUTER_MODEL
            print(f"[INFO] Using OpenRouter with model: {self.model}")
        except ImportError:
            raise ImportError(
                "openai package not installed. "
                "Install it with: pip install openai"
            )

    def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: int = MAX_TOKENS,
        temperature: float = TEMPERATURE
    ) -> Dict:
        """
        Generate AI response from messages

        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt to set context
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)

        Returns:
            Dict with response data including:
            - content: The generated text
            - usage: Token usage info
            - model: Model used
            - response_time_ms: Response time in milliseconds
        """
        start_time = time.time()

        try:
            # Use mock AI if configured (free mode)
            if self.use_mock or self.provider == 'mock':
                from .mock_ai_client import get_mock_ai_client
                mock_client = get_mock_ai_client()
                return mock_client.generate_response(
                    messages, system_prompt, max_tokens, temperature
                )

            if self.provider == 'claude':
                result = self._generate_claude_response(
                    messages, system_prompt, max_tokens, temperature
                )
            elif self.provider == 'openai':
                result = self._generate_openai_response(
                    messages, system_prompt, max_tokens, temperature
                )
            elif self.provider == 'openrouter':
                result = self._generate_openrouter_response(
                    messages, system_prompt, max_tokens, temperature
                )
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")

            response_time_ms = int((time.time() - start_time) * 1000)
            result['response_time_ms'] = response_time_ms
            result['success'] = True

            return result

        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            return {
                'content': '',
                'error': str(e),
                'success': False,
                'response_time_ms': response_time_ms
            }

    def _generate_claude_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float
    ) -> Dict:
        """Generate response using Claude API"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt if system_prompt else "You are a helpful AI assistant.",
            messages=messages
        )

        return {
            'content': response.content[0].text,
            'usage': {
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens
            },
            'model': response.model,
            'stop_reason': response.stop_reason
        }

    def _generate_openai_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float
    ) -> Dict:
        """Generate response using OpenAI API"""

        # Add system message if provided
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return {
            'content': response.choices[0].message.content,
            'usage': {
                'input_tokens': response.usage.prompt_tokens,
                'output_tokens': response.usage.completion_tokens
            },
            'model': response.model,
            'finish_reason': response.choices[0].finish_reason
        }

    def _generate_openrouter_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float
    ) -> Dict:
        """Generate response using OpenRouter API"""

        # For Gemma models, include system prompt in the first user message
        # since they don't support system messages
        if system_prompt and 'gemma' in self.model.lower():
            # Prepend system prompt to the first user message
            if messages and messages[0]['role'] == 'user':
                messages[0]['content'] = f"{system_prompt}\n\n{messages[0]['content']}"
        elif system_prompt:
            # For other models that support system messages
            messages = [{"role": "system", "content": system_prompt}] + messages

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return {
            'content': response.choices[0].message.content,
            'usage': {
                'input_tokens': response.usage.prompt_tokens,
                'output_tokens': response.usage.completion_tokens
            },
            'model': response.model,
            'finish_reason': response.choices[0].finish_reason
        }

    def analyze_text(
        self,
        text: str,
        analysis_type: str,
        context: Optional[Dict] = None
    ) -> str:
        """
        Analyze text with specific instructions

        Args:
            text: Text to analyze
            analysis_type: Type of analysis (resume, job_description, etc.)
            context: Additional context for analysis

        Returns:
            Analysis result as string
        """
        # Use mock AI if configured
        if self.use_mock or self.provider == 'mock':
            from .mock_ai_client import get_mock_ai_client
            mock_client = get_mock_ai_client()
            return mock_client.analyze_text(text, analysis_type, context)

        from .prompt_templates import get_analysis_prompt

        system_prompt = get_analysis_prompt(analysis_type, context)

        messages = [
            {"role": "user", "content": text}
        ]

        result = self.generate_response(
            messages=messages,
            system_prompt=system_prompt
        )

        return result.get('content', '')


# Singleton instance
_ai_client_instance = None


def get_ai_client() -> AIClient:
    """Get or create AI client instance"""
    global _ai_client_instance
    if _ai_client_instance is None:
        _ai_client_instance = AIClient()
    return _ai_client_instance
