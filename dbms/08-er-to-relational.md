# Lecture 8: ER Model to Relational Model

> **The story:** You built the ER diagram for a bank. Now you must turn every shape in it into tables. Each panel converts one shape.

## 1. The big picture

The ER diagram says what exists. The tables say how to store it. Conversion decides the tables, the PKs and the FKs.

```mermaid
flowchart LR
  E["ER diagram<br/>(bank)"] -->|"convert each shape"| T["Tables<br/>+ PKs + FKs"] -->|"CREATE TABLE"| R["RDBMS"]
```

## 2. Strong entity: Loan gets its own table

Loan stands on its own. It becomes a table, and its key becomes the PK.

```mermaid
flowchart LR
  E["Strong entity<br/>Loan(loan_no, amount)"] --> T["Table loan<br/>PK = loan_no"]
```

| loan_no (PK) | amount |
|---|---|
| L1 | 50000 |
| L2 | 20000 |

## 3. Weak entity: Payment cannot live without Loan

Payment 1 exists for loan L1 and for loan L2. So payment_no alone cannot be the PK. Borrow the loan's PK.

```mermaid
flowchart LR
  W["Weak entity<br/>Payment(payment_no, date, amt)"] --> A["Add loan_no<br/>as FK"] --> P["PK = {loan_no, payment_no}<br/>FK + discriminator"]
```

| loan_no (PK, FK) | payment_no (PK) | amt |
|---|---|---|
| L1 | 1 | 5000 |
| L1 | 2 | 5000 |
| L2 | 1 | 2000 |

```mermaid
erDiagram
  loan ||--o{ payment : "loan payment"
  loan {
    string loan_no PK
    int amount
  }
  payment {
    string loan_no PK, FK
    int payment_no PK "discriminator"
    int amt
  }
```

## 4. Four kinds of attributes, four fates

A customer arrives with an address, many phone numbers and a birth date. Each attribute type is stored differently.

```mermaid
flowchart TB
  A["Attribute type?"]
  A -- "single-valued<br/>name" --> S["One column"]
  A -- "composite<br/>address = street + city + pin" --> C["One column per part<br/>address_street, address_city, address_pin<br/>drop 'address' itself"]
  A -- "multivalued<br/>dependents of emp 1" --> M["New table<br/>PK = {emp_id FK, dname}"]
  A -- "derived<br/>age from DOB" --> D["Not stored<br/>calculate it in a query"]
```

Employee 1 has three dependents. A new table stores one row per dependent.

| emp_id (PK, FK) | dname (PK) |
|---|---|
| 1 | Father |
| 1 | Mother |
| 1 | Wife |

> **Why a new table?** A dependents column in employee would repeat every other employee column for each dependent.

## 5. Generalisation: Account splits into Savings and Current

The bank has one Account type with two kinds. There are two ways to store it.

```mermaid
flowchart TB
  subgraph M1["Method 1: 3 tables"]
    A1["account(acc_no PK, balance)"]
    S1["savings(acc_no PK FK, interest_rate, daily_limit)"]
    C1["current(acc_no PK FK, overdraft, txn_charge)"]
    A1 --> S1
    A1 --> C1
  end
  subgraph M2["Method 2: 2 tables, no parent table"]
    S2["savings(acc_no PK, balance, interest_rate, daily_limit)"]
    C2["current(acc_no PK, balance, overdraft, txn_charge)"]
  end
```

| | Method 1 | Method 2 |
|---|---|---|
| Tables | It has a parent table plus one per child. | It has one table per child only. |
| Parent attributes | They are stored once, in the parent. | They are copied into every child. |
| When it works | It always works. | It works only if the split is disjoint and complete. |
| Overlap problem | There is none. | An account that is both types stores balance twice. |
| Incomplete problem | There is none. | A third account type has no table. |

## 6. Aggregation: a manager manages a whole relationship

Employee works on a job at a branch. A manager manages that whole combination. Make one table for the outer relationship.

```mermaid
flowchart LR
  subgraph WO["Aggregation: works_on"]
    E["employee"] --- J["job"] --- B["branch"]
  end
  M["manager"] -->|"manages"| WO
  WO --> T["Table manages<br/>PK = {manager_id, emp_id, job_id, branch_id}<br/>all four are FKs"]
```

## 7. Unary relationship: a table points to itself

Some relationships connect an entity to itself. The cardinality decides the shape.

```mermaid
flowchart TB
  U["Unary relationship"]
  U -- "1:N<br/>employee managed by employee" --> A["Add manager_id to employee<br/>FK to its own emp_id<br/>NULL for the CEO"]
  U -- "1:1<br/>person married to person" --> B["Add spouse_id to person<br/>FK to its own id"]
  U -- "M:N<br/>course needs prereq course" --> C["New table prereq<br/>PK = {course_id, prereq_id}<br/>both FKs to course"]
```

| emp_id (PK) | name | manager_id (FK) |
|---|---|---|
| 205 | Asha | NULL |
| 201 | Ravi | 205 |
| 202 | Meena | 205 |

## 8. Facebook: the whole ER diagram becomes 9 tables

Apply every rule above to the Facebook ER diagram. You get 9 tables.

```mermaid
erDiagram
  user_profile ||--o{ user_profile_email : "multivalued"
  user_profile ||--o{ user_profile_contact : "multivalued"
  user_profile ||--o{ friendship : "requested"
  user_profile ||--o{ friendship : "accepted"
  user_profile ||--o{ user_post : "posts"
  user_profile ||--o{ post_like : "likes"
  user_profile ||--o{ post_comment : "comments"
  user_post ||--o{ post_like : "has"
  user_post ||--o{ post_comment : "has"
  user_post ||--o{ user_post_image : "multivalued"
  user_post ||--o{ user_post_video : "multivalued"
  user_profile {
    string user_name PK
    string password
    date dob
  }
  user_profile_email {
    string user_name PK, FK
    string email PK
  }
  user_profile_contact {
    string user_name PK, FK
    string contact PK
  }
  friendship {
    string requester PK, FK
    string accepter PK, FK
  }
  user_post {
    int post_id PK
    string content
    string user_name FK
  }
  user_post_image {
    int post_id PK, FK
    string image_url PK
  }
  user_post_video {
    int post_id PK, FK
    string video_url PK
  }
  post_like {
    int post_like_id PK
    int post_id FK
    string user_name FK
  }
  post_comment {
    int post_comment_id PK
    string text_content
    int post_id FK
    string user_name FK
  }
```

| Table | Why it exists |
|---|---|
| user_profile | It is a strong entity. |
| user_profile_email, user_profile_contact | Email and contact are multivalued. |
| friendship | It is a unary M:N relationship. Its PK is a compound key of two FKs. |
| user_post | It is a strong entity with user_name as FK. |
| user_post_image, user_post_video | Image and video are multivalued. |
| post_like, post_comment | Each one links a user to a post through two FKs. |

## 9. Cheat sheet

| ER shape | Becomes |
|---|---|
| Strong entity | It becomes its own table with its own PK. |
| Weak entity | It becomes a table with PK = owner's PK (FK) + discriminator. |
| Single-valued attribute | It becomes one column. |
| Composite attribute | Each part becomes its own column. |
| Multivalued attribute | It becomes a new table with PK = entity PK (FK) + value. |
| Derived attribute | It is not stored. |
| Generalisation | It becomes Method 1 (parent + children) or Method 2 (children only). |
| Aggregation | It becomes a table holding the PKs of every participant. |
| Unary 1:N or 1:1 | It becomes a self-referencing FK column. |
| Unary M:N | It becomes a new table with two FKs to the same table. |
