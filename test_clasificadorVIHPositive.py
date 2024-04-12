import unittest
from clasificadorVIH import ClasificadorVIH

class TestClasificadorVIHPositive(unittest.TestCase):

    def setUp(self):
        """Initialization before each test."""
        self.clasificador = ClasificadorVIH()


def generate_test(n_text):
    def test(self):
        """Test to verify that the classifier returns True for n_text={0}""".format(n_text)
        vih = self.clasificador.execute(n_text)
        self.assertTrue(vih[0])
    return test

for i in range(50, 100):
    test_name = 'test_{0}'.format(i)
    test = generate_test(i)
    setattr(TestClasificadorVIHPositive, test_name, test)

if __name__ == '__main__':
    unittest.main()
