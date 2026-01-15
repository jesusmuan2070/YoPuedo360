"""
OpenAI Client
Centralized client for all OpenAI API calls
"""

import os
import json
from typing import Optional, Dict, Any, List
from openai import OpenAI


class OpenAIClient:
    """
    Centralized OpenAI client for YoPuedo360.
    Handles all API calls with consistent error handling and logging.
    """
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
    
    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        response_format: Optional[str] = None
    ) -> str:
        """
        Send a completion request to OpenAI.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system context
            temperature: Creativity (0.0 = deterministic, 1.0 = creative)
            max_tokens: Maximum response length
            response_format: "json" for JSON output
        
        Returns:
            The model's response text
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        if response_format == "json":
            kwargs["response_format"] = {"type": "json_object"}
        
        try:
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            raise
    
    def complete_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Get a JSON response from OpenAI.
        
        Returns:
            Parsed JSON as dictionary
        """
        response = self.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format="json"
        )
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response", "raw": response}
