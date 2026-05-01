from postgres_driver import PostgresDriver


def run_demo() -> None:
    driver = PostgresDriver()
    driver.create_tables()

    print("=== ADD USERS ===")
    user_1 = driver.add_user("Ivan Petrov", 29)
    user_2 = driver.add_user("Maria Sidorova", 34)
    user_3 = driver.add_user("Alex Johnson", 27)
    user_4 = driver.add_user("Sofia Garcia", 31)
    print(user_1)
    print(user_2)
    print(user_3)
    print(user_4)

    print("\n=== ADD ORDERS ===")
    orders_data = [
        (user_1["id"], 1490.50),
        (user_2["id"], 2599.00),
        (user_3["id"], 980.75),
        (user_4["id"], 4200.00),
        (user_2["id"], 3150.25),
    ]
    for user_id, amount in orders_data:
        order = driver.add_order(user_id, amount)
        print(order)

    print("\n=== USER TOTALS ===")
    for row in driver.get_user_totals():
        print(f"{row['name']} - {float(row['total_amount']):.2f}")


if __name__ == "__main__":
    run_demo()
