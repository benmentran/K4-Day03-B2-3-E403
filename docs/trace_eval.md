# BÁO CÁO GIÁM SÁT & ĐÁNH GIÁ (OBSERVABILITY TRACE LOGS)

**Dành cho:** Role 5: Observability & Reviewer
**Chủ đề:** OrderCare Assistant — Trợ Lý Tra Cứu Đơn Hàng & Xử Lý Đổi Trả

---

## 🎯 1. Bảng Chấm Điểm Agentic Fit (Scoring Matrix)

| Tiêu chí | Điểm (1-5) | Lý do đánh giá |
|---|---|---|
| 🧠 Multi-step Reasoning | 5/5 | Quy trình gồm nhiều bước phụ thuộc nhau: tra cứu đơn → kiểm tra điều kiện → tính hoàn tiền → quyết định |
| 🛠️ Tool Interaction | 5/5 | Cần truy cập dữ liệu thật (order DB) và logic nghiệp vụ |
| 🔀 Dynamic Decision | 5/5 | Nhánh xử lý phụ thuộc vào trạng thái đơn & lý do đổi trả |
| ⏳ Long Horizon | 4/5 | 3–4 bước liên tiếp có branching |
| **TỔNG ĐIỂM FIT** | **19/20** | **KẾT LUẬN: RẤT PHÙ HỢP VỚI REACT AGENT** |

---

## 🔍 2. So Sánh Phản Hồi (Test Case #TC02)

**Câu hỏi:**
> "Đơn #DH67890 của tôi bị lỗi, tôi được hoàn bao nhiêu tiền?"

### 🤖 Chatbot Baseline:

> "Thông thường sẽ hoàn 100% nếu lỗi trong 7 ngày."

**❌ Vấn đề:**
- Không biết đơn có tồn tại không
- Không biết có còn trong hạn không
- Có thể hallucinate → gây thiệt hại tài chính

### 🧠 ReAct Agent:

```
Thought 1: Xác minh đơn hàng tồn tại
Action 1: get_order(order_id="DH67890")
Observation 1: Đơn tồn tại. Giá: 590.000đ. Ngày mua: 3 ngày trước.

Thought 2: Kiểm tra điều kiện đổi trả
Action 2: check_return_eligibility(order_id="DH67890")
Observation 2: Hợp lệ — lý do sản phẩm lỗi.

Thought 3: Tính tiền hoàn
Action 3: calculate_refund_amount(order_id="DH67890", reason="defective")
Observation 3: Hoàn 100% = 590.000đ.
```

**✅ Final Answer:**
> Bạn sẽ được hoàn 100% = 590.000đ do sản phẩm bị lỗi.

---

## 🧪 3. Trace Từ src/app.py (Updated)

### ✅ Trace Test Case 1

**Question:** Chính sách đổi trả trong bao nhiêu ngày?

```
Thought 1: Đây là câu hỏi chung → không cần tool
Action: None
Final Answer: Chính sách đổi trả áp dụng trong vòng 7 ngày kể từ ngày nhận hàng.
```

### ✅ Trace Test Case 2

**Question:** Đổi trả cần chuẩn bị gì?

```
Thought 1: Đây là câu hỏi hướng dẫn
Action: None
Final Answer:
Bạn cần:
- Mã đơn hàng
- Lý do đổi trả
- Hình ảnh sản phẩm (nếu lỗi)
- Thông tin liên hệ
```

### ✅ Trace Test Case 3

**Question:** Đơn #DH12345 đang ở đâu?

```
Thought 1: Cần tra cứu đơn hàng
Action 1: get_order(order_id="DH12345")
Observation 1: Trạng thái: Đang giao hàng
Final Answer: Đơn hàng đang được giao.
```

### ✅ Trace Test Case 4

**Question:** Đơn #DH67890 có đủ điều kiện đổi trả không?

```
Thought 1: Tra cứu đơn
Action 1: get_order(order_id="DH67890")
Observation 1: Ngày mua: 3 ngày trước

Thought 2: Kiểm tra điều kiện
Action 2: check_return_eligibility(order_id="DH67890")
Observation 2: Hợp lệ
Final Answer: Đơn vẫn đủ điều kiện đổi trả.
```

### ✅ Trace Test Case 5

**Question:** Đơn #DH67890 bị lỗi, hoàn bao nhiêu tiền?

```
Thought 1: Lấy thông tin đơn
Action 1: get_order(order_id="DH67890")
Observation 1: Giá: 590.000đ

Thought 2: Kiểm tra điều kiện
Action 2: check_return_eligibility(order_id="DH67890")
Observation 2: Hợp lệ — defective

Thought 3: Tính tiền hoàn
Action 3: calculate_refund_amount(...)
Observation 3: 590.000đ
Final Answer: Hoàn 590.000đ (100%)
```

---

## 🧪 4. Trace Edge Case & Guardrail

### ❗ Case: Tool chưa trả về dữ liệu

**Question:** Đơn #DH99999 của tôi đâu?

```
Thought 1: Tra cứu đơn
Action 1: get_order(order_id="DH99999")
Observation 1: Không tìm thấy
Final Answer:
Xin lỗi, mình không tìm thấy đơn hàng này. Bạn kiểm tra lại mã đơn hoặc cung cấp thêm SĐT/email nhé.
```

### ⚙️ Guardrail

- `MAX_ITERATIONS = 5` → tránh loop vô hạn
- Không retry cùng 1 action quá 2 lần
- Nếu tool fail → fallback hỏi user

---

## 📌 5. Nhận Xét Tổng Quan

| Khía cạnh | Chatbot | ReAct Agent |
|---|---|---|
| Độ chính xác | Suy đoán | Dựa trên dữ liệu thật |
| Xử lý edge case | Kém | Tốt |
| Rủi ro tài chính | Cao | Thấp |
| Khả năng scale | Trung bình | Cao |

---

## 🎯 Kết Luận Cuối

**👉 Với bài toán Order & Refund:**

- Chatbot = ❌ không đủ an toàn
- ReAct Agent = ✅ bắt buộc dùng

**Lý do:**
- Có dữ liệu thật
- Có logic nghiệp vụ
- Có rủi ro tiền