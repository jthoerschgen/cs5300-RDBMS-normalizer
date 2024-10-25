# -*- coding: utf-8 -*-

"""rdbms_normalizer.py

CS 5300 - Programming Project - RDBMS Normalizer.

Core Components:

1. Input Parser
2. Normalizer
3. Final Relation Generator

"""
from itertools import combinations

import pandas as pd

from objects.fd import FD
from objects.relation import Relation


def normalize_to_1NF(relation: Relation) -> list[Relation]:
    """Normalize a Relation into First Normal Form (1NF).

    First Normal Form:

    Test:
        -   Relation should have no multivalued attributes.

    Remedy:
        -   Form new relations for each multi-valued attribute.

    Approach:
        -   Create a separate relation for each multivalued attribute
            along with the primary key of the base relation.

    Args:
        relation (Relation): Relation that is being normalized into the First
            Normal Form.

    Returns:
        list[Relation]: The decomposition of the original relation into a
            list of relations in 1NF.
    """

    decomposition: list[Relation] = []
    non_atomic_columns: set[str] = relation.non_atomic_columns.copy()
    for attribute in non_atomic_columns:
        columns: set[str] = relation.primary_key.copy()
        columns.add(attribute)

        decomposed_relation = Relation(
            name="",  # TODO: name
            columns=columns,
            primary_key=columns,
            # TODO: candidate keys
            functional_dependencies={
                fd
                for fd in relation.functional_dependencies
                if fd.lhs <= columns and fd.rhs <= columns
            },
        )
        decomposition.append(decomposed_relation)

        relation.remove_attribute(attribute)
    decomposition.append(relation)

    return decomposition


def normalize_to_2NF(relation: Relation) -> list[Relation]:
    """Normalize a Relation into Second Normal Form (2NF).

    Second Normal Form:

    Test:
        -   For relations where the primary key contains multiple
            attributes, no non-key attributes should be functionally
            dependent on a part of the primary key.

    Remedy:
        -   Decompose and set up a new relation for each partial key with
            its dependent attributes(s). Make sure to keep a relation with
            the original primary key and any attributes that are fully
            functionally dependent on it.

    Approach:
        -   Create a separate relation for each partial functional
            dependency violation against the keys of the base relation.

    Args:
        relation (Relation): Relation that is being normalized into the Second
            Normal Form.

    Returns:
        list[Relation]: The decomposition of the original relation into a
            list of relations in 2NF.
    """

    """Definition of a Partial Functional Dependency:

        Partial Functional Dependency (PFD):
            -   A functional dependency X → Y is a partial dependency if some
                attribute A ε X can be removed from X and the dependency still
                holds; that is, for some A ε X, (X - {A}) → Y.
    """

    minimal_fds = relation.minimal_fd_set()

    pfds: set[FD] = set()
    for fd in relation.functional_dependencies:
        if (
            relation.primary_key <= fd.lhs
        ):  # Skip if the primary key is entirely present in the LHS of the FD.
            continue
        if fd.lhs.isdisjoint(
            relation.primary_key
        ):  # Skip if LHS of the FD contains no attribute in the primary key.
            continue

        for rhs_attribute in fd.rhs:  # Minimize each FD
            for lhs_attribute in fd.lhs | {""}:  # For each A in X
                reduced_fd = FD(
                    lhs=fd.lhs - {lhs_attribute}, rhs={rhs_attribute}
                )
                if reduced_fd in minimal_fds:  # Test if (X - {A}) → Y holds.
                    pfds.add(fd)
                    break

    decomposition: list[Relation] = []
    for pfd in pfds:
        print(f"PFD: {pfd}")
        decomposition_pk: set[str] = (pfd.lhs | pfd.rhs).intersection(
            relation.primary_key
        )
        decomposition_columns: set[str] = pfd.lhs | pfd.rhs
        decomposition_fds: set[str] = {
            fd
            for fd in relation.functional_dependencies
            if fd.lhs <= decomposition_columns
            and fd.rhs <= decomposition_columns
        }

        decomposed_relation = Relation(
            name="",  # TODO: name
            columns=decomposition_columns,
            primary_key=decomposition_pk,
            # TODO: candidate keys
            functional_dependencies=({pfd} | decomposition_fds),
        )
        decomposition.append(decomposed_relation)

        for attribute in pfd.rhs:
            if attribute not in relation.columns:
                continue  # already removed
            relation.remove_attribute(attribute)
    decomposition.append(relation)

    return decomposition


