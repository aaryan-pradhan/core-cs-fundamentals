# Lecture 1: Classes, Objects, Constructors and Destructors

1. **What is LLD?**
   1. Low Level Design is the component-level design process. High Level Design decides which big boxes (services, databases, queues) exist. LLD decides what goes inside one box.
   2. It gives the internal logic of the software being built.
   3. It defines the class diagram: the classes, their attributes and methods, and the relationships between them.
   4. The foundation of LLD is **OOP (Object-Oriented Programming)**. So the course first builds OOP, then design principles (SOLID), then design patterns, then real interview problems.
2. **What is OOP?**
   1. Object-Oriented Programming is a way of writing software around **classes** and **objects**.
   2. It rests on four pillars. Each one gets its own place in these notes:
      1. **Encapsulation**: keep data and the functions that work on it together, and hide the internals (this lecture).
      2. **Inheritance**: a class reuses another class's members, an IS-A relationship (lecture 2).
      3. **Polymorphism**: one call, many forms, decided at runtime (lecture 3).
      4. **Abstraction**: expose only what something does, not how it does it (lecture 3, abstract and interface classes).
3. **Classes and objects**
   1. `int a;` declares a variable of a built-in (primitive) type. The compiler already knows `int` is a 32-bit integer.
   2. A class lets us define our own type. It is custom defined, a **non-primitive data type**.

      ```cpp
      class Person {
      public:
          int age;
          string name;
          string address;
      };

      int main() {
          int a;
          Person p1, p2;   // p1 and p2 are objects of type Person
          return 0;
      }
      ```

   3. **Difference between class and object**
      1. A class is a template (blueprint) for creating objects. It does not occupy memory until an object is created.
      2. An object is a tangible entity created from the class's blueprint. Each object has its own copy of the data members.
   4. **Class vs structure**
      1. In a `class`, members are private by default. We mark them public or private separately.
      2. In a `struct`, members are public by default.
      3. That default is the only real difference in C++. By convention, `struct` is used for plain data and `class` for types with behaviour.
4. **Public and private members**
   1. Class members are accessed with the `.` operator on an object, and with `->` on a pointer to an object.

      ```cpp
      Person p1;            // object
      p1.SetName("abc");
      Person *p2 = &p1;     // pointer to an object
      p2->SetName("def");   // same as (*p2).SetName("def")
      ```

   2. **Public** members can be accessed from anywhere in the program with the `.` operator.
   3. **Private** members cannot be accessed outside the class. Only the class's own member functions can touch them.

      ```cpp
      class Person {
      public:
          string GetName() { return name_; }
          void SetName(string name) { name_ = name; }   // private members can be accessed here
      private:
          int age_;
          string name_;
          string address_;
      };

      int main() {
          Person p1;
          p1.SetName("abc");
          cout << p1.GetName();
          p1.age_ = 25;   // won't compile: age_ is private
      }
      ```

   4. **Getter and setter pattern**: keep the data private and expose small public functions to read it (`GetAge`) and write it (`SetAge`). The class stays in control of its own data. A setter can, for example, reject a negative age.
5. **Encapsulation**
   1. Encapsulation is the integration of data and the operations on that data into one class.
   2. It also means hiding the functional details from whoever calls the object.
   3. Example: a car exposes the clutch, brake and accelerator to the driver and hides the engine.

      ```cpp
      class Car {
      public:          // exposed to the user
          void Clutch();
          void Brake();
          void Accelerate();
      private:         // hidden from the user
          Engine engine_;
      };
      ```

   4. Public and private members are how C++ implements encapsulation.
6. **Naming conventions** (Google C++ style, used throughout these notes)
   1. Class names start with a capital letter: `Person`, `TextEditor`.
   2. The three common styles:
      1. `push_back()`: snake_case
      2. `PushBack()`: PascalCase, used here for functions
      3. `pushBack()`: camelCase
   3. Private data members end with an underscore: `int age_;`. This separates members from parameters with the same name (`age_ = age;`).
7. **Constructors**
   1. A constructor is a special member function that is called automatically when an object is created. It sets up the object's initial state.
   2. Naming rules:
      1. A constructor must have the same name as the class, with the same capitalization.
      2. A constructor has no return type, not even `void`.
   3. A constructor is normally public. If it is private, code outside the class cannot create an object. (Lecture 8, Singleton, makes the constructor private on purpose.)
   4. Constructors can take parameters, and parameters can have default values.

      ```cpp
      #include <iostream>
      #include <string>
      using namespace std;

      class Person {
      public:
          Person(int age, string name, string add = "delhi") {
              cout << "Person cons. called" << endl;
              age_ = age;
              name_ = name;
              add_ = add;
          }
          void SetAge(int age) { age_ = age; }
          int GetAge() { return age_; }
          string GetName() { return name_; }
      private:
          int age_;
          string name_;
          string add_;
      };

      int main() {
          Person p2(25, "def", "mumbai");
          cout << p2.GetAge() << " " << p2.GetName() << endl;   // 25 def
      }
      ```

