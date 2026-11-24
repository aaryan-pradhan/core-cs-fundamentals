# Lecture 7: Relational Model

> **The story:** You run an online shop. Customers sign up and place orders. You must store them in tables safely.

## 1. The ER diagram becomes tables

You drew the ER diagram. Each entity becomes a table, and each attribute becomes a column.

```mermaid
flowchart LR
  E["ER entity<br/>Customer<br/>(cust_id, name, contact, email)"] -->|"convert"| T["Table<br/>Customer<br/>4 columns"] -->|"CREATE TABLE"| R["RDBMS<br/>MySQL, Oracle"]
```

## 2. Anatomy of a table

Two customers sign up. Here is the Customer table.

| cust_id | name | contact | email |
|---|---|---|---|
| 1 | Lakshya | 98100 | l@x.com |
| 2 | Raj | 98200 | r@x.com |

```mermaid
flowchart TB
  T["Customer table = a relation"]
  T --> SC["Schema<br/>Customer(cust_id, name, contact, email)"]
  T --> C["Each column = attribute<br/>4 columns, so degree = 4"]
  T --> R["Each row = tuple = one customer<br/>2 rows, so cardinality = 2"]
  C --> D["Domain = allowed values<br/>cust_id holds only integers"]
```

| Term | Meaning |
|---|---|
| Relation | A relation is a table. |
| Tuple | A tuple is one row. |
| Attribute | An attribute is one column. |
| Domain | A domain is the set of allowed values of a column. |
| Schema | A schema is the table name plus its columns. |
| Degree | Degree is the number of columns. |
| Cardinality | Cardinality is the number of rows. |

## 3. Rules every table follows

A careless clerk tries to break the table. Each attempt breaks a rule.

```mermaid
flowchart LR
  A["Add Lakshya's row again"] -->|"breaks"| A1["Rows are unique"]
  B["contact = '98100, 98111'"] -->|"breaks"| B1["Values are atomic"]
  C["Two columns named 'name'"] -->|"breaks"| C1["Column names are unique"]
  D["A second table named Customer"] -->|"breaks"| D1["Table names are unique"]
```

Row order and column order do not matter.

## 4. Which column identifies a customer?

Then a second Raj signs up. Name can no longer tell customers apart, so you hunt for a key.

```mermaid
flowchart LR
  S1["Start: all column sets<br/>that identify a row<br/>= SUPER KEYS"] --> S2["Remove extra columns<br/>name repeats, so drop it<br/>= CANDIDATE KEYS"]
  S2 --> S3["Pick the shortest one<br/>{cust_id}<br/>= PRIMARY KEY"]
  S2 --> S4["The others left over<br/>{contact}, {email}<br/>= ALTERNATE KEYS"]
```

```mermaid
flowchart TB
  subgraph SK["Super keys: any attribute set that identifies a tuple"]
    X1["{cust_id, name, contact, email}"]
    subgraph CK["Candidate keys: minimal, no redundant attribute, never NULL"]
      subgraph PKS["Primary key: one CK, the shortest"]
        P["{cust_id}"]
      end
      subgraph AK["Alternate keys: CKs minus PK"]
        A1["{contact}"]
        A2["{email}"]
      end
    end
  end
```

Every candidate key is a super key, but not every super key is a candidate key.

## 5. Orders arrive, so link them with a foreign key

Lakshya places order 21. The Order table must say who placed it. It stores Lakshya's PK as a foreign key.

| order_id | cust_id (FK) |
|---|---|
| 21 | 1 |
| 22 | 2 |

```mermaid
flowchart LR
  Q["Who placed order 21?"] --> O["Order row 21<br/>cust_id = 1"] -->|"look up PK 1"| C["Customer row 1<br/>Lakshya"]
```

```mermaid
erDiagram
  Customer ||--o{ Order : "places"
  Customer {
    int cust_id PK "parent (referenced)"
    string name
  }
  Order {
    int order_id PK
    int cust_id FK "child (referencing)"
  }
```

