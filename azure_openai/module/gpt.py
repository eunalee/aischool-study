import os
import base64
from dotenv import load_dotenv
from openai import AzureOpenAI

# gpt-4o-mini
def request_gpt(chat_history) :
    try :
        # 환경설정 가져오기
        load_dotenv()
        azure_oai_endpoint = os.getenv('GPT_ENDPOINT_URL')
        azure_oai_key = os.getenv('GPT_API_KEY')
        azure_oai_deployment = os.getenv('GPT_DEPLOYMENT')
        azure_oai_api_version = os.getenv('GPT_API_VERSION')

        # Azure OpenAI 클라이언트 초기화
        client = AzureOpenAI(
            azure_endpoint=azure_oai_endpoint,
            api_key=azure_oai_key,
            api_version=azure_oai_api_version,
        )

        # 채팅 프롬프트
        messages = [
            {
                'role' : 'system',
                'content' : '너는 사용자를 친절하게 도와주는 AI 어시스턴트야.'
            }
        ]

        # 채팅내역 전부 저장
        for msg in chat_history :
            role = msg['role']

            # assistant
            if role == 'assistant' :
                messages.append({
                    'role': role,
                    'content' : msg['content']
                })
                continue
            # user
            if role == 'user' :
                user_contents = []
                has_text = False

                # 이미지 URL
                if isinstance(msg['content'], tuple) and len(msg['content']) == 1 :
                    encoded_image = base64.b64encode(open(msg['content'][0], 'rb').read()).decode('ascii')
                    user_contents.append({
                        'type' : 'image_url',
                        'image_url' : {
                            'url' : f'data:image/jpeg;base64,{encoded_image}'
                        }
                    })
                # 텍스트
                elif isinstance(msg['content'], str) :
                    user_contents.append({
                        'type' : 'text',
                        'text' : msg['content']
                    })
                    has_text = True
                
                # 이미지 셋팅 시, 텍스트 추가 
                if not has_text :
                    user_contents.insert(0, {
                        'type' : 'text',
                        'text' : ''
                    })
                
                messages.append({
                    'role': 'user',
                    'content' : user_contents
                })


        # 대화내역 6개까지 기억
        if len(messages) > 7 :
            # 시스템 메세지 + 최근 대화내역 6개
            messages = [messages[0]] + messages[-6:]
    
        # 완료 생성
        completion = client.chat.completions.create(
            model=azure_oai_deployment,
            messages=messages,
            max_tokens=800,
            temperature=1,
            top_p=0.5
        )

        # 응답 출력
        response = completion.choices[0].message.content
        return response
    except Exception as e :
        return e