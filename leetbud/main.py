import sys
import os
from leetbud.leetcode_client import LeetCodeClient
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("OpenAI API key not found")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)
MODEL = "gpt-3.5-turbo"


def main():
    leetcode = LeetCodeClient()
    print("Enter problem name or number")

    problem_query = input("[Problem ID/Name]: ").strip()

    problem = leetcode.get_problem(problem_query)

    if not problem:
        print("Count not find problem")
        return
    else:
        problem_description = (
            f"Problem {problem['id']}: {problem['title']} ({problem['difficulty']})\n\n"
            f"{problem['description']}\n\n"
            f"Test cases:\n{problem['test_cases']}\n\n"
        )
        problem_title = problem['title']

        print(f"\nProblem {problem['id']}: {problem['title']} ({problem['difficulty']})\n")

    messages = [
        {"role": "system", "content": f"""
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
        """},
        {"role": "assistant", "content": f"I'll help you solve the '{problem_title}' problem step by step. Let's break down the problem first. What's your initial understanding of the problem, and do you have any ideas on how to approach it?"}
    ]

    print("Let's it rip!!!")

    while True:
        user_input = input("[You]: ").strip()

        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            print(f"Assistant is thinking")
            response = client.chat.completions.create(
                model = MODEL,
                max_tokens = 1500,
                messages = messages
            )

            assistant_response = response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_response})

            sys.stdout.write("\033[F]")
            sys.stdout.write("\033[K")
            print(f"[Assistant]: {assistant_response}")

            if len(messages) > 10:
                messages = [messages[0]] + messages[-10:]

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()