"""textbook_tests.py

Test the different normalization functions on examples from the textbook and
compare them to the correct result.

Textbook: `Fundamentals of Database Systems` (Elmasri, Navathe).

"""

from objects.fd import FD, MVD, NonAtomic
from objects.relation import Relation
from rdbms_normalizer import (
    normalize_to_1NF,
    normalize_to_2NF,
    normalize_to_3NF,
    normalize_to_4NF,
    normalize_to_5NF,
    normalize_to_BCNF,
)

"""Relations for testing First Normal Form (1NF)"""

Department = Relation(
    name="DEPARTMENT",
    columns={"Dname", "Dnumber", "Dmgr_ssn", "Dlocations"},
    primary_key={"Dnumber"},
    non_atomic_columns={NonAtomic(lhs={"Dnumber"}, rhs={"Dlocations"})},
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

Enrollment = Relation(
    name="Enrollment",
    columns={
        "StudentID",
        "Semester",
        "CourseID",
        "TuitionCost",
        "Grade",
        "Classroom",
    },
    primary_key={"StudentID", "Semester"},
    functional_dependencies={
        FD(lhs={"StudentID", "Semester"}, rhs={"CourseID"}),
        FD(lhs={"StudentID", "Semester"}, rhs={"TuitionCost"}),  # PFD
        FD(lhs={"StudentID", "Semester"}, rhs={"Grade"}),
        FD(lhs={"StudentID", "Semester"}, rhs={"Classroom"}),
        FD(lhs={"Semester"}, rhs={"TuitionCost"}),  # PFD
        FD(lhs={"CourseID"}, rhs={"Classroom"}),
    },
)  # Question 6, Quiz: Understanding Functional Dependencies and Normalization

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

""" Relations for testing determining Multivalued Dependencies (MVDs)"""

Emp_no_MVDs_provided = Relation(
    name="EMP",
    columns={
        "Ename",
        "Pname",
        "Dname",
    },
    primary_key={"Ename", "Pname", "Dname"},
    multivalued_dependencies=set(),
    # MVD(lhs={"Ename"},rhs={"Pname", "Dname"})
    data_instances=[
        {"Ename": "Smith", "Pname": "X", "Dname": "John"},
        {"Ename": "Smith", "Pname": "Y", "Dname": "Anna"},
        {"Ename": "Smith", "Pname": "X", "Dname": "Anna"},
        {"Ename": "Smith", "Pname": "Y", "Dname": "John"},
        {"Ename": "Brown", "Pname": "W", "Dname": "Jim"},
        {"Ename": "Brown", "Pname": "X", "Dname": "Jim"},
        {"Ename": "Brown", "Pname": "Y", "Dname": "Jim"},
        {"Ename": "Brown", "Pname": "Z", "Dname": "Jim"},
        {"Ename": "Brown", "Pname": "W", "Dname": "Joan"},
        {"Ename": "Brown", "Pname": "X", "Dname": "Joan"},
        {"Ename": "Brown", "Pname": "Y", "Dname": "Joan"},
        {"Ename": "Brown", "Pname": "Z", "Dname": "Joan"},
        {"Ename": "Brown", "Pname": "W", "Dname": "Bob"},
        {"Ename": "Brown", "Pname": "X", "Dname": "Bob"},
        {"Ename": "Brown", "Pname": "Y", "Dname": "Bob"},
        {"Ename": "Brown", "Pname": "Z", "Dname": "Bob"},
    ],
)  # Figure 15.4, Page 529

"""Relations for testing Fourth Normal Form (4NF)"""

Emp = Relation(
    name="EMP",
    columns={
        "Ename",
        "Pname",
        "Dname",
    },
    primary_key={"Ename", "Pname", "Dname"},
    multivalued_dependencies={
        MVD(lhs={"Ename"}, rhs=({"Pname"}, {"Dname"})),
    },
    data_instances=[
        {"Ename": "Smith", "Pname": "X", "Dname": "John"},
        {"Ename": "Smith", "Pname": "Y", "Dname": "Anna"},
        {"Ename": "Smith", "Pname": "X", "Dname": "Anna"},
        {"Ename": "Smith", "Pname": "Y", "Dname": "John"},
        {"Ename": "Brown", "Pname": "W", "Dname": "Jim"},
        {"Ename": "Brown", "Pname": "X", "Dname": "Jim"},
        {"Ename": "Brown", "Pname": "Y", "Dname": "Jim"},
        {"Ename": "Brown", "Pname": "Z", "Dname": "Jim"},
        {"Ename": "Brown", "Pname": "W", "Dname": "Joan"},
        {"Ename": "Brown", "Pname": "X", "Dname": "Joan"},
        {"Ename": "Brown", "Pname": "Y", "Dname": "Joan"},
        {"Ename": "Brown", "Pname": "Z", "Dname": "Joan"},
        {"Ename": "Brown", "Pname": "W", "Dname": "Bob"},
        {"Ename": "Brown", "Pname": "X", "Dname": "Bob"},
        {"Ename": "Brown", "Pname": "Y", "Dname": "Bob"},
        {"Ename": "Brown", "Pname": "Z", "Dname": "Bob"},
    ],
)  # Figure 15.4, Page 529

"""Relations for testing Fifth Normal Form (5NF)"""

Supply = Relation(
    name="Suppy",
    columns={"Sname", "Part_name", "Proj_name"},
    primary_key={"Sname", "Part_name", "Proj_name"},
    data_instances=[
        {"Sname": "Smith", "Part_name": "Bolt", "Proj_name": "ProjX"},
        {"Sname": "Smith", "Part_name": "Nut", "Proj_name": "ProjY"},
        {"Sname": "Adamsky", "Part_name": "Bolt", "Proj_name": "ProjY"},
        {"Sname": "Walton", "Part_name": "Nut", "Proj_name": "ProjZ"},
        {"Sname": "Adamsky", "Part_name": "Nail", "Proj_name": "ProjX"},
        {"Sname": "Adamsky", "Part_name": "Bolt", "Proj_name": "ProjX"},
        {"Sname": "Smith", "Part_name": "Bolt", "Proj_name": "ProjY"},
    ],
)  # Figure 14.15, Page 492


def run_tests() -> None:
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

    print("~=" * 20)
    print("TESTING SECOND NORMAL FORM")
    print("~=" * 20)
    print()
    print("ORIGINAL RELATION:")
    print()
    print(Enrollment)
    print()
    print("--" * 20)
    print()
    print("DECOMPOSITION FOR SECOND NORMAL FORM:")
    print()
    for relation in normalize_to_2NF(relation=Enrollment):
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

    # DETERMINING MVDs
    # print("~=" * 20)
    # print("TESTING DETERMINING MVDs")
    # print("~=" * 20)
    # print()
    # print("ORIGINAL RELATION:")
    # print()
    # print(Emp_no_MVDs_provided)
    # print()
    # print("--" * 20)
    # print()
    # print("MULTIVALUED DEPENDENCIES FOR RELATION:")
    # print()
    # Emp_with_MVDs = Emp_no_MVDs_provided
    # Emp_with_MVDs.determine_mvds()
    # for mvd in Emp_with_MVDs.multivalued_dependencies:
    #     print()
    #     print(mvd)
    #     print(".." * 20)
    # print()

    # 4NF
    print("~=" * 20)
    print("TESTING FOURTH NORMAL FORM")
    print("~=" * 20)
    print()
    print("ORIGINAL RELATION:")
    print()
    print(Emp)
    print()
    print("--" * 20)
    print()
    print("DECOMPOSITION FOR FOURTH NORMAL FORM:")
    print()
    for relation in normalize_to_4NF(relation=Emp):
        print()
        print(relation)
        print(".." * 20)
    print()

    # 5NF
    print("~=" * 20)
    print("TESTING FIFTH NORMAL FORM")
    print("~=" * 20)
    print()
    print("ORIGINAL RELATION:")
    print()
    print(Supply)
    print()
    print("--" * 20)
    print()
    print("DECOMPOSITION FOR FIFTH NORMAL FORM:")
    print()
    for relation in normalize_to_5NF(relation=Supply):
        print()
        print(relation)
        print(".." * 20)
    print()
