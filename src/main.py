from src.plan_tasks import plan_tasks
from src.execute_tasks import execute_tasks
from util.utility import invoke_claude
import asyncio

# Prompt Output: 
xml_string_format = """
        <Data>
            <Task>
                <TaskID>
                </TaskID>
                <TaskName>
                </TaskName> 
            </Task>
            <Task>
                <TaskID>
                </TaskID>
                <TaskName>
                </TaskName> 
            </Task>
            <Message>
            </Message>
        </Data>
    """

organizational_context = "Use the latest information found on the internet"

async def main(xml_string_format: str, organizational_context: str): 
    user_input = input("Enter task:") 
    response = plan_tasks(user_input, xml_string_format, organizational_context)
    print(response)

    if response == "user_declined":
        print("User declined to proceed with tasks")
        return

    else: 
        await execute_tasks(response)


if __name__ == "__main__":
    asyncio.run(main(xml_string_format, organizational_context))


