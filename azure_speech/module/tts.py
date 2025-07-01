import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# tts
def request_tts(text, locale, voice) :
    # 환경설정 가져오기
    load_dotenv()
    azure_oai_endpoint = os.getenv('TTS_ENDPOINT_URL')
    azure_oai_key = os.getenv('TTS_API_KEY')

    endpoint = azure_oai_endpoint
    headers = {
        'Content-Type' : 'application/ssml+xml',
        'X-Microsoft-OutputFormat' : 'riff-16khz-16bit-mono-pcm',
        'Ocp-Apim-Subscription-Key' : azure_oai_key
    }

    body = f'''
        <speak version='1.0' xml:lang='ko-KR'>
            <voice xml:lang='{locale}' xml:gender='Female' name='{voice}'>
            {text}
            </voice>
        </speak>
    '''

    response = requests.post(endpoint, headers=headers, data=body)
    if response.status_code != 200 : 
        return None
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'tts_result_{timestamp}.wav'
    with open(filename, 'wb') as audio_file :
        audio_file.write(response.content)

    return filename