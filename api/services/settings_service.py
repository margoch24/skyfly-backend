from api.models import Setting


class SettingsService:

    def get_discounts():
        return get_discounts()


def get_discounts():
    try:
        discounts = Setting.find(comparative_condition=[Setting.key.like("%discount%")])
    except Exception as e:
        print(f"ERROR (get_discounts): {e}")

        response = {"error": 1, "data": {"message": "Internal server error"}}
        return response, 500

    serialized_discounts = [discount.serialize() for discount in discounts]

    response = {
        "error": 0,
        "data": serialized_discounts,
    }
    return response, 200
