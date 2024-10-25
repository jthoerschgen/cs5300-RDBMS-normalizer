# -*- coding: utf-8 -*-

from objects.fd import FD
from objects.relation import Relation
from rdbms_normalizer import normalize_to_2NF

CoffeeShopPromocodeUsedData = Relation(
    name="CoffeeShopPromocodeUsedData",
    columns={"OrderID", "DrinkID", "FoodID", "PromocodeUsed"},
    primary_key={"OrderID", "DrinkID", "FoodID", "PromocodeUsed"},
    functional_dependencies={
        FD(
            lhs={"OrderID"},
            rhs={"PromocodeUsed"},
        ),  # PFD Violation
    },
)  # Not in 2NF

CoffeeShopData = Relation(
    name="CoffeeShopData",
    columns={
        "OrderID",
        "Date",
        "TotalCost",
        "TotalDrinkCost",
        "TotalFoodCost",
        "CustomerID",
        "CustomerName",
        "DrinkID",
        "DrinkName",
        "DrinkSize",
        "DrinkQuantity",
        "Milk",
        "FoodID",
        "FoodName",
        "FoodQuantity",
    },
    primary_key={"OrderID", "DrinkID", "FoodID"},
    functional_dependencies={
        FD(
            lhs={"OrderID"},
            rhs={
                "Date",
                "TotalCost",
                "TotalDrinkCost",
                "TotalFoodCost",
                "CustomerID",
                "CustomerName",
            },
        ),  # PFD Violation
        FD(
            lhs={"OrderID", "DrinkID"},
            rhs={"DrinkName", "DrinkSize", "DrinkQuantity", "Milk"},
        ),  # PFD Violation
        FD(
            lhs={"OrderID", "FoodID"},
            rhs={"FoodName", "FoodQuantity"},
        ),  # PFD Violation
        FD(
            lhs={"CustomerID"},
            rhs={"CustomerName"},
        ),
        FD(
            lhs={"DrinkID"},
            rhs={"DrinkName"},
        ),
        FD(
            lhs={"FoodID"},
            rhs={"FoodName"},
        ),
    },
)  # Not in 2NF


def test_2NF():
    # 2NF
    for relation in (
        CoffeeShopPromocodeUsedData,
        CoffeeShopData,
    ):
        print("~=" * 20)
        print("TESTING SECOND NORMAL FORM")
        print("~=" * 20)
        print()
        print("ORIGINAL RELATION:")
        print()
        print(relation)
        print()
        print("--" * 20)
        print()
        print("DECOMPOSITION FOR SECOND NORMAL FORM:")
        print()
        for decomposed_relation in normalize_to_2NF(relation):
            print()
            print(decomposed_relation)
            print(".." * 20)
        print()
