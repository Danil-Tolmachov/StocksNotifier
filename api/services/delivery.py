from services.abstractions import AbstractDelivery
from services.api.models import User, Developer
from services.smtp.tasks import send_email
from settings import settings


class TestDelivery(AbstractDelivery):
    def _send(self, source, *args, **kwargs):
        print(f'Delivered notification to {source}, delivery_id:{id(self)}')


class EmailDelivery(AbstractDelivery):
    default_template = settings.get_default_template()

    def get_template(self, *args, **kwargs):
        owner = self.user.developer_id

        if not owner:
            return self.default_template
        
        owner_obj = Developer.objects.get({'id': self.user.developer_id})
        return owner_obj.html_template

    def _send(self, *args, **kwargs):
        user: User = self.user
        subject = kwargs.get('subject')
        template = self.get_template(kwargs.get('context'))
        ticker: str = kwargs.get('ticker')

        if user.email is None:
            print(f'User has no email: {user.id}')
            return

        if ticker:
            send_email([user.email,], subject, template)
        else:
            send_email([user.email,], subject, template)
