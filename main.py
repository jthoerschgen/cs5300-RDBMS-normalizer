# -*- coding: utf-8 -*-

from tests import textbook_tests
from tests.test_1NF import test_1NF
from tests.test_2NF import test_2NF
from tests.test_3NF import test_3NF
from tests.test_4NF import test_4NF
from tests.test_5NF import test_5NF

# from tests.test_BCNF import test_BCNF


def main():
    test_1NF()
    test_2NF()
    test_3NF()
    # test_BCNF()
    test_4NF()
    test_5NF()
    # textbook_tests.run_tests()

    return


if __name__ == "__main__":
    main()
