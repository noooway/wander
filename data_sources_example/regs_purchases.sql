CREATE TABLE regs (
       id INTEGER PRIMARY KEY,
       reg_date DATE
);


INSERT INTO regs (reg_date)
VALUES
       ('2019-01-02'),
       ('2019-01-03'),
       ('2019-01-02'),
       ('2019-01-05'),
       ('2019-01-05'),
       ('2019-01-06'),
       ('2019-01-06'),
       ('2019-01-06'),
       ('2019-01-07'),
       ('2019-01-08');


CREATE TABLE purchases (
       id INTEGER PRIMARY KEY,
       reg_id INTEGER NOT NULL,
       purchase_datetime DATETIME,
       purchase_amount REAL,
FOREIGN KEY(reg_id) REFERENCES regs(id)
);


INSERT INTO purchases (reg_id, purchase_datetime, purchase_amount)
VALUES
       (1, '2019-01-02 12:00:01', 10),
       (2, '2019-01-02 13:00:01', 10),
       (2, '2019-01-04 12:00:01', 10),
       (3, '2019-01-05 12:00:01', 10),
       (1, '2019-01-07 12:00:01', 10),
       (5, '2019-01-02 12:00:01', 10),
       (6, '2019-01-03 12:00:01', 10),
       (1, '2019-01-02 12:00:01', 10),
       (8, '2019-01-09 12:00:01', 10),
       (9, '2019-01-12 12:00:01', 10);
