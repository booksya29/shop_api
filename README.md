# shop_api

Невеликий REST API для вигаданого магазину. Робив, щоб розібратися, як зв'язати FastAPI з PostgreSQL без ORM, на чистому SQL через `psycopg2`. Тут є користувачі, товари і транзакції між ними: хтось купує, а API перевіряє, чи вистачає і грошей, і товару на складі.
## Що використано

- Python
- FastAPI
- PostgreSQL
- psycopg2 (запити пишу руками)
- python-dotenv

## Як запустити

Клонуємо репозиторій і ставимо залежності:

```bash
git clone https://github.com/booksya29/shop_api.git
cd shop_api
python -m venv .venv
source .venv/Scripts/activate.bat
pip install -r requirements.txt
```

Далі створюємо файл `.env` у корені проєкту:

```
DB_USER=postgres
DB_PASSWORD=твій_пароль
DB_HOST=localhost
DB_PORT=5432
DB_NAME=shop
```

Для створення самої бази даних потрібно викликати функцію create_tables з файлу database.py або вручну написати в pgAdmin 
Запуск:

```bash
uvicorn main:app
```

Сервер підніметься на `http://127.0.0.1:8000`. Swagger з усіма ендпоінтами, де їх можна одразу пробувати, лежить на `/docs`.

## Що вміє

### Користувачі (`/user`)

| Метод | Шлях | Що робить |
|-------|------|-----------|
| POST | `/user` | додає нового користувача |
| GET | `/user` | повертає всіх користувачів |
| GET | `/user/?user_id={id}` | повертає одного користувача |
| PATCH | `/user/{user_id}` | змінює дані користувача |
| DELETE | `/user/{user_id}` | видаляє користувача |

### Товари (`/products`)

Товар визначається за штрихкодом (`barcode`), а не за числовим id.

| Метод | Шлях | Що робить |
|-------|------|-----------|
| POST | `/products/add` | додає товар |
| GET | `/products/` | список товарів |
| PATCH | `/products/{barcode}` | редагує товар |
| DELETE | `/products/{barcode}` | видаляє товар |

### Транзакції (`/transactions`)

| Метод | Шлях | Що робить |
|-------|------|-----------|
| POST | `/transactions/new` | створює покупку |
| GET | `/transactions/show` | усі транзакції |
| GET | `/transactions/show?buyer_id=2` | транзакції конкретного покупця |

Перед створенням покупки API дивиться, чи є потрібна кількість товару і чи вистачає грошей у покупця. Якщо ні, транзакція не проходить.
