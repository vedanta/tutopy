#!/usr/bin/env python3
"""
TutoPy: Automatic Python Tutorial Generator

This script uses Claude AI to generate Python tutorials based on user input.
The tutorials are created in the JINC format for easy conversion to Jupyter notebooks.
"""

import os
import requests
import sys
import json

def generate_tutorial_with_claude(topic):
    api_key = os.environ.get('CLAUDE_API_KEY')
    if not api_key:
        print("Error: CLAUDE_API_KEY not set in environment variables", file=sys.stderr)
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    prompt = f"""Generate a Python tutorial on {topic} with examples inspired by 80s and 90s pop culture. 
    Include three difficulty levels: simple, intermediate, and expert. 
    For each difficulty level, provide three examples with actual Python code.
    Use the following format:

    #!/usr/bin/env python3
    #  DESCRIPTION This is a tutorial on {topic}, featuring examples inspired by 80s and 90s pop culture.

    # MARKDOWN CELL
    # {topic.capitalize()} Tutorial

    This tutorial will guide you through {topic} with examples inspired by 80s and 90s pop culture.

    # MARKDOWN CELL
    ## Simple Examples

    Here are three simple examples of {topic}:

    # CODE CELL
    # Example 1: [Pop culture reference]
    [Include actual Python code here]

    # MARKDOWN CELL
    [Explanation of the above example]

    [Repeat for Examples 2 and 3, then for Intermediate and Expert levels]
    """
    
    data = {
        "model": "claude-3-opus-20240229",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 3000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
        response.raise_for_status()
        return response.json()['content'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f"Error calling Claude API: {e}", file=sys.stderr)
        if response:
            print(f"Response content: {response.text}", file=sys.stderr)
        return None

def main():
    topic = os.environ.get('INPUT_TOPIC')
    if not topic:
        print("Error: No topic provided. Please set the 'topic' input in your GitHub Actions workflow.", file=sys.stderr)
        sys.exit(1)

    tutorial_content = generate_tutorial_with_claude(topic)
    if tutorial_content is None:
        print("Failed to generate tutorial content.", file=sys.stderr)
        sys.exit(1)

    filename = f"{topic.replace(' ', '_').lower()}_tutorial.py"
    with open(filename, 'w') as f:
        f.write(tutorial_content)

    print(f"Tutorial for '{topic}' has been generated and saved as '{filename}'.")

if __name__ == "__main__":
    main()
