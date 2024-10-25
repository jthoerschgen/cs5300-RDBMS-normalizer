# -*- coding: utf-8 -*-

from objects.fd import FD
from objects.relation import Relation
from rdbms_normalizer import normalize_to_5NF

# CoffeeShopDrinksOrderData (R):
#   Potential Business Rule:
#       -   When a drink is available in multiple dairy variants, and a
#           customer orders any version of that drink within a single order,
#           then the customer is expected to order ALL other variants of that
#           drink within the same order.
CoffeeShopDrinksOrderData = Relation(
    name="CoffeeShopDrinksOrderData",
    columns={"OrderID", "CustomerID", "DrinkID", "Milk"},
    primary_key={"OrderID", "CustomerID", "DrinkID", "Milk"},
    data_instances=[
        {"OrderID": "1001", "CustomerID": "1", "DrinkID": "1", "Milk": "ND"},
        {"OrderID": "1001", "CustomerID": "1", "DrinkID": "1", "Milk": "D"},
        {"OrderID": "1002", "CustomerID": "1", "DrinkID": "2", "Milk": "D"},
        {"OrderID": "1003", "CustomerID": "2", "DrinkID": "3", "Milk": "ND"},
        {"OrderID": "1003", "CustomerID": "2", "DrinkID": "3", "Milk": "D"},
        {"OrderID": "1003", "CustomerID": "2", "DrinkID": "4", "Milk": "ND"},
    ],
)  # Join Dependency: (R = R1(DrinkID, Milk) * R2(OrderID, CustomerID, DrinkID)

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
    data_instances=[
        {
            "OrderID": "1001",
            "Date": "6/30/2024",
            "TotalCost": "$7.25 ",
            "TotalDrinkCost": "$7.25 ",
            "TotalFoodCost": "$0.00 ",
            "CustomerID": "1",
            "CustomerName": "Alice Brown",
        },
        {
            "OrderID": "1002",
            "Date": "6/30/2026",
            "TotalCost": "$9.98 ",
            "TotalDrinkCost": "$5.99 ",
            "TotalFoodCost": "$3.99 ",
            "CustomerID": "2",
            "CustomerName": "David Miller",
        },
        {
            "OrderID": "1003",
            "Date": "6/29/2024",
            "TotalCost": "$115.00 ",
            "TotalDrinkCost": "$115.00 ",
            "TotalFoodCost": "$0.00 ",
            "CustomerID": "3",
            "CustomerName": "Emily Garcia",
        },
    ],
)  # Not a 5NF violation, for unit testing.


def test_5NF():
    # 5NF
    for relation in (CoffeeShopDrinksOrderData, CoffeeShopOrderSummaryData):
        print("~=" * 20)
        print("TESTING FIFTH NORMAL FORM")
        print("~=" * 20)
        print()
        print("ORIGINAL RELATION:")
        print()
        print(relation)
        print()
        print("--" * 20)
        print()
        print("DECOMPOSITION FOR FIFTH NORMAL FORM:")
        print()
        for decomposed_relation in normalize_to_5NF(relation):
            print()
            print(decomposed_relation)
            print(".." * 20)
        print()
