from copy import deepcopy

from core import (
    Product,
    make_processor,
    process_inventory,
)


def sample_products() -> list[Product]:
    return [
        {
            "id": 1,
            "stock": 5,
            "price": 100.0,
            "min_stock": 10,
            "category": "electronics",
        },
        {
            "id": 2,
            "stock": 20,
            "price": 50.0,
            "min_stock": 10,
            "category": "office",
        },
        {
            "id": 3,
            "stock": 3,
            "price": 200.0,
            "min_stock": 8,
            "category": "electronics",
        },
    ]


def test_referential_transparency() -> None:
    products = sample_products()

    reorder_policy = lambda product: product["stock"] < product["min_stock"]
    discount_policy = lambda cost: cost * 0.9

    args = {
        "reorder_policy": reorder_policy,
        "discount_policy": discount_policy,
    }

    result_1 = process_inventory(products, **args)
    result_2 = process_inventory(products, **args)

    assert result_1 == result_2


def test_no_mutation() -> None:
    products = sample_products()
    original = deepcopy(products)

    process_inventory(
        products,
        reorder_policy=lambda product: True,
        discount_policy=lambda cost: cost,
    )

    assert products == original


def test_reorder_quantity() -> None:
    products = sample_products()

    result = process_inventory(
        products,
        reorder_policy=lambda product: True,
        discount_policy=lambda cost: cost,
    )

    assert result["products"][0]["reorder_quantity"] == 5
    assert result["products"][1]["reorder_quantity"] == 0
    assert result["products"][2]["reorder_quantity"] == 5


def test_discount_policy() -> None:
    products = sample_products()

    result = process_inventory(
        products,
        reorder_policy=lambda product: product["stock"] < product["min_stock"],
        discount_policy=lambda cost: cost * 0.9,
    )

    assert result["total_cost"] == 1350.0


def test_callable_processor() -> None:
    products = sample_products()

    reorder_policy = lambda product: product["category"] == "electronics"
    discount_policy = lambda cost: cost * 0.8

    processor = make_processor(
        reorder_policy=reorder_policy,
        discount_policy=discount_policy,
    )

    result = processor(products)

    assert result["count"] == 2
    assert result["total_cost"] == 1200.0
