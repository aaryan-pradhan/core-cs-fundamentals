# Lecture 2: Inheritance

1. **What is inheritance?**
   1. Inheritance is a mechanism where one class acquires all the properties (data) and behaviours (functions) of a parent class.
   2. It represents an **IS-A** relationship. An Employee is a Person. A SoftwareEngineer is an Employee.
   3. **Why we need it:** Without inheritance, every class repeats the members of the classes above it.

      ```cpp
      class Person {
      public:
          int age;
          string name;
          string address;
          string mobile_no;
          string aadhaar_no;
      };

      class Employee : public Person {      // gets all of Person's members
      public:
          string job_role;
          string company;
          int salary;
          int id;
      };

      class SoftwareEngineer : public Employee {   // gets Person's and Employee's members
      public:
          string team;
          string tech_stack;
          string language_expertise;
          int level;
      };
      ```

      1. Without inheritance, `SoftwareEngineer` would declare all 13 members itself. So would every other kind of employee.
      2. A change to `Person` would have to be copied everywhere.
2. **Terminology**
   1. **Base class:** The class being inherited from. It is also called parent or superclass. Here it is `Person`.
   2. **Derived class:** The class that inherits. It is also called child or subclass. Here it is `Employee`.

   ```mermaid
   classDiagram
       Person <|-- Employee
       Employee <|-- SoftwareEngineer
   ```

3. **Order of construction and destruction**
   1. A derived object contains a base part inside it. The base part must exist before the derived part is built on top of it.
   2. So the **most base class is constructed first**. The **most derived class is destructed first**. Destruction is the exact mirror image of construction.
      1. **Example:** For the chain Base1, Base2, Derived, constructors run Base1, Base2, Derived. Destructors run Derived, Base2, Base1.

      ```cpp
      #include <iostream>
      using namespace std;

      class A {
      public:
          A() { cout << "consA" << endl; }
          ~A() { cout << "desA" << endl; }
      };

      class B : public A {
      public:
          B() { cout << "consB" << endl; }
          ~B() { cout << "desB" << endl; }
      };

      int main() {
          B b;
      }
      // Output:
      // consA
      // consB
      // desB
      // desA
      ```

4. **Access specifiers**

   | Specifier | Who can access it |
   |-----------|-------------------|
   | **Public** | Anybody. |
   | **Private** | Only the class's own members. Not even derived classes can see it. |
   | **Protected** | The class's own members and derived classes. Not code outside. |

5. **Three kinds of inheritance**
   1. The keyword in `class B : public A` controls how A's members appear inside B, and to anyone using B.
   2. A's private members are never accessible in B, whichever kind is used. They still exist inside the object. A's own public functions can still use them.

   | A's member | `class B : public A` | `class B : protected A` | `class B : private A` |
   |---|---|---|---|
   | public | public in B | protected in B | private in B |
   | protected | protected in B | protected in B | private in B |
   | private | not accessible | not accessible | not accessible |

   3. Take `B b;` in `main()`.
      1. **Public inheritance:** `b.a_public_` works. `b.a_protected_` and `b.a_private_` do not compile.
      2. **Private or protected inheritance:** None of the three compile from `main()`. Inside B's own functions, `a_public_` and `a_protected_` are still accessible.
   4. **Public inheritance is the one used in practice.** It is the only one that models IS-A. The other two exist mostly for theory.
6. **Best practice: construct the base from the derived constructor**
   1. In the derived constructor, call the base class constructor in the initializer list.
   2. Each constructor initializes its own class's members. The derived class does not touch the base's members directly. It cannot if they are private.

      ```cpp
      #include <iostream>
      using namespace std;

      class A {
      public:
          A(int a_public, int a_private, int a_protected)
              : a_public_(a_public), a_private_(a_private), a_protected_(a_protected) {
              cout << "cons A" << endl;
          }
          void PrintA() {
              cout << a_public_ << " " << a_private_ << " " << a_protected_ << endl;
          }
          int a_public_;
      private:
          int a_private_;
      protected:
          int a_protected_;
      };

      class B : public A {
      public:
          B(int a, int b, int c) : A(a, b, c) {   // base constructor called first
              cout << "cons B" << endl;
          }
          void PrintB() {
              PrintA();   // a_private_ is not accessible in B, so ask A to print it
          }
      };

      int main() {
          B b(1, 2, 3);
          b.PrintB();
      }
      // Output:
      // cons A
      // cons B
      // 1 2 3
      ```

7. **Name hiding: the closest scope wins**
   1. If the derived class declares a member with the same name as a base member, the derived one **hides** the base one inside the derived class.
   2. **Example:** B declares its own `int a_public_;` and sets it from a fourth parameter: `B(int a, int b, int c, int d) : A(a, b, c), a_public_(d) {}`. Inside B, `a_public_` now means B's copy.

      ```cpp
      void PrintB() {
          PrintA();                      // prints A's members: 1 2 3
          cout << a_public_ << endl;     // prints B's own a_public_: 4
      }
      ```

      1. A's copy is still there. It can be reached as `A::a_public_`.
   3. The same rule applies to function calls. Say the base has `A()`, `B()`, `C()` and the derived class has `A()`, `D()`, `E()`. Take `Derived D;`.
      1. `D.D()` is found in Derived.
      2. `D.B()` is not in Derived, so lookup moves up and finds it in Base.
      3. `D.A()` exists in both. The search starts from the most derived class and stops at the first match. So Derived's `A()` runs.
8. **Why polymorphism comes next:** We can call Derived's functions on a Derived object. But code that only knows "this is some Person" holds a Base pointer or reference. Which function runs then is the question polymorphism answers.
