# services.py

import requests
from pydub import AudioSegment

def get_ai_chat_response(text: str, openai_api_key: str) -> str:
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'text-davinci-003',
        'prompt': text,
        'max_tokens': 50,
    }
    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
    return response.json().get('choices', [{}])[0].get('text', 'Sorry, I could not understand that.')

def remove_bg(image_path: str, remove_bg_api_key: str):
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            headers={'X-Api-Key': remove_bg_api_key},
            files={'image_file': image_file}
        )
        if response.status_code == requests.codes.ok:
            with open('temp_photo_no_bg.png', 'wb') as out:
                out.write(response.content)
        else:
            print("Error:", response.status_code, response.text)

def change_voice(input_path: str, output_path: str):
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format='ogg')
