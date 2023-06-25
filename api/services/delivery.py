from sqlalchemy.orm.exc import NoResultFound

from database.models import EmailTemplate
from services.abstractions import AbstractChecker, AbstractDelivery
import settings

    

class EmailDelivery(AbstractDelivery):
    def get_template(id: int) -> EmailTemplate:
        pass
        # try:
        #     return EmailTemplate.query().get(id)
        # except:
        #     pass
        # 
        # return settings.DEFAULT_EMAIL_TEMPLATE

    def _send(self, checker: AbstractChecker):
        pass
