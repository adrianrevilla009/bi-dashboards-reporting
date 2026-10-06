-- Same data as seed.sql (Postgres dialect is identical for this subset)
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, tenant TEXT NOT NULL);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id),
  status TEXT NOT NULL, amount NUMERIC NOT NULL, ordered_at DATE NOT NULL);
INSERT INTO customers VALUES (1,'Ada','acme'),(2,'Linus','acme'),(3,'Grace','globex'),(4,'Alan','globex');
INSERT INTO orders VALUES
 (1,1,'PAID',120.00,'2026-01-05'),(2,1,'PAID',80.50,'2026-01-20'),(3,2,'CANCELLED',45.00,'2026-02-02'),
 (4,3,'PAID',300.00,'2026-02-11'),(5,3,'NEW',60.00,'2026-03-03'),(6,4,'PAID',210.25,'2026-03-15'),
 (7,2,'PAID',99.99,'2026-03-28'),(8,4,'CANCELLED',15.00,'2026-04-01');
