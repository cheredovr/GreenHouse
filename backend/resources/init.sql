-- Таблица блюд
CREATE TABLE IF NOT EXISTS dishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

-- Таблица ингредиентов (только название)
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Связь блюд и ингредиентов
CREATE TABLE IF NOT EXISTS dish_ingredients (
    dish_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    PRIMARY KEY (dish_id, ingredient_id),
    FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE
);

-- Таблица тегов (только название)
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Связь блюд и тегов
CREATE TABLE IF NOT EXISTS dish_tags (
    dish_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (dish_id, tag_id),
    FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Базовые теги
INSERT OR IGNORE INTO tags (name) VALUES 
    ('веганское'),
    ('без лактозы'),
    ('острое'),
    ('вегетарианское'),
    ('без глютена'),
    ('десерт'),
    ('основное блюдо'),
    ('закуска');

-- Популярные ингредиенты
INSERT OR IGNORE INTO ingredients (name) VALUES 
    ('картофель'),
    ('лук'),
    ('морковь'),
    ('чеснок'),
    ('помидоры'),
    ('огурцы'),
    ('масло растительное'),
    ('соль'),
    ('перец'),
    ('курица'),
    ('говядина'),
    ('рис'),
    ('макароны'),
    ('сыр'),
    ('яйца');