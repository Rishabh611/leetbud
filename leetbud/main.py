import sys
import os
import threading

from openai import OpenAI
from dotenv import load_dotenv

from leetbud.leetcode_client import LeetCodeClient
from leetbud.llm_client import LLMClient
from leetbud.utils import loading_animation, format_response


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("OpenAI API key not found")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)


def main():
    leetcode = LeetCodeClient()
    llm_client = LLMClient()

    print("Welcome to LeetBud!")
    print("I'm your LeetBud assistant. I can help you solve LeetCode problems step by step.")

    print("What problem would you like help with today?")
    
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

        print(f"\nProblem {problem['id']}: {problem['title']} ({problem['difficulty']})\n")
        llm_client.setup_conversation(problem_description)
    

    print("Let's it rip!!!")

    while True:
        user_input = input("[You]: ").strip()

        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        try:
            stop_event = threading.Event()
            t = threading.Thread(target=loading_animation, args=(stop_event,))
            t.start()

            assistant_response = llm_client.get_response(user_input)

            stop_event.set()
            t.join()

            sys.stdout.write("\033[F")  # Move cursor up one line
            sys.stdout.write("\033[K")  # Clear the line
            
            # Add some spacing before the response
            print("\n")
            print(f"\033[94m[You]:\033[0m {user_input}")
            print(f"\n{format_response(assistant_response)}\n")
            
            if len(llm_client.messages) > 10:
                llm_client.messages = [llm_client.messages[0]] + llm_client.messages[-10:]

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()