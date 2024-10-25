# -*- coding: utf-8 -*-


class Dependency:
    """Representation of a dependency.

    Attributes:
        lhs (set[str]): Left-hand side of the dependency.
        rhs (set[str]): Right-hand side of the dependency.
    """

    def __init__(self, lhs: set[str], rhs: set[str]):
        """The constructor for a dependency.

        Args:
            lhs (set[str]): The attributes that comprise the left-hand side
                of the dependency.
            rhs (set[str]): The attributes that comprise the right-hand side
                of the dependency.
        """
        self.lhs: set[str] = lhs.copy()
        self.rhs: set[str] = rhs.copy()

    def __repr__(self) -> NotImplementedError:
        """Representation method for a Dependency object.

        Raises:
            NotImplementedError: Implement method for each kind of dependency.
        """
        raise NotImplementedError

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __hash__(self):
        return hash((frozenset(self.lhs), frozenset(self.rhs)))


class FD(Dependency):
    """Representation of a functional dependency"""

    def __init__(self, lhs: set[str], rhs: set[str]):
        super().__init__(lhs, rhs)

    def __repr__(self) -> str:
        """Representation method for the FD class.

        Returns:
            str: The string representation of a FD.
        """
        return f"{self.lhs} -> " + (", ".join(self.rhs) if self.rhs else "{}")


class MVD(Dependency):
    """Representation of a multivalued dependency.

    Definition:
        A multivalued dependency X → Y specified on relation schema R, where X
        and Y are both subsets of R, specifies the following constraint on any
        relation state r of R: If two tuples t1 and t2 exist in r such that
        t1[X] = t2[X], then two tuples t3 and t4 should also exist in r with
        the following properties*, where we use Z to denote (R - (X U Y)):**

            -   t3[X] = t4[X] = t1[X] = t2[X]
            -   t3[Y] = t1[Y] and t4[Y] = t2[Y]
            -   t3[Z] = t2[Z] and t4[Z] = t1[Z]

    Notes:
        -   *The tuples t1, t2, t3 , and t4 are not necessarily distinct.
        -   **Z is shorthand for the attributes in R after the attributes in
            (X U Y) are removed from R.

    """

    def __init__(self, lhs: set[str], rhs: set[str]):
        super().__init__(lhs, rhs)

    def __repr__(self) -> str:
        """Representation method for the MVD class.

        Returns:
            str: The string representation of a FD.
        """
        return f"{self.lhs} ->> " + (
            " | ".join(self.rhs) if self.rhs else "{}"
        )
