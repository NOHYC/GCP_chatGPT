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


# 사용자로부터 API 키 입력 받기
if st.session_state["api_key"] is None:
    api_key_input = st.text_input("OpenAI API 키를 입력하세요", type="password")
    if api_key_input:
        st.session_state["api_key"] = api_key_input
        st.rerun()  # 키가 입력되면 페이지 리로드로 적용
else:
    # 메시지 입력 UI
    user_input = st.chat_input("궁금한 내용을 물어보세요")

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

    # 사용자 입력 처리
    if user_input:
        add_message = lambda role, msg: st.session_state["messages"].append(
            ChatMessage(role=role, content=msg)
        )

        add_message("user", user_input)
        chain = create_chain()
        response = chain.invoke({"question": user_input})
        add_message("ai", response)

    # 채팅 기록 출력
    for msg in st.session_state["messages"]:
        with st.chat_message(msg.role):
            st.markdown(msg.content)

