import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

st.title("chatGPT[gpt-4o]")

# 세션 상태 초기화
if "api_key" not in st.session_state:
    st.session_state["api_key"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# 사이드바 생성
with st.sidebar:
    clear_btn = st.button("대화 초기화")

# 초기화 버튼이 눌리면
if clear_btn:
    st.session_state["messages"] = []


def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

# 사용자로부터 API 키 입력 받기
if st.session_state["api_key"] is None:
    api_key_input = st.text_input("OpenAI API 키를 입력하세요(openai key 확인을위해 약간의 토큰이 사용됩니다.)", type="password")
    if api_key_input:
        st.session_state["api_key"] = api_key_input
        try:
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 또는 "gpt-4"
            messages=[{"role": "user", "content": "안녕"}],
            timeout=10
            )
            st.rerun()  # 키가 입력되면 페이지 리로드로 적용
        except openai.error.AuthenticationError:
            print("❌ OpenAI API 키를 다시 확인해주세요.")
            api_key_input = None  
        except OpenAIError as e:
            print(f"⚠️ 오류 발생: {str(e)}")
            api_key_input = None

else:
    # 메시지 입력 UI
    user_input = st.chat_input("궁금한 내용을 물어보세요")
    print_messages()

    # 체인 생성 함수
    def create_chain():
        prompt = ChatPromptTemplate.from_messages([
            ("system", "당신은 친절한 AI assistant입니다."),
            ("user", "#Question:\n{question}"),
        ])
        llm = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0,
            openai_api_key=st.session_state["api_key"]
        )
        output_parser = StrOutputParser()
        return prompt | llm | output_parser

    if user_input:
        # 사용자 입력
        st.chat_message("user").write(user_input)
        # chain create
        chain = create_chain()
    
        response = chain.stream({"question": user_input})
        with st.chat_message("assistant"): # 유저가 질문을 던지면 컨테이너 안에 답변을 실시간 출력
            # 빈공간(컨테이너)을 만들어서,여기에 스트리밍 출력한다
            container = st.empty()
            ai_answer = ""
            for token in response:
                ai_answer += token
                container.markdown(ai_answer)

    
        # 대화기록 저장
        add_message("user",user_input)
        add_message("assistant",ai_answer)
