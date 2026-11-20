# Lecture 2: Inheritance

1. **What is inheritance?**
   1. Inheritance is a mechanism in which one class acquires all the properties (data) and behaviours (functions) of a parent class.
   2. It represents an **IS-A** relationship: an Employee is a Person, a SoftwareEngineer is an Employee.
   3. Why we need it: without inheritance, every class repeats the members of the classes above it.

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

      1. Without inheritance, `SoftwareEngineer` would have to declare all 13 members itself, and so would every other kind of employee. A change to `Person` would have to be copied everywhere.
2. **Terminology**
   1. The class being inherited from is the **base class** (also parent or superclass). Here, `Person`.
   2. The class that inherits is the **derived class** (also child or subclass). Here, `Employee`.

   ```mermaid
   classDiagram
       Person <|-- Employee
       Employee <|-- SoftwareEngineer
   ```

3. **Order of construction and destruction**
   1. A derived object contains a base part inside it. The base part must exist before the derived part can be built on top of it.
   2. So the **most base class is constructed first**, and the **most derived class is destructed first**. Destruction is the exact mirror image of construction.
      1. Chain Base1, Base2, Derived: constructors run Base1, Base2, Derived. Destructors run Derived, Base2, Base1.

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
   1. **Public**: can be accessed by anybody.
   2. **Private**: can be accessed only by the class's own members. Not even derived classes can see it.
   3. **Protected**: can be accessed by the class's own members and by derived classes, but not from outside.
5. **Three kinds of inheritance**
   1. The keyword in `class B : public A` controls how A's members appear inside B, and to anyone using B.
   2. A's private members are never accessible in B, whichever kind is used. They still exist inside the object. A's own public functions can still use them.

   | A's member | `class B : public A` | `class B : protected A` | `class B : private A` |
   |---|---|---|---|
   | public | public in B | protected in B | private in B |
   | protected | protected in B | protected in B | private in B |
   | private | not accessible | not accessible | not accessible |

   3. So for `B b;` in `main()`:
      1. With public inheritance, `b.a_public_` works. `b.a_protected_` and `b.a_private_` don't compile.
      2. With private or protected inheritance, none of the three compile from `main()`. Inside B's own functions, `a_public_` and `a_protected_` are still accessible.
   4. **Public inheritance is the one used in practice.** It is the only one that models IS-A. The other two exist mostly for theory.
6. **Best practice: construct the base from the derived constructor**
   1. From the constructor of the derived class, call the constructor of the base class in the initializer list.
   2. Each constructor takes care of initializing its own class's members. The derived class doesn't touch the base's members directly, and it can't if they are private.

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
   2. Say B declares its own `int a_public_;` and sets it from a fourth parameter: `B(int a, int b, int c, int d) : A(a, b, c), a_public_(d) {}`. Then inside B, `a_public_` means B's copy:

      ```cpp
      void PrintB() {
          PrintA();                      // prints A's members: 1 2 3
          cout << a_public_ << endl;     // prints B's own a_public_: 4
      }
      ```

      1. A's copy is still there and can be reached as `A::a_public_`.
   3. The same rule applies to function calls. Say the base has `A()`, `B()`, `C()` and the derived class has `A()`, `D()`, `E()`. For `Derived D;`:
      1. `D.D()` is found in Derived.
      2. `D.B()` is not in Derived, so lookup moves up and finds it in Base.
      3. `D.A()` exists in both. The search starts from the most derived class and stops at the first match, so Derived's `A()` runs.
8. Next: we can call Derived's functions on a Derived object. But code that only knows "this is some Person" has a Base pointer or reference. Which function runs then is the question polymorphism answers.
