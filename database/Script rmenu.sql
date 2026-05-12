
-- ТИПЫ БЛЮД

CREATE TABLE dish_types (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(100) UNIQUE NOT NULL
);
INSERT INTO dish_types (type_name)
VALUES ('Суп');
SELECT * FROM dish_types;


-- БЛЮДА

CREATE TABLE dishes (
    dish_id SERIAL PRIMARY KEY,
    dish_name VARCHAR(150) NOT NULL,
    price NUMERIC(8,2) NOT NULL CHECK (price > 0),
    calories_total NUMERIC(8,2),
    cost_price NUMERIC(8,2),
    type_id INTEGER NOT NULL,

    CONSTRAINT fk_dish_type
        FOREIGN KEY (type_id)
        REFERENCES dish_types(type_id)
        ON DELETE RESTRICT
);

-- КОМПОНЕНТЫ

CREATE TABLE components (
    component_id SERIAL PRIMARY KEY,
    component_name VARCHAR(150) UNIQUE NOT NULL,
    calories NUMERIC(6,2) CHECK (calories >= 0),
    price NUMERIC(8,2) CHECK (price >= 0),
    weight NUMERIC(6,2) CHECK (weight > 0),
    price_per_gram NUMERIC(8,4)
);

-- СОСТАВ БЛЮДА

