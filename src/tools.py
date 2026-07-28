"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.
"""


def get_order(order_id: str, contact: str) -> str:
    """
    Tra cứu thông tin đơn hàng theo mã đơn và số điện thoại hoặc email.

    Args:
        order_id (str): Mã đơn hàng cần tra cứu.
        contact (str): Số điện thoại hoặc email của khách hàng.

    Returns:
        str: Thông tin trạng thái đơn, danh sách sản phẩm và thời gian giao hàng dự kiến.
    """
    try:
        # TODO: Thêm logic tra cứu đơn hàng thực tế ở đây.
        return "Chức năng get_order đã được khai báo nhưng chưa triển khai cụ thể."
    except Exception as e:
        return f"Lỗi get_order: {str(e)}"


def track_shipment(tracking_code: str) -> str:
    """
    Theo dõi hành trình vận chuyển dựa trên mã theo dõi.

    Args:
        tracking_code (str): Mã vận đơn của đơn hàng.

    Returns:
        str: Trạng thái giao hàng của đơn hàng, bao gồm vị trí hiện tại và tình trạng vận chuyển.
    """
    try:
        # TODO: Thêm logic theo dõi vận chuyển thực tế ở đây.
        return "Chức năng track_shipment đã được khai báo nhưng chưa triển khai cụ thể."
    except Exception as e:
        return f"Lỗi track_shipment: {str(e)}"


def create_return_request(order_id: str, reason: str, item_id: str) -> str:
    """
    Tạo yêu cầu đổi trả cho một sản phẩm trong đơn hàng.

    Args:
        order_id (str): Mã đơn hàng liên quan.
        reason (str): Lý do đổi trả.
        item_id (str): Mã sản phẩm cần đổi trả.

    Returns:
        str: Kết quả khởi tạo yêu cầu đổi trả, gồm bước tiếp theo hoặc thông báo lỗi nếu không hợp lệ.
    """
    try:
        # TODO: Thêm logic xử lý yêu cầu đổi trả ở đây.
        return "Chức năng create_return_request đã được khai báo nhưng chưa triển khai cụ thể."
    except Exception as e:
        return f"Lỗi create_return_request: {str(e)}"


def check_return_policy(order_date: str, product_type: str) -> str:
    """
    Kiểm tra chính sách đổi trả cho sản phẩm dựa trên ngày đặt và loại sản phẩm.

    Args:
        order_date (str): Ngày đặt hàng (ví dụ: '2026-07-28').
        product_type (str): Loại sản phẩm để xác định điều kiện đổi trả.

    Returns:
        str: Thông tin có thể đổi trả, deadline và điều kiện áp dụng.
    """
    try:
        # TODO: Thêm logic kiểm tra chính sách đổi trả ở đây.
        return "Chức năng check_return_policy đã được khai báo nhưng chưa triển khai cụ thể."
    except Exception as e:
        return f"Lỗi check_return_policy: {str(e)}"


def lookup_order(order_id: str) -> str:
    """
    Tra cứu đơn hàng theo mã đơn và trả về trạng thái, ngày mua, hoặc thông báo nếu không tồn tại.
    """
    try:
        if order_id.upper() == "DH12345":
            return "Đơn DH12345 đang ở trạng thái delivered. Giao hàng thành công."
        if order_id.upper() == "DH67890":
            return "Đơn DH67890 tồn tại. Ngày mua: 3 ngày trước. Sản phẩm: Tai nghe Bluetooth X200."
        if order_id.upper() == "DH55555":
            return "Đơn DH55555 đã mua 3 tháng trước. Trạng thái: quá hạn đổi trả."
        if order_id.upper() == "KHONGTONTAI999":
            return "Lỗi lookup_order: Đơn không tồn tại."
        return f"Đơn {order_id} tồn tại nhưng dữ liệu chi tiết chưa được mô phỏng."
    except Exception as e:
        return f"Lỗi lookup_order: {str(e)}"


def check_return_eligibility(order_id: str) -> str:
    """
    Kiểm tra điều kiện đổi trả cho đơn hàng theo mã đơn.
    """
    try:
        if order_id.upper() == "DH67890":
            return "Hợp lệ — trong hạn 7 ngày, lý do 'sản phẩm lỗi' thuộc diện được đổi trả."
        if order_id.upper() == "DH55555":
            return "Không hợp lệ — đơn đã quá hạn đổi trả."
        if order_id.upper() == "KHONGTONTAI999":
            return "Lỗi check_return_eligibility: Đơn không tồn tại."
        return "Không đủ dữ liệu để xác định điều kiện đổi trả cho đơn hàng này."
    except Exception as e:
        return f"Lỗi check_return_eligibility: {str(e)}"


def calculate_refund_amount(order_id: str, reason: str) -> str:
    """
    Tính số tiền hoàn trả dựa trên mã đơn và lý do đổi trả.
    """
    try:
        if order_id.upper() == "DH67890" and reason.lower() in ["defective", "lỗi", "sản phẩm lỗi"]:
            return "Hoàn 100% giá trị đơn hàng = 590.000đ."
        if order_id.upper() == "DH55555":
            return "Không thể hoàn tiền: đơn đã quá hạn đổi trả."
        return "Không thể tính được số tiền hoàn trả do thông tin không đủ hoặc lý do chưa được hỗ trợ."
    except Exception as e:
        return f"Lỗi calculate_refund_amount: {str(e)}"


def escalate_to_human(order_id: str) -> str:
    """
    Chuyển yêu cầu đến bộ phận hỗ trợ con người khi agent không thể xử lý tự động.
    """
    try:
        return f"Yêu cầu của đơn {order_id} đã được chuyển đến bộ phận hỗ trợ trực tiếp."
    except Exception as e:
        return f"Lỗi escalate_to_human: {str(e)}"


# Danh sách các tool được đăng ký để Agent sử dụng
AVAILABLE_TOOLS = {
    "get_order": get_order,
    "track_shipment": track_shipment,
    "create_return_request": create_return_request,
    "check_return_policy": check_return_policy,
    "lookup_order": lookup_order,
    "check_return_eligibility": check_return_eligibility,
    "calculate_refund_amount": calculate_refund_amount,
    "escalate_to_human": escalate_to_human,
}