def normalize_to_3NF(relation: Relation) -> list[Relation]:
    """Normalize a Relation into Third Normal Form (3NF).

    Third Normal Form:

    Test:
        -   Relation should not have a non-key attribute functionally
            determined by another non-key attribute (or by a set of
            non-key attributes). That is, there should be no transitive
            dependency of a non-key attribute on the primary key.

    Remedy:
        -   Decompose and set up a relation that includes the non-key
            attribute(s) that functionally determine(s) other non-key
            attribute(s).

    Approach:
        -   Create a separate relation for each transitive functional
            dependency violation against the keys of the base relation.

    Args:
        relation (Relation): Relation that is being normalized into the
            Third Normal Form.

    Returns:
        list[Relation]: The decomposition of the original relation into a
            list of relations in 3NF.
    """

    """Definition of a Transitive Functional Dependency:

        Transitive Functional Dependency (TFD):
            -   A functional dependency X → Y in a relation schema R is a
                transitive dependency if there exists a set of attributes Z in
                R that is neither a candidate key nor a subset of any key of R
                and both X → Z and Z → Y hold.
    """

    tfd_violations: set[FD] = set()
    for fd in relation.functional_dependencies:
        if (
            relation.primary_key <= fd.lhs
        ):  # The primary key is a subset of the Left-Hand Side of the FD.
            continue  # not a violation of 3NF
        for candidate_key in relation.candidate_keys:
            if (
                candidate_key <= fd.lhs
            ):  # Any candidate key is a subset of the Left-Hand Side of the
                # FD.
                continue  # not a violation of 3NF
        if (
            not fd.rhs - relation.prime_attributes()
        ):  # No attributes in the Right-Hand Side of the FD are nonprime.
            continue  # not a violation of 3NF
        tfd_violations.add(fd)

    decomposition: list[Relation] = []
    for tfd in tfd_violations:
        print(f"TFD: {tfd}")
        decomposition_pk: set[str] = tfd.lhs.copy()
        decomposition_columns: set[str] = tfd.lhs | tfd.rhs
        decomposition_fds: set[str] = {
            fd
            for fd in relation.functional_dependencies
            if fd.lhs <= decomposition_columns
            and fd.rhs <= decomposition_columns
        }

        decomposed_relation = Relation(
            name="",  # TODO: name
            columns=decomposition_columns,
            primary_key=decomposition_pk,
            # TODO: candidate keys
            functional_dependencies=({tfd} | decomposition_fds),
        )
        decomposition.append(decomposed_relation)

        for attribute in tfd.rhs:
            if attribute not in relation.columns:
                continue  # already removed
            relation.remove_attribute(attribute)
    decomposition.append(relation)

    return decomposition


def normalize_to_BCNF(relation: Relation) -> list[Relation]:
    """Normalize a Relation into Boyce-Codd Normal Form (3NF).

    Boyce-Codd Normal Form:

    Definition:
        -   A relation schema R is in BCNF if whenever a nontrivial
            functional dependency X → A holds in R, then X is a superkey
            of R.

    General rule:
        1.  Let R be the relation not in BCNF, let X ⊆ R, and let X → A be
            the FD that causes a violation of BCNF. R may be decomposed
            into two relations: R-A and XA.
        2.  If either R-A or XA is not in BCNF, repeat the process.

    Approach:
        -   Approach: Create a separate relation for each BCNF functional
            dependency violation against the keys of the base relation.

    Args:
        relation (Relation): Relation that is being normalized into the
        Boyce-Codd Normal Form.

    Returns:
        list[Relation]: The decomposition of the original relation into a
            list of relations in BCNF.
    """

    # # Determine FDs that are in violation of BCNF
    bncf_violations: set[FD] = set()
    for fd in relation.functional_dependencies:
        if (
            relation.primary_key <= fd.lhs
        ):  # The primary key is a subset of the Left-Hand Side of the FD.
            continue  # not a violation of 3NF
        for candidate_key in relation.candidate_keys:
            if (
                candidate_key <= fd.lhs
            ):  # Any candidate key is a subset of the Left-Hand Side of the
                # FD.
                continue  # not a violation of 3NF
        bncf_violations.add(fd)

    # Decompose the given relation so that BCNF is satisfied.
    decomposition: list[Relation] = []
    for bcnf_violation in bncf_violations:
        print(f"BCNF Violation: {bcnf_violation}")

        decomposition_pk: set[str] = bcnf_violation.lhs.copy()
        decomposition_columns: set[str] = (
            bcnf_violation.lhs | bcnf_violation.rhs
        )
        decomposition_fds: set[str] = {
            fd
            for fd in relation.functional_dependencies
            if fd.lhs <= decomposition_columns
            and fd.rhs <= decomposition_columns
        }

        # New relation XA
        decomposed_relation = Relation(
            name="",  # TODO: name
            columns=decomposition_columns,
            primary_key=decomposition_pk,
            # TODO: candidate keys
            functional_dependencies=({bcnf_violation} | decomposition_fds),
        )
        decomposition.append(decomposed_relation)

        # R becomes R-A
        for attribute in bcnf_violation.rhs:
            if attribute not in relation.columns:
                continue  # already removed
            relation.remove_attribute(attribute)

    # Adjust the remaining original relation's primary key
    for attribute in (
        relation.columns - relation.primary_key
    ):  # Current non-prime attributes
        if (
            FD(lhs=relation.primary_key, rhs={attribute})
            not in relation.minimal_fd_set()
        ):  # If the primary key cannot uniquely identify the attribute, add
            # it to the primary key.
            relation.primary_key.add(attribute)

    decomposition.append(relation)

    return decomposition


