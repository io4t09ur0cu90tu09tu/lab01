from core import InventoryResult, Product, make_processor


def render_report(result: InventoryResult) -> None:
    """Виводить результат обробки на екран."""
    print("Товари для дозамовлення:")

    for product in result["products"]:
        print(
            f'Товар {product["id"]}: '
            f'дозамовити {product["reorder_quantity"]} шт., '
            f'вартість {product["replenishment_cost"]:.2f}'
        )

    print(f'Кількість товарів: {result["count"]}')
    print(f'Загальна вартість поповнення: {result["total_cost"]:.2f}')


def main() -> None:
    products: list[Product] = [
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
        {
            "id": 4,
            "stock": 15,
            "price": 80.0,
            "min_stock": 15,
            "category": "office",
        },
    ]

    reorder_policy = lambda product: product["stock"] < product["min_stock"]
    discount_policy = lambda cost: cost * 0.9

    processor = make_processor(
        reorder_policy=reorder_policy,
        discount_policy=discount_policy,
    )

    result = processor(products)
    render_report(result)


if __name__ == "__main__":
    main()