The table holding the FK is the child. The table whose PK it copies is the parent.

## 6. More kinds of keys

The shop grows, and new tables need new kinds of keys.

```mermaid
flowchart TB
  subgraph CO["Composite key: PK of 2+ columns"]
    C1["OrderItem(order_id, item_no)<br/>order 21, item 1 / order 21, item 2"]
  end
  subgraph CP["Compound key: PK made of 2+ FKs"]
    P1["Wishlist(cust_id FK, product_id FK)"]
  end
  subgraph SU["Surrogate key: DB-made integer PK"]
    S1["School A reg 101 + School B reg B101<br/>merge, and the reg numbers can clash"] --> S2["DB adds auto-increment id<br/>1, 2, 3, 4 as the PK"]
  end
```

| Key | Definition |
|---|---|
| Super key | It is any set of columns that identifies each row. |
| Candidate key | It is a minimal super key. It is never NULL. |
| Primary key | It is the chosen candidate key. A table has only one. |
| Alternate key | It is every candidate key that is not the PK. |
| Foreign key | It is the PK of another table, stored here to link the two. |
| Composite key | It is a PK made of 2 or more columns. |
| Compound key | It is a PK made of 2 or more FKs. |
| Surrogate key | It is an auto-increment integer that the DB generates as the PK. |

## 7. Guards at the door: integrity constraints

Every insert, update and delete passes four guards. Each guard stops one kind of bad data.

```mermaid
flowchart LR
  X1["cust_id = 'abc'"] --> G1["Domain guard<br/>wrong type or range"] --> N1["Rejected"]
  X2["cust_id = NULL"] --> G2["Entity guard<br/>PK must exist, never NULL"] --> N2["Rejected"]
  X3["Order for cust_id 4<br/>(no customer 4)"] --> G3["Referential guard<br/>FK must exist in parent"] --> N3["Rejected"]
  X4["age = 17 with CHECK age >= 18"] --> G4["Key-constraint guard<br/>NOT NULL, UNIQUE, CHECK ..."] --> N4["Rejected"]
```

> **Interview:** The entity constraint is a favourite question. The PK is never NULL, otherwise rows cannot be told apart.

## 8. Customer 3 leaves: three endings

Customer 3 asks you to delete their account. Order 23 still points to them. The FK rule decides what happens.

```mermaid
flowchart TB
  D["Delete customer 3<br/>order 23 has cust_id = 3"] --> R{"FK rule on Order?"}
  R -- "no rule" --> R1["Ending 1: delete rejected<br/>customer 3 stays"]
  R -- "ON DELETE CASCADE" --> R2["Ending 2: customer 3 deleted<br/>order 23 deleted too"]
  R -- "ON DELETE SET NULL" --> R3["Ending 3: customer 3 deleted<br/>order 23 stays, cust_id = NULL"]
```

> **Interview:** Can an FK be NULL? Yes. It becomes NULL when its parent row is deleted under SET NULL.

## 9. The six key constraints in one table

You write all six rules into the table when you create it.

```sql
CREATE TABLE Customer (
  cust_id INT PRIMARY KEY,           -- unique + not NULL, one per table
  name    VARCHAR(50) NOT NULL,      -- cannot be empty
  email   VARCHAR(50) UNIQUE,        -- no two customers share it
  age     INT CHECK (age >= 18),     -- must pass the condition
  prime   BOOLEAN DEFAULT FALSE      -- used when no value is given
);

CREATE TABLE Orders (
  order_id INT PRIMARY KEY,
  cust_id  INT,
  FOREIGN KEY (cust_id) REFERENCES Customer(cust_id)
    ON DELETE CASCADE                -- or ON DELETE SET NULL
);
```

| | PRIMARY KEY | UNIQUE |
|---|---|---|
| Count per table | A table has only one. | A table can have many. |
| NULL | It is never NULL. | It can be NULL. |
| Purpose | It identifies each row. | It stops duplicate values. |
