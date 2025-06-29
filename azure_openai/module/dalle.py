import os
import json
import requests
from dotenv import load_dotenv
from openai import AzureOpenAI
from datetime import datetime
from PIL import Image

# dall-e 3
def request_dalle(prompt) :
    try :
        # 환경설정 가져오기
        load_dotenv()
        azure_oai_endpoint = os.getenv('DALLE_ENDPOINT_URL')
        azure_oai_key = os.getenv('DALLE_API_KEY')
        azure_oai_deployment = os.getenv('DALLE_DEPLOYMENT')
        azure_oai_api_version = os.getenv('DALLE_API_VERSION')

        # Azure OpenAI 클라이언트 초기화
        client = AzureOpenAI(
            api_version=azure_oai_api_version,
            azure_endpoint=azure_oai_endpoint,
            api_key=azure_oai_key,
        )

        # 완료 생성
        result = client.images.generate(
            model=azure_oai_deployment,
            prompt=prompt,
            n=1,
            style='vivid',
            quality='standard',
        )

        image_url = json.loads(result.model_dump_json())['data'][0]['url']

        # 이미지 가져오기
        response = requests.get(image_url)
        if response.status_code == 200 : 
            generated_image = response.content

            # 이미지 저장하기
            output_dir = 'assets'
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_filename = f'img_{timestamp}.png'
            image_path = os.path.join(output_dir, image_filename)
            with open(image_path, 'wb') as image_file :
                image_file.write(generated_image)
            
            # 이미지 출력하기
            image = Image.open(image_path)

            return image
        else :
            return None
    except Exception as e :
        return e