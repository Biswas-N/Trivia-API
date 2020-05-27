CREATE TABLE categories (
	id SERIAL PRIMARY KEY,
    type VARCHAR
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question VARCHAR,
    answer VARCHAR,
    category_id INTEGER REFERENCES categories(id),
    difficulty INTEGER
);

INSERT INTO categories (type)
values 
    ('Science'),
    ('Art'),
    ('Geography'),
    ('History'),
    ('Entertainment'),
    ('Sports');

INSERT INTO questions (question, answer, category_id, difficulty)
values 
    (
        'Whose autobiography is entitled ''I Know Why the Caged Bird Sings''?', 
        'Maya Angelou', 
        (SELECT id from categories WHERE type='History'),
        4
    ),
    (
        'What boxer''s original name is Cassius Clay?', 
        'Muhammad Ali', 
        (SELECT id from categories WHERE type='Sports'),
        4
    ),
    (
        'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?', 
        'Apollo 13', 
        (SELECT id from categories WHERE type='Entertainment'), 
        5
    ),
    (
        'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?', 
        'Tom Cruise',
        (SELECT id from categories WHERE type='Entertainment'),
        5
    ),
    (
        'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?', 
        'Edward Scissorhands', 
        (SELECT id from categories WHERE type='Art'),
        4
    ),
    (
        'Which is the only team to play in every soccer World Cup tournament?', 
        'Brazil', 
        (SELECT id from categories WHERE type='Art'),
        6
    ),
    (
        'Which country won the first ever soccer World Cup in 1930?', 
        'Uruguay', 
        (SELECT id from categories WHERE type='Science'),
        4
    ),
    (
        'Who invented Peanut Butter?', 
        'George Washington Carver', 
        (SELECT id from categories WHERE type='Science'),
        4
    ),
    (
        'What is the largest lake in Africa?', 
        'Lake Victoria', 
        (SELECT id from categories WHERE type='Sports'),
        3
    ),
    (
        'In which royal palace would you find the Hall of Mirrors?', 
        'The Palace of Versailles', 
        (SELECT id from categories WHERE type='Art'),
        3
    ),
    (
        'The Taj Mahal is located in which Indian city?', 
        'Agra', 
        (SELECT id from categories WHERE type='Geography'),
        3
    );