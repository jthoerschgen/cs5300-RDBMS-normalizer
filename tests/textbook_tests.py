# -*- coding: utf-8 -*-

"""textbook_tests.py

Test the different normalization functions on examples from the textbook and
compare them to the correct result.

Textbook: `Fundamentals of Database Systems` (Elmasri, Navathe).

"""

from objects.fd import FD, MVD
from objects.relation import Relation
from rdbms_normalizer import (
    normalize_to_1NF,
    normalize_to_2NF,
    normalize_to_3NF,
    normalize_to_BCNF,
)

"""Relations for testing First Normal Form (1NF)"""

Department = Relation(
    name="DEPARTMENT",
    columns={"Dname", "Dnumber", "Dmgr_ssn", "Dlocations"},
    primary_key={"Dnumber"},
    non_atomic_columns={"Dlocations"},
    functional_dependencies={
        FD(lhs={"Dnumber"}, rhs={"Dname", "Dmgr_ssn", "Dlocations"}),
    },
)  # Figure 14.9(a), Page 478

"""Relations for testing Second Normal Form (2NF)"""

Emp_Proj = Relation(
    name="EMP_PROJ",
    columns={"Ssn", "Pnumber", "Hours", "Ename", "Pname", "Plocation"},
    primary_key={"Ssn", "Pnumber"},
    functional_dependencies={
        FD(lhs={"Ssn", "Pnumber"}, rhs={"Hours"}),
        FD(lhs={"Ssn"}, rhs={"Ename"}),
        FD(lhs={"Pnumber"}, rhs={"Pname", "Plocation"}),
    },
)  # Figure 14.11(a), Page 482

"""Relations for testing Third Normal Form (3NF)"""

Emp_Dept = Relation(
    name="EMP_DEPT",
    columns={
        "Ename",
        "Ssn",
        "Bdate",
        "Address",
        "Dnumber",
        "Dname",
        "Dmgr_ssn",
    },
    primary_key={"Ssn"},
    functional_dependencies={
        FD(lhs={"Ssn"}, rhs={"Ename", "Bdate", "Address", "Dnumber"}),
        FD(lhs={"Dnumber"}, rhs={"Dname", "Dmgr_ssn"}),
    },
)  # Figure 14.11(b), Page 482

"""Relations for testing Boyce-Codd Normal Form (BCNF)"""

Teach = Relation(
    name="TEACH",
    columns={"Student", "Course", "Instructor"},
    primary_key={"Student", "Course"},
    functional_dependencies={
        FD(lhs={"Student", "Course"}, rhs={"Instructor"}),
        FD(lhs={"Instructor"}, rhs={"Course"}),
    },
)  # Figure 14.14, Page 489


def run_tests():
    # 1NF
    print("~=" * 20)
    print("TESTING FIRST NORMAL FORM")
    print("~=" * 20)
    print()
    print("ORIGINAL RELATION:")
    print()
    print(Department)
    print()
    print("--" * 20)
    print()
    print("DECOMPOSITION FOR FIRST NORMAL FORM:")
    print()
    for relation in normalize_to_1NF(relation=Department):
        print(relation)
        print(".." * 20)
    print()

    # 2NF
    print("~=" * 20)
    print("TESTING SECOND NORMAL FORM")
    print("~=" * 20)
    print()
    print("ORIGINAL RELATION:")
    print()
    print(Emp_Proj)
    print()
    print("--" * 20)
    print()
    print("DECOMPOSITION FOR SECOND NORMAL FORM:")
    print()
    for relation in normalize_to_2NF(relation=Emp_Proj):
        print()
        print(relation)
        print(".." * 20)
    print()

    # 3NF
    print("~=" * 20)
    print("TESTING THIRD NORMAL FORM")
    print("~=" * 20)
    print()
    print("ORIGINAL RELATION:")
    print()
    print(Emp_Dept)
    print()
    print("--" * 20)
    print()
    print("DECOMPOSITION FOR THIRD NORMAL FORM:")
    print()
    for relation in normalize_to_3NF(relation=Emp_Dept):
        print()
        print(relation)
        print(".." * 20)
    print()

    # BCNF
    print("~=" * 20)
    print("TESTING BOYCE-CODD NORMAL FORM")
    print("~=" * 20)
    print()
    print("ORIGINAL RELATION:")
    print()
    print(Teach)
    print()
    print("--" * 20)
    print()
    print("DECOMPOSITION FOR BOYCE-CODD NORMAL FORM:")
    print()
    for relation in normalize_to_BCNF(relation=Teach):
        print()
        print(relation)
        print(".." * 20)
    print()
