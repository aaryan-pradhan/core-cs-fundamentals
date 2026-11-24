# Lecture 7: Relational Model

## 1. Where the relational model fits

```mermaid
flowchart LR
  A["ER model<br/>(ER diagram)"] --> B["Relational model<br/>(tables)"] --> C["RDBMS<br/>MySQL, Oracle"]
```

## 2. Terms

```mermaid
flowchart TB
  S["Relation = table<br/>Customer(cust_id, name, contact, email)"]
  S --> SC["Schema<br/>= name + columns"]
  S --> COL["Column = attribute<br/>count = degree (4)"]
  S --> ROW["Row = tuple<br/>count = cardinality"]
  COL --> DOM["Domain<br/>= allowed values"]
```

| Term | Meaning |
|---|---|
| Relation | A relation is a table. |
| Tuple | A tuple is one row. |
| Attribute | An attribute is one column. |
| Domain | A domain is the set of allowed values of a column. |
| Schema | A schema is the relation name plus its columns. |
| Degree | Degree is the number of columns. |
| Cardinality | Cardinality is the number of rows. |

## 3. Properties of a table

| Property | Rule |
|---|---|
| Name | Each table name is unique. |
| Values | Each value is atomic. |
| Columns | Each column name is unique. |
| Rows | No two rows are the same. |
| Order | Row and column order does not matter. |

## 4. Keys

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

## 5. Foreign key

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

## 6. Surrogate key example

```mermaid
flowchart LR
  A["School A<br/>reg: 101, 102"] --> M["Merged table<br/>reg alone can clash"]
  B["School B<br/>reg: B101, B102"] --> M
  M --> S["Add surrogate key<br/>1, 2, 3, 4 as PK"]
```

## 7. Integrity constraints

```mermaid
flowchart TB
  IC["Integrity constraints<br/>keep the DB consistent on every CRUD"]
  IC --> D["Domain<br/>type and range of a column<br/>age >= 18"]
  IC --> E["Entity<br/>every table has a PK<br/>PK is never NULL"]
  IC --> R["Referential<br/>FK value must exist in parent<br/>or be NULL"]
  IC --> K["Key<br/>NOT NULL, UNIQUE, DEFAULT,<br/>CHECK, PK, FK"]
```

## 8. Referential constraint in action

```mermaid
flowchart TB
  I["Insert order with cust_id 4"] --> I1{"cust_id 4 in Customer?"}
  I1 -- No --> I2["Rejected: FK violation"]
  I1 -- Yes --> I3["Inserted"]
  D["Delete customer 3<br/>(an order refers to it)"] --> R{"FK rule?"}
  R -- "none" --> R1["Delete rejected"]
  R -- "ON DELETE CASCADE" --> R2["Customer and its orders<br/>both deleted"]
  R -- "ON DELETE SET NULL" --> R3["Customer deleted<br/>order stays, cust_id = NULL"]
```

> **Interview:** An FK can be NULL. It becomes NULL when its parent row is deleted under SET NULL.

## 9. Key constraints

| Constraint | Rule |
|---|---|
| NOT NULL | The column cannot be empty. |
| UNIQUE | All values in the column differ. A table can have many. |
| DEFAULT | The column gets this value when none is given. |
| CHECK | The value must pass a condition, such as `age >= 18`. |
| PRIMARY KEY | The value is unique and not NULL. A table has only one. |
| FOREIGN KEY | The value must match a PK in the parent table. |

```mermaid
flowchart LR
  PK["PRIMARY KEY<br/>one per table<br/>no NULL"] --- U["UNIQUE<br/>many per table<br/>NULL allowed"]
```
