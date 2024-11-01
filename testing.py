from tests import textbook_tests
from tests.test_1NF import test_1NF
from tests.test_2NF import test_2NF
from tests.test_3NF import test_3NF
from tests.test_4NF import test_4NF
from tests.test_5NF import test_5NF


def unit_tests():
    test_1NF()
    print("\n" * 3)
    test_2NF()
    print("\n" * 3)
    test_3NF()
    print("\n" * 3)
    test_4NF()
    print("\n" * 3)
    test_5NF()
    print("\n" * 3)
    textbook_tests.run_tests()
    return


if __name__ == "__main__":
    unit_tests()
