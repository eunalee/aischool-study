import os
import re
from dotenv import load_dotenv
from openai import AzureOpenAI

# search
def request_gpt_rag(prompt, chat_history) :
    try :
        # 환경설정 가져오기
        load_dotenv()
        azure_oai_endpoint = os.getenv('GPT_ENDPOINT_URL')
        azure_oai_key = os.getenv('GPT_API_KEY')
        azure_oai_deployment = os.getenv('GPT_DEPLOYMENT')
        azure_oai_api_version = os.getenv('GPT_API_VERSION')

        azure_rag_endpoint = os.getenv('RAG_ENDPOINT_URL')
        azure_rag_key = os.getenv('RAG_API_KEY')
        azure_rag_index_name = os.getenv('RAG_INDEX_NAME')
        azure_rag_semantic_config = os.getenv('RAG_SEMANTIC_CONFIG')

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
            messages.append({
                'role': msg['role'],
                'content': msg['content']
            })
        
        # 입력 프롬프트
        messages.append({
            'role' : 'user',
            'content' : prompt
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
            top_p=0.5,
            extra_body={
                'data_sources': [{
                    'type': 'azure_search',
                    'parameters': {
                        'endpoint': azure_rag_endpoint,
                        'index_name': azure_rag_index_name,
                        'semantic_configuration': azure_rag_semantic_config,
                        'query_type': 'semantic',
                        'fields_mapping': {},
                        'in_scope': True,
                        'filter': None,
                        'strictness': 3,
                        'top_n_documents': 5,
                        'authentication': {
                            'type': 'api_key',
                            'key': azure_rag_key
                        }
                    }
                }]
            }
        )

        # 응답 출력
        response = completion.choices[0].message.content

        # 인용된 문서 번호
        doc_nums = re.findall(r'\[doc(\d+)\]', response)

        # 인용된 내용
        citations = completion.choices[0].message.context['citations']

        # 답변에 직접 인용된 경우에만 노출
        if doc_nums : 
            for num in doc_nums :
                index = int(num) - 1
                response += f"\n[doc{num}]\n {citations[index]['content']}\n"

        return response
    except Exception as e :
        return e