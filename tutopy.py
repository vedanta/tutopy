#!/usr/bin/env python3
"""
TutoPy: Automatic Python Tutorial Generator

This script uses Claude AI to generate Python tutorials based on user input.
The tutorials are created in the JINC format for easy conversion to Jupyter notebooks.

This version is designed to work with GitHub Actions.
"""

import os
import random

# Placeholder for Claude AI integration
def generate_tutorial_with_claude(topic):
    return f"Generated tutorial content for {topic}"

def create_example(difficulty, topic):
    pop_culture_references = {
        'bands': ['The Beatles', 'Queen', 'Nirvana', 'Guns N\' Roses', 'Bon Jovi'],
        'songs': ['Billie Jean', 'Sweet Child O\' Mine', 'Smells Like Teen Spirit', 'Like a Prayer', 'Take On Me'],
        'movies': ['Back to the Future', 'The Breakfast Club', 'Jurassic Park', 'Pulp Fiction', 'The Matrix'],
        'food': ['Pop Rocks', 'Fruit Roll-Ups', 'Pizza Bagels', 'Dunkaroos', 'Gushers'],
        'tv_shows': ['Friends', 'The Simpsons', 'Seinfeld', 'The X-Files', 'Saved by the Bell']
    }

    reference_type = random.choice(list(pop_culture_references.keys()))
    reference = random.choice(pop_culture_references[reference_type])

    return f"{difficulty.capitalize()} example for {topic} using {reference}"

def generate_tutorial(topic):
    tutorial = f"""#!/usr/bin/env python3
#  DESCRIPTION This is a tutorial on {topic}, featuring examples inspired by 80s and 90s pop culture.

# MARKDOWN CELL
# {topic.capitalize()} Tutorial

This tutorial will guide you through {topic} with examples inspired by 80s and 90s pop culture.

"""

    difficulties = ['simple', 'intermediate', 'expert']
    for difficulty in difficulties:
        tutorial += f"""# MARKDOWN CELL
## {difficulty.capitalize()} Examples

Here are three {difficulty} examples of {topic}:

"""
        for i in range(1, 4):
            example = create_example(difficulty, topic)
            tutorial += f"""# CODE CELL
# Example {i}: {example}
# Your code here

# MARKDOWN CELL
Explanation of the above example goes here.

"""

    return tutorial

def main():
    # Get the topic from GitHub Actions input
    topic = os.environ.get('INPUT_TOPIC')
    if not topic:
        raise ValueError("No topic provided. Please set the 'topic' input in your GitHub Actions workflow.")

    tutorial_content = generate_tutorial(topic)
    
    # Save the tutorial content to a file
    with open('tutorial.py', 'w') as f:
        f.write(tutorial_content)

    print(f"Tutorial for '{topic}' has been generated and saved as 'tutorial.py'.")

if __name__ == "__main__":
    main()
