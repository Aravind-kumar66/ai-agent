from agent import AIAgent
from google.genai import errors

def main():

    print("=" * 60)
    print("🤖 GEMINI AI AGENT")
    print("=" * 60)

    print("Available tools:")
    print("  🧮 Calculator")
    print("  🌤️  Weather")
    print("  🌐 Web Search")
    print("  📚 Document RAG")
    print()
    print("Type 'exit' to quit.")
    print("=" * 60)

    agent = AIAgent()

    while True:

        try:
            user_input = input("\n🧑 You: ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\n\n🤖 Agent: Goodbye! 👋")
            break

        if not user_input:
            continue

        if user_input.lower() in {
            "exit",
            "quit",
            "bye",
        }:
            print("🤖 Agent: Goodbye! 👋")
            break

        try:

            answer = agent.run(user_input)

            print(f"\n🤖 Agent: {answer}")

        except Exception as e:

            print(
                f"\n❌ Agent error: {e}"
            )


if __name__ == "__main__":
    main()