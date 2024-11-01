# -*- coding: utf-8 -*-

from objects.fd import NonAtomic
from objects.relation import Relation
from rdbms_normalizer import normalize_to_1NF

CoffeeShopData = Relation(
    name="CoffeeShopData",
    columns={
        "OrderID",
        "Date",
        "PromoCodeUsed",
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
        "DrinkIngredient",
        "DrinkAllergen",
        "FoodID",
        "FoodName",
        "FoodQuantity",
        "FoodIngredient",
        "FoodAllergen",
    },
    primary_key={"OrderID", "DrinkID", "FoodID"},
    non_atomic_columns={
        NonAtomic(
            lhs={"OrderID", "DrinkID", "FoodID"},
            rhs={"PromoCodeUsed"},
        ),
        NonAtomic(
            lhs={"OrderID", "DrinkID", "FoodID"},
            rhs={"DrinkIngredient"},
        ),
        NonAtomic(
            lhs={"OrderID", "DrinkID", "FoodID"},
            rhs={"DrinkAllergen"},
        ),
        NonAtomic(
            lhs={"OrderID", "DrinkID", "FoodID"},
            rhs={"FoodIngredient"},
        ),
        NonAtomic(
            lhs={"OrderID", "DrinkID", "FoodID"},
            rhs={"FoodAllergen"},
        ),
    },
    functional_dependencies=set(),
)


def test_1NF():
    # 1NF
    for relation in (CoffeeShopData,):
        print("~=" * 20)
        print("TESTING FIRST NORMAL FORM")
        print("~=" * 20)
        print()
        print("ORIGINAL RELATION:")
        print()
        print(relation)
        print()
        print("--" * 20)
        print()
        print("DECOMPOSITION FOR FIRST NORMAL FORM:")
        print()
        for relation in normalize_to_1NF(relation):
            print(relation)
            print(".." * 20)
        print()
