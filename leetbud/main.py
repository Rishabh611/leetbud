"""
Main entry point for LeetBud application.
"""
import sys
from leetbud.cli.app import LeetBudCLI
from leetbud.config.settings import OPENAI_API_KEY

def main():
    """Main entry point."""
    if not OPENAI_API_KEY:
        print("Error: OpenAI API key not found")
        print("Please set the OPENAI_API_KEY environment variable")
        sys.exit(1)

    try:
        app = LeetBudCLI()
        app.start()
    except KeyboardInterrupt:
        print("\nGoodbye! Happy coding!")
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()