# Lecture 5: UML Class Diagrams

1. **What is a class diagram?**
   1. A class diagram shows the classes of a system before you code them.
   2. It is a **static** picture of the structure. It shows which classes exist, what each holds, and how they relate. It does not show the order in which things happen.

   > **Interview:** In an LLD interview, the class diagram is the main deliverable (lecture 11). Code comes after it.

2. **A class box** has three sections: name, attributes (data), and methods (functions).

   ```mermaid
   classDiagram
       class Person {
           -Heart heart_
           #int age_
           -vector~Home*~ homes_
           +AddHome(Home* home) void
           +GetAge() int
       }
   ```

   1. **Attribute format:** `visibility name : type`.
   2. **Method format:** `visibility name(params) : return type`.
   3. **Visibility symbols:**

      | Symbol | Meaning |
      |--------|---------|
      | `+` | public |
      | `-` | private |
      | `#` | protected |
3. **Arrows: the six relationships**

   | Relationship | Meaning | Drawn as | Example |
   |--------------|---------|----------|---------|
   | **Inheritance** | IS-A | Solid line, hollow triangle pointing at the base class | "Employee inherited from Person." |
   | **Composition** | Part of | Solid line, **filled** diamond at the whole (the owner) | Person ◆— Heart |
   | **Aggregation** | Has a | Solid line, **hollow** diamond at the whole | Person ◇— Home address |
   | **Association** | Uses a | Plain solid line, with an optional arrowhead for direction | Doctor — Patient |
   | **Realization / implementation** | Implements an interface | **Dashed** line, hollow triangle pointing at the interface | "B is an implementation of A." |
   | **Dependency** | Uses briefly | Dashed line with an open arrow | A factory depends on the products it creates. |

   - **Dependency:** A uses B briefly. For example, B is a function parameter, or A creates B.

   ```mermaid
   classDiagram
       Person <|-- Employee : inheritance
       Person *-- Heart : composition
       Person *-- Kidney : composition
       Person o-- Address : aggregation
       Doctor --> Patient : association
       class Shape {
           <<interface>>
           +Draw() void
       }
       Shape <|.. Circle : realization
       ShapeFactory ..> Circle : dependency
   ```

   - **Memory trick:** The diamond always sits at the "whole" end.
   - **Filled diamond:** The whole owns the part's life.
   - **Hollow diamond:** The whole does not own the part's life.
4. **Interfaces and abstract classes**
   1. **Interface:** Mark it with the stereotype `<<interface>>` above its name. All of its methods are pure virtual.
   2. **Abstract class:** Mark it with `<<abstract>>`, or write its name in italics.
   3. **Implementing:** Concrete classes implement an interface with the realization arrow (dashed line, hollow triangle).
   4. **Enums:** Mark them `<<enum>>` and list their values. See `GameStatus` in Tic-Tac-Toe (lecture 12).
5. **Multiplicity** is optional. Use it in bigger designs. Write it at the ends of a line.

   | Symbol | Meaning |
   |--------|---------|
   | `1` | exactly one |
   | `0..1` | zero or one |
   | `*` | many |
   | `1..*` | at least one |

   - **Example:** One `ParkingFloor` has many (`*`) `ParkingSpot`s.
6. **How to draw one**
   1. List the nouns in the problem. They become the classes.
   2. For each class, write what it knows (attributes) and what it does (methods).
   3. For each pair of classes, ask four questions:
      - **Inheritance:** Does one IS-A the other?
      - **Composition:** Is one part of the other, and does it die with it?
      - **Aggregation:** Does one have the other, and the part lives on?
      - **Association:** Do they just use each other?
   4. Put an interface above several classes that do the same job differently.
7. **Next:** We can now model and draw classes. The next question is how to split responsibilities so the design survives change. The SOLID principles answer that.
