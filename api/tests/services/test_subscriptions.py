from fixtures import subscriptions_list

from services.checkers import Tiker
from services.subscriptions import IndividualSubscription, GroupSubscription
from services.delivery import EmailDelivery

from services.abstractions import AbstractDelivery, AbstractSubscription


# Individual Subscriptions
def test_individual_subscription():
    sub = IndividualSubscription(Tiker('AAPL'), EmailDelivery(), 1)
    assert isinstance(sub, IndividualSubscription)

    sub = IndividualSubscription(Tiker('AAPL'), 1)
    assert isinstance(sub, IndividualSubscription)

    sub = IndividualSubscription(Tiker('AAPL'))
    assert isinstance(sub, IndividualSubscription)

def test_individual_subscription_setters():
    sub = IndividualSubscription(Tiker('AAPL'))

    sub.delivery = EmailDelivery()
    assert isinstance(sub.delivery, AbstractDelivery)

    sub.subscribe(3)
    assert sub.subscriber == 3


# Group Subscriptions
def test_group_subscription():
    sub = GroupSubscription(Tiker('AAPL'), EmailDelivery(), [2, 4])
    assert isinstance(sub, GroupSubscription)

    sub = GroupSubscription(Tiker('AAPL'), [2, 4])
    assert isinstance(sub, GroupSubscription)

    sub = GroupSubscription(Tiker('AAPL'))
    assert isinstance(sub, GroupSubscription)

def test_group_subscription_setters():
    sub = GroupSubscription(Tiker('AAPL'))

    sub.delivery = EmailDelivery()
    assert isinstance(sub.delivery, AbstractDelivery)

    sub.subscribe(1)
    sub.subscribe_many([2, 3])
    assert sub.subscriber == [1, 2, 3]


# Mutural tests
def test_unsubscribe_methods(subscriptions_list: list[AbstractSubscription]):
    individual, group = subscriptions_list[1:3] # subs: individual - 2; group - [3,]

    assert individual.subscriber == 2
    assert group.subscriber == [3,]

    individual.unsubscribe()
    assert individual.subscriber == 0
    group.unsubscribe(3)
