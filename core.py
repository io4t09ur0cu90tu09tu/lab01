from collections.abc import Callable, Iterable
from typing import TypedDict


class Product(TypedDict):
    id: int
    stock: int
    price: float
    min_stock: int
    category: str


class ProcessedProduct(Product, total=False):
    reorder_quantity: int
    replenishment_cost: float


class InventoryResult(TypedDict):
    count: int
    total_cost: float
    products: list[ProcessedProduct]


ReorderFn = Callable[[Product], bool]
DiscountFn = Callable[[float], float]


def needs_reorder(product: Product) -> bool:
    """Перевіряє, чи потрібно дозамовити товар."""
    return product["stock"] < product["min_stock"]


def calculate_reorder_quantity(product: Product) -> int:
    """Розраховує кількість товару для поповнення."""
    return max(product["min_stock"] - product["stock"], 0)


def calculate_replenishment_cost(
    product: Product,
    discount: DiscountFn,
) -> float:
    """Розраховує вартість поповнення з урахуванням знижки."""
    quantity = calculate_reorder_quantity(product)
    base_cost = quantity * product["price"]
    return discount(base_cost)


def with_replenishment_data(
    product: Product,
    quantity: int,
    cost: float,
) -> ProcessedProduct:
    """Повертає новий запис товару з даними про поповнення."""
    return {
        **product,
        "reorder_quantity": quantity,
        "replenishment_cost": cost,
    }


def process_inventory(
    products: Iterable[Product],
    *,
    reorder_policy: ReorderFn,
    discount_policy: DiscountFn,
) -> InventoryResult:
    """Обробляє складські товари без зміни вхідних даних."""
    qualified: list[ProcessedProduct] = []
    total_cost = 0.0

    for product in products:
        if not reorder_policy(product):
            continue

        quantity = calculate_reorder_quantity(product)
        cost = calculate_replenishment_cost(
            product,
            discount_policy,
        )

        new_product = with_replenishment_data(
            product,
            quantity,
            cost,
        )

        qualified.append(new_product)
        total_cost += cost

    return {
        "count": len(qualified),
        "total_cost": total_cost,
        "products": qualified,
    }


def make_processor(
    *,
    reorder_policy: ReorderFn,
    discount_policy: DiscountFn,
) -> Callable[[list[Product]], InventoryResult]:
    """Створює налаштований обробник складських товарів."""

    def process(products: list[Product]) -> InventoryResult:
        return process_inventory(
            products,
            reorder_policy=reorder_policy,
            discount_policy=discount_policy,
        )

    return process
