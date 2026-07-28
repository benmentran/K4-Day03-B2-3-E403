"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Test Cases + Multi-Provider.
"""

import json
import os
import sys
import re
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


def run_baseline_chatbot(user_query: str, provider):
    """
    Dựng Chatbot gốc (Baseline) không có công cụ.
    """
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    print(f"⚙️ System Prompt: {CHATBOT_BASELINE_PROMPT.strip()}")
    
    # Gọi LLM Provider thực hiện sinh câu trả lời
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"🤖 Chatbot trả lời:\n{response}")


def parse_agent_response(response: str) -> tuple[str, str | None, str | None]:
    """Trích xuất Thought, Action và Final Answer từ phản hồi LLM."""
    thought = None
    action = None
    final_answer = None
    for line in response.splitlines():
        line = line.strip()
        if not line:
            continue
        lower = line.lower()
        if lower.startswith("thought:"):
            thought = line.split(":", 1)[1].strip()
        elif lower.startswith("action:"):
            action = line.split(":", 1)[1].strip()
        elif lower.startswith("final answer:"):
            final_answer = line.split(":", 1)[1].strip()
    return thought, action, final_answer


def parse_action(action: str) -> tuple[str | None, list[str], str | None]:
    """Phân tích cú pháp Action dạng tool[arg1, arg2]."""
    if not action:
        return None, [], "Không có Action để thực thi."

    match = re.match(r"^([a-zA-Z_][\w]*)\s*\[\s*(.*?)\s*\]$", action)
    if not match:
        return None, [], f"Cú pháp Action không hợp lệ: {action}"

    tool_name = match.group(1)
    args_text = match.group(2)
    args = []
    if args_text:
        args = [arg.strip().strip("'\"") for arg in args_text.split(",")]
    return tool_name, args, None


def execute_tool(action: str) -> tuple[str, bool]:
    """Thực thi tool và trả về Observation cùng chỉ báo lỗi nếu có."""
    tool_name, args, parse_error = parse_action(action)
    if parse_error:
        return parse_error, True

    if tool_name not in AVAILABLE_TOOLS:
        return f"Lỗi tool: '{tool_name}' không hợp lệ.", True

    try:
        result = AVAILABLE_TOOLS[tool_name](*args)
        is_error = isinstance(result, str) and result.strip().lower().startswith("lỗi")
        return result, is_error
    except Exception as exc:
        return f"Lỗi thực thi tool {tool_name}: {str(exc)}", True


def build_agent_prompt(user_query: str, history: list[dict]) -> str:
    """Xây dựng prompt cho LLM bằng câu hỏi và lịch sử Thought/Action/Observation."""
    prompt_lines = [f"User Query: {user_query}"]
    if history:
        prompt_lines.append("History:")
        for step, item in enumerate(history, start=1):
            prompt_lines.append(f"Thought {step}: {item['thought']}")
            prompt_lines.append(f"Action {step}: {item['action']}")
            prompt_lines.append(f"Observation {step}: {item['observation']}")
    return "\n".join(prompt_lines)


def append_trace_to_doc(test_id: int, question: str, history: list[dict], final_answer: str | None) -> None:
    """Nối trace log vào docs/trace_eval.md để review sau này."""
    trace_lines = [
        "\n---\n",
        f"## Trace Test Case {test_id}\n",
        f"**Question**: {question}\n",
    ]
    for idx, item in enumerate(history, start=1):
        trace_lines.append(f"* **Thought {idx}**: {item['thought']}\n")
        trace_lines.append(f"* **Action {idx}**: `{item['action']}`\n")
        trace_lines.append(f"* **Observation {idx}**: `{item['observation']}`\n")
    if final_answer:
        trace_lines.append(f"* **Final Answer**: {final_answer}\n")
    else:
        trace_lines.append("* **Final Answer**: [Chưa có Final Answer trước khi chạm guardrail]\n")

    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "trace_eval.md"), "a", encoding="utf-8") as f:
        f.writelines(trace_lines)


def run_react_agent(user_query: str, provider):
    """Duyệt vòng lặp ReAct Agent và retry nếu chọn sai tool hoặc tool trả về lỗi."""
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")
    history = []
    step = 0
    final_answer = None

    while step < MAX_ITERATIONS:
        step += 1
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")

        prompt = build_agent_prompt(user_query, history)
        response = provider.generate(prompt, system_prompt=REACT_SYSTEM_PROMPT)
        thought, action, final = parse_agent_response(response)

        if thought:
            print(f"🧠 Thought: {thought}")
        else:
            print("🧠 Thought: [Không có Thought rõ ràng]")

        if final:
            print(f"🏁 Final Answer: {final}")
            final_answer = final
            break

        if action:
            print(f"🛠️ Action: {action}")
            observation, tool_failed = execute_tool(action)
        else:
            observation = "Lỗi: Agent không cung cấp Action."
            tool_failed = True

        print(f"👁️ Observation: {observation}")
        history.append({"thought": thought or "[Không có Thought]", "action": action or "[Không có Action]", "observation": observation})

        if tool_failed:
            print("⚠️ Phát hiện lỗi trong bước này, sẽ suy luận lại và thử công cụ khác nếu cần.")
            continue

    if not final_answer and step >= MAX_ITERATIONS:
        print(f"🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn tối đa {MAX_ITERATIONS} bước. Ngắt lặp an toàn!")

    return history, final_answer


def run_all_tests(provider):
    tests = load_test_cases()
    for test in tests:
        print(f"\n============================")
        print(f"TEST CASE {test['id']}: {test['question']}")
        print(f"============================")
        run_baseline_chatbot(test['question'], provider)
        history, final_answer = run_react_agent(test['question'], provider)
        append_trace_to_doc(test['id'], test['question'], history, final_answer)


if __name__ == "__main__":
    print("==================================================")
    print("🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT")
    print("==================================================")
    
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")
    
    print("--- CHẠY TOÀN BỘ TEST CASES ---")
    run_all_tests(provider)
