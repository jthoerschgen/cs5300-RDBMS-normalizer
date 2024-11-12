from tests.test_1NF import test_1NF
from tests.test_2NF import test_2NF
from tests.test_3NF import test_3NF
from tests.test_4NF import test_4NF
from tests.test_5NF import test_5NF
from tests.textbook_tests import run_tests as run_textbook_tests


def unit_tests() -> None:
    run_textbook_tests()
    print("\n" * 3)
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
    return


if __name__ == "__main__":
    unit_tests()
