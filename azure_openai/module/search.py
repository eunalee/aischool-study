import os
import pytz
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from serpapi import GoogleSearch
from datetime import datetime

# 현재 시간 출력
def get_time(timezone='Asia/Seoul') :
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime('%Y년 %m월 %d일 %H시 %M분 %S초')
    now_timezone = f'{now} {timezone}'
    return now_timezone


# 응답 결과
def get_response(chat_prompt, tools=None) :
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

        # 완료 생성
        response = client.chat.completions.create(
            model=azure_oai_deployment,
            messages=chat_prompt,
            tools=tools
        )
        return response
    except Exception as e :
        return e


# 구글 검색 결과 출력
def search_google_search(query) :
    if not query : 
        return '검색어를 입력해주세요.'

    try :
        # 환경설정 가져오기
        load_dotenv()
        google_search_key = os.getenv('GOOGLE_SEARCH_API_KEY')

        param = {
            'q' : query,
            'api_key' : google_search_key,
            'num' : 3
        }

        # 구글 검색
        search = GoogleSearch(param)
        results = search.get_dict()
        if 'error' in results :
            return results['error']
 
        response = '\n'.join([f"{result['snippet']}\n{result['link']}" for result in results['organic_results']])
    except Exception as e :
        return f'검색 오류 : {e}'

    return response


# google search
def request_google_search(prompt, chat_history) :
    try :
        # 함수 등록
        tools = [
            {
                'type' : 'function',
                'function' : {
                    'name' : 'get_time',
                    'description' : '현재 날짜와 시간을 반환합니다.',
                    'parameters' : {
                        'type' : 'object',
                        'properties' : {
                            'timezone' : {
                                'type' : 'string',
                                'description' : '현재 날짜와 시간을 반환할 타임존을 입력하세요(예:Asia/Seoul)',
                            },
                        },
                        'required' : ['timezone'],
                    },
                }
            },
            {
                'type' : 'function',
                'function' : {
                    'name' : 'search_google_search',
                    'description' : 'googleSearch 로 정보를 검색합니다.',
                    'parameters' : {
                        'type' : 'object',
                        'properties' : {
                            'prompt' : {
                                'type' : 'string',
                                'description' : '검색할 키워드 또는 문장을 입력하세요.',
                            },
                        },
                        'required' : ['query'],
                    },
                }
            }
        ]

        # 채팅 프롬프트
        chat_prompt = [
            {
                'role' : 'system',
                'content' : '너는 사용자를 친절하게 도와주는 AI 어시스턴트야.'
            }
        ]

        # 채팅내역 전부 저장
        for msg in chat_history :
            chat_prompt.append({
                'role': msg['role'],
                'content': msg['content']
            })
        
        # 입력 프롬프트
        chat_prompt.append({
            'role' : 'user',
            'content' : prompt
        })

         # 대화내역 6개까지 기억
        if len(chat_prompt) > 7 :
            # 시스템 메세지 + 최근 대화내역 6개
            chat_prompt = [chat_prompt[0]] + chat_prompt[-6:]

        # 완료 생성
        # 프롬프트 내용이 tools 이 필요한지 아닌지 LLM 이 알아서 판단
        completion = get_response(chat_prompt, tools=tools)

        # AI 응답
        response = completion.choices[0].message

        # 등록된 함수가 있을때만
        tool_calls = response.tool_calls
        if tool_calls :
            # 함수 정보 추출
            for tool_call in tool_calls :
                tool_calls_id = tool_call.id
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                # 등록된 함수에 따른 응답 처리
                # 현재 시간 출력
                if tool_name == 'get_time' :
                    result = get_time(timezone=arguments['timezone'])
                # 웹 검색 결과 출력
                elif tool_name == 'search_google_search' :
                    result = search_google_search(query=arguments['prompt'])
                else :
                    result = '지원하지 않는 함수입니다.'
                
                chat_prompt.append({
                    'tool_call_id': tool_calls_id,
                    'role': 'function',
                    'name': tool_name,
                    'content': result,
                })

            # 답변 지침 설정
            chat_prompt.append({
                'role' : 'system',
                'content' : '주어진 결과를 바탕으로 답변해줘'
            })

            # 재요청
            completion = get_response(chat_prompt, tools=tools)
            response = completion.choices[0].message
        return response.content
    except Exception as e :
        return e