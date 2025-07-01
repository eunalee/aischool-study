import os
import requests
from dotenv import load_dotenv

# stt
def request_stt(audio_path, locale) :
    # 환경설정 가져오기
    load_dotenv()
    azure_oai_endpoint = os.getenv('STT_ENDPOINT_URL')
    azure_oai_key = os.getenv('STT_API_KEY')

    endpoint = f'{azure_oai_endpoint}language={locale}'

    headers = {
        'Ocp-Apim-Subscription-Key' : azure_oai_key
    }

    with open(audio_path, 'rb') as audio_file :
        audio_data = audio_file.read()

    response = requests.post(endpoint, headers=headers, data=audio_data)
    if response.status_code != 200 :
        return None
    
    content = response.json()['DisplayText']
    return content