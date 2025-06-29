import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from datetime import datetime

# tts
def request_text_to_speech(response) :
    try :
        # 환경설정 가져오기
        load_dotenv()
        azure_oai_endpoint = os.getenv('TTS_ENDPOINT_URL')
        azure_oai_key = os.getenv('TTS_API_KEY')
        azure_oai_deployment = os.getenv('TTS_DEPLOYMENT')
        azure_oai_api_version = os.getenv('TTS_API_VERSION')

        # Azure OpenAI 클라이언트 초기화
        tts_client = AzureOpenAI(
            azure_endpoint=azure_oai_endpoint,
            api_key=azure_oai_key,
            api_version=azure_oai_api_version,
        )

        # 요청 (Text To Speech)
        tts_response = tts_client.audio.speech.create(
            model=azure_oai_deployment,
            voice='alloy',
            input=response
        )

        # 음성 파일로 저장
        output_dir = 'assets'
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_filename = f'tts_{timestamp}.mp3'
        audio_path = os.path.join(output_dir, audio_filename)

        tts_response.write_to_file(audio_path)

        return audio_path
    except Exception as e :
        return e