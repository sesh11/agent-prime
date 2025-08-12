from agents.taskplanning import TaskPlanningAgent
import textwrap
from util.utility import invoke_claude


def plan_tasks(user_input: str, xml_string_format: str, organizational_context: str):
    tasks = []
    completed_tasks = []
    task_planning_agent = TaskPlanningAgent(user_input, tasks, xml_string_format, completed_tasks, organizational_context)
    response = task_planning_agent.task_planning()
    return response


