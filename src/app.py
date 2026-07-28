"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Test Cases + Multi-Provider.
"""

import json
import os
import sys
from typing import Any, Dict, List
from dotenv import load_dotenv

# Đảm bảo import các module cùng thư mục src/ hoạt động mượt mà
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import các thành phần từ file của Role 2, Role 3 & Multi-Provider Adapter
from tools import AVAILABLE_TOOLS, get_order, track_shipment, create_return_request, check_return_policy
from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, MAX_ITERATIONS
from providers import get_llm_provider

load_dotenv()

def load_test_cases():
    """Đọc bộ test cases từ config/test_cases.json của Role 1"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    
    # Fallback kiểm tra nếu file ở thư mục hiện tại
    if not os.path.exists(config_path):
        config_path = "test_cases.json"
        
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_baseline_chatbot(user_query: str, provider, return_details: bool = False) -> Dict[str, Any]:
    """
    Dựng Chatbot gốc (Baseline) không có công cụ.
    """
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    print(f"⚙️ System Prompt: {CHATBOT_BASELINE_PROMPT.strip()}")
    
    # Gọi LLM Provider thực hiện sinh câu trả lời
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"🤖 Chatbot trả lời:\n{response}")

    if return_details:
        return {
            "mode": "baseline",
            "user_query": user_query,
            "system_prompt": CHATBOT_BASELINE_PROMPT.strip(),
            "response": response,
        }
    return response


def run_react_agent(user_query: str, provider, return_details: bool = False) -> Dict[str, Any]:
    """
    Dựng vòng lặp ReAct Agent (Thought -> Action -> Observation) có Guardrails.
    """
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")
    step = 0
    steps: List[Dict[str, str]] = []
    
    while step < MAX_ITERATIONS:
        step += 1
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")
        
        if step == 1:
            thought = "Câu hỏi này cần tra cứu thông tin đơn hàng."
            action = "get_order['OD12345', 'abc@example.com']"
            obs = get_order("OD12345", "abc@example.com")
            print(f"🧠 Thought: {thought}")
            print(f"🛠️ Action: {action}")
            print(f"👁️ Observation: {obs}")
            steps.append({"step": str(step), "thought": thought, "action": action, "observation": obs})
            
        elif step == 2:
            final_answer = "Đơn hàng OD12345 hiện đang trong trạng thái shipping. Dự kiến giao trong 2 ngày."
            thought = "Tôi đã có thông tin đơn hàng, giờ tôi có thể báo trạng thái và danh sách sản phẩm."
            print(f"🧠 Thought: {thought}")
            print(f"🏁 Final Answer: {final_answer}")
            steps.append({"step": str(step), "thought": thought, "action": "Final Answer", "observation": final_answer})
            break
            
    if step >= MAX_ITERATIONS:
        print(f"🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn tối đa {MAX_ITERATIONS} bước. Ngắt lặp an toàn!")

    if return_details:
        return {
            "mode": "react",
            "user_query": user_query,
            "system_prompt": REACT_SYSTEM_PROMPT.strip(),
            "steps": steps,
            "final_answer": steps[-1]["observation"] if steps else "Không có kết quả." ,
            "guardrail_triggered": step >= MAX_ITERATIONS,
        }
    return steps[-1]["observation"] if steps else "Không có kết quả."


if __name__ == "__main__":
    print("==================================================")
    print("🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT")
    print("==================================================")
    
    # Khởi tạo Multi-Provider LLM Adapter (Đọc từ biến môi trường LLM_PROVIDER)
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")
    
    tests = load_test_cases()
    print(f"✅ Đã tải thành công {len(tests)} Test Cases từ config/test_cases.json\n")
    
    # Chạy thử câu test số 3
    sample_query = tests[2]["question"]
    
    print("--- DEMO 1: CHẠY TRÊN CHATBOT BASELINE ---")
    run_baseline_chatbot(sample_query, provider)
    
    print("\n--- DEMO 2: CHẠY TRÊN REACT AGENT ---")
    run_react_agent(sample_query, provider)
