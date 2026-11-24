# Lecture 11: Normalisation

> **The story:** A college office keeps everything in one big table. It breaks again and again. You split it, step by step, until every table has one job.

## 1. Functional dependency: who finds whom

If you know A, you can find B. We write it `A -> B`. A is the **determinant**, and B is the **dependent**.

```mermaid
flowchart LR
  ID["student_id = 1<br/>(determinant)"] --> N["name = Ravi<br/>(dependent)"]
  ID --> BR["branch = CS<br/>(dependent)"]
```

| FD type | Rule | Example |
|---|---|---|
| Trivial | B is a subset of A. | `(id, name) -> id` |
| Non-trivial | B is not a subset of A. | `id -> branch` |

## 2. Armstrong's axioms: rules to derive new FDs

Three rules let you derive new FDs from given ones.

```mermaid
flowchart LR
  subgraph RE["Reflexive: a set finds its subset"]
    X1["{A, B, C}"] --> Y1["{A, B}"]
  end
  subgraph AU["Augmentation: add X to both sides"]
    X2["A -> B"] --> Y2["AX -> BX"]
  end
  subgraph TR["Transitivity: chain them"]
    A3["A"] --> B3["B"] --> C3["C"]
    A3 -. "derived" .-> C3
  end
```

A worked check uses R(A, B, C, D, E) with `A -> B`, `A -> C`, `CD -> E`, `B -> D`, `E -> A`.

| Claim | Proof | Result |
|---|---|---|
| `BC -> CD` | Augment `B -> D` with C. | It is valid. |
| `EC -> AC` | Augment `E -> A` with C. | It is valid. |
| `B -> C` | No rule derives it. | It is illegal. |
| `CD -> AC` | `CD -> E -> A` by transitivity, and `CD -> C` by reflexive. | It is valid. |

## 3. The messy table

The office stores students, branches, HODs and subjects together. One cell holds two subjects.

| student_id | name | branch | hod | subject | professor |
|---|---|---|---|---|---|
| 1 | Ravi | CS | Dr X | Java, C++ | PJ, PC |
| 2 | Asha | CS | Dr X | Java | PJ2 |
| 3 | Mohan | ME | Dr Y | Java | PJ |

## 4. Three anomalies strike

Redundant data causes three anomalies. The DB also grows larger and gets slower.

```mermaid
flowchart TB
  subgraph INS["Insertion anomaly"]
    I1["A new IT branch opens with HOD Dr Z"] --> I2["No student has joined yet"] --> I3["IT cannot be added<br/>without NULL student data"]
  end
  subgraph DEL["Deletion anomaly"]
    D1["Mohan graduates, and his row is deleted"] --> D2["ME and Dr Y vanish too"]
  end
  subgraph UPD["Updation anomaly"]
    U1["The CS HOD changes"] --> U2["Every CS row must change"] --> U3["Miss one row<br/>and the data is inconsistent"]
  end
```

| Anomaly | What goes wrong |
|---|---|
| Insertion | You cannot insert data without some other, unrelated data. |
| Deletion | Deleting one fact loses another fact. |
| Updation | One change needs many rows to be updated. |

**Normalisation** fixes this. It splits a big table into smaller linked tables until each table has a single job (the Single Responsibility Principle).

## 5. The ladder of normal forms

Each form needs the one before it.

```mermaid
flowchart LR
  U["Unnormalised"] -- "atomic values" --> N1["1NF"] -- "no partial<br/>dependency" --> N2["2NF"] -- "no transitive<br/>dependency" --> N3["3NF"] -- "every determinant<br/>is a super key" --> BC["BCNF"]
```

| Term | Meaning |
|---|---|
| Prime attribute | It is part of some candidate key. |
| Non-prime attribute | It is not part of any candidate key. |

## 6. 1NF: one value per cell

Ravi's cell holds "Java, C++". Give each subject its own row.

| student_id | name | branch | hod | subject | professor |
|---|---|---|---|---|---|
| 1 | Ravi | CS | Dr X | Java | PJ |
| 1 | Ravi | CS | Dr X | C++ | PC |
| 2 | Asha | CS | Dr X | Java | PJ2 |
| 3 | Mohan | ME | Dr Y | Java | PJ |

The PK is now (student_id, subject). Ravi's data repeats, so redundancy remains. 1NF only demands atomic values.

## 7. 2NF: no partial dependency

The name depends on student_id alone, which is only part of the PK. That is a partial dependency.

```mermaid
flowchart LR
  subgraph BEFORE["PK = (student_id, subject)"]
    K["student_id + subject"] -- "full" --> P["professor"]
    S["student_id<br/>(part of PK)"] -- "partial" --> NB["name, branch, hod"]
  end
  BEFORE -- "split" --> T1["Student(student_id, name, branch, hod)<br/>PK student_id"]
  BEFORE -- "split" --> T2["Enrol(student_id, subject, professor)<br/>PK (student_id, subject)"]
```

A non-prime attribute must depend on the **whole** PK, never on a part of it.

## 8. 3NF: no transitive dependency

In Student, student_id finds branch, and branch finds hod. A non-prime column finds another non-prime column.

```mermaid
flowchart LR
  subgraph BEFORE["Student, PK = student_id"]
    ID["student_id"] --> B["branch<br/>(non-prime)"] -- "transitive" --> H["hod<br/>(non-prime)"]
  end
  BEFORE -- "split" --> T1["Student(student_id, name, branch)"]
  BEFORE -- "split" --> T2["Branch(branch, hod)<br/>Dr X is stored once"]
```

All three anomalies are gone. IT can open without a student. Mohan can leave without deleting ME. The HOD changes in one row.

## 9. BCNF: every determinant is a super key

In Enrol, each professor teaches one subject, so `professor -> subject`. The professor is not a super key, yet it finds the prime attribute subject.

```mermaid
flowchart LR
  subgraph BEFORE["Enrol, PK = (student_id, subject)"]
    K["student_id + subject"] --> P["professor<br/>(non-prime)"]
    P -- "not a super key,<br/>finds a prime attribute" --> S["subject<br/>(prime)"]
  end
  BEFORE -- "split" --> T1["Professor(professor, subject)<br/>PJ: Java, PC: C++, PJ2: Java"]
  BEFORE -- "split" --> T2["Enrol(student_id, professor)"]
```

BCNF is a stronger 3NF. For every `A -> B`, A must be a super key.

## 10. The final tables

The one messy table became four clean tables. Each has one job.

```mermaid
erDiagram
  BRANCH ||--o{ STUDENT : "has"
  STUDENT ||--o{ ENROL : "takes"
  PROFESSOR ||--o{ ENROL : "teaches"
  BRANCH {
    string branch PK
    string hod
  }
  STUDENT {
    int student_id PK
    string name
    string branch FK
  }
  ENROL {
    int student_id PK,FK
    string professor PK,FK
  }
  PROFESSOR {
    string professor PK
    string subject
  }
```

## 11. Normal forms at a glance

For an FD `X -> Y`, each form forbids one pattern.

| Form | It forbids | Fix in the story |
|---|---|---|
| 1NF | It forbids a multi-valued cell. | We gave each subject its own row. |
| 2NF | It forbids Y depending on part of the PK. | We split name out of Enrol. |
| 3NF | It forbids a non-prime X finding a non-prime Y. | We split hod into Branch. |
| BCNF | It forbids an X that is not a super key. | We split subject into Professor. |

| Advantage | Why |
|---|---|
| Less redundancy | Each fact is stored once. |
| Consistency | Each fact changes in one place only. |
| No anomalies | Insert, delete and update behave safely. |
| Space and speed | The DB is smaller and queries run faster. |
