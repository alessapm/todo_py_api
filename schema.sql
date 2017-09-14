-- database is called todo_tictail (created)

BEGIN TRANSACTION;

DROP TABLE IF EXISTS todo_list;

CREATE TABLE todo_list
(id BIGSERIAL PRIMARY KEY,
item TEXT,
highlight BOOLEAN,
COMPLETED BOOLEAN
);

COMMIT;
