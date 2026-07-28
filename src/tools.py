"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.
"""

ORDERS = {
    "DH12345": {
        "contact": "0912345678",
        "status": "delivered",
        "date": "2026-07-25",
        "items": ["Áo thun VinUni M", "Túi xách Canvas"],
        "shipping_status": "Giao hàng thành công",
        "return_deadline_days": 7,
        "total_value": "420.000đ",
    },
    "DH67890": {
        "contact": "0987654321",
        "status": "delivered",
        "date": "2026-07-25",
        "items": ["Tai nghe Bluetooth X200"],
        "shipping_status": "Đã giao, khách báo lỗi khi mở hộp",
        "return_deadline_days": 7,
        "total_value": "590.000đ",
    },
    "DH55555": {
        "contact": "0911222333",
        "status": "delivered",
        "date": "2026-04-28",
        "items": ["Sạc dự phòng 10.000mAh"],
        "shipping_status": "Đã giao lâu, quá hạn đổi trả",
        "return_deadline_days": 7,
        "total_value": "350.000đ",
    },
}


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
        order_key = order_id.upper().strip()
        print(f"[get_order] Lookup order {order_key} with contact {contact}")
        order = ORDERS.get(order_key)
        if not order:
            return f"Đơn {order_id} không tồn tại trong hệ thống giả lập."

        if contact not in [order["contact"], order["contact"] + "@example.com"]:
            return "Thông tin liên hệ không trùng khớp. Vui lòng kiểm tra lại số điện thoại hoặc email."

        items = ", ".join(order["items"])
        return (
            f"Đơn {order_key} hiện trạng: {order['status']}. "
            f"Sản phẩm: {items}. "
            f"Tổng giá trị: {order['total_value']}. "
            f"Trạng thái vận chuyển: {order['shipping_status']}.")
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
        print(f"[track_shipment] Tracking {tracking_code}")
        code = tracking_code.upper().strip()
        if code == "TN123":
            return "Vận đơn TN123: Đã rời kho, đang trên đường giao."
        if code == "TN456":
            return "Vận đơn TN456: Đang lưu kho tại trung tâm phân phối."
        if code == "TN789":
            return "Vận đơn TN789: Đã giao thành công."
        return f"Không tìm thấy thông tin vận đơn cho mã {tracking_code}."
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
        order_key = order_id.upper().strip()
        print(f"[create_return_request] Request return for {order_key}, item {item_id}, reason {reason}")
        order = ORDERS.get(order_key)
        if not order:
            return f"Không thể tạo yêu cầu: đơn {order_id} không tồn tại."

        if order["status"] != "delivered":
            return "Không thể tạo yêu cầu đổi trả vì đơn chưa giao."

        if order_key == "DH55555":
            return "Không thể tạo yêu cầu đổi trả: đơn đã quá hạn đổi trả."

        if item_id not in order["items"]:
            return f"Sản phẩm {item_id} không thuộc đơn {order_id}."

        return (
            f"Yêu cầu đổi trả cho {item_id} trên đơn {order_key} đã được ghi nhận. "
            f"Nhân viên sẽ liên hệ bạn trong 1-2 ngày làm việc.")
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
        print(f"[check_return_policy] order_date={order_date}, product_type={product_type}")
        if product_type.lower() in ["điện tử", "tai nghe bluetooth x200", "sạc dự phòng"]:
            return (
                "Chính sách đổi trả: trong vòng 7 ngày kể từ ngày giao hàng, "
                "sản phẩm lỗi hoặc không đúng mô tả có thể được hoàn 100%."
            )
        if product_type.lower() in ["thời trang", "áo thun", "túi xách canvas"]:
            return (
                "Chính sách đổi trả: trong vòng 7 ngày kể từ ngày giao hàng, "
                "sản phẩm có lỗi hoặc sai kích cỡ có thể đổi trả."
            )
        return (
            "Chính sách đổi trả chung: thông thường 7-15 ngày. "
            "Một số sản phẩm đặc thù có thể có điều kiện riêng."
        )
    except Exception as e:
        return f"Lỗi check_return_policy: {str(e)}"


def lookup_order(order_id: str) -> str:
    """
    Tra cứu đơn hàng theo mã đơn và trả về trạng thái, ngày mua, hoặc thông báo nếu không tồn tại.
    """
    try:
        order_key = order_id.upper().strip()
        print(f"[lookup_order] Lookup {order_key}")
        order = ORDERS.get(order_key)
        if not order:
            return "Lỗi lookup_order: Đơn không tồn tại."

        return (
            f"Đơn {order_key} đang ở trạng thái {order['status']}. "
            f"Ngày mua: {order['date']}. "
            f"Sản phẩm: {', '.join(order['items'])}. "
            f"Trạng thái vận chuyển: {order['shipping_status']}"
        )
    except Exception as e:
        return f"Lỗi lookup_order: {str(e)}"


def check_return_eligibility(order_id: str) -> str:
    """
    Kiểm tra điều kiện đổi trả cho đơn hàng theo mã đơn.
    """
    try:
        order_key = order_id.upper().strip()
        print(f"[check_return_eligibility] Check {order_key}")
        order = ORDERS.get(order_key)
        if not order:
            return "Lỗi check_return_eligibility: Đơn không tồn tại."

        if order_key == "DH67890":
            return "Hợp lệ — trong hạn 7 ngày, lý do 'sản phẩm lỗi' thuộc diện được đổi trả."
        if order_key == "DH55555":
            return "Không hợp lệ — đơn đã quá hạn đổi trả."
        return "Đơn có thể được xem xét đổi trả nếu sản phẩm lỗi hoặc sai mô tả."
    except Exception as e:
        return f"Lỗi check_return_eligibility: {str(e)}"


def calculate_refund_amount(order_id: str, reason: str) -> str:
    """
    Tính số tiền hoàn trả dựa trên mã đơn và lý do đổi trả.
    """
    try:
        order_key = order_id.upper().strip()
        print(f"[calculate_refund_amount] Calculate {order_key}, reason {reason}")
        order = ORDERS.get(order_key)
        if not order:
            return "Lỗi calculate_refund_amount: Đơn không tồn tại."

        if order_key == "DH67890" and reason.lower() in ["defective", "lỗi", "sản phẩm lỗi"]:
            return f"Hoàn 100% giá trị đơn hàng = {order['total_value']}."
        if order_key == "DH55555":
            return "Không thể hoàn tiền: đơn đã quá hạn đổi trả."
        return "Không thể tính được số tiền hoàn trả do thông tin không đủ hoặc lý do chưa được hỗ trợ."
    except Exception as e:
        return f"Lỗi calculate_refund_amount: {str(e)}"


def escalate_to_human(order_id: str) -> str:
    """
    Chuyển yêu cầu đến bộ phận hỗ trợ con người khi agent không thể xử lý tự động.
    """
    try:
        print(f"[escalate_to_human] Escalate {order_id}")
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
