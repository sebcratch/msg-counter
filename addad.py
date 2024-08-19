import json

# Define the list of keys you want to keep
keys_to_keep = ['senderName', 'text', 'timestamp', 'type']

# Function to filter the message
def filter_message(message):
    return {key: message[key] for key in message.keys() if key in keys_to_keep}

# Load the JSON data
def load_and_filter_json(json_file):
    with open(json_file, 'r', encoding="utf-8") as f:
        data = json.load(f)
    
    # Assuming data is a list of messages
    filtered_data = [filter_message(msg) for msg in data['messages']]
    
    return filtered_data

# Example usage
filtered_messages = load_and_filter_json('C:/Users/S/Downloads/messages/Zuzanna Dębowska_4.json')
for msg in filtered_messages:
    print(msg)