# -*- coding: utf-8 -*-

from .fd import FD, MVD


class Relation:
    """A representation of a database relation/table.

    Attributes:
        name (str): The name of the table/relation.
        columns (set[str]): The set of all of the column names.
        primary_key (set[str]): The set of all of the primary keys.
        candidate_keys (set[set[str]]): The set of all the candidate keys.
        non_atomic_columns (set[str]): The set of all of the columns which
            hold multi-valued or non-atomic data.
        functional_dependencies (set[FD]): The set of the functional
            dependencies of the relation.
        multivalued_dependencies (set[MV]): The set of the multivalued
            dependencies of the relation.

    TODO:
        Add representation for foreign keys.
    """

    def __init__(
        self,
        name: str,
        columns: set[str],
        primary_key: set[str],
        candidate_keys: set[set[str]] = set(),
        non_atomic_columns: set[str] = set(),
        functional_dependencies: set[FD] = set(),
        multivalued_dependencies: set[MVD] = set(),
    ):
        """The constructor for Relation.

        Args:
            name (str): The name of the table/relation.
            columns (set[str]): The set of all of the column names.
            primary_key (set[str]): The set of all of the primary
                keys.
            candidate_keys (set[set[str]], optional): The set of all the
                candidate keys. Defaults to set().
            non_atomic_columns (set[str], optional): The set of all of the
                columns which hold multi-valued or non-atomic data. Defaults
                to set().
            functional_dependencies (set[FD], optional): The set of the
                functional dependencies of the relation. Defaults to set().
            multivalued_dependencies (set[MVD], optional): The set of the
                multivalued dependencies of the relation. Defaults to set().
        """

        # Data Validation

        for attribute in primary_key:
            assert (
                attribute in columns
            ), f"Primary key {primary_key}, {attribute} not in columns"

        for candidate_key in candidate_keys:
            for attribute in candidate_key:
                assert (
                    attribute in columns
                ), f"Candidate key {candidate_key}, {attribute} not in columns"

        for column in non_atomic_columns:
            assert (
                column in columns
            ), f"Non-atomic column {column} not in columns"

        for fd in functional_dependencies:
            for attribute in fd.lhs.union(
                fd.rhs
            ):  # Set of all attributes involved in the functional dependency.
                assert (
                    attribute in columns
                ), f"Attribute {attribute} from FD, {fd} not in columns"

        for mvd in multivalued_dependencies:
            for attribute in mvd.lhs.union(
                mvd.rhs
            ):  # Set of all attributes involved in the functional dependency.
                assert (
                    attribute in columns
                ), f"Attribute {attribute} from MVD, {mvd} not in columns"

        # Add the Primary Key Functional Dependency

        # if columns:
        #     functional_dependencies.add(
        #         FD(lhs=primary_key, rhs=columns - primary_key)
        #     )  # Primary Key is a determinant of all non-prime attributes.

        # Assign Values to Class Variables

        self.name: str = name
        self.columns: set[str] = columns.copy()
        self.primary_key: set[str] = primary_key.copy()
        self.candidate_keys: set[set[str]] = candidate_keys.copy()
        self.non_atomic_columns: set[str] = non_atomic_columns.copy()
        self.functional_dependencies: set[FD] = {
            fd for fd in functional_dependencies.copy() if fd.lhs or fd.rhs
        }
        self.multivalued_dependencies: set[MVD] = {
            mvd
            for mvd in multivalued_dependencies.copy()
            if mvd.lhs or mvd.rhs
        }

    def _repr_attribute_list(
        self, attribute: set, attribute_title: str
    ) -> str:
        """Private method for representing an attribute which is a set as a
        string.

        Args:
            attribute (set): A set of items that can be represented as strings.
            attribute_title (str): The title for representing the attribute.

        Returns:
            str: The final string representation of the attribute.
        """
        attributes_info: list[str] = []
        for item in attribute:
            attributes_info.append(f"\t\t{item},")
        attributes_info = "\n".join(attributes_info)
        return (
            f"{attribute_title}: "
            + "{"
            + (
                "\n" + f"{attributes_info}" + "\n\t}"
                if len(attributes_info) > 0
                else "\t}"
            )
        )

    def __repr__(self) -> str:
        """Representation method for the Relation class.

        Returns:
            str: The string representation of a Relation.
        """
        return "\n".join(
            (
                f"Name:\t{self.name}",
                self._repr_attribute_list(self.columns, "Columns"),
                f"Primary Key:\t{self.primary_key}",
                self._repr_attribute_list(
                    self.candidate_keys, "Candidate Keys"
                ),
                self._repr_attribute_list(
                    self.non_atomic_columns,
                    "Columns with Non-Atomic Attributes",
                ),
                self._repr_attribute_list(
                    self.functional_dependencies, "Functional Dependencies"
                ),
                self._repr_attribute_list(
                    self.multivalued_dependencies, "Multivalued Dependencies"
                ),
            )
        )

    def remove_attribute(self, attribute: str) -> None:
        """Remove a given attribute from the relation.

        Args:
            attribute (str): The attribute which will be removed from the
                relation.

        Raises:
            KeyError: If the input attribute is not in the relation.
            ValueError: If the input attribute is part of the primary or a
                candidate key and removing it would remove the key.
        """
        if attribute not in self.columns:
            raise KeyError(f"Attribute '{attribute}' not found in columns.")

        if attribute in self.primary_key:
            if len(self.primary_key) == 1:
                raise ValueError(
                    f"Cannot remove attribute '{attribute}', "
                    + f"part of the primary key {self.primary_key}"
                )
            self.primary_key.remove(attribute)

        updated_candidate_keys = set()
        for candidate_key in self.candidate_keys:
            if attribute in candidate_key:
                if len(candidate_key) == 1:
                    raise ValueError(
                        f"Cannot remove attribute '{attribute}', "
                        + f"part of a candidate key {candidate_key}."
                    )
                updated_candidate_keys.add(candidate_key - {attribute})
            else:
                updated_candidate_keys.add(candidate_key)
        self.candidate_keys = updated_candidate_keys

        if attribute in self.non_atomic_columns:
            self.non_atomic_columns.remove(attribute)

        updated_functional_dependencies = set()
        for fd in self.functional_dependencies:
            if attribute in fd.lhs:
                continue  # FD would become invalid, do not include in new FDs.
            if (
                attribute in fd.rhs
            ):  # Set of all attributes involved in the functional dependency.
                lhs: set[str] = fd.lhs.copy()
                rhs: set[str] = fd.rhs - {attribute}

                if lhs and rhs and lhs != rhs:
                    updated_functional_dependencies.add(FD(lhs=lhs, rhs=rhs))
            else:
                updated_functional_dependencies.add(fd)
        self.functional_dependencies = updated_functional_dependencies

        updated_multivalued_dependencies = set()
        for mvd in self.multivalued_dependencies:
            if (
                attribute in mvd.lhs | mvd.rhs
            ):  # Set of all attributes involved in the multivalued dependency.
                lhs: set[str] = mvd.lhs - {attribute}
                rhs: set[str] = mvd.rhs - {attribute}

                if lhs and rhs and lhs != rhs:
                    updated_multivalued_dependencies.add(MVD(lhs=lhs, rhs=rhs))
            else:
                updated_multivalued_dependencies.add(mvd)
        self.multivalued_dependencies = updated_multivalued_dependencies.copy()

        self.columns.remove(attribute)

        return

    def minimal_fd_set(self) -> set[FD]:
        """Minimal Sets of Functional Dependencies for the Relation.

        We can formally define a set of functional dependencies F to be
        minimal if it satisfies the following conditions:

        1.  Every dependency in F has a single attribute for its
            right-hand side.

        2.  We cannot replace any dependency X → A in F with a dependency
            Y → A, where Y is a proper subset of X, and still have a set
            of dependencies that is equivalent to F.

        3.  We cannot remove any dependency from F and still have a set of
            dependencies that is equivalent to F."""

        # Satisfy Step 1
        minimal_functional_dependencies: set[FD] = set()
        for fd in self.functional_dependencies:
            for attribute in fd.rhs:
                minimal_functional_dependencies.add(
                    FD(lhs=fd.lhs, rhs={attribute})
                )

        # Satisfy Step 2
        corrected_minimal_functional_dependencies: set[FD] = set()
        for fd in minimal_functional_dependencies:
            for lhs_attribute in fd.lhs:
                lhs_subset_fd = FD(lhs=fd.lhs - {lhs_attribute}, rhs=fd.rhs)
                if lhs_subset_fd in minimal_functional_dependencies:
                    corrected_minimal_functional_dependencies.add(
                        lhs_subset_fd
                    )
                else:
                    corrected_minimal_functional_dependencies.add(fd)

        return corrected_minimal_functional_dependencies

    def prime_attributes(self) -> set[str]:
        """Prime Attributes for the Relation.

        Definition:
            An attribute of relation schema R is called a prime attribute of R
            if it is a member of some candidate key of R. An attribute is
            called nonprime if it is not a prime attribute — that is, if it is
            not a member of any candidate key.
        """
        prime_attributes: set[str] = set()

        # Include attributes from the primary key.
        prime_attributes = prime_attributes | self.primary_key

        # Include attributes from every candidate key.
        for candidate_key in self.candidate_keys:
            prime_attributes = prime_attributes | candidate_key

        return prime_attributes
