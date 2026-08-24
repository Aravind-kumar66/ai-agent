from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL

# Import your existing tool functions
from tools.calculator import calculate
from tools.weather import get_weather
from tools.web_search import search_web
from rag.rag_tool import DocumentRAG

# 1. Initialize RAG and define TOOL_MAP for execute_tool
rag_instance = DocumentRAG()

TOOL_MAP = {
    "calculate": calculate,
    "get_weather": get_weather,
    "search_web": search_web,
    "search_pdf_documents": rag_instance.search,
}


# 2. Define the missing execute_tool function called in run()
def execute_tool(name: str, args: dict):
    func = TOOL_MAP.get(name)
    if func:
        return func(**args)
    return f"Tool {name} not found."


# --------------------------------------------------
# Agent
# --------------------------------------------------

class AIAgent:

    def __init__(self):
        # 3. Create client instance and config before creating chat
        self.client = genai.Client(api_key=GEMINI_API_KEY)

        config = types.GenerateContentConfig(
            system_instruction="You are a helpful AI assistant with tools.",
            tools=list(TOOL_MAP.values()),
        )

        # 4. Use self.client instead of undefined client
        self.chat = self.client.chats.create(
            model=GEMINI_MODEL,
            config=config,
        )

    def run(self, user_message, max_tool_calls=5):

        response = self.chat.send_message(
            message=user_message
        )

        tool_call_count = 0

        while True:

            function_calls = []

            # 5. Guard against empty response candidates
            if response.candidates:
                for candidate in response.candidates:

                    if not candidate.content or not candidate.content.parts:
                        continue

                    for part in candidate.content.parts:

                        if part.function_call:
                            function_calls.append(
                                part.function_call
                            )

            # Gemini returned a normal answer
            if not function_calls:
                return response.text

            # Count tool calls
            tool_call_count += len(function_calls)

            # Safety limit
            if tool_call_count > max_tool_calls:

                return (
                    "I stopped because the maximum number "
                    "of tool calls for this request was reached."
                )

            tool_responses = []

            # Execute each requested tool
            for function_call in function_calls:

                function_name = function_call.name
                arguments = dict(function_call.args) if function_call.args else {}

                print(
                    f"\n🔧 Using tool: {function_name}"
                )

                print(
                    f"   Arguments: {arguments}"
                )

                result = execute_tool(
                    function_name,
                    arguments
                )

                print("   ✓ Tool completed")

                tool_responses.append(
                    types.Part.from_function_response(
                        name=function_name,
                        response={
                            "result": result
                        },
                    )
                )

            # Send tool results back to Gemini
            response = self.chat.send_message(
                message=tool_responses
            )