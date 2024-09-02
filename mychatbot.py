import openai
import streamlit as st

st.title("친근한 챗봇")

# 사용자에게 API 키를 입력받는 부분 추가
api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

# API 키가 입력된 경우에만 OpenAI 설정
if api_key:
    openai.api_key = api_key
    
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    # 시스템 메시지 설정 (사용자에게는 표시되지 않음)
    system_message = '''
    너의 이름은 친구봇이야.
    너는 항상 반말을 하는 챗봇이야. 다나까나 요 같은 높임말로 절대로 끝내지 마
    항상 반말로 친근하게 대답해줘.
    영어로 질문을 받아도 무조건 한글로 답변해줘.
    한글이 아닌 답변일 때는 다시 생각해서 꼭 한글로 만들어줘
    모든 답변 끝에 답변에 맞는 이모티콘도 추가해줘
    '''

    # 메시지 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_message}]    

    # 기존 메시지 표시 (시스템 메시지 제외)
    for message in st.session_state.messages:
        if message["role"] != "system":  # 시스템 메시지는 표시하지 않음
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API 호출 및 응답 처리
        with st.chat_message("assistant"):
            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            assistant_message = response['choices'][0]['message']['content']
            st.markdown(assistant_message)
            
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

else:
    st.warning("API 키를 입력해야 챗봇이 작동합니다.")
