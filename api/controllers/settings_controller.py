from flask_restful import Resource

from api.services.settings_service import SettingsService


class DiscountsResource(Resource):

    def get(self):

        response = SettingsService.get_discounts()
        return response
