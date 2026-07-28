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
    return "Chức năng get_order đã được khai báo nhưng chưa triển khai cụ thể."


def track_shipment(tracking_code: str) -> str:
    """
    Theo dõi hành trình vận chuyển dựa trên mã theo dõi.

    Args:
        tracking_code (str): Mã vận đơn của đơn hàng.

    Returns:
        str: Trạng thái giao hàng của đơn hàng, bao gồm vị trí hiện tại và tình trạng vận chuyển.
    """
    return "Chức năng track_shipment đã được khai báo nhưng chưa triển khai cụ thể."


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
    return "Chức năng create_return_request đã được khai báo nhưng chưa triển khai cụ thể."


def check_return_policy(order_date: str, product_type: str) -> str:
    """
    Kiểm tra chính sách đổi trả cho sản phẩm dựa trên ngày đặt và loại sản phẩm.

    Args:
        order_date (str): Ngày đặt hàng (ví dụ: '2026-07-28').
        product_type (str): Loại sản phẩm để xác định điều kiện đổi trả.

    Returns:
        str: Thông tin có thể đổi trả, deadline và điều kiện áp dụng.
    """
    return "Chức năng check_return_policy đã được khai báo nhưng chưa triển khai cụ thể."


# Danh sách các tool được đăng ký để Agent sử dụng
AVAILABLE_TOOLS = {
    "get_order": get_order,
    "track_shipment": track_shipment,
    "create_return_request": create_return_request,
    "check_return_policy": check_return_policy,
}
