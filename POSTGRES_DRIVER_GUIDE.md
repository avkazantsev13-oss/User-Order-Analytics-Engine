# Инструкция по использованию `PostgresDriver`

Этот документ описывает, как использовать модуль `postgres_driver.py` во внешних проектах.

## 1. Что это за модуль

`PostgresDriver` — это простой драйвер для PostgreSQL с базовыми CRUD-операциями:

- `create` — создать запись
- `read` — получить записи
- `update` — обновить записи
- `delete` — удалить записи

Подключение к БД строится через переменные окружения (как в `test_postgres_connection.py`).

## 2. Подготовка окружения

Установите зависимости:

```bash
pip install -r requirements.txt
```

Создайте файл `.env` в корне проекта (или рядом с модулем) и заполните:

```env
PGHOST=localhost
PGPORT=5432
PGDATABASE=test
PGUSER=user
PGPASSWORD=11111
```

## 3. Быстрый старт

```python
from postgres_driver import PostgresDriver

driver = PostgresDriver()
```

По умолчанию класс пытается загрузить `.env` автоматически.

Если нужно отключить автозагрузку:

```python
driver = PostgresDriver(auto_load_env=False)
```

Если нужен конкретный путь к env-файлу:

```python
driver = PostgresDriver(env_path="C:/path/to/.env", auto_load_env=True)
```

## 4. Описание методов

### `create(table: str, data: dict) -> dict`

Создает запись и возвращает добавленную строку (`RETURNING *`).

Пример:

```python
new_user = driver.create(
    table="users",
    data={"name": "Alice", "email": "alice@example.com", "age": 25},
)
```

---

### `read(table: str, filters: dict | None = None, columns: list[str] | None = None, limit: int | None = None, offset: int | None = None) -> list[dict]`

Читает записи из таблицы.

- `filters` — словарь условий `{"поле": значение}`, объединяется через `AND`
- `columns` — список нужных колонок (если `None`, выбираются все)
- `limit` и `offset` — пагинация

Примеры:

```python
# Все записи
rows = driver.read("users")

# Фильтр по полю
rows = driver.read("users", filters={"name": "Alice"})

# Только нужные колонки + limit
rows = driver.read("users", columns=["id", "name"], limit=10)
```

---

### `update(table: str, data: dict, filters: dict) -> list[dict]`

Обновляет записи по фильтру и возвращает обновленные строки (`RETURNING *`).

Важно:

- `data` не должен быть пустым
- `filters` не должен быть пустым (защита от массового обновления всей таблицы)

Пример:

```python
updated = driver.update(
    table="users",
    data={"age": 26},
    filters={"id": 1},
)
```

---

### `delete(table: str, filters: dict) -> list[dict]`

Удаляет записи по фильтру и возвращает удаленные строки (`RETURNING *`).

Важно:

- `filters` не должен быть пустым (защита от удаления всей таблицы)

Пример:

```python
deleted = driver.delete("users", filters={"id": 1})
```

## 5. Демонстрационный запуск

В проекте есть пример в `main.py`. Запуск:

```bash
python main.py
```

Скрипт показывает полный цикл CRUD на таблице `demo_users`.

## 6. Обработка ошибок и безопасность

- При ошибке подключения выбрасывается `ConnectionError`.
- Для `update` и `delete` без фильтров выбрасывается `ValueError`.
- Имена таблиц и колонок формируются безопасно через `psycopg2.sql.Identifier`.
- Значения передаются параметризованно (`%s`) для защиты от SQL-инъекций.

## 7. Рекомендации для внешнего проекта

- Скопируйте `postgres_driver.py` в ваш проект или подключите как внутренний модуль.
- Храните секреты только в `.env` (не коммитьте реальные пароли в репозиторий).
- Для каждой сущности держите понятные имена таблиц/полей и явно задавайте `filters` в `update/delete`.
