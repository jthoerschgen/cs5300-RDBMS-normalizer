from objects.relation import Relation
from rdbms_normalizer import normalize_to_4NF

Emp_no_MVDs_provided = Relation(
    name="EMP",
    columns={
        "Ename",
        "Pname",
        "Dname",
    },
    primary_key={"Ename", "Pname", "Dname"},
    multivalued_dependencies=set(),  # Provide no Multivalued Dependencies
    # MVD(lhs={"Ename"},rhs={"Pname", "Dname"}) # The MVD for the relation
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


CoffeeShopDrinkIngredientData = Relation(
    name="CoffeeShopDrinkIngredientData",
    columns={"OrderID", "DrinkID", "FoodID", "DrinkIngredient"},
    primary_key={"OrderID", "DrinkID", "FoodID", "DrinkIngredient"},
    functional_dependencies=set(),
    # multivalued_dependencies={
    #     MVD(
    #         lhs={"OrderID", "DrinkID"},
    #         rhs=({"FoodID"}, {"DrinkIngredient"}),
    #     ),
    # },
    data_instances=[
        {
            "OrderID": "1001",
            "DrinkID": "1",
            "FoodID": "0",
            "DrinkIngredient": "Espresso",
        },
        {
            "OrderID": "1001",
            "DrinkID": "1",
            "FoodID": "0",
            "DrinkIngredient": "Oat Milk",
        },
        {
            "OrderID": "1002",
            "DrinkID": "2",
            "FoodID": "3",
            "DrinkIngredient": "Espresso",
        },
        {
            "OrderID": "1002",
            "DrinkID": "2",
            "FoodID": "3",
            "DrinkIngredient": "Vanilla Syrup",
        },
        {
            "OrderID": "1002",
            "DrinkID": "2",
            "FoodID": "3",
            "DrinkIngredient": "Milk",
        },
        {
            "OrderID": "1002",
            "DrinkID": "2",
            "FoodID": "3",
            "DrinkIngredient": "Ice",
        },
        {
            "OrderID": "1002",
            "DrinkID": "3",
            "FoodID": "3",
            "DrinkIngredient": "Matcha",
        },
        {
            "OrderID": "1002",
            "DrinkID": "3",
            "FoodID": "3",
            "DrinkIngredient": "Coconut Milk",
        },
        {
            "OrderID": "1002",
            "DrinkID": "3",
            "FoodID": "3",
            "DrinkIngredient": "Ice",
        },
        {
            "OrderID": "1003",
            "DrinkID": "4",
            "FoodID": "0",
            "DrinkIngredient": "Coffee",
        },
        {
            "OrderID": "1003",
            "DrinkID": "4",
            "FoodID": "0",
            "DrinkIngredient": "Ice",
        },
        {
            "OrderID": "1003",
            "DrinkID": "4",
            "FoodID": "0",
            "DrinkIngredient": "Vanilla Syrup",
        },
        {
            "OrderID": "1003",
            "DrinkID": "4",
            "FoodID": "0",
            "DrinkIngredient": "Soy Milk",
        },
    ],
)

CoffeeShopOrderSummaryData = Relation(
    name="CoffeeShopOrderSummaryData",
    columns={
        "OrderID",
        "Date",
        "TotalCost",
        "TotalDrinkCost",
        "TotalFoodCost",
        "CustomerID",
        "CustomerName",
    },
    primary_key={
        "OrderID",
    },
    data_instances=[
        {
            "OrderID": "1001",
            "Date": "6/30/2024",
            "TotalCost": "$7.25",
            "TotalDrinkCost": "$7.25",
            "TotalFoodCost": "$0.00",
            "CustomerID": "1",
            "CustomerName": "Alice Brown",
        },
        {
            "OrderID": "1002",
            "Date": "6/30/2026",
            "TotalCost": "$9.98",
            "TotalDrinkCost": "$5.99",
            "TotalFoodCost": "$3.99",
            "CustomerID": "2",
            "CustomerName": "David Miller",
        },
        {
            "OrderID": "1003",
            "Date": "6/29/2024",
            "TotalCost": "$115.00",
            "TotalDrinkCost": "$115.00",
            "TotalFoodCost": "$0.00",
            "CustomerID": "3",
            "CustomerName": "Emily Garcia",
        },
    ],
)  # ALREADY IN 4NF, FOR TESTING


def determine_multivalued_dependencies(
    relation: Relation = Emp_no_MVDs_provided,
) -> list[Relation]:
    """Recursively decomposes a relation into 4NF by determining a set of
    valid multivalue dependencies that is selected by the user.

    REPORT:
        This approach uses the Relation.verify_mvd() and
        Relation.determine_mvds() methods.

        A set of possible multivalued dependencies is generated in the
        determine_mvds() method.

        Before these multivalued dependencies are returned to the user they
        are verified via the verify_mvd() method.

        The verify_mvd() method executes a test on a multivalued dependency to
        see if that dependency is compliant with the definition of a
        multivalued dependency.

        If the multivalued dependency is compliant with the definition, then
        the dependency is added to the set that is returned via
        determine_mvds().

        For each step in the decomposition the user is prompted to choose from
        the set of verified multivalued dependencies. That multivalued
        dependency is added to the relation and used to decompose the relation.

        The final result is a fully 4NF set of relations from the original
        relation, only using the data instances of the relation.

    Args:
        relation (Relation): The Relation being decomposed.

    Returns:
        list[Relation]: A list of relations that makes up the decomposition.
    """
    print()
    print("INPUT Relation:")
    print("-" * 40)
    print(relation)
    print()
    print("#" * 40)
    print()

    available_mvds = list(relation.determine_mvds())

    if not available_mvds:
        return [relation]

    print("\nPOSSIBLE DECOMPOSITIONS:")
    for i, available_mvd in enumerate(available_mvds):
        print(f"\t#{i}\t{available_mvd}")

    mvd_selection_number: int = (
        int(input(f"Choose a MVD (0-{len(available_mvds) - 1}): "))
        if len(available_mvds) > 1
        else 0
    )

    assert mvd_selection_number < len(available_mvds)

    selected_mvd = available_mvds[mvd_selection_number]
    relation.multivalued_dependencies.add(selected_mvd)

    decomposition: list[Relation] = normalize_to_4NF(relation)
    for decomposed_relation in decomposition:
        print(decomposed_relation)
        print("-" * 40)
    print("=" * 40)

    all_decomposed_relations = []
    for decomposed_relation in decomposition:
        all_decomposed_relations.extend(
            determine_multivalued_dependencies(decomposed_relation)
        )

    return all_decomposed_relations


if __name__ == "__main__":
    determine_multivalued_dependencies()
