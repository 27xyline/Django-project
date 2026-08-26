from django.test import TestCase


class LogicTestCase(TestCase):
    def test_plus(self,):
        result = operations(6, 13, "+")
        self.assertEqual(result, 19)

    def test_minus(self,):
        result = operations(100, 20, "-")
        self.assertEqual(result, 80)


def operations(a: int, b: int, c: str) -> int:
    types_of_operations = {"+": a + b, "-": a - b, "*": a * b}
    return types_of_operations[c]
