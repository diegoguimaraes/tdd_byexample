import abc

from utils import PairDict


class Bank(object):

    _rates = PairDict()

    def reduce(self, source, to):
        return source.reduce(self, to)

    def add_rate(self, fromm, to, rate):
        self._rates.add(fromm, to, rate)

    def rate(self, fromm, to):
        return 1 if fromm == to else self._rates.get(fromm, to)


class Expression(object):

    __metacass__ = abc.ABCMeta

    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend

    @abc.abstractmethod
    def reduce(self, bank, to):
        raise NotImplementedError("Not implemented")

    @abc.abstractmethod
    def plus(self, addend):
        raise NotImplementedError("Not implemented")

    @abc.abstractmethod
    def times(self, multiplier):
        raise NotImplementedError("Not implemented")


class Sum(Expression):

    def reduce(self, bank, to):
        amount = self.augend.reduce(bank, to)._amount + self.addend.reduce(bank, to)._amount
        return Money(amount, to)

    def plus(self, addend):
        return Sum(self, addend)

    def times(self, multiplier):
        return Sum(self.augend.times(multiplier), self.addend.times(multiplier))


class Money(Expression):

    def __init__(self, amount, currency):
        self._amount = amount
        self._currency = currency

    def __eq__(self, other):
        return self._amount == other._amount and self._currency == other._currency

    @staticmethod
    def dollar(amount):
        return Money(amount, "USD")

    @staticmethod
    def franc(amount):
        return Money(amount, "CHF")

    @property
    def currency(self):
        return self._currency

    def times(self, multiplier):
        return Money(self._amount * multiplier, self._currency)

    def reduce(self, bank, to):
        rate = bank.rate(self._currency, to)
        return Money(self._amount / rate, to)

    def __repr__(self):
        return "<{0} {1} {2}>".format(self.__class__, self._amount, self._currency)
