# Lecture 4: Extended ER Features

1. **Basic ER Features** were studied in **LEC-3**. They can model most DB features. When complexity increases, it is better to use some Extended ER features to model the DB schema.
    1. **Big systems:** A big system has many entities, relations, and attributes of different types (multi-valued, composite). Basic ER alone may not give a refined DB.
    2. **Origin:** Extended ER features were not part of the original ER model. They were added as the need was felt, because modern systems use inheritance heavily.

2. **Specialisation**
    1. In the ER model, we may need to subgroup an entity set into other entity sets that are distinct in some way from other entity sets.
        1. **Problem:** The entity `Person` has name, address, contact, salary (for employee), profile picture and customer id (for customer). Some attributes do not apply to every person. This adds redundancy.
        2. **Fix:** Break Person into new entity sets `Customer` and `Employee`. Move customer id and profile picture to Customer. Move salary (and for example job role) to Employee. Each entity now has its own identity and its own attributes.
        3. **New problem:** Customer and Employee both still need name, address and contact. Copying them repeats them (redundancy).
        4. **ER solution:** Specialisation relates the broken-down entity sets back to the original with a relationship.
    2. **Specialisation** is **splitting** an entity set into further **sub entity sets**. The split is based on **functionalities**, **specialities** and **features**.
    3. It is a **Top-Down** approach.
        1. Start thinking at a higher, abstract level (Person). Then keep breaking it down.
    4. **Example:** The **Person** entity set can be divided into **customer**, **student** and **employee**. Person is the **superclass**. The other specialised entity sets are **subclasses**.
        1. There is an **"is-a"** relationship between superclass and subclass.
            1. Customer is-a Person. Employee is-a Person.
            2. **Same as OOP:** The terms match inheritance in OOP. There is a parent class and child classes. Child entities inherit the attributes (name, address) of the parent.
        2. It is depicted by a **triangle** component.

            ```
                 Person
                   |
                   ▽  (is-a)
              _____|_____
             |           |
          Customer    Employee
            ```

        3. Specialisation can be applied again on a subclass.
            1. Employee can be specialised into HR Manager, Developer and Housekeeping Employee (each is-a Employee).
            2. Each has the Employee attributes plus its own. HR has working hours. Developer has the tech stack. Housekeeping has the building number or block.
            3. Repeated specialisation keeps the ER model simple. You avoid putting all attributes into Person.
        4. **More examples:** Engineer splits into Civil Engineer, CS Engineer and Chemical Engineer, each with its own attributes. Vehicle splits into Car, SUV and Bus, each with its own properties plus the common ones from Vehicle.

    5. **Why** Specialisation?
        1. Certain attributes may apply only to a few entities of the parent entity set.
            1. **Example:** Salary should not be an attribute of a customer. Without splitting, overlapping attributes would be given to every entity set. This causes redundancy.
        2. The DB designer can show the distinctive features of the sub entities.
            3. Specialisation **refines** the overall DB blueprint.
        4. **How to think:** Think top to bottom. Look for redundant attributes on an entity. Check whether it can be specialised into separate entities.

3. **Generalisation**
    1. It is just the **reverse** of Specialisation.
        1. Specialisation goes top to bottom. Generalisation goes bottom to top.
    2. The DB designer may find that certain properties of two entities overlap. The designer may make a new generalised entity set. That generalised entity set will be a super class.
        1. **Example:** The designer first creates Car, SUV and Bus as separate entities and finds their attributes. Vehicle does not exist yet.
        2. Car, SUV and Bus share two properties. For example, mileage and vehicle type (such as BS6 engine yes or no).
        3. The designer generalises. The designer creates the super entity Vehicle, deletes the common attributes from the three entities, and puts them in Vehicle.
    3. An **"is-a"** relationship is present between subclass and super class.
    4. **Example:** **Car**, **Jeep** and **Bus** all have some common attributes. To avoid repeating the common attributes, the DB designer may generalise to a new entity set "**Vehicle**".
    5. It is a **Bottom-up** approach.
    6. **Why** Generalisation?
        1. It makes the DB more **refined** and **simpler**.
        2. Common attributes are not **repeated**.
    7. Specialisation and Generalisation are the same thing in the ER model.
        1. The ER diagram looks identical for both. Both use the is-a relationship.
        2. The only difference is the way of thinking: top-down (specialisation) or bottom-up (generalisation).
        3. **Classic example:** Customer and Employee first, then generalise into Person (bottom-up). Or Person first, then split (top-down). The final diagram is the same.

4. **Attribute Inheritance**
    1. **Both** Specialisation and Generalisation have attribute inheritance.
    2. Lower level entity sets inherit the attributes of higher level entity sets.
    3. **Example:** **Customer and Employee** inherit the attributes of **Person**.
    4. Without attribute inheritance, generalising or specialising has no benefit. The attributes moved up to Person would not reach Customer and Employee.

5. **Participation Inheritance**
    1. If a parent entity set participates in a relationship, its child entity sets also participate in that relationship.
    2. **Example:** Person and Vehicle have a relationship "has". It is applied on Person, so it automatically applies to Customer and Employee as well.

6. **Aggregation**
    1. **How to show relationships among relationships?** Aggregation is the technique.
        1. **Problem in basic ER:** Take the ternary relationship from LEC-3, Employee works on Branch with Job.
        2. **Requirement:** A Manager manages the combination of Employee, Branch and Job (for example Rahul, housekeeping job, Dwarka Delhi branch). The manager does not manage an employee, branch or job individually.
        3. **Without aggregation:** Add a new relationship "manages" connecting Manager to Employee, Branch and Job. This is a quaternary relationship.
        4. **Why it is wrong:** It is redundant. It says the manager manages the branch, the job and the employee separately.
    2. **Abstraction** is applied to treat relationships as higher-level entities. We can call this an abstract entity.
        1. Abstraction hides the underlying complexity and acts like a black box.
        2. Treat the relationship "works on" (Employee, Branch, Job) as one entity. Name it after the relationship (the "works on" entity). It hides Employee, Branch and Job inside it.
        3. Draw the relationship "manages" between Manager and this aggregated entity.
        4. Now the ER diagram shows that a manager manages the combination of the three. Nobody manages any of them individually.
    3. **Avoid redundancy** by aggregating a relationship as an entity set itself.
        1. **Example 2:** Student attends Semester. The requirement is a "has" relationship with Subject on the aggregated unit of Student and Semester.
        2. Aggregate "Student attends Semester" into a higher-level unit. Relate it with Subject through "has".
        3. **Not Student has Subject directly:** A student may not be enrolled yet, so would have no subjects.
        4. **Not Semester has Subject directly:** Only the subjects a student has taken in the semester attended are wanted.
