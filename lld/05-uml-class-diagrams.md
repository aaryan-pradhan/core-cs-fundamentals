# Lecture 5: UML Class Diagrams

1. **What is a class diagram?**
   1. Class diagrams are a neat way of visualizing the classes in a system before actually coding them up.
   2. They are a **static** picture of the system's structure: which classes exist, what each holds, and how they relate. They don't show the order things happen in.
   3. In an LLD interview, the class diagram is the main deliverable (lecture 11). Code comes after it.
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

   1. Attribute format: `visibility name : type`. Method format: `visibility name(params) : return type`.
   2. **Visibility symbols**:
      1. `+` public
      2. `-` private
      3. `#` protected
3. **Arrows: the six relationships**
   1. **Inheritance** (IS-A): solid line, hollow triangle pointing at the base class. "Employee inherited from Person."
   2. **Composition** (part of): solid line, **filled** diamond at the whole (the owner). Person ◆— Heart.
   3. **Aggregation** (has a): solid line, **hollow** diamond at the whole. Person ◇— Home address.
   4. **Association** (uses a): plain solid line, with an optional arrowhead for direction. Doctor — Patient.
   5. **Realization / implementation**: **dashed** line, hollow triangle pointing at the interface. "B is an implementation of A."
   6. **Dependency**: dashed line with an open arrow. A uses B briefly, for example as a function parameter or by creating it. A factory depends on the products it creates.

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

   7. Memory trick: the diamond always sits at the "whole" end. Filled means the whole owns the part's life, hollow means it doesn't.
4. **Interfaces and abstract classes**
   1. Mark an interface with the stereotype `<<interface>>` above its name. All of its methods are pure virtual.
   2. Mark an abstract class with `<<abstract>>`, or write its name in italics.
   3. Concrete classes implement an interface with the realization arrow (dashed line, hollow triangle).
   4. Enums are marked `<<enum>>` and list their values (see `GameStatus` in Tic-Tac-Toe, lecture 12).
5. **Multiplicity** (optional, used in bigger designs): written at the ends of a line. `1` means exactly one, `0..1` means zero or one, `*` means many, and `1..*` means at least one. Example: one `ParkingFloor` has many (`*`) `ParkingSpot`s.
6. **How to draw one**
   1. List the nouns in the problem. They become the classes.
   2. For each class, write what it knows (attributes) and what it does (methods).
   3. For each pair of classes, ask: does one IS-A the other (inheritance)? Is one part of the other and dies with it (composition)? Does one have the other, but it lives on (aggregation)? Or do they just use each other (association)?
   4. Wherever several classes do the same job differently, put an interface above them.
7. Next: we can now model and draw classes. The next question is how to split responsibilities so the design survives change. The SOLID principles answer that.
