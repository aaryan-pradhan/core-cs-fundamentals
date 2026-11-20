# Lecture 4: Extended ER Features

1. **Basic ER Features** studied in the **LEC-3**, can be used to model most DB features but when complexity increases, it is better to use some Extended ER features to model the DB Schema.
    1. In a big system there are many entities, many relations and many attributes of different types (multi-valued, composite); basic ER features alone may not give a refined DB.
    2. Extended ER features were not part of the original ER model; they were added as the need was felt, because modern systems use inheritance heavily.
2. **Specialisation**
    1. In ER model, we may require to subgroup an entity set into other entity sets that are distinct in some way with other entity sets.
        1. Example of the problem: entity `Person` with name, address, contact, plus salary (for employee), profile picture and customer id (for customer). Person now carries attributes that don't apply to every person, which adds redundancy.
        2. Fix: break Person into new entity sets `Customer` and `Employee`; move customer id and profile picture to Customer, salary (and e.g. job role) to Employee. Each entity now has its own identity and own attributes.
        3. New problem: Customer and Employee both still need name, address, contact. Copying them into both entity sets repeats them (redundancy).
        4. ER model's solution is Specialisation: a way to relate the broken-down entity sets back to the original with a relationship.
    2. **Specialisation** is **splitting** up the entity set into further **sub entity sets** on the basis of their **functionalities**, **specialities** and **features**.
    3. It is a **Top-Down** approach.
        1. Start thinking at a higher, abstract level (Person), then keep breaking it down.
    4. e.g., **Person** entity set can be divided into **customer**, **student**, **employee**. Person is **superclass** and other specialised entity sets are **subclasses**.
        1. We have **"is-a"** relationship between superclass and subclass.
            1. Customer is-a Person, Employee is-a Person.
            2. Same terminology as inheritance in OOP: parent class and child classes; child entities inherit the attributes (name, address) of the parent.
        2. Depicted by **triangle** component.

            ```
                 Person
                   |
                   ▽  (is-a)
              _____|_____
             |           |
          Customer    Employee
            ```

        3. Specialisation can be applied again on a subclass.
            1. Employee can be specialised into HR Manager, Developer, Housekeeping Employee (each is-a Employee).
            2. Each has the Employee attributes plus its own, e.g. HR: working hours; Developer: tech stack they work in; Housekeeping: building number / block where they work.
            3. Applying specialisation again and again keeps the ER model simple, instead of putting all attributes into Person.
        4. More examples
            1. Engineer entity set specialised into Civil Engineer, CS Engineer, Chemical Engineer, each with its own attributes.
            2. Vehicle specialised into Car, SUV, Bus (each is-a Vehicle); each has its own distinctive properties plus the common properties given by Vehicle.
    5. **Why** Specialisation?
        1. Certain attributes may only be applicable to a few entities of the parent entity set.
            1. Example: salary should not be an attribute of a customer; without splitting, overlapping attributes would be given to every entity set, causing redundancy.
        2. DB designer can show the distinctive features of the sub entities.
            1. Employee and Customer are both persons but have different features; they become independent entity sets.
        3. To group such entities we apply Specialisation, to overall **refine** the DB blueprint.
        4. How to think: think top to bottom; look for redundant attributes on an entity and check if it can be specialised into separate entities.
3. **Generalisation**
    1. It is just a **reverse** of Specialisation.
        1. Specialisation goes top to bottom; Generalisation goes bottom to top.
    2. DB Designer, may encounter certain properties of two entities are overlapping. Designer may consider to make a new generalised entity set. That generalised entity set will be a super class.
        1. Example: designer first creates Car, SUV and Bus as separate entities and finds their attributes. Vehicle does not exist yet.
        2. Car, SUV and Bus share two properties (e.g. mileage, vehicle type such as BS6 engine yes/no).
        3. Designer generalises: creates super entity Vehicle, deletes the common attributes from the three entities and puts them in Vehicle.
    3. **"is-a"** relationship is present between subclass and super class.
    4. e.g., **Car**, **Jeep** and **Bus** all have some common attributes, to avoid data repetition for the common attributes. DB designer may consider to Generalise to a new entity set "**Vehicle**".
    5. It is a **Bottom-up** approach.
    6. **Why** Generalisation?
        1. Makes DB more **refined** and **simpler**.
        2. Common attributes are not **repeated**.
    7. Specialisation and Generalisation are the same thing in the ER model.
        1. The ER diagram looks identical for both; both use the is-a relationship.
        2. The only difference is the way of thinking: top-down (specialisation) or bottom-up (generalisation).
        3. Classic example both ways: think Customer and Employee first, both with address and name, then generalise into Person (bottom-up); or think Person first, then split (top-down). The final diagram is the same.
4. **Attribute Inheritance**
    1. **Both** Specialisation and Generalisation, has attribute inheritance.
    2. The attributes of higher level entity sets are inherited by lower level entity sets.
    3. E.g., **Customer & Employee** inherit the attributes of **Person**.
    4. Without attribute inheritance there is no benefit of generalising or specialising: if Customer and Employee did not inherit the common attributes moved up to Person, the move would be pointless.
5. **Participation Inheritance**
    1. If a parent entity set participates in a relationship then its child entity sets will also participate in that relationship.
    2. Example: Person and Vehicle have a relationship "has". It is applied on Person, so it automatically applies to Customer and Employee as well.
6. **Aggregation**
    1. **How to show relationships among relationships?** - Aggregation is the technique.
        1. Problem in basic ER: take the ternary relationship from LEC-3, Employee works on Branch with Job.
        2. Requirement: a Manager manages the combination of Employee, Branch and Job (e.g. Rahul, housekeeping job, Dwarka Delhi branch), not an employee or branch or job individually.
        3. Without aggregation: add a new relationship "manages" connecting Manager to Employee, Branch and Job, a quaternary relationship.
        4. That is redundant and wrong: it says the manager manages the branch, manages the job and manages the employee separately, while the requirement is only the combination of the three.
    2. **Abstraction** is applied to treat relationships as higher-level entities. We can call it Abstract entity.
        1. Abstraction hides the underlying complexity and acts like a black box.
        2. Treat the relationship "works on" (Employee, Branch, Job) as one entity, named after the relationship (the "works on" entity), hiding Employee, Branch and Job inside it.
        3. Draw the relationship "manages" between Manager and this aggregated entity.
        4. Now the ER diagram shows that a manager manages the combination of the three, and nobody manages any of them individually.
    3. **Avoid redundancy** by aggregating relationship as an entity set itself.
        1. Example 2: Student attends Semester. Requirement: a "has" relationship with Subject on the aggregated unit of Student and Semester.
        2. Aggregate "Student attends Semester" into a higher-level unit and relate it with Subject through "has".
        3. Not directly Student has Subject, since a student may not be enrolled yet and so have no subjects.
        4. Not directly Semester has Subject either; only the subjects a student has taken in the semester attended are wanted.
