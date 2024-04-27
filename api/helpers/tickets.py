import os
from datetime import datetime

import qrcode

from api.constants import TEST_QRCODE, Environment, TicketType
from api.helpers import get_random
from api.models import Setting
from config import DefaultConfig


def check_age(date_of_birth):
    date_of_birth_sec = date_of_birth / 1000

    birth_date = datetime.fromtimestamp(date_of_birth_sec)

    today = datetime.now()

    age_in_years = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )

    ticket_type = TicketType.ADULT

    if age_in_years < 18:
        ticket_type = TicketType.CHILD

    return ticket_type


def calculate_discount(flight, date_of_birth):
    price = flight.price
    ticket_type = check_age(date_of_birth)

    if ticket_type == TicketType.CHILD:
        setting = Setting.find_one({"key": "ticket_child_discount"})
        ticket_child_discount = float(setting.value)
        price *= ticket_child_discount

    return [price, ticket_type]


def generate_qrcode(ticket_id: str):
    if DefaultConfig.ENV == Environment.TEST:
        return TEST_QRCODE

    current_dir = os.path.dirname(os.path.abspath(__file__))

    uploads_dir = os.path.join(current_dir, "../../../uploads/qrcodes")

    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=50,
        border=1,
    )
    qr.add_data(f"{DefaultConfig.BACKEND_API_URL}/check-ticket?ticket_id={ticket_id}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="#212940", back_color="white")
    img_name = f"{get_random(100000)}_qrcode.png"
    img_path = os.path.join(uploads_dir, img_name)
    img.save(img_path)

    return img_path
