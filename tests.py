import unittest

from multicurrency import Bank, Money, Sum
from utils import PairDict


class TestMultiCurrency(unittest.TestCase):

    def setUp(self):
        self.five_bucks = Money.dollar(5)
        self.ten_francs = Money.franc(10)
        self.bank = Bank()

    def test_multiplication(self):
        self.assertEquals(Money.dollar(10), self.five_bucks.times(2))
        self.assertEquals(Money.dollar(15), self.five_bucks.times(3))

    def test_equality(self):
        self.assertTrue(Money.dollar(5) == Money.dollar(5))
        self.assertFalse(Money.dollar(5) == Money.dollar(6))
        self.assertFalse(Money.dollar(5) == Money.franc(5))

    def test_currency(self):
        self.assertEquals("USD", Money.dollar(5).currency)
        self.assertEquals("CHF", Money.franc(5).currency)

    def test_simple_addition(self):
        sum = Sum(self.five_bucks, self.five_bucks)
        reduced = self.bank.reduce(sum, "USD")
        self.assertEquals(Money.dollar(10), reduced)

    def test_plus_return_sum(self):
        sum = Sum(self.five_bucks, self.five_bucks)
        self.assertEquals(self.five_bucks, sum.augend)
        self.assertEquals(self.five_bucks, sum.addend)

    def test_reduce_sum(self):
        sum = Sum(Money.dollar(3), Money.dollar(4))
        result = self.bank.reduce(sum, "USD")
        self.assertEquals(Money.dollar(7), result)

    def test_reduce_money(self):
        result = self.bank.reduce(Money.dollar(1), "USD")
        self.assertEquals(Money.dollar(1), result)

    def test_reduce_money_different_currency(self):
        self.bank.add_rate("CHF", "USD", 2)
        result = self.bank.reduce(Money.franc(2), "USD")
        self.assertEquals(Money.dollar(1), result)

    def test_identity_rate(self):
        self.assertEquals(1, Bank().rate('USD', 'USD'))

    def test_add_mixed_addition(self):
        self.bank.add_rate("CHF", "USD", 2)
        sum = Sum(self.five_bucks, self.ten_francs)
        result = self.bank.reduce(sum, "USD")
        self.assertEquals(Money.dollar(10), result)

    def test_sum_plus_money(self):
        self.bank.add_rate("CHF", "USD", 2)
        sum = Sum(self.five_bucks, self.ten_francs).plus(self.five_bucks)
        result = self.bank.reduce(sum, "USD")
        self.assertEquals(Money.dollar(15), result)

    def test_sum_times(self):
        self.bank.add_rate("CHF", "USD", 2)
        sum = Sum(self.five_bucks, self.ten_francs).times(2)
        result = self.bank.reduce(sum, "USD")
        self.assertEquals(Money.dollar(20), result)


class TestPairDict(unittest.TestCase):

    def test_pairdict_key_and_value(self):
        pd = PairDict()
        pd.add('CHF', 'USD', 2)
        self.assertTrue("CHF/USD" in pd.keys())
        self.assertEquals(pd["CHF/USD"], 2)

    def test_pairdict_equality(self):
        pd = PairDict()
        pd.add('CHF', 'USD', 2)
        pd1 = PairDict()
        pd1.add('CHF', 'USD', 2)
        pd2 = PairDict()
        pd2.add('USD', 'USD', 1)
        self.assertTrue(pd == pd1)
        self.assertFalse(pd1 == pd2)

if __name__ == '__main__':
    unittest.main()
