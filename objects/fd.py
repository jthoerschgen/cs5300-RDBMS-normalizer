class FD:
    """Representation of a functional dependency"""

    def __init__(self, lhs: set[str], rhs: set[str]):
        """The constructor for a functional dependency.

        Args:
            lhs (set[str]): The attributes that comprise the left-hand side
                of the dependency.
            rhs (set[str]): The attributes that comprise the right-hand side
                of the dependency.
        """
        self.lhs: set[str] = lhs.copy()
        self.rhs: set[str] = rhs.copy()

    def __repr__(self) -> str:
        """Representation method for the FD class.

        Returns:
            str: The string representation of a FD.
        """
        return f"{self.lhs} -> " + (", ".join(self.rhs) if self.rhs else "{}")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FD):
            return False
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __hash__(self) -> int:
        return hash((frozenset(self.lhs), frozenset(self.rhs)))


class MVD:
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

    def __init__(self, lhs: set[str], rhs: tuple[set[str], set[str]]):
        """The constructor for a Multivalued dependency.

        Args:
            lhs (set[str]): The attributes that comprise the left-hand side
                of the dependency.
            rhs (set[str]): The attributes that comprise the right-hand side
                of the dependency.
        """
        assert (
            len(rhs) == 2
        ), f"RHS of MVD must be == 2 items, got {len(rhs)}, {rhs}"

        self.lhs: set[str] = lhs.copy()
        self.rhs: tuple[set[str], set[str]] = (rhs[0].copy(), rhs[1].copy())

    def __repr__(self) -> str:
        """Representation method for the MVD class.

        Returns:
            str: The string representation of a FD.
        """
        return (
            f"{self.lhs} ->> "
            + (",".join(self.rhs[0]) if self.rhs[0] else "{}")
            + " | "
            + (",".join(self.rhs[1]) if self.rhs[1] else "{}")
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MVD):
            return False
        return (
            self.lhs == other.lhs
            and self.rhs[0] == other.rhs[0]
            and self.rhs[1] == other.rhs[1]
        )

    def __hash__(self) -> int:
        return hash(
            (
                frozenset(self.lhs),
                (frozenset(self.rhs[0]), frozenset(self.rhs[1])),
            )
        )


class NonAtomic:
    """Representation of a non-atomic attribute"""

    def __init__(self, lhs: set[str], rhs: set[str]):
        """The constructor for a non-atomic value dependency.

        Args:
            lhs (set[str]): The attributes that comprise the left-hand side
                of the dependency.
            rhs (set[str]): The attributes that comprise the right-hand side
                of the dependency.
        """
        self.lhs: set[str] = lhs.copy()
        self.rhs: set[str] = rhs.copy()

    def __repr__(self) -> str:
        """Representation method for the NonAtomic class.

        Returns:
            str: The string representation of a non-atomic.
        """
        return (
            f"{self.lhs} -> "
            + (", ".join(self.rhs) if self.rhs else "{}")
            + " (a non-atomic attribute)"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NonAtomic):
            return False
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __hash__(self) -> int:
        return hash((frozenset(self.lhs), frozenset(self.rhs)))
