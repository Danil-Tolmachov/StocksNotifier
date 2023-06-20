from abc import ABC, abstractmethod
from sqlalchemy.orm.exc import NoResultFound

from database.models import EmailTemplate
import settings
        

class AbstractDelivery(ABC):
    @abstractmethod
    def send(self):
        """Sends a message about the event"""
        pass
    

class EmailDelivery(AbstractDelivery):

    def get_template(id: int) -> EmailTemplate:
        try:
            return EmailTemplate.query().get(id)
        except:
            pass
        
        return settings.DEFAULT_EMAIL_TEMPLATE

    def send(self, receivers: list):
        pass
