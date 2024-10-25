# -*- coding: utf-8 -*-

from objects.fd import FD
from objects.relation import Relation
from rdbms_normalizer import normalize_to_3NF

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
    functional_dependencies={
        FD(
            lhs={"CustomerID"},
            rhs={"CustomerName"},
        )
    },
)

CoffeeShopDrinksOrderData = Relation(
    name="CoffeeShopDrinksOrderData",
    columns={
        "OrderID",
        "DrinkID",
        "DrinkName",
        "DrinkSize",
        "DrinkQuantity",
        "Milk",
    },
    primary_key={
        "OrderID",
        "DrinkID",
    },
    functional_dependencies={
        FD(
            lhs={"DrinkID"},
            rhs={"DrinkName"},
        )
    },
)

CoffeeShopFoodOrderData = Relation(
    name="CoffeeShopFoodOrderData",
    columns={
        "OrderID",
        "FoodID",
        "FoodName",
        "FoodQuantity",
    },
    primary_key={"OrderID", "FoodID"},
    functional_dependencies={
        FD(
            lhs={"FoodID"},
            rhs={"FoodName"},
        )
    },
)


def test_3NF():
    # 3NF
    for relation in (
        CoffeeShopOrderSummaryData,
        CoffeeShopDrinksOrderData,
        CoffeeShopFoodOrderData,
    ):
        print("~=" * 20)
        print("TESTING THIRD NORMAL FORM")
        print("~=" * 20)
        print()
        print("ORIGINAL RELATION:")
        print()
        print(relation)
        print()
        print("--" * 20)
        print()
        print("DECOMPOSITION FOR THIRD NORMAL FORM:")
        print()
        for decomposed_relation in normalize_to_3NF(relation):
            print()
            print(decomposed_relation)
            print(".." * 20)
        print()
