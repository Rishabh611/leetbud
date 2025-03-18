import os

from openai import OpenAI

class LLMClient:
    def __init__(self, model="gpt-4o"):
        self.model = model
        self._client = self._initiate_client()

    def _initiate_client(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("OpenAI API key not found")

        return OpenAI(api_key=api_key)

    def setup_conversation(self, problem):
        problem_str = str(problem)

        self.messages = [
            {"role": "system", "content": f"""
            You are a helpful LeetCode buddy that helps users solve coding problems through guidance, not by giving away complete solutions.
            
            The user is working on this problem:
            {problem_str}
            
            Your job is to:
            - Help break down the problem
            - Provide hints and guidance when asked
            - Review code snippets and suggest improvements
            - Identify optimization opportunities
            - Never give the full solution upfront
            - Be encouraging and supportive
            - When giving feedback on code, be specific about what works well and what could be improved
            """}
        ]

    
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_completion(self, messages, max_tokens=1500):
        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content

    def get_response(self, user_mesage):
        self.add_message("user", user_mesage)
        try:
            response = self.get_completion(self.messages)
            self.add_message("assistant", response)

            if len(self.messages) > 10:
                self.messages = [self.messages[0]] + self.messages[-10:]
            return response
        except Exception as e:
            print("An error occurred:", e) 
            return "An error occurred. Please try again later."


   