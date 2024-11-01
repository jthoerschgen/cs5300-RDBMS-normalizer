# -*- coding: utf-8 -*-

from objects.fd import FD, MVD, NonAtomic
from objects.relation import Relation
from rdbms_normalizer import Normalizer

CoffeeShopDataSpecial = Relation(
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
        NonAtomic(lhs={"OrderID"}, rhs={"PromoCodeUsed"}),
        NonAtomic(lhs={"DrinkID"}, rhs={"DrinkIngredient"}),
        NonAtomic(lhs={"DrinkID"}, rhs={"DrinkAllergen"}),
        NonAtomic(lhs={"FoodID"}, rhs={"FoodIngredient"}),
        NonAtomic(lhs={"FoodID"}, rhs={"FoodAllergen"}),
    },
    functional_dependencies={
        # FD(
        #     lhs={"OrderID"},
        #     rhs={"PromoCodeUsed"},
        # ),  # CORRECTION: NOT PFD VIOLATION - IS INVALID FD - IGNORE
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
            rhs={"DrinkSize", "DrinkQuantity", "Milk"},
        ),  # PFD Violation
        FD(
            lhs={"OrderID", "FoodID"},
            rhs={"FoodQuantity"},
        ),  # PFD Violation
        FD(
            lhs={"CustomerID"},
            rhs={"CustomerName"},
        ),
        FD(
            lhs={"DrinkID"},
            rhs={"DrinkName"},
        ),  # CORRECTION: PFD Violation
        FD(
            lhs={"FoodID"},
            rhs={"FoodName"},
        ),  # CORRECTION: PFD Violation
    },
    multivalued_dependencies={
        MVD(
            lhs={"OrderID"},
            rhs=({"DrinkID"}, {"FoodID"}),
        )
        # MVD(
        #     lhs={"OrderID", "DrinkID"},
        #     rhs={"FoodID", "DrinkIngredient"},
        # ),
        # MVD(
        #     lhs={"OrderID", "DrinkID"},
        #     rhs={"FoodID", "DrinkAllergen"},
        # ),
        # MVD(
        #     lhs={"OrderID", "FoodID"},
        #     rhs={"DrinkID", "FoodIngredient"},
        # ),
        # MVD(
        #     lhs={"OrderID", "FoodID"},
        #     rhs={"DrinkID", "FoodAllergen"},
        # ),
    },
    data_instances=[
        {
            "OrderID": "1001",
            "Date": "6/30/2024",
            "PromoCodeUsed": "NONE",
            "TotalCost": "$7.25 ",
            "TotalDrinkCost": "$7.25 ",
            "TotalFoodCost": "$0.00 ",
            "CustomerID": "1",
            "CustomerName": "Alice Brown",
            "DrinkID": "1",
            "DrinkName": "Caffe Latte",
            "DrinkSize": "Grande",
            "DrinkQuantity": "1",
            "Milk": "ND",
            "DrinkIngredient": {"Espresso", "Oat Milk"},
            "DrinkAllergen": {"Oat"},
            "FoodID": "0",
            "FoodName": "NULL",
            "FoodQuantity": "0",
            "FoodIngredient": "NONE",
            "FoodAllergen": "NONE",
        },
        {
            "OrderID": "1002",
            "Date": "6/30/2026",
            "PromoCodeUsed": "SUMMERFUN",
            "TotalCost": "$9.98 ",
            "TotalDrinkCost": "$5.99 ",
            "TotalFoodCost": "$3.99 ",
            "CustomerID": "2",
            "CustomerName": "David Miller",
            "DrinkID": "2",
            "DrinkName": "Iced Caramel Macchiato",
            "DrinkSize": "Tall",
            "DrinkQuantity": "2",
            "Milk": "D",
            "DrinkIngredient": {"Expresso", "Vanilla" "Syrup", "Milk", "Ice"},
            "DrinkAllergen": {"Dairy", "Nuts"},
            "FoodID": "3",
            "FoodName": "Blueberry Muffin",
            "FoodQuantity": "1",
            "FoodIngredient": {"Flour", "Sugar", "Blueberries", "Eggs"},
            "FoodAllergen": {"Wheat", "Egg"},
        },
        {
            "OrderID": "1002",
            "Date": "6/30/2026",
            "PromoCodeUsed": "SUMMERFUN",
            "TotalCost": "$9.98 ",
            "TotalDrinkCost": "$5.99 ",
            "TotalFoodCost": "$3.99 ",
            "CustomerID": "2",
            "CustomerName": "David Miller",
            "DrinkID": "3",
            "DrinkName": "Iced Matcha Latte",
            "DrinkSize": "Grande",
            "DrinkQuantity": "1",
            "Milk": "ND",
            "DrinkIngredient": {"Matcha", "Coconut Milk", "Ice"},
            "DrinkAllergen": {"Nuts"},
            "FoodID": "3",
            "FoodName": "Blueberry Muffin",
            "FoodQuantity": "1",
            "FoodIngredient": {"Flour", "Sugar", "Blueberries", "Eggs"},
            "FoodAllergen": {"Wheat", "Egg"},
        },
        {
            "OrderID": "1003",
            "Date": "6/29/2024",
            "PromoCodeUsed": {"SUMMERFUN", "JUNEVIP"},
            "TotalCost": "$115.00 ",
            "TotalDrinkCost": "$115.00 ",
            "TotalFoodCost": "$0.00 ",
            "CustomerID": "3",
            "CustomerName": "Emily Garcia",
            "DrinkID": "4",
            "DrinkName": "Vanilla Bean Frappuccino",
            "DrinkSize": "Venti",
            "DrinkQuantity": "8",
            "Milk": "ND",
            "DrinkIngredient": {
                "Coffee",
                "Ice",
                "Vanilla" "Syrup",
                "Soy Milk",
            },
            "DrinkAllergen": {"Nuts", "Soy"},
            "FoodID": "0",
            "FoodName": "NULL",
            "FoodQuantity": "0",
            "FoodIngredient": "NONE",
            "FoodAllergen": "NONE",
        },
    ],
)

