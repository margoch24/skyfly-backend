from api.models import ContactUs


class ContactUsService:

    def create_contact_us(name: str, email: str, phone_number: str, message: str):
        return create_contact_us(name, email, phone_number, message)


def create_contact_us(name: str, email: str, phone_number: str, message: str):
    try:
        contact_us = ContactUs.create(
            name=name, email=email, phone_number=phone_number, message=message
        )
    except Exception as e:
        print(f"ERROR (create_contact_us): {e}")

    if not contact_us:
        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    response = {
        "error": 0,
        "data": contact_us.serialize(),
    }
    return response, 200
