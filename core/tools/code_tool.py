def analyze_code(llm, code, task="explain"):

    prompt = f"""
You are an expert programmer.

Task: {task}

Code:
{code}

If task is:
- explain → explain step by step
- debug → find bug + fix
- optimize → improve performance
- convert → rewrite in better style

Return structured output.
"""

    response = llm.invoke(prompt)

    return response.content