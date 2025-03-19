"""
Command-line interface for LeetBud application.
"""
import sys
from typing import Optional

from leetbud.core.leetcode_client import LeetCodeClient
from leetbud.core.llm_client import LLMClient
from leetbud.ui.display import Display, LoadingSpinner

class LeetBudCLI:
    def __init__(self):
        """Initialize the CLI application."""
        self.leetcode = LeetCodeClient()
        self.llm = LLMClient()
        self.display = Display()

    def start(self):
        """Start the CLI application."""
        self._print_welcome()
        
        problem = self._get_problem()
        if not problem:
            print("Could not find problem. Please try again.")
            sys.exit(1)

        self._setup_problem(problem)
        self._start_conversation_loop()

    def _print_welcome(self):
        """Print welcome message."""
        print("\nWelcome to LeetBud!")
        print("I'm your LeetBud assistant. I can help you solve LeetCode problems step by step.")
        print("\nWhat problem would you like help with today?")
        print("Enter problem name or number")

    def _get_problem(self) -> Optional[dict]:
        """Get problem details from user input."""
        problem_query = input("[Problem ID/Name]: ").strip()
        return self.leetcode.get_problem(problem_query)

    def _setup_problem(self, problem: dict):
        """Setup the problem context."""
        problem_description = (
            f"Problem {problem['id']}: {problem['title']} ({problem['difficulty']})\n\n"
            f"{problem['description']}\n\n"
            f"Test cases:\n{problem['test_cases']}\n\n"
        )

        print(f"\nProblem {problem['id']}: {problem['title']} ({problem['difficulty']})\n")
        self.llm.setup_conversation(problem_description)
        print("\nLet's solve this problem together!")

    def _start_conversation_loop(self):
        """Start the main conversation loop."""
        while True:
            user_input = input("[You]: ").strip()

            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye! Happy coding!")
                break

            try:
                # Show loading animation
                spinner = LoadingSpinner()
                spinner.start()

                # Get response from LLM
                assistant_response = self.llm.get_response(user_input)

                # Stop loading animation and clear line
                spinner.stop()
                self.display.clear_line()

                # Display the conversation
                print("\n" + self.display.format_user_message(user_input))
                print(f"\n{self.display.draw_box(assistant_response)}\n")

            except Exception as e:
                print(f"\nError: {str(e)}")
                print("Please try again or type 'exit' to quit.") 