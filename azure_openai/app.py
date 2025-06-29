import gradio as gr
import time
from module import gpt, rag, dalle, search, stt, tts

# GPT 채팅기록
def add_message(chat_history, message) :
    # 업로드된 파일이 있을 때,
    for x in message['files'] :
        chat_history.append({
            'role' : 'user',
            'content' : {
                'path' : x
            }
        })
    
    # 메시지 입력이 있을때,
    if message['text'] :
        chat_history.append({
            'role' : 'user',
            'content' : message['text']
        })
    
    return chat_history, gr.MultimodalTextbox(value=None, interactive=False)


# GPT
def bot(chat_history: list) :
    response = gpt.request_gpt(chat_history)
    if response :
        chat_history.append({
            'role' : 'assistant',
            'content' : response
        })

    # 타이핑 효과
    for character in response :
        time.sleep(0.05)
        yield chat_history

# RAG
def get_rag_result(input_message, chat_history) :
    bot_message = rag.request_gpt_rag(input_message, chat_history)

    # 사용자 메세지
    chat_history.append({
        'role' : 'user',
        'content' : input_message
    })
    
    # 챗봇 메세지
    chat_history.append({
        'role' : 'assistant',
        'content' : bot_message
    })

    return '', chat_history


# DALL-E 3
def generate_image(prompt) :
    return dalle.request_dalle(prompt)


# Google Search
def get_google_search_result(input_message, chat_history) :
    bot_message = search.request_google_search(input_message, chat_history)
    audio_path = tts.request_text_to_speech(bot_message)

    # 사용자 메세지
    chat_history.append({
        'role' : 'user',
        'content' : input_message
    })
    
    # 챗봇 메세지
    chat_history.append({
        'role' : 'assistant',
        'content' : bot_message
    })

    return '', chat_history, audio_path


# Whisper
def get_speech_to_text_result(audio_path) :
    return stt.request_speech_to_text(audio_path)


# Web UI
with gr.Blocks() as demo :
    with gr.Tabs() :
        # GPT
        with gr.Tab('GPT-4o-mini') :
            chatbot = gr.Chatbot(label='채팅기록', elem_id='chatbot', bubble_full_width=False, type='messages')

            chat_input = gr.MultimodalTextbox(
                interactive=True,
                file_count='multiple',
                placeholder='메시지 입력 or 파일 업로드',
                show_label=False,
                sources=['upload']
            )

            chat_msg = chat_input.submit(
                fn=add_message,
                inputs=[chatbot, chat_input],
                outputs=[chatbot, chat_input]
            )

            bot_msg = chat_msg.then(
                fn=bot,
                inputs=[chatbot],
                outputs=[chatbot],
                api_name='bot_response'
            )

            bot_msg.then(
                fn=lambda : gr.MultimodalTextbox(interactive=True),
                inputs=None,
                outputs=[chat_input]
            )
        # RAG
        with gr.Tab('RAG') :
            gr.Markdown('### 🎆 서울시 문화행사 정보를 알려드립니다.')
            rag_chatbot = gr.Chatbot(label='채팅기록', type='messages')
            rag_input_textbox = gr.Textbox(label='프롬프트 입력')
            rag_submit_button = gr.Button('전송')

            # 엔터 눌렀을 때,
            rag_input_textbox.submit(
                fn=get_rag_result,
                inputs=[rag_input_textbox, rag_chatbot],
                outputs=[rag_input_textbox, rag_chatbot]
            )

            # 전송 버튼 클릭 시,
            rag_submit_button.click(
                fn=get_rag_result,
                inputs=[rag_input_textbox, rag_chatbot],
                outputs=[rag_input_textbox, rag_chatbot]
            )
        # DALL-E3
        with gr.Tab('DALL-E3') :
            dalle_output_image = gr.Image(label='이미지')
            dalle_input_textbox = gr.Textbox(label='프롬프트 입력')
            dalle_submit_button = gr.Button('이미지 생성')

            # 엔터 눌렀을 때,
            dalle_input_textbox.submit(
                fn=generate_image,
                inputs=[dalle_input_textbox],
                outputs=[dalle_output_image]
            )

            # 전송 버튼 클릭 시,
            dalle_submit_button.click(
                fn=generate_image,
                inputs=[dalle_input_textbox],
                outputs=[dalle_output_image]
            )
        # Google Search
        with gr.Tab('Google Search') : 
            search_chatbot = gr.Chatbot(label='채팅기록', type='messages')
            search_input_textbox = gr.Textbox(label='프롬프트 입력')
            voice_audio_input = gr.Audio(label='음성으로 질문', sources='microphone', type='filepath')
            search_submit_button = gr.Button('전송')
            voice_audio_output = gr.Audio(label='음성 응답', autoplay=True)

            voice_audio_input.change(
                fn=get_speech_to_text_result,
                inputs=[voice_audio_input],
                outputs=[search_input_textbox]
            )

            # 엔터 눌렀을 때,
            search_input_textbox.submit(
                fn=get_google_search_result,
                inputs=[search_input_textbox, search_chatbot],
                outputs=[search_input_textbox, search_chatbot, voice_audio_output]
            )

            # 전송 버튼 클릭 시,
            search_submit_button.click(
                fn=get_google_search_result,
                inputs=[search_input_textbox, search_chatbot],
                outputs=[search_input_textbox, search_chatbot, voice_audio_output]
            )

demo.launch()