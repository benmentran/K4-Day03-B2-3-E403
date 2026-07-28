# 📊 BÁO CÁO GIÁM SÁT & ĐÁNH GIÁ (OBSERVABILITY TRACE LOGS)
*Dành cho Role 5: Observability & Reviewer*
*Chủ đề: OrderCare Assistant — Trợ Lý Tra Cứu Đơn Hàng & Xử Lý Đổi Trả*

---

## 🎯 1. BẢNG CHẤM ĐIỂM AGENTIC FIT (SCORING MATRIX)

| Tiêu chí | Điểm (1-5) | Lý do đánh giá |
| :--- | :---: | :--- |
| 🧠 **Multi-step Reasoning** | `5/5` | Phải suy luận qua nhiều bước: tra cứu đơn → kiểm tra điều kiện đổi trả → tính số tiền hoàn → ra quyết định cuối cùng. |
| 🛠️ **Tool Interaction** | `5/5` | Cần tra cứu dữ liệu động qua hệ thống đơn hàng (`lookup_order`) và thực hiện tính toán nghiệp vụ thực (`calculate_refund_amount`) mà LLM không thể tự biết hay tự bịa. |
| 🔀 **Dynamic Decision** | `5/5` | Kết quả bước trước quyết định hành động bước sau: nếu đơn không hợp lệ → dừng và giải thích; nếu hợp lệ nhưng lý do khác nhau (lỗi NSX vs đổi ý) → áp dụng chính sách hoàn tiền khác nhau. |
| ⏳ **Long Horizon** | `4/5` | Quy trình gồm 3-4 bước xử lý liên tiếp, có nhánh rẽ theo điều kiện (branching), không chỉ là chuỗi cố định. |
| **TỔNG ĐIỂM FIT** | **19/20** | **KẾT LUẬN: BÀI TOÁN RẤT NÊN DÙNG REACT AGENT!** Chatbot thường không thể xác minh dữ liệu đơn hàng thật hay tính đúng số tiền hoàn, dễ dẫn đến hallucination gây thiệt hại tài chính. |

---

## 🔍 2. SO SÁNH PHẢN HỒI (TEST CASE #TC02)

**Câu hỏi**: *"Đơn #DH67890 của tôi bị lỗi ngay khi mở hộp, tôi muốn trả hàng thì được hoàn bao nhiêu tiền?"*

### 🤖 Chatbot Baseline:
* **Phản hồi**: *"Thông thường các shop sẽ hoàn tiền 100% nếu sản phẩm bị lỗi trong vòng 7 ngày kể từ ngày mua. Bạn có thể liên hệ shop để được hỗ trợ cụ thể."*
* **Nhận xét**: Nghe có vẻ hợp lý nhưng **hoàn toàn là suy đoán** — chatbot không biết đơn #DH67890 có thật hay không, không biết ngày mua thực tế, và không xác nhận được đơn có còn trong hạn hay không. Nếu đơn thực tế đã quá hạn hoặc không tồn tại, câu trả lời này gây hiểu lầm nghiêm trọng cho khách hàng.

### 🧠 ReAct Agent:
* **Thought 1**: Cần xác minh đơn tồn tại trước khi xử lý bất kỳ yêu cầu nào.
* **Action 1**: `lookup_order(order_id='DH67890')`
* **Observation 1**: `Đơn tồn tại. Ngày mua: 3 ngày trước. Sản phẩm: Tai nghe Bluetooth X200.`
* **Thought 2**: Đơn hợp lệ, giờ cần kiểm tra điều kiện đổi trả có đáp ứng chính sách 7 ngày không.
* **Action 2**: `check_return_eligibility(order_id='DH67890')`
* **Observation 2**: `Hợp lệ — trong hạn 7 ngày, lý do "sản phẩm lỗi" thuộc diện được đổi trả.`
* **Thought 3**: Đơn đủ điều kiện, lý do là lỗi sản phẩm (không phải đổi ý) nên áp dụng mức hoàn tiền cao nhất.
* **Action 3**: `calculate_refund_amount(order_id='DH67890', reason='defective')`
* **Observation 3**: `Hoàn 100% giá trị đơn hàng = 590.000đ.`
* **Final Answer**: *"Đơn #DH67890 của bạn (Tai nghe Bluetooth X200, mua 3 ngày trước) đủ điều kiện đổi trả do lỗi sản phẩm. Bạn sẽ được hoàn 100% = 590.000đ. Mình sẽ ghi nhận yêu cầu đổi trả ngay, bạn xác nhận nhé?"*
* **Nhận xét**: Câu trả lời **dựa hoàn toàn trên dữ liệu thật** được xác minh qua 3 bước Tool, không có bịa đặt, số tiền hoàn chính xác theo đúng chính sách áp dụng cho đúng loại lý do.

---

## 📌 3. NHẬN XÉT TỔNG QUAN

| Khía cạnh | Chatbot Baseline | ReAct Agent |
| :--- | :--- | :--- |
| Độ chính xác dữ liệu | Suy đoán, có thể sai lệch thực tế | Xác minh qua Tool ở mọi bước |
| Khả năng xử lý edge case (đơn không tồn tại, quá hạn) | Không xử lý được, dễ trả lời chung chung sai lệch | Phát hiện và phản hồi đúng thực tế (xem TC04, TC05) |
| Rủi ro tài chính khi triển khai thật | Cao — có thể hứa hoàn tiền sai chính sách | Thấp — mọi quyết định hoàn tiền đều có Observation làm bằng chứng |
| Độ phù hợp với bài toán | Thấp | Rất cao (19/20 điểm Agentic Fit) |

**Kết luận Role 5**: Với bài toán tra cứu đơn hàng & xử lý đổi trả, ReAct Agent là lựa chọn bắt buộc chứ không chỉ là "nên dùng" — vì hậu quả của một câu trả lời sai (hoàn tiền sai, xác nhận nhầm đơn) có chi phí thực tế, trong khi Chatbot baseline không có cách nào xác minh được các thông tin này trước khi trả lời.