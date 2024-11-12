from objects.fd import FD
from objects.relation import Relation
from rdbms_normalizer import normalize_to_BCNF

Teach = Relation(
    name="TEACH",
    columns={"Student", "Course", "Instructor"},
    primary_key={"Student", "Course"},
    functional_dependencies={
        FD(lhs={"Student", "Course"}, rhs={"Instructor"}),
        FD(lhs={"Instructor"}, rhs={"Course"}),
    },
)


def test_BCNF() -> None:
    # BCNF
    for relation in (Teach,):
        print("~=" * 20)
        print("TESTING BOYCE-CODD NORMAL FORM")
        print("~=" * 20)
        print()
        print("ORIGINAL RELATION:")
        print()
        print(relation)
        print()
        print("--" * 20)
        print()
        print("DECOMPOSITION FOR BOYCE-CODD NORMAL FORM:")
        print()
        for decomposed_relation in normalize_to_BCNF(relation):
            print()
            print(decomposed_relation)
            print(".." * 20)
        print()
