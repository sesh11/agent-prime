import xml.etree.ElementTree as ET
import textwrap
import os
import anthropic
from dotenv import load_dotenv
from util.utility import invoke_claude

load_dotenv()

class TaskPlanningAgent:
    def __init__(self, user_input: str, tasks: list, xml_string_format: str, completed_tasks: list, organizational_context: str):
        self.user_input = user_input
        self.tasks = tasks
        self.xml_string_format = xml_string_format
        self.completed_tasks = completed_tasks
        self.organizational_context = organizational_context
        pass

    def task_planning(self):
        
        tstring = "".join(self.tasks) 
        completedtstring = "".join(self.completed_tasks)
        
        prompt = textwrap.dedent("""
        You are a task management specialist that is excellent at breaking down complex requests into an actionable and executable tasks. These tasks are standalone and can be executed independently with the right input.
        Take the user request defined at {{user_input}} and breakdown the request into a series of actionable tasks to be executed sequentially to achieve the desired outcome requested from the user.
        
        Output the list of tasks in the format defined at 
        {{xml_string_format}}
        Don't add anything before or after the prescribed format.

        Review the {{completed_tasks}} and the {{existing_tasks}} that were defined previously. If you find that there are {{existing_tasks}}, then consider the {{user_input}} in the context of the {{completed_tasks}} and the {{existing_tasks}}. 
        Validate if there is a change needed to any of the existing tasks based on the updated user input. The {{completed_tasks}} are in the past so they don't need to be changed.

        Use {{organizational_context}} as input in the definition of tasks. 

        When creating the list of tasks:
        1. Each individual should be a logical unit of work
        2. The tasks should be self-contained and executed easily
        3. The tasks should rely on no more than a single tool call for execution
        4. The final set of tasks that are output in the {{xml_string_format}} should include an updated set of tasks that is a combination of the existing tasks as well as any new updated tasks. 
        5. Based on the user request, retain what is appropriate from the existing tasks {{existing_tasks}} as needed and define additional tasks if appropriate. 
        6. The final set of tasks published should be holistic
        7. End with a question back to the user to ask them what they would like to do next in the <Message> tag.

        Examples: 
        User Request: How much has the apple stock appreciated in the last 6 months? 
        Response: 
            <Data>
                <Task>
                    <TaskID>1</TaskID>
                    <TaskName>Find the stock tickets for Apple</TaskName> 
                </Task>
                <Task>
                    <TaskID>2</TaskID>
                    <TaskName>Retreive 6 months of data for Apple Stock Ticker</TaskName> 
                </Task>
                <Task>
                    <TaskID>3</TaskID>
                    <TaskName>Find the rate of appreciation for the last 6 months of Apple stock</TaskName> 
                </Task>
                <Message>What would you like to do next?</Message>
            </Data>

        IMPORTANT:
        Adhere to the format prescribed in {xml_string_format}. Don't add any additional information before or after the request. 
        Remember that the response should start with <Data> and end with </Data>
        Forward looking, return only the tasks that need to be executed in the future. Don't return any of the completed tasks in the response. 
        
        """).replace("{{user_input}}", self.user_input).replace("{{xml_string_format}}", self.xml_string_format).replace("{{completed_tasks}}", completedtstring).replace("{{existing_tasks}}", tstring)

        #Additional model parameters 
        model = "claude-sonnet-4-20250514"
        assist_content = ""
        stop_sequences = "</Messages>"
        system_prompt = "Think logically and develop a set of tasks that are logical and can be executed indepedently" 

        #Invoke the LLM
        updated_tasks = invoke_claude(model, prompt, system_prompt, assist_content=assist_content, stop_sequences=None)

        # DEBUG: Print what Claude returned
        print("=== CLAUDE RESPONSE ===")
        print(repr(updated_tasks))
        print("=== END RESPONSE ===")

        #Parse the results in the xml to create a list of updated tasks
        updated_tasks_list = self.parse_xml(updated_tasks, self.xml_string_format)
        
        return updated_tasks_list
            
        # else: 
        #     tasks_list = tasks
        #     tasks_string = invoke_claude(model, prompt, system_prompt, assist_content=assist_content, stop_sequences=None)
        #     tasks_list.append(tasks_string)
        #     tasks_string = invoke_claude(model, prompt, system_prompt, assist_content=assist_content, stop_sequences=None)

    @staticmethod
    def parse_xml(tasks_string: str, xml_string_format: str):
            root = ET.fromstring(tasks_string)
            tasks_list = []
            for item in root.iter('Task'):
                taskid = item.find('TaskID').text
                taskname = item.find('TaskName').text
                tasks_list.append({"taskid": taskid, "taskname": taskname})
            return tasks_list

    # @staticmethod
    # def invoke_claude(model: str, prompt: str, system_prompt: str, assist_content= "", stop_sequences=None, max_tokens=1024) -> str:
    #     api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    #     if not api_key:
    #         return "Anthropic API key not found in environment"
    
    #     if not api_key:
    #         return "Anthropic API key not found in environment"
        
    #     client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    #     response = client.messages.create(
    #         model=model,
    #         system=system_prompt, 
    #         max_tokens=max_tokens,
    #         # stop_sequences=stop_sequences,
    #         messages = [
    #             {"role": "user", "content": prompt},
    #             {"role": "assistant", "content": assist_content}]
    #     )
    #     return response.content[0].text