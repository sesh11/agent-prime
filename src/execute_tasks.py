from agents.taskexecution import TaskExecutionAgent
import textwrap
from util.utility import invoke_claude_with_tools
from util.utility import invoke_claude


async def execute_tasks(response: list):
    prev_task_list = []

    for resp in response: 
        print(f"Task ID: {resp["taskid"]} - {resp["taskname"]}")
        user_input = input("Do you wish to proceed with executing this task?")
        model = "claude-sonnet-4-20250514"
        assist_content = ""
        system_prompt = textwrap.dedent("""IMPORTANT: Respond with only one word. You options are Yes or No. The user was asked if they wished to proceed with a task. 
        Read the input from the user found in {{user_input}} and translate it to only return Yes or No.
        Example: 
        If the user says yes, Yes, Y, Affirmative, let's do it, or similar, then return Yes.
        If the user says no, No, N, Negative, I don't want that, or similar, then return No""").replace("{{user_input}}", user_input)
        prompt = (f"the user has responded with the following: {user_input}")
        user_response = invoke_claude(model, prompt, system_prompt)
        print(f"Does the user wish to proceed? {user_response}")

        if user_response == 'Yes':
            task_execution = TaskExecutionAgent(resp["taskname"], prev_task_list)
            answer = await task_execution.task_execution()
            prev_task_list.append(f" For Task {resp["taskname"]}, the response is {answer}")
            print(f"task id is {resp["taskid"]}, take name is {resp["taskname"]}, and the answer is {answer}")

        else:
            return "user_declined"



