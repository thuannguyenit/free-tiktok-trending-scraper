# Import built-in libraries
import re

# Function to extract hashtags from description
def extract_hashtags(description):
    hashtags = re.findall(r'#\w+', description)
    return hashtags

# Function to remove hashtags from description
def remove_hashtags(description):
    return re.sub(r'#\w+', '', description).strip()