from openai import OpenAI
import time
import json
from functions.main import *

DELAY = 0.1

def call_function(function_name: str, arguments):
    if function_name in globals() and callable(globals()[function_name]):
        function = globals()[function_name]
        return function(**arguments)
    else:
        raise ValueError(f"Function '{function_name}' does not exist")

def get_assistant_response(prompt, client: OpenAI, assistant, thread):
    # Add user message to thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    # Run the thread
    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = assistant.id
    )

    # Check for status
    while True:
        time.sleep(DELAY)

        # Retrieve the run status
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        # If run is completed, get messages
        if run_status.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )

            break
        elif run_status.status == 'requires_action':
            
            if run_status.required_action.type == "submit_tool_outputs":
                required_actions = run_status.required_action.submit_tool_outputs.model_dump()
                tool_outputs = []

                for action in required_actions["tool_calls"]:
                    func_name = action['function']['name']
                    arguments = json.loads(action['function']['arguments'])

                    # print(f"Calling Function {func_name} with arguments {arguments}")
                    
                    # This might create exception if the function is not defined
                    output = call_function(func_name, arguments)
                    tool_outputs.append({
                            "tool_call_id": action['id'],
                            "output": output
                        })
                    
                    
                print(f"Submitting outputs back to the Assistant: {tool_outputs}")
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
        else:
            print("Waiting for the Assistant to process...")
    
    message = messages.data[0].content[-1]
    message = message.text.value

    return message