CoffeeShopDataStandard = Relation(
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
    functional_dependencies={
        # FD(
        #     lhs={"OrderID"},
        #     rhs={"PromoCodeUsed"},
        # ),  # CORRECTION: NOT PFD VIOLATION - IS INVALID FD - IGNORE
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
            rhs={"DrinkSize", "DrinkQuantity", "Milk"},
        ),  # PFD Violation
        FD(
            lhs={"OrderID", "FoodID"},
            rhs={"FoodQuantity"},
        ),  # PFD Violation
        FD(
            lhs={"CustomerID"},
            rhs={"CustomerName"},
        ),  # TFD Violation
        FD(
            lhs={"DrinkID"},
            rhs={"DrinkName"},
        ),  # CORRECTION: PFD Violation
        FD(
            lhs={"FoodID"},
            rhs={"FoodName"},
        ),  # CORRECTION: PFD Violation
    },
    multivalued_dependencies={
        MVD(
            lhs={"OrderID"},
            rhs=({"DrinkID", "FoodID"}, {"PromoCodeUsed"}),
        ),
        # MVD(
        #     lhs={"OrderID", "DrinkID"},
        #     rhs=({"FoodID"}, {"DrinkIngredient"}),
        # ),
        # MVD(
        #     lhs={"OrderID", "DrinkID"},
        #     rhs=({"FoodID"}, {"DrinkAllergen"}),
        # ),
        # MVD(
        #     lhs={"OrderID", "FoodID"},
        #     rhs=({"DrinkID"}, {"FoodIngredient"}),
        # ),
        # MVD(
        #     lhs={"OrderID", "FoodID"},
        #     rhs=({"DrinkID"}, {"FoodAllergen"}),
        # ),
        MVD(
            lhs={"DrinkID"},
            rhs=({"OrderID"}, {"DrinkIngredient"}),
        ),
        MVD(
            lhs={"DrinkID"},
            rhs=({"OrderID"}, {"DrinkAllergen"}),
        ),
        MVD(
            lhs={"FoodID"},
            rhs=({"OrderID"}, {"FoodIngredient"}),
        ),
        MVD(
            lhs={"FoodID"},
            rhs=({"OrderID"}, {"FoodAllergen"}),
        ),
    },
    data_instances=[
        {
            "OrderID": "1001",
            "Date": "6/30/2024",
            "PromoCodeUsed": "NONE",
            "TotalCost": "$7.25 ",
            "TotalDrinkCost": "$7.25 ",
            "TotalFoodCost": "$0.00 ",
            "CustomerID": "1",
            "CustomerName": "Alice Brown",
            "DrinkID": "1",
            "DrinkName": "Caffe Latte",
            "DrinkSize": "Grande",
            "DrinkQuantity": "1",
            "Milk": "ND",
            "DrinkIngredient": {"Espresso", "Oat Milk"},
            "DrinkAllergen": {"Oat"},
            "FoodID": "0",
            "FoodName": "NULL",
            "FoodQuantity": "0",
            "FoodIngredient": "NONE",
            "FoodAllergen": "NONE",
        },
        {
            "OrderID": "1002",
            "Date": "6/30/2026",
            "PromoCodeUsed": "SUMMERFUN",
            "TotalCost": "$9.98 ",
            "TotalDrinkCost": "$5.99 ",
            "TotalFoodCost": "$3.99 ",
            "CustomerID": "2",
            "CustomerName": "David Miller",
            "DrinkID": "2",
            "DrinkName": "Iced Caramel Macchiato",
            "DrinkSize": "Tall",
            "DrinkQuantity": "2",
            "Milk": "D",
            "DrinkIngredient": {"Expresso", "Vanilla" "Syrup", "Milk", "Ice"},
            "DrinkAllergen": {"Dairy", "Nuts"},
            "FoodID": "3",
            "FoodName": "Blueberry Muffin",
            "FoodQuantity": "1",
            "FoodIngredient": {"Flour", "Sugar", "Blueberries", "Eggs"},
            "FoodAllergen": {"Wheat", "Egg"},
        },
        {
            "OrderID": "1002",
            "Date": "6/30/2026",
            "PromoCodeUsed": "SUMMERFUN",
            "TotalCost": "$9.98 ",
            "TotalDrinkCost": "$5.99 ",
            "TotalFoodCost": "$3.99 ",
            "CustomerID": "2",
            "CustomerName": "David Miller",
            "DrinkID": "3",
            "DrinkName": "Iced Matcha Latte",
            "DrinkSize": "Grande",
            "DrinkQuantity": "1",
            "Milk": "ND",
            "DrinkIngredient": {"Matcha", "Coconut Milk", "Ice"},
            "DrinkAllergen": {"Nuts"},
            "FoodID": "3",
            "FoodName": "Blueberry Muffin",
            "FoodQuantity": "1",
            "FoodIngredient": {"Flour", "Sugar", "Blueberries", "Eggs"},
            "FoodAllergen": {"Wheat", "Egg"},
        },
        {
            "OrderID": "1003",
            "Date": "6/29/2024",
            "PromoCodeUsed": {"SUMMERFUN", "JUNEVIP"},
            "TotalCost": "$115.00 ",
            "TotalDrinkCost": "$115.00 ",
            "TotalFoodCost": "$0.00 ",
            "CustomerID": "3",
            "CustomerName": "Emily Garcia",
            "DrinkID": "4",
            "DrinkName": "Vanilla Bean Frappuccino",
            "DrinkSize": "Venti",
            "DrinkQuantity": "8",
            "Milk": "ND",
            "DrinkIngredient": {
                "Coffee",
                "Ice",
                "Vanilla" "Syrup",
                "Soy Milk",
            },
            "DrinkAllergen": {"Nuts", "Soy"},
            "FoodID": "0",
            "FoodName": "NULL",
            "FoodQuantity": "0",
            "FoodIngredient": "NONE",
            "FoodAllergen": "NONE",
        },
    ],
)


def main() -> list[Relation]:
    normalize_to: str = input("Desired Normal Form: ")
    Normalizer(CoffeeShopDataStandard, normalize_to)

    return 0


if __name__ == "__main__":
    main()
