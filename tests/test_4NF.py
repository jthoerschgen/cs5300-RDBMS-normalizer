# -*- coding: utf-8 -*-

from objects.fd import MVD
from objects.relation import Relation
from rdbms_normalizer import normalize_to_4NF

CoffeeShopDrinkIngredientData = Relation(
    name="CoffeeShopDrinkIngredientData",
    columns={"OrderID", "DrinkID", "FoodID", "DrinkIngredient"},
    primary_key={"OrderID", "DrinkID", "FoodID", "DrinkIngredient"},
    functional_dependencies=set(),
    multivalued_dependencies={
        MVD(
            lhs={"OrderID", "DrinkID"},
            rhs={"FoodID", "DrinkIngredient"},
        ),
    },
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


CoffeeShopDrinkAllergenData = Relation(
    name="CoffeeShopDrinkAllergenData",
    columns={"OrderID", "DrinkID", "FoodID", "DrinkAllergen"},
    primary_key={"OrderID", "DrinkID", "FoodID", "DrinkAllergen"},
    functional_dependencies=set(),
    multivalued_dependencies={
        MVD(
            lhs={"OrderID", "DrinkID"},
            rhs={"FoodID", "DrinkAllergen"},
        ),
    },
    data_instances=[
        {
            "OrderID": "1001",
            "DrinkID": "1",
            "FoodID": "0",
            "DrinkAllergen": "Oat",
        },
        {
            "OrderID": "1002",
            "DrinkID": "2",
            "FoodID": "3",
            "DrinkAllergen": "Dairy",
        },
        {
            "OrderID": "1002",
            "DrinkID": "2",
            "FoodID": "3",
            "DrinkAllergen": "Nuts",
        },
        {
            "OrderID": "1002",
            "DrinkID": "3",
            "FoodID": "3",
            "DrinkAllergen": "Nuts",
        },
        {
            "OrderID": "1003",
            "DrinkID": "4",
            "FoodID": "0",
            "DrinkAllergen": "Nuts",
        },
        {
            "OrderID": "1003",
            "DrinkID": "4",
            "FoodID": "0",
            "DrinkAllergen": "Soy",
        },
    ],
)

CoffeeShopFoodIngredientData = Relation(
    name="CoffeeShopFoodIngredientData",
    columns={"OrderID", "DrinkID", "FoodID", "FoodIngredient"},
    primary_key={"OrderID", "DrinkID", "FoodID", "FoodIngredient"},
    functional_dependencies=set(),
    multivalued_dependencies={
        MVD(
            lhs={"OrderID", "DrinkID"},
            rhs={"FoodID", "FoodIngredient"},
        ),
    },
    data_instances=[
        {
            "OrderID": "1001",
            "DrinkID": "1",
            "FoodID": "0",
            "FoodIngredient": "NONE",
        },
        {
            "OrderID": "1002",
            "DrinkID": "2",
            "FoodID": "3",
            "FoodIngredient": "Flour",
        },
        {
            "OrderID": "1002",
            "DrinkID": "2",
            "FoodID": "3",
            "FoodIngredient": "Sugar",
        },
        {
            "OrderID": "1002",
            "DrinkID": "2",
            "FoodID": "3",
            "FoodIngredient": "Blueberries",
        },
        {
            "OrderID": "1002",
            "DrinkID": "2",
            "FoodID": "3",
            "FoodIngredient": "Eggs",
        },
        {
            "OrderID": "1002",
            "DrinkID": "3",
            "FoodID": "3",
            "FoodIngredient": "Flour",
        },
        {
            "OrderID": "1002",
            "DrinkID": "3",
            "FoodID": "3",
            "FoodIngredient": "Sugar",
        },
        {
            "OrderID": "1002",
            "DrinkID": "3",
            "FoodID": "3",
            "FoodIngredient": "Blueberries",
        },
        {
            "OrderID": "1002",
            "DrinkID": "3",
            "FoodID": "3",
            "FoodIngredient": "Eggs",
        },
        {
            "OrderID": "1003",
            "DrinkID": "4",
            "FoodID": "0",
            "FoodIngredient": "NONE",
        },
    ],
)

CoffeeShopFoodAllergenData = Relation(
    name="CoffeeShopFoodAllergenData",
    columns={"OrderID", "DrinkID", "FoodID", "FoodAllergen"},
    primary_key={"OrderID", "DrinkID", "FoodID", "FoodAllergen"},
    functional_dependencies=set(),
    multivalued_dependencies={
        MVD(
            lhs={"OrderID", "DrinkID"},
            rhs={"FoodID", "FoodAllergen"},
        ),
    },
    data_instances=[
        {
            "OrderID": "1001",
            "DrinkID": "1",
            "FoodID": "0",
            "FoodAllergen": "NONE",
        },
        {
            "OrderID": "1002",
            "DrinkID": "2",
            "FoodID": "3",
            "FoodAllergen": "Wheat",
        },
        {
            "OrderID": "1002",
            "DrinkID": "2",
            "FoodID": "3",
            "FoodAllergen": "Egg",
        },
        {
            "OrderID": "1002",
            "DrinkID": "3",
            "FoodID": "3",
            "FoodAllergen": "Wheat",
        },
        {
            "OrderID": "1002",
            "DrinkID": "3",
            "FoodID": "3",
            "FoodAllergen": "Egg",
        },
        {
            "OrderID": "1003",
            "DrinkID": "4",
            "FoodID": "0",
            "FoodAllergen": "NONE",
        },
    ],
)


def test_4NF():
    # 4NF
    for relation in (
        CoffeeShopDrinkIngredientData,
        CoffeeShopDrinkAllergenData,
        CoffeeShopFoodIngredientData,
        CoffeeShopFoodAllergenData,
    ):
        print("~=" * 20)
        print("TESTING FOURTH NORMAL FORM")
        print("~=" * 20)
        print()
        print("ORIGINAL RELATION:")
        print()
        print(relation)
        print()
        print("--" * 20)
        print()
        print("DECOMPOSITION FOR FOURTH NORMAL FORM:")
        print()
        for decomposed_relation in normalize_to_4NF(relation):
            print()
            print(decomposed_relation)
            print(".." * 20)
        print()
