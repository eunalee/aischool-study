import gradio as gr
import re
from module import gpt, stt, tts


# 지원 언어 선택
def select_language(language) :
    voice_list = [
        {
            'English' : ['en-US-FableTurboMultilingualNeural', 'en-US-BlueNeural'],
            'Japanese' : ['ja-JP-NanamiNeural', 'ja-JP-KeitaNeural'],
            'Spanish' : ['es-ES-ArabellaMultilingualNeural', 'es-ES-TristanMultilingualNeural'],
        }
    ]

    choices = voice_list[0].get(language)
    return gr.Dropdown(choices=choices, label='Choose from a set of voices.', type='value', value=choices[0])


# Speech Voice 선택
def select_voice(value) :
    return value


# locale 정보 추출
def get_locale(language) :
    locale = 'en-US'
    if language == 'Japanese' :
        locale = 'ja-JP'
    elif language == 'Spanish' :
        locale = 'es-ES'

    return locale


# 프롬프트 입력 정보 추출
def get_content(message, language) :
    content = ''
    if message['files'] :       # 오디오 파일이 있을때, 해당 파일에서 텍스트 가져오기
        locale = get_locale(language)
        content = stt.request_stt(message['files'][0], locale)
    elif message['text'] :      # 메시지 입력이 있을때, 해당 메시지 사용
        content = message['text']

    return content


# 채팅기록 저장
def add_message(chat_history, message, language) :
    content = get_content(message, language)
    chat_history.append({
        'role' : 'user',
        'content' : content
    })

    return chat_history, gr.MultimodalTextbox(value=None, interactive=False)


# gpt 결과 - 텍스트 및 음성 응답
def bot(chat_history, language, voice) :
    filename = None
    # 오디오에서 읽어온 텍스트로 gpt 응답 생성
    content = gpt.request_gpt(chat_history)
    if content : 
        chat_history.append({
            'role' : 'assistant',
            'content' : content
        })

        # 음성 응답 생성
        locale = get_locale(language)
        pattern = f'[^가-힣a-zA-Z0-9\s!.,]'
        cleaned_content = re.sub(pattern, '', content)
        filename = tts.request_tts(cleaned_content, locale, voice)

    return chat_history, filename


with gr.Blocks() as demo :
    gr.Markdown('## 📋 Korean Name Generator')
    radio_button = gr.Radio(label='Please select your language.', choices=['English', 'Japanese', 'Spanish'], value='English')
    dropdown = gr.Dropdown(choices=['en-US-FableTurboMultilingualNeural', 'en-US-BlueNeural'], label='Choose from a set of voices.', type='value', value='en-US-FableTurboMultilingualNeural')
    chatbot = gr.Chatbot(label='chat', type='messages')
    chat_input = gr.MultimodalTextbox(
        interactive=True,
        placeholder='Input your message.',
        show_label=False,
        sources=['microphone', 'upload'],
        file_types=['.wav'], 
    )
    audio = gr.Audio(sources='microphone', type='filepath', label='Voice Message', autoplay=True)

    radio_button.input(
        fn=select_language,
        inputs=[radio_button],
        outputs=[dropdown]
    )

    dropdown.change(
        fn=select_voice,
        inputs=[dropdown],
        outputs=[dropdown]
    )

    chat_input.input(
        fn=get_content,
        inputs=[chat_input, radio_button],
        outputs=[chat_input]
    )

    chat_msg = chat_input.submit(
        fn=add_message,
        inputs=[chatbot, chat_input, radio_button],
        outputs=[chatbot, chat_input]
    )

    bot_msg = chat_msg.then(
        fn=bot,
        inputs=[chatbot, radio_button, dropdown],
        outputs=[chatbot, audio]
    )

    bot_msg.then(
        fn=lambda : gr.MultimodalTextbox(interactive=True),
        inputs=None,
        outputs=[chat_input]
    )

demo.launch()