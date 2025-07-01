import os
import requests
from dotenv import load_dotenv

# gpt-4.1
def request_gpt(chat_history) :
    # 환경설정 가져오기
    load_dotenv()
    azure_oai_endpoint = os.getenv('GPT_ENDPOINT_URL')
    azure_oai_key = os.getenv('GPT_AUTH_KEY')

    endpoint = azure_oai_endpoint

    headers = {
        'Authorization' : f'Bearer {azure_oai_key}'
    }

    messages = [
        # 시스템 설정
        {
            'role' : 'system',
            'content' : "You're looking for a traditional Korean name that’s similar-sounding but also meaningful in Korean. The Korean names look simple-typically three syllables, a one-syllable family name first followed by a two-syllable given name."
        },
        # Few-shot
        {
            'role' :'user',
            'content' : "I'm Antonio."
        },
        {
            'role' :'assistant',
            'content' : '''Hello, Antonio! That's a nice name. Let’s find you a Korean traditional name that matches both the sound and spirit of your original name. 😊
                        ## ✅ Recommended Traditional Korean Name: 안도현 (An Do-hyun / 安道賢)

                        | Element       | Explanation                                                                 |
                        |---------------|-----------------------------------------------------------------------------|
                        | **안 (An)**     | Korean surname that closely mirrors the "An" in *Antonio*                   |
                        | **도 (Do / 道)** | "The way, path" – symbolizing morality, principle, and integrity             |
                        | **현 (Hyun / 賢)** | "Wise, virtuous" – a common and respected name character                  |

                        → **안도현** means *“a wise person who follows the right path”* — a strong, poetic, and dignified traditional name.

                        🪷 Alternative Suggestions:

                        | Korean Name             | Hanja Meaning           | Vibe                     |
                        | ----------------------- | ----------------------- | ------------------------ |
                        | **도윤 (Do-yoon / 道潤)**   | "Moral and gentle"      | Calm and graceful        |
                        | **태형 (Tae-hyung / 太亨)** | "Great prosperity"      | Powerful and noble       |
                        | **현우 (Hyun-woo / 賢祐)**  | "Wise and blessed"      | Spiritual and classic    |
                        | **준석 (Joon-seok / 俊錫)** | "Talented and precious" | Intellectual and refined |
                '''
        }
    ]

    for msg in chat_history :
        messages.append({
            'role' : msg['role'],
            'content' : msg['content']
        })

    body = {
        'messages' : messages,
        'max_completion_tokens' : 800,
        'temperature' : 1,
        'top_p' : 1,
        'frequency_penalty' : 0,
        'presence_penalty' : 0,
        'model' : 'fimtrus-gpt-41'
    }

    response = requests.post(endpoint, headers=headers, json=body)
    if response.status_code != 200 :
        return None
    
    content = response.json()['choices'][0]['message']['content']
    return content