CREATE TABLE dish_components (
    dish_id INTEGER NOT NULL,
    component_id INTEGER NOT NULL,
    amount_grams NUMERIC(6,2) NOT NULL CHECK (amount_grams > 0),

    PRIMARY KEY (dish_id, component_id),

    CONSTRAINT fk_dc_dish
        FOREIGN KEY (dish_id)
        REFERENCES dishes(dish_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_dc_component
        FOREIGN KEY (component_id)
        REFERENCES components(component_id)
        ON DELETE RESTRICT
);

-- МИКРОЭЛЕМЕНТЫ

CREATE TABLE microelements (
    microelement_id SERIAL PRIMARY KEY,
    microelement_name VARCHAR(150) UNIQUE NOT NULL
);

-- СОСТАВ КОМПОНЕНТОВ

CREATE TABLE component_microelements (
    component_id INTEGER NOT NULL,
    microelement_id INTEGER NOT NULL,
    amount_per_100g NUMERIC(8,3) NOT NULL CHECK (amount_per_100g >= 0),

    PRIMARY KEY (component_id, microelement_id),

    CONSTRAINT fk_cm_component
        FOREIGN KEY (component_id)
        REFERENCES components(component_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_cm_microelement
        FOREIGN KEY (microelement_id)
        REFERENCES microelements(microelement_id)
        ON DELETE CASCADE
);

-- СУТОЧНАЯ НОРМА

CREATE TABLE daily_microelement_requirements (
    microelement_id INTEGER PRIMARY KEY,
    daily_amount_mg NUMERIC(8,3) NOT NULL CHECK (daily_amount_mg > 0),

    CONSTRAINT fk_daily_microelement
        FOREIGN KEY (microelement_id)
        REFERENCES microelements(microelement_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_dishes_type_id
ON dishes(type_id);


CREATE INDEX idx_dc_component
ON dish_components(component_id);


CREATE INDEX idx_cm_microelement
ON component_microelements(microelement_id);


CREATE OR REPLACE FUNCTION update_price_per_gram()
RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.weight > 0 THEN
        NEW.price_per_gram := NEW.price / NEW.weight;
    END IF;

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;


CREATE TRIGGER trg_update_price_per_gram
BEFORE INSERT OR UPDATE
ON components
FOR EACH ROW
EXECUTE FUNCTION update_price_per_gram();


CREATE OR REPLACE FUNCTION update_dish_totals()
RETURNS TRIGGER AS
$$
BEGIN

UPDATE dishes
SET

calories_total =
(
SELECT SUM(c.calories * dc.amount_grams / 100)
FROM dish_components dc
JOIN components c
ON dc.component_id = c.component_id
WHERE dc.dish_id = NEW.dish_id
),

cost_price =
(
SELECT SUM(c.price_per_gram * dc.amount_grams)
FROM dish_components dc
JOIN components c
ON dc.component_id = c.component_id
WHERE dc.dish_id = NEW.dish_id
)

WHERE dish_id = NEW.dish_id;


RETURN NEW;

END;
$$
LANGUAGE plpgsql;




CREATE TRIGGER trg_update_dish_totals
AFTER INSERT OR UPDATE OR DELETE
ON dish_components
FOR EACH ROW
EXECUTE FUNCTION update_dish_totals();


-- состав блюда

CREATE VIEW dish_structure_view AS

SELECT
d.dish_name,
c.component_name,
dc.amount_grams

FROM dish_components dc

JOIN dishes d
ON d.dish_id = dc.dish_id

JOIN components c
ON c.component_id = dc.component_id;


--калории блюда

CREATE VIEW dish_calories_view AS

SELECT

d.dish_name,

SUM(c.calories * dc.amount_grams / 100) AS total_calories

FROM dishes d

JOIN dish_components dc
ON d.dish_id = dc.dish_id

JOIN components c
ON c.component_id = dc.component_id

GROUP BY d.dish_name;


--микроэлементы блюда

CREATE VIEW dish_microelements_view AS

SELECT

d.dish_name,
m.microelement_name,

SUM(
cm.amount_per_100g * dc.amount_grams / 100
) AS microelement_amount

FROM dishes d

JOIN dish_components dc
ON d.dish_id = dc.dish_id

JOIN component_microelements cm
ON dc.component_id = cm.component_id

JOIN microelements m
ON cm.microelement_id = m.microelement_id

GROUP BY
d.dish_name,
m.microelement_name

HAVING
SUM(cm.amount_per_100g * dc.amount_grams / 100) > 0;


--прибыль

CREATE VIEW dish_profit_view AS

SELECT

dish_name,
price,
cost_price,
(price - cost_price) AS profit

FROM dishes;

SELECT tgname
FROM pg_trigger
WHERE tgrelid = 'dish_components'::regclass;

ALTER TABLE dish_components
ADD COLUMN id SERIAL;

ALTER TABLE component_microelements
ADD COLUMN id SERIAL;

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'dish_components';


-- Значения по умолчанию для числовых полей

ALTER TABLE dishes
ALTER COLUMN calories_total
SET DEFAULT 0;

ALTER TABLE dishes
ALTER COLUMN cost_price
SET DEFAULT 0;

ALTER TABLE components
ALTER COLUMN calories
SET DEFAULT 0;

ALTER TABLE components
ALTER COLUMN price_per_gram
SET DEFAULT 0;

ALTER TABLE component_microelements
ALTER COLUMN amount_per_100g
SET DEFAULT 0;

ALTER TABLE daily_microelement_requirements
ALTER COLUMN daily_amount_mg
SET DEFAULT 0;


--блюда, покрывающие суточную норму

CREATE VIEW daily_microelement_menu_view AS

SELECT

ROW_NUMBER() OVER () AS id,

d.dish_name,

m.microelement_id,

m.microelement_name,

SUM(
cm.amount_per_100g * dc.amount_grams / 100
) AS microelement_amount,

dmr.daily_amount_mg,

ROUND(
SUM(cm.amount_per_100g * dc.amount_grams / 100)
/ dmr.daily_amount_mg
* 100
, 2
) AS coverage_percent


FROM dishes d

JOIN dish_components dc
ON d.dish_id = dc.dish_id

JOIN component_microelements cm
ON dc.component_id = cm.component_id

JOIN microelements m
ON cm.microelement_id = m.microelement_id

JOIN daily_microelement_requirements dmr
ON m.microelement_id = dmr.microelement_id


GROUP BY

d.dish_name,
m.microelement_id,
m.microelement_name,
dmr.daily_amount_mg


HAVING

SUM(cm.amount_per_100g * dc.amount_grams / 100)
/ dmr.daily_amount_mg >= 1;



CREATE VIEW dish_type_calories_report AS

SELECT

ROW_NUMBER() OVER () AS id,

dt.type_name,

ROUND(AVG(d.calories_total),2) AS avg_calories,

MAX(d.calories_total) AS max_calories,

MIN(d.calories_total) AS min_calories,

COUNT(*) AS dishes_count

FROM dishes d

JOIN dish_types dt
ON d.type_id = dt.type_id

GROUP BY dt.type_name;


--процент покрытия нормы

CREATE VIEW dish_microelement_coverage_view AS

SELECT
ROW_NUMBER() OVER () AS id,

d.dish_name,

m.microelement_id,
m.microelement_name,

SUM(
cm.amount_per_100g * dc.amount_grams / 100
) AS microelement_amount,

dmr.daily_amount_mg,

ROUND(
SUM(cm.amount_per_100g * dc.amount_grams / 100)
/
NULLIF(dmr.daily_amount_mg, 0)
* 100,
2
) AS coverage_percent

FROM dishes d

JOIN dish_components dc
ON d.dish_id = dc.dish_id

JOIN component_microelements cm
ON dc.component_id = cm.component_id

JOIN microelements m
ON cm.microelement_id = m.microelement_id

JOIN daily_microelement_requirements dmr
ON m.microelement_id = dmr.microelement_id

GROUP BY
d.dish_name,
m.microelement_id,
m.microelement_name,
dmr.daily_amount_mg;

SELECT * FROM microelements;

