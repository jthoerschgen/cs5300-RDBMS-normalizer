# -*- coding: utf-8 -*-

"""rdbms_normalizer.py

CS 5300 - Programming Project - RDBMS Normalizer

Core Components:

1. Input Parser
2. Normalizer
3. Final Relation Generator

"""

from objects.fd import FD
from objects.relation import Relation


def normalize_to_1NF(relation: Relation) -> list[Relation]:
    """Normalize a Relation into First Normal Form (1NF)

    First Normal Form:

    Test
        -   Relation should have no multivalued attributes.

    Remedy
        -   Form new relations for each multi-valued attribute.

    Approach
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
        new_primary_key: set[str] = relation.primary_key.copy()
        new_primary_key.add(attribute)

        relation.remove_attribute(attribute)

        decomposed_relation = Relation(
            name=f"{relation.name.rstrip('Data')}{attribute}Data",
            columns=new_primary_key,
            primary_key=new_primary_key,
            functional_dependencies=set(),
        )
        decomposition.append(decomposed_relation)
    decomposition.append(relation)

    return decomposition


def normalize_to_2NF(relation: Relation) -> list[Relation]:
    """Normalize a Relation into Second Normal Form (2NF)

    Second Normal Form:

    Test
        -   For relations where the primary key contains multiple
            attributes, no non-key attributes should be functionally
            dependent on a part of the primary key.

    Remedy
        -   Decompose and set up a new relation for each partial key with
            its dependent attributes(s). Make sure to keep a relation with
            the original primary key and any attributes that are fully
            functionally dependent on it.

    Approach
        -   Create a separate relation for each partial functional
            dependency violation against the keys of the base relation.

    Args:
        relation (Relation): Relation that is being normalized into the Second
            Normal Form.

    Returns:
        list[Relation]: The decomposition of the original relation into a
            list of relations in 2NF.
    """

    """Definition of a Partial Functional Dependency

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
        new_primary_key: set[str] = (pfd.lhs | pfd.rhs).intersection(
            relation.primary_key
        )

        for attribute in pfd.rhs:
            if attribute not in relation.columns:
                continue  # already removed
            relation.remove_attribute(attribute)

        decomposed_relation = Relation(
            name=(
                relation.name.rstrip("Data")
                + "".join([column.rstrip("ID") for column in new_primary_key])
                + "Data"
            ),
            columns=pfd.lhs | pfd.rhs,
            primary_key=new_primary_key,
            functional_dependencies={pfd},
        )
        decomposition.append(decomposed_relation)
    decomposition.append(relation)

    return decomposition


def normalize_to_3NF(relation: Relation) -> list[Relation]:
    """Normalize a Relation into Third Normal Form (3NF)

    Third Normal Form:

    Test
        -   Relation should not have a non-key attribute functionally
            determined by another non-key attribute (or by a set of
            non-key attributes). That is, there should be no transitive
            dependency of a non-key attribute on the primary key.

    Remedy
        -   Decompose and set up a relation that includes the non-key
            attribute(s) that functionally determine(s) other non-key
            attribute(s).

    Approach
        -   Create a separate relation for each transitive functional
            dependency violation against the keys of the base relation.

    Args:
        relation (Relation): Relation that is being normalized into the
            Third Normal Form.

    Returns:
        list[Relation]: The decomposition of the original relation into a
            list of relations in 3NF.
    """

    """Definition of a Transitive Functional Dependency

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
        new_primary_key: set[str] = tfd.lhs.copy()

        for attribute in tfd.rhs:
            if attribute not in relation.columns:
                continue  # already removed
            relation.remove_attribute(attribute)

        decomposed_relation = Relation(
            name=(
                relation.name.rstrip("Data")
                + "".join([column.rstrip("ID") for column in new_primary_key])
                + "Data"
            ),
            columns=tfd.lhs | tfd.rhs,
            primary_key=new_primary_key,
            functional_dependencies={tfd},
        )
        decomposition.append(decomposed_relation)
    decomposition.append(relation)

    return decomposition


def normalize_to_BCNF(relation: Relation) -> list[Relation]:
    """Normalize a Relation into Boyce-Codd Normal Form (3NF)

    Boyce-Codd Normal Form:

    Definition
        -   A relation schema R is in BCNF if whenever a nontrivial
            functional dependency X → A holds in R, then X is a superkey
            of R.

    General rule
        1.  Let R be the relation not in BCNF, let X ⊆ R, and let X → A be
            the FD that causes a violation of BCNF. R may be decomposed
            into two relations: R-A and XA
        2.  If either R-A or XA is not in BCNF, repeat the process.

    Approach
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

        new_primary_key: set[str] = bcnf_violation.lhs.copy()

        # R becomes R-A
        for attribute in bcnf_violation.rhs:
            if attribute not in relation.columns:
                continue  # already removed
            relation.remove_attribute(attribute)

        # New relation XA
        decomposed_relation = Relation(
            name=(
                relation.name.rstrip("Data")
                + "".join([column.rstrip("ID") for column in new_primary_key])
                + "Data"
            ),
            columns=bcnf_violation.lhs | bcnf_violation.rhs,
            primary_key=new_primary_key,
            functional_dependencies={
                fd
                for fd in relation.minimal_fd_set()
                if (fd.lhs == bcnf_violation.lhs)
                and (fd.rhs == bcnf_violation.rhs)
            },
        )
        decomposition.append(decomposed_relation)

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
    """Normalize a Relation into Fourth Normal Form (4NF)

    Fourth Normal Form:

    Definition
        -   A relation schema R is in 4NF with respect to a set of
            dependencies F (that includes functional dependencies and
            multivalued dependencies) if, for every nontrivial multivalued
            dependency X →→ Y in F+ *, X is a superkey for R.

            (*  F+ refers to the cover of functional dependencies F, or all
                dependencies that are implied by F.)

    General rule
        -   The process of normalizing a relation involving the nontrivial
            MVDs that is not in 4NF consists of decomposing it so that each
            MVD is represented by a separate relation where it becomes a
            trivial MVD.

    Approach
        -   Create a separate relation for each MVD violation.

    Args:
        relation (Relation): Relation that is being normalized into the Fourth
            Normal Form.

    Returns:
        list[Relation]: The decomposition of the original relation into a
            list of relations in 4NF.
    """

    ...


def normalize_to_5NF(relation: Relation) -> list[Relation]:
    """Normalize a Relation into Fifth Normal Form (5NF)

    Fifth Normal Form:

    Definition
        -   A relation schema R is in fifth normal form (5NF) (or project-join
            normal form (PJNF)) with respect to a set F of functional,
            multivalued, and join dependencies if, for every nontrivial join
            dependency JD(R1, R2, … , Rn) in F+ (that is, implied by F),*
            every R_i is a superkey of R.

            (*  F+ refers to the cover of functional dependencies F, or all
                dependencies that are implied by F.)

    General rule
        - TODO

    Approach
        -   Decompose each base relation into its sub-relation projection if a
            non-trivial join dependency is identified.

    Args:
        relation (Relation): Relation that is being normalized into the Fifth
            Normal Form.

    Returns:
        list[Relation]: The decomposition of the original relation into a
            list of relations in 5NF.
    """

    """Definition of a Join Dependency

        Join Dependency (JD):
            -   A join dependency (JD), denoted by JD(R1 , R2 , … , R n),
                specified on relation schema R, specifies a constraint on the
                states r of R. The constraint states that every legal state r
                of R should have a nonadditive join decomposition into R1, R2,
                … , Rn. Hence, for every such r we have:

                * (π_R1(r), π_R2(r), … , π_Rn(r)) = r
    """

    ...