def normalize_to_4NF(relation: Relation) -> list[Relation]:
    """Normalize a Relation into Fourth Normal Form (4NF).

    Fourth Normal Form:

    Definition:
        -   A relation schema R is in 4NF with respect to a set of
            dependencies F (that includes functional dependencies and
            multivalued dependencies) if, for every nontrivial multivalued
            dependency X →→ Y in F+ *, X is a superkey for R.

    Note:
        -   *F+ refers to the cover of functional dependencies F, or all
            dependencies that are implied by F.

    General rule:
        -   The process of normalizing a relation involving the nontrivial
            MVDs that is not in 4NF consists of decomposing it so that each
            MVD is represented by a separate relation where it becomes a
            trivial MVD.

    Approach:
        -   Create a separate relation for each MVD violation.

    Instructor Note:
        -   You may assume that MVDs are provided by the user, detailing the
            expected independent relationships between attribute groups.
        -   Data instances are REQUIRED ONLY on the relations where MVDs are
            provided by the user.
        -   Your program must validate these provided MVDs against the actual
            data instances. If and only if upon successful validation of the
            MVDs, your program should then perform the necessary decomposition
            of the relation schema to achieve 4NF.

    Args:
        relation (Relation): Relation that is being normalized into the Fourth
            Normal Form.

    Returns:
        list[Relation]: The decomposition of the original relation into a
            list of relations in 4NF.
    """

    # TODO - Determine MVDs for Extra Credit

    decomposition: list[Relation] = []
    for mvd in relation.multivalued_dependencies:
        print(f"MVD: {mvd}")

        if not relation.verify_mvd(mvd):
            print("\tMVD is invalid, skipping...")
            continue
        print("\tMVD is valid, decomposing...")

        # Decompose the Relation
        for rhs_attribute in mvd.rhs:
            decomposition_pk: set[str] = mvd.lhs | {rhs_attribute}
            decomposition_columns: set[str] = mvd.lhs | {rhs_attribute}

            # Decompose the Data Instance
            decomposition_data_instances = (
                relation.data_instances[
                    list(decomposition_columns)
                ].drop_duplicates()
                if relation.data_instances is not None
                else None
            )

            decomposed_relation = Relation(
                name="",  # TODO: name
                columns=decomposition_columns,
                primary_key=decomposition_pk,
                # TODO: candidate keys
                # TODO: functional_dependencies
                # TODO: multivalued dependencies
                data_instances=(decomposition_data_instances),
            )
            decomposition.append(decomposed_relation)

        #     relation.remove_attribute(rhs_attribute),
        # decomposition.append(relation)

    return decomposition


