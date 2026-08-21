# --------------------------------------------------
# Agent
# --------------------------------------------------

class AIAgent:

    def __init__(self):

        self.chat = client.chats.create(
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

            for candidate in response.candidates:

                if not candidate.content:
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
                arguments = dict(function_call.args)

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