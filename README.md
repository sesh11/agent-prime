# General Purpose Agent Framework

A core idea that I’ve been experimenting with is building a general purpose agent that can accomplish a wide variety of tasks both in a consumer and enterprise context. I prefer building agents with simple loops and tool calls (or building workflows enabled with LLMs) but this doesn’t scale as tasks start to get more complex. 

This is my attempt at building a general purpose agent framework that breaks down complex requests into simple self-contained executable tasks. Inspired by Claude Code, the framework first creates a set of decomposable tasks and then executes each task with approval from the user. This pattern is particularly useful for agents working on critical operations. 

This was intended as a learning exercise and to create a foundation for more complex agentic workflows. The ultimate goal is to build a single all-encompassing agent that works agnostic of model and in theory, perform all tasks that humans can over the internet. In an enterprise context, this could be a single agent that works across the organization to accomplish work. 

It's still early and there is a lot more to build here. 

## Overview

The framework follows a simple but powerful pattern:

1. **Planning**: Takes your request and breaks it down into logical, sequential tasks
2. **Review**: Shows you the planned tasks and waits for your approval
3. **Execution**: Executes each approved task using Claude and available tools, with checkpoints for your confirmation


## Quick Start

1. Clone the repository

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file with your API keys:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

5. Run the framework:
   ```bash
   python -m src.main
   ```

## Usage

1. Enter your request when prompted
2. Review the proposed task breakdown
3. Approve tasks for execution
4. View results as each task completes

## Contributing

Contributions are welcome! Take a look at the open issues to see what needs work, or feel free to propose new features. 
