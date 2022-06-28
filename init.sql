''схема данных''

CREATE TABLE sheet (
    id SERIAL PRIMARY KEY,
    id_order INTEGER,
    price_usd INTEGER,
    price_rub INTEGER,
    delivery_date DATE,
    is_notified BOOLEAN
);

CREATE TABLE tg_users(
    id SERIAL PRIMARY KEY,
);