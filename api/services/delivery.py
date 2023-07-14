from services.abstractions import AbstractDelivery
from services.api.models import User


class TestDelivery(AbstractDelivery):
    def _send(self, source, *args, **kwargs):
        print(f'Delivered notification to {source}, delivery_id:{id(self)}')

class EmailDelivery(AbstractDelivery):
    def get_template(id: int):
        pass

    def _send(self, user: User):
        pass
