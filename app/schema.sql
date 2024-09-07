CREATE TABLE IF NOT EXISTS user_account (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    type VARCHAR(10) CHECK (type IN ('super', 'normal')) NOT NULL
);

CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    user_id INT REFERENCES user_account(id) ON DELETE CASCADE,
    quantity INT CHECK (quantity >= 0) DEFAULT 0,
    price DECIMAL(10, 2) CHECK (price >= 0) DEFAULT 0
);

CREATE OR REPLACE FUNCTION check_product_limit() RETURNS TRIGGER
AS $$
BEGIN
    IF (SELECT COUNT(*) FROM product WHERE user_id = NEW.user_id) >= 3 AND
       (SELECT type FROM user_account WHERE user_id = NEW.user_id) = 'normal' THEN
        RAISE EXCEPTION 'Usuários normais podem cadastrar no máximo 3 produtos.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER product_limit_trigger
BEFORE INSERT ON product
FOR EACH ROW EXECUTE FUNCTION check_product_limit();

