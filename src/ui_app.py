import os
import sys

import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import get_llm_provider, load_test_cases, run_baseline_chatbot, run_react_agent

st.set_page_config(
    page_title="VinUni Agent Lab",
    page_icon="🤖",
    layout="wide",
)

CUSTOM_CSS = """
<style>
:root {
    color-scheme: dark;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #07111f 0%, #111d33 45%, #1a2f4f 100%);
}

[data-testid="stHeader"] {
    background: rgba(7, 17, 31, 0.8);
    backdrop-filter: blur(12px);
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2.5rem;
}

.hero-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.04));
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 24px;
    padding: 1.25rem 1.4rem;
    box-shadow: 0 18px 60px rgba(0,0,0,0.24);
    margin-bottom: 1rem;
}

.chat-shell {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 24px;
    padding: 1rem;
    min-height: 70vh;
}

.user-bubble {
    background: linear-gradient(90deg, #4f8cff, #6ee7f9);
    color: white;
    border-radius: 18px 18px 6px 18px;
    padding: 0.8rem 0.95rem;
    margin-bottom: 0.7rem;
}

.assistant-bubble {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px 18px 18px 6px;
    padding: 0.8rem 0.95rem;
    margin-bottom: 0.7rem;
}

.sidebar-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 0.8rem;
    margin-bottom: 0.8rem;
}

.stButton > button {
    border-radius: 999px;
    padding: 0.6rem 1rem;
    font-weight: 700;
}

[data-testid="stChatInput"] {
    border-radius: 16px;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero-card">
        <h1 style="margin:0 0 0.3rem 0; font-size: 1.9rem;">🤖 VinUni Agent Lab</h1>
        <p style="margin:0; font-size: 0.98rem; color: #dfe7f7;">
            Giao diện chatbot hiện đại để nhập câu hỏi và xem phản hồi ngay lập tức từ Chatbot hoặc ReAct Agent.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Cấu hình")
    mode = st.radio(
        "Chọn luồng chạy",
        ["baseline", "react"],
        horizontal=False,
        format_func=lambda value: "💬 Chatbot Baseline" if value == "baseline" else "🧠 ReAct Agent",
    )
    provider_name = st.selectbox(
        "Provider",
        ["mock", "openai", "gemini", "anthropic", "openrouter"],
        index=0,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
    st.markdown("### 💡 Câu hỏi mẫu")
    test_cases = load_test_cases()
    for case in test_cases:
        if st.button(f"Ví dụ {case['id']}", key=f"sample_{case['id']}", use_container_width=True):
            st.session_state["pending_prompt"] = case["question"]
    st.markdown("</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Xin chào! Tôi là trợ lý VinUni. Bạn có thể nhập câu hỏi ở khung dưới đây để bắt đầu.",
        }
    ]

main_col, info_col = st.columns([2.2, 0.8], gap="large")

with main_col:
    st.markdown("<div class='chat-shell'>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='assistant-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    user_prompt = st.chat_input("Nhập câu hỏi của bạn...")

    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.spinner("Đang xử lý..."):
            provider = get_llm_provider(provider_name)
            if mode == "baseline":
                result = run_baseline_chatbot(user_prompt, provider, return_details=True)
                answer = result["response"]
            else:
                result = run_react_agent(user_prompt, provider, return_details=True)
                answer = result["final_answer"]
                if result.get("steps"):
                    steps_text = "\n".join(
                        f"- Step {i}: {step['thought']} → {step['action']} → {step['observation']}"
                        for i, step in enumerate(result["steps"], start=1)
                    )
                    answer = f"{answer}\n\n🧭 Chi tiết luồng ReAct:\n{steps_text}"

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

with info_col:
    st.markdown("### ✨ Tính năng")
    st.info("Nhập câu hỏi ở ô trống dưới cùng để trò chuyện như chatbot thực thụ.")
    st.markdown("- Chọn chế độ Chatbot hoặc ReAct")
    st.markdown("- Dùng provider mock để demo offline")
    st.markdown("- Nhấn câu hỏi mẫu ở thanh bên để thử nhanh")

if __name__ == "__main__":
    st.write("")