8. **Destructors**
   1. A destructor is a special member function that is called automatically when an object is destroyed.
   2. Its job is cleanup before the object goes away: free memory, close files, release locks.
   3. Naming rules:
      1. Same name as the class, preceded by a tilde (`~`).
      2. It takes no arguments, so a class has exactly one destructor.
      3. It has no return type.
   4. If we don't write one, the compiler gives a default destructor, equivalent to `~A() {}`. It is called when the object is destroyed, but it does no cleanup of its own. For example, it will not `delete` memory the class allocated with `new`.

      ```cpp
      #include <iostream>
      using namespace std;

      class A {
      public:
          A(int a) : a_(a) { cout << "cons is called" << endl; }
          ~A() { cout << "Des is called" << endl; }
          int GetA() { return a_; }
      private:
          int a_;
      };

      int main() {
          A obj(3);
          cout << obj.GetA() << endl;
      }
      // Output:
      // cons is called
      // 3
      // Des is called
      ```

9. **When constructors and destructors run: scope**
   1. A local object lives until the closing brace `}` of the scope it was created in. At that brace its destructor runs.
   2. A function body is a scope:

      ```cpp
      void dummy() {
          A obj(3);    // Const. A is called
      }                // Des. A is called (dummy's scope ends)

      int main() {
          dummy();
          B obj(5);    // Const. B is called
          return 0;    // Des. B is called
      }
      ```

   3. A bare pair of braces is also a scope. This gives the same sequence (Con. A, Des. A, Con. B, Des. B), because everything defined inside the braces is destroyed when we leave them.

      ```cpp
      int main() {
          {
              A obj1(3);
          }
          B obj(5);
          return 0;
      }
      ```

   4. Objects in the **same** scope are destroyed in reverse order of creation, like a stack (last in, first out).

      ```cpp
      int main() {
          A obj1(3);
          B obj2(5);
          return 0;
      }
      // Const. A, Const. B, Dest. B, Dest. A
      ```

10. **Constructor member initializer list**
    1. The usual way for a constructor to set members is a member initializer list, written after a `:`.

       ```cpp
       class A {
       public:
           A(int a, int b) : a_(a), b_(b) {}
       private:
           int a_;
           int b_;
       };
       ```

    2. Members are initialized directly with the values, instead of being created first and assigned later in the body. For `const` members and reference members, this is the only option.
    3. Members are always initialized in the order they are **declared in the class**, not the order written in the list. Here `a_` is still initialized first:

       ```cpp
       A(int a, int b) : b_(b), a_(a) {}   // a_ first, then b_ (declaration order)
       ```

       1. This matters when one member is initialized from another. If `b_` were initialized from `a_`, `a_` must be declared first.
       2. Rule: write the list in the same order as the declarations. Compilers warn (`-Wreorder`) if you don't.
    4. The constructor body runs **after** the initializer list. So the body is usually empty, and holds any extra setup work that is needed.
    5. Brace initialization `A obj{4, 5};` passes the values straight to the constructor. It also works for many members: `A obj{a, b, c, d, e};`.
11. **Stack vs heap objects, and memory leaks**
    1. `A obj(3);` creates the object on the **stack**. It is destroyed automatically at the end of its scope.
    2. `new` creates the object on the **heap** and returns a pointer to it. It lives until someone calls `delete`.

       ```cpp
       A* ptr = new A(3, 4);   // allocated on heap
       delete ptr;             // destructor runs and memory is freed
       ```

    3. If we forget `delete`, only the pointer variable `ptr` (on the stack) is destroyed when the scope ends. The heap object stays allocated, but nothing points to it any more. That is a **memory leak**.
    4. C++ has no garbage collector, so raw pointers can cause memory leaks. Modern C++ uses smart pointers (`std::unique_ptr`, `std::shared_ptr`), which call `delete` automatically. Rust takes this further and enforces memory safety at compile time.
12. Next: classes rarely stand alone. Many classes share common data, so a `Person` and an `Employee` both have a name and an age. Inheritance lets one class build on another instead of repeating those members.