def normalize_to_5NF(relation: Relation) -> list[Relation]:
    """Normalize a Relation into Fifth Normal Form (5NF).

    Fifth Normal Form:

    Definition:
        -   A relation schema R is in fifth normal form (5NF) (or project-join
            normal form (PJNF)) with respect to a set F of functional,
            multivalued, and join dependencies if, for every nontrivial join
            dependency JD(R1, R2, … , Rn) in F+ (that is, implied by F),*
            every R_i is a superkey of R.

    Note:
        -   *F+ refers to the cover of functional dependencies F, or all
            dependencies that are implied by F.)

    Approach:
        -   Decompose each base relation into its sub-relation projection if a
            non-trivial join dependency is identified.
        -   Decompose the base relation if a valid join dependency is detected.

    Instructor Note:
        -   This advanced form of normalization aims to eliminate redundancy
            caused by join dependencies that are not implied by candidate keys.
            You will likely need detailed data instances as part of the user
            input in order to effectively determine any existing join
            dependencies within the relation table.

    Args:
        relation (Relation): Relation that is being normalized into the Fifth
            Normal Form.

    Returns:
        list[Relation]: The decomposition of the original relation into a
            list of relations in 5NF.
    """

    """Definition of a Join Dependency:

        Join Dependency (JD):
            -   A join dependency (JD), denoted by JD(R1 , R2 , ... , R n),
                specified on relation schema R, specifies a constraint on the
                states r of R. The constraint states that every legal state r
                of R should have a nonadditive join decomposition into R1, R2,
                … , Rn. Hence, for every such r we have:

                    * (π_R1(r), π_R2(r), ... , π_Rn(r)) = r
    """

    # Get a list of the combination of every prime attribute
    prime_attribute_combinations = list()
    prime_key_list = list(relation.primary_key)
    for i in range(2, len(prime_key_list) + 1):
        for combination in combinations(prime_key_list, i):
            prime_attribute_combinations.append(set(combination))

    # Get all unique decompositions
    decompositions = []
    for prime_attribute_combination in prime_attribute_combinations:
        r1_projection = relation.data_instances[
            list(prime_attribute_combination)
        ].drop_duplicates()
        r1_projection = r1_projection.reindex(
            sorted(r1_projection.columns), axis=1
        )

        for prime_attribute in prime_attribute_combination:
            remainder = (
                relation.primary_key - prime_attribute_combination
            ) | {prime_attribute}
            if len(prime_attribute_combination) == 1 or len(remainder) == 1:
                continue
            if (
                prime_attribute_combinations == relation.primary_key
                or remainder == relation.primary_key
            ):
                continue  # Trivial

            r2_projection = relation.data_instances[
                list(remainder)
            ].drop_duplicates()
            r2_projection = r2_projection.reindex(
                sorted(r2_projection.columns), axis=1
            )

            # Check if the projection with the same columns is already in the
            # decompositions
            if not any(
                set(r1_projection.columns) == set(decomposition.columns)
                for decomposition in decompositions
            ):
                decompositions.append(r1_projection)

            if not any(
                set(r2_projection.columns) == set(decomposition.columns)
                for decomposition in decompositions
            ):
                decompositions.append(r2_projection)

    # Check for Join Dependencies
    original_df = relation.data_instances.reindex(
        sorted(relation.data_instances.columns), axis=1
    )
    original_df = original_df.sort_values(
        by=list(original_df.columns)
    ).reset_index(drop=True)
    decomposition_columns: set[tuple[tuple[str, ...]]] = set()

    print("Verifying Join Dependencies....")
    for i in range(2, len(decompositions) + 1):
        for combination in combinations(decompositions, i):

            join_df = combination[0]
            for table in combination[1:]:
                common_columns = list(
                    set(table.columns) & set(join_df.columns)
                )
                if common_columns:
                    join_df = pd.merge(
                        join_df, table, on=common_columns, how="inner"
                    )

            join_df = join_df.reindex(sorted(join_df.columns), axis=1)

            join_df = join_df.sort_values(
                by=list(join_df.columns)
            ).reset_index(drop=True)

            valid_join = original_df.equals(join_df)

            if valid_join:
                h = set()
                for table in combination:
                    h.add(tuple(table.columns))
                decomposition_columns.add(tuple(h))

    if len(decomposition_columns) == 0:
        return [relation]

    least_number_columns: int = min(
        sum(len(columns) for columns in decomposition)
        for decomposition in decomposition_columns
    )  # Decompositions with the least amount of columns
    decomposition_columns = {
        decomposition
        for decomposition in decomposition_columns
        if sum(len(columns) for columns in decomposition)
        == least_number_columns
    }
    print(decomposition_columns)

    decomposition: list[Relation] = []
    for decomposition_columns in decomposition_columns.pop():
        # Construct the Decomposition

        decomposition_pk: set[str] = set(decomposition_columns)
        decomposition_columns: set[str] = set(decomposition_columns)

        # Decompose the Data Instance
        decomposition_data_instances = (
            relation.data_instances[
                list(decomposition_columns)
            ].drop_duplicates()
            if relation.data_instances is not None
            else None
        )

        decomposed_relation = Relation(
            name="",  # TODO: name
            columns=decomposition_columns,
            primary_key=decomposition_pk,
            # TODO: candidate keys
            # TODO: functional_dependencies
            # TODO: multivalued dependencies
            data_instances=decomposition_data_instances,
        )
        decomposition.append(decomposed_relation)

    return decomposition
