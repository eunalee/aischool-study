import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# whisper
def request_speech_to_text(audio_path) :
    try :
        # 환경설정 가져오기
        load_dotenv()
        azure_oai_endpoint = os.getenv('WHISPER_ENDPOINT_URL')
        azure_oai_key = os.getenv('WHISPER_API_KEY')
        azure_oai_deployment = os.getenv('WHISPER_DEPLOYMENT')
        azure_oai_api_version = os.getenv('WHISPER_API_VERSION')

        # Azure OpenAI 클라이언트 초기화
        whisper_client = AzureOpenAI(
            azure_endpoint=azure_oai_endpoint,
            api_key=azure_oai_key,
            api_version=azure_oai_api_version,
        )

        # 오디오 파일 열기
        audio_file_path = audio_path
        with open(audio_file_path, 'rb') as audio_file :
            # 요청 (Speech To Text)
            transcription = whisper_client.audio.transcriptions.create(
                model=azure_oai_deployment,
                file=audio_file
            )
        
        return transcription.text
    except Exception as e :
        return e