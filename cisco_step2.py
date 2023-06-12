"""
Author: Matthew Schafer
Date: June 5, 2023
Description: A script to generate a random Cisco IOS command question, get an answer from GPT-3, 
             and create a memory in Personal.ai with the question and answer.
             
             
             
             REPLACE AI DOMAIN IN MEMORY SEND AND APIKEY 
"""

import requests
import json
import random
import openai
from datetime import datetime
import pytz

# List of some Common Cisco IOS commands
cisco_hardware_models = [
    # Routers
    "ISR 4221", "ISR 4321", "ISR 4331", "ISR 4351", "ISR 4431", "ISR 4451",
    "819", "829", "881", "887", "891",
    "ASR 1001-X", "ASR 1002-X", "ASR 1006-X",
    # Switches
    "Catalyst 9200", "Catalyst 9300", "Catalyst 9400", "Catalyst 9500",
    "Catalyst 3850",
    "Nexus 2000", "Nexus 5000", "Nexus 7000", "Nexus 9000",
    # Wireless
    "Aironet 1800", "Aironet 2800", "Aironet 3800",
    "Catalyst 9100",
    # Security Appliances
    "ASA 5506-X", "ASA 5508-X", "ASA 5516-X",
    "FPR 1010", "FPR 1120", "FPR 1140", "FPR 1150",
    "MX64", "MX67", "MX84", "MX100", "MX250", "MX450"
]


def get_local_time():
    # Get local time in a specific format
    user_tz = datetime.now(pytz.utc).astimezone().tzinfo
    local_time = datetime.now(user_tz).strftime('%a, %d %b %Y %H:%M:%S %Z')
    return local_time

def create_memory(api_key, memory_data):
    # Make a POST request to the Personal.ai API to create a memory
    base_url = 'https://api.personal.ai/v1/memory'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    response = requests.post(base_url, headers=headers, json=memory_data)
    
    if response.status_code == 200:
        creation_status = response.json()['status']
        return creation_status
    else:
        return None

def ask_gpt(question):
    # Get an answer for a question from GPT-3.5
    openai.api_key = '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'

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful Cisco specialist networking and hardware assistant."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response['choices'][0]['message']['content']

def main():
    api_key = 'apikeyzhere'
    local_time = get_local_time()
    print("Starting the main process...")  # Starting print statement

    for model in cisco_hardware_models:
        # Generate question and answer about each Cisco hardware model
        print(f"Processing model: {model}")  # Print the model being processed
        question = f"""
        1. **Hardware Overview**: Can you provide a detailed overview of the Cisco hardware model '{model}'?
        2. **Specifications**: What are the technical specifications for '{model}'? Please include details such as performance, ports, power requirements, and more.
        3. **Related Hardware**: What other hardware models are in the same series or family as '{model}'? What are their differences and similarities?
        4. **Use Cases**: In what types of network environments or scenarios would '{model}' be most effectively used?
        5. **Modules and Extensions**: What types of modules, extensions, or add-ons are available for '{model}'? What functionality do they provide?
        6. **Configuration**: How is '{model}' typically configured? What are some common IOS commands used with it?
        7. **Troubleshooting**: What are some common issues that might arise when using '{model}' and how can they be resolved?
        8. **Learning Resources**: What resources are available for further learning about '{model}'? Can you recommend any online tutorials, courses, or documentation?
        9. **Purchasing**: Where can '{model}' be purchased, and what is its approximate cost? Are there any considerations to be aware of when purchasing?
        10. **Security Considerations**: What are the security implications or potential risks of using '{model}'?
        """
        answer = ask_gpt(question)
    
        memory_data = {
            "Text": f"Question: {question}\nAnswer: {answer}",
            "SourceName": "Python Cisco Hardware Knowledge Generator",
            "CreatedTime": local_time,
            "DeviceName": "Laptop",
            "DomainName": "your ai domain here",
            "RawFeedText": f"<p>Question: {question}<br>Answer: {answer}</p>",
            "Tags": ["Cisco", "Hardware", "Model", model]  # Add any additional tags here
        }
        
        print(f"Memory data for '{model}': {memory_data}")  # Print the memory data for the model

        # Create a memory in Personal.ai with the question and answer
        creation_status = create_memory(api_key, memory_data)
    
        if creation_status is not None:
            print(f"Memory creation status for '{model}': {creation_status}")
        else:
            print(f"Error creating memory for '{model}'")

    print("Completed the main process.")  # Completion print statement

if __name__ == "__main__":
    main()
