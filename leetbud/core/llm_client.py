"""
OpenAI LLM client for handling conversations.
"""
from typing import List, Dict, Any
from openai import OpenAI
from leetbud.config.settings import OPENAI_API_KEY, DEFAULT_MODEL, MAX_TOKENS, MAX_CONVERSATION_HISTORY

class LLMClient:
    def __init__(self, model: str = DEFAULT_MODEL):
        """Initialize the LLM client."""
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found in environment variables")
        
        self.model = model
        self._client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages: List[Dict[str, str]] = []

    def setup_conversation(self, problem_description: str):
        """Initialize conversation with problem context."""
        system_message = f"""
        You are a helpful LeetCode buddy that helps users solve coding problems through guidance, not by giving away complete solutions.
        
        The user is working on this problem:
        {problem_description}
        
        Your job is to:
        - Help break down the problem
        - Provide hints and guidance when asked
        - Review code snippets and suggest improvements
        - Identify optimization opportunities
        - Never give the full solution upfront
        - Be encouraging and supportive
        - When giving feedback on code, be specific about what works well and what could be improved
        """
        
        self.messages = [{"role": "system", "content": system_message}]

    def get_response(self, user_message: str) -> str:
        """Get response from the LLM for user message."""
        try:
            self.messages.append({"role": "user", "content": user_message})
            
            response = self._client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                max_tokens=MAX_TOKENS,
            )
            
            assistant_message = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": assistant_message})
            
            # Trim conversation history if needed
            if len(self.messages) > MAX_CONVERSATION_HISTORY:
                self.messages = [self.messages[0]] + self.messages[-MAX_CONVERSATION_HISTORY:]
            
            return assistant_message
            
        except Exception as e:
            raise RuntimeError(f"Error getting LLM response: {str(e)}") 