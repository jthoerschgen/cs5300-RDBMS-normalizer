from itertools import combinations

import pandas as pd

from .fd import FD, MVD, NonAtomic


class Relation:
    """A representation of a database relation/table.

    Attributes:
        name (str): The name of the table/relation.
        columns (set[str]): The set of all of the column names.
        primary_key (set[str]): The set of all of the primary keys.
        candidate_keys (set[set[str]]): The set of all the candidate keys.
        non_atomic_columns (set[NonAtomic]): The set of all of the columns
            which hold multi-valued or non-atomic data.
        functional_dependencies (set[FD]): The set of the functional
            dependencies of the relation.
        multivalued_dependencies (set[MV]): The set of the multivalued
            dependencies of the relation.
        data_instances (pd.DataFrame) | None: The data instances for the
            relation, used for 4NF and 5NF normalization. (Optional)

    TODO:
        Add representation for foreign keys.
    """

    def __init__(
        self,
        name: str,
        columns: set[str],
        primary_key: set[str],
        candidate_keys: set[set[str]] = set(),
        non_atomic_columns: set[NonAtomic] = set(),
        functional_dependencies: set[FD] = set(),
        multivalued_dependencies: set[MVD] = set(),
        data_instances: list[dict[str, str]] | pd.DataFrame | None = None,
    ):
        """The constructor for Relation.

        Args:
            name (str): The name of the table/relation.
            columns (set[str]): The set of all of the column names.
            primary_key (set[str]): The set of all of the primary
                keys.
            candidate_keys (set[set[str]], optional): The set of all the
                candidate keys. Defaults to set().
            non_atomic_columns (set[NonAtomic], optional): The set of all of
                the columns which hold multi-valued or non-atomic data.
                Defaults to set().
            functional_dependencies (set[FD], optional): The set of the
                functional dependencies of the relation. Defaults to set().
            multivalued_dependencies (set[MVD], optional): The set of the
                multivalued dependencies of the relation. Defaults to set().
            data_instances (list[dict[str, str]] | pd.DataFrame | None,
                optional): Optional parameter for specifying a list of data
                instances, where each instance is a dictionary where the key
                is the column name and the value is the column value for that
                row. Defaults to None.
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

        for non_atomic_dependency in non_atomic_columns:
            for column in (
                non_atomic_dependency.lhs | non_atomic_dependency.rhs
            ):
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
            for attribute in (
                mvd.lhs | mvd.rhs[0] | mvd.rhs[1]
            ):  # Set of all attributes involved in the functional dependency.
                assert (
                    attribute in columns
                ), f"Attribute {attribute} from MVD, {mvd} not in columns"

        if data_instances is not None:
            if isinstance(data_instances, dict):
                for row in data_instances:
                    assert set(row.keys()) == columns
            elif isinstance(data_instances, pd.DataFrame):
                assert set(data_instances.columns) == columns

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
        self.non_atomic_columns: set[NonAtomic] = {
            non_atomic
            for non_atomic in non_atomic_columns.copy()
            if non_atomic.lhs or non_atomic.rhs
        }
        self.functional_dependencies: set[FD] = {
            fd for fd in functional_dependencies.copy() if fd.lhs or fd.rhs
        }
        self.multivalued_dependencies: set[MVD] = {
            mvd
            for mvd in multivalued_dependencies.copy()
            if mvd.lhs or mvd.rhs
        }
        self.data_instances: pd.DataFrame = (
            pd.DataFrame(data_instances)
            if data_instances is not None
            else None
        )

    def _repr_attribute_list(
        self,
        attribute: (
            set[str] | set[set[str]] | set[NonAtomic] | set[FD] | set[MVD]
        ),
        attribute_title: str,
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
        attributes_info_str: str = "\n".join(attributes_info)
        return (
            f"{attribute_title}: "
            + "{"
            + (
                "\n" + f"{attributes_info_str}" + "\n\t}"
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
                "Data Instances:\n",
                (
                    self.data_instances.to_string()
                    if self.data_instances is not None
                    else ""
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

        # if attribute in self.non_atomic_columns:
        #     self.non_atomic_columns.remove(attribute)
        updated_non_atomic_columns = set()
        for non_atomic in self.non_atomic_columns:
            if attribute in non_atomic.lhs:
                continue
                # Non-atomic dependency would become invalid, do not include
                # in new non-atomic dependencies.
            if (
                attribute in non_atomic.rhs
            ):  # Set of all attributes involved in the non-atomic dependency.
                lhs: set[str] = non_atomic.lhs.copy()
                rhs: set[str] = non_atomic.rhs - {attribute}

                if lhs and rhs and lhs != rhs:
                    updated_non_atomic_columns.add(NonAtomic(lhs=lhs, rhs=rhs))
            else:
                updated_non_atomic_columns.add(non_atomic)
        self.non_atomic_columns = updated_non_atomic_columns

        updated_functional_dependencies = set()
        for fd in self.functional_dependencies:
            if attribute in fd.lhs:
                continue  # FD would become invalid, do not include in new FDs.
            if (
                attribute in fd.rhs
            ):  # Set of all attributes involved in the functional dependency.
                lhs = fd.lhs.copy()
                rhs = fd.rhs - {attribute}

                if lhs and rhs and lhs != rhs:
                    updated_functional_dependencies.add(FD(lhs=lhs, rhs=rhs))
            else:
                updated_functional_dependencies.add(fd)
        self.functional_dependencies = updated_functional_dependencies

        updated_multivalued_dependencies = set()
        for mvd in self.multivalued_dependencies:
            if (
                attribute in mvd.lhs | mvd.rhs[0] | mvd.rhs[1]
            ):  # Set of all attributes involved in the multivalued dependency.
                continue  # MVD becomes invalid
            else:
                updated_multivalued_dependencies.add(mvd)
        self.multivalued_dependencies = updated_multivalued_dependencies.copy()

        if self.data_instances is not None:
            self.data_instances = self.data_instances.drop(attribute, axis=1)

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
            dependencies that is equivalent to F.
        """

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

    def verify_mvd(self, mvd: MVD) -> bool:
        """Definition of a Multivalued Dependency:

        Multivalued Dependency (MVD):

            -   A multivalued dependency X → Y specified on relation schema R,
                where X and Y are both subsets of R, specifies the following
                constraint on any relation state r of R: If two tuples t1 and
                t2 exist in r such that t1[X] = t2[X], then two tuples t3 and
                t4 should also exist in r with the following properties*,
                where we use Z to denote (R - (X U Y)):**

                -   t3[X] = t4[X] = t1[X] = t2[X]
                -   t3[Y] = t1[Y] and t4[Y] = t2[Y]
                -   t3[Z] = t2[Z] and t4[Z] = t1[Z]

        Notes:
            -   *The tuples t1, t2, t3 , and t4 are not necessarily distinct.
            -   **Z is shorthand for the attributes in R after the attributes
                in (X U Y) are removed from R.
        """
        assert (
            mvd.lhs | mvd.rhs[0] | mvd.rhs[1]
        ) <= self.columns, f"Attributes in MVD not in columns: {self.columns}"

        X, Y, Z = mvd.lhs, mvd.rhs[0], mvd.rhs[1]

        if (
            self.primary_key <= X
            or self.primary_key <= Y
            or self.primary_key <= Z
        ):  # The primary key is a subset of any X, Y, or Z
            return False

        X_cols, Y_cols, Z_cols = list(X), list(Y), list(Z)

        for _, group in self.data_instances.groupby(list(X_cols)):
            if len(group) <= 1:
                continue

            for i1, t1 in group.iterrows():  # Index 1, Tuple 1
                for i2, t2 in group.iterrows():  # Index 2, Tuple 2
                    if i1 == i2:
                        continue

                    y1 = tuple(t1[Y_cols])
                    z1 = tuple(t1[Z_cols])

                    y2 = tuple(t2[Y_cols])
                    z2 = tuple(t2[Z_cols])

                    if (
                        y1 == y2 and z1 == z2
                    ):  # t1 and t2 have the same values, skip
                        continue

                    # t3: should have X=t1[X], Y=t1[Y], Z=t2[Z]
                    has_t3 = (
                        (group[Y_cols].apply(tuple, axis=1) == y1)
                        & (group[Z_cols].apply(tuple, axis=1) == z2)
                    ).any()

                    # t4: should have X=t1[X], Y=t2[Y], Z=t1[Z]
                    has_t4 = (
                        (group[Y_cols].apply(tuple, axis=1) == y2)
                        & (group[Z_cols].apply(tuple, axis=1) == z1)
                    ).any()

                    if not (has_t3 or has_t4):
                        return False
        return True

    def determine_mvds(self) -> set[MVD]:
        """EXTRA CREDIT

        Calculates a list of possible multivalued dependencies from the set of
        columns. Then verifies each possible multivalued dependency and returns
        the set of all valid multivalued dependencies.
        """
        # Get every combination of attributes
        column_combinations = list()
        columns_list = list(self.columns)
        for i in range(1, len(columns_list) + 1):
            for combination in combinations(columns_list, i):
                column_combinations.append(set(combination))

        possible_mvds: list[MVD] = list()
        for X in column_combinations:
            remaining_columns: set[str] = self.columns - X
            for i in range(1, len(remaining_columns)):
                for Y_list in combinations(remaining_columns, i):
                    Y = {Y_list[0]}
                    Z = remaining_columns - Y

                    potential_mvd = MVD(
                        lhs=X, rhs=(Y, Z) if sorted(Y) < sorted(Z) else (Z, Y)
                    )  # Sort RHS to avoid duplicate MVDs

                    if potential_mvd not in possible_mvds:
                        # self.multivalued_dependencies.add(potential_mvd)
                        possible_mvds.append(potential_mvd)

        verified_mvds: set[MVD] = set()
        for mvd in possible_mvds:
            verified = self.verify_mvd(mvd)
            if verified:
                verified_mvds.add(mvd)

        return verified_mvds
