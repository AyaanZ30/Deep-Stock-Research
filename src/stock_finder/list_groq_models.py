import os
import requests

# Set your Groq API key as an environment variable: GROQ_API_KEY
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not GROQ_API_KEY:
    raise EnvironmentError('Please set the GROQ_API_KEY environment variable.')

GROQ_API_URL = 'https://api.groq.com/openai/v1/models'

headers = {
    'Authorization': f'Bearer {GROQ_API_KEY}',
    'Accept': 'application/json',
}

def list_groq_models():
    try:
        response = requests.get(GROQ_API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        print('Available Groq API Models:')
        for model in data.get('data', []):
            model_id = model.get('id', 'N/A')
            description = model.get('description', 'No description')
            print(f'- {model_id}: {description}')
    except Exception as e:
        print(f'Error fetching models: {e}')

if __name__ == '__main__':
    list_groq_models()
    print('\nSet your Groq API key in the environment variable GROQ_API_KEY.') 