from sqlalchemy.orm.exc import NoResultFound

from database.models import EmailTemplate
from services.abstractions import AbstractChecker, AbstractDelivery
import settings

class TestDelivery(AbstractDelivery):
    def _send(self, source, *args, **kwargs):
        print(f'Delivered notification to {source}, delivery_id:{id(self)}')

class EmailDelivery(AbstractDelivery):
    def get_template(id: int) -> EmailTemplate:
        pass

    def _send(self, checker: AbstractChecker):
        pass
