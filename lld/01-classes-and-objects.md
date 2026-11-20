# Lecture 1: Classes, Objects, Constructors and Destructors

1. **What is LLD?**
   1. **Low Level Design** is the component-level design process.
      - **HLD:** High Level Design decides which big boxes (services, databases, queues) exist.
      - **LLD:** Low Level Design decides what goes inside one box.
   2. It gives the internal logic of the software being built.
   3. It defines the class diagram. The diagram shows the classes, their attributes and methods, and the relationships between them.
   4. The foundation of LLD is **OOP (Object-Oriented Programming)**.
      - **Course order:** OOP first, then design principles (SOLID), then design patterns, then real interview problems.
2. **What is OOP?**
   1. Object-Oriented Programming is a way of writing software around **classes** and **objects**.
   2. It rests on four pillars.

      | Pillar | Meaning | Covered in |
      |--------|---------|------------|
      | **Encapsulation** | Keep data and the functions that work on it together. Hide the internals. | Lecture 1 |
      | **Inheritance** | A class reuses another class's members. This is an IS-A relationship. | Lecture 2 |
      | **Polymorphism** | One call, many forms. The form is decided at runtime. | Lecture 3 |
      | **Abstraction** | Expose only what something does, not how it does it. | Lecture 3 (abstract and interface classes) |

3. **Classes and objects**
   1. `int a;` declares a variable of a built-in (primitive) type. The compiler already knows `int` is a 32-bit integer.
   2. A class lets us define our own type. It is custom defined, so it is a **non-primitive data type**.

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

      | | Class | Object |
      |---|-------|--------|
      | **What it is** | A template (blueprint) for creating objects. | A tangible entity created from the class's blueprint. |
      | **Memory** | Takes no memory until an object is created. | Has its own copy of the data members. |

   4. **Class vs structure**

      | | `class` | `struct` |
      |---|---------|----------|
      | **Default access** | Private. We mark members public or private separately. | Public. |

      - **Only difference:** The default access is the only real difference in C++.
      - **Convention:** `struct` is for plain data. `class` is for types with behaviour.
4. **Public and private members**
   1. We access class members with the `.` operator on an object. We use `->` on a pointer to an object.

      ```cpp
      Person p1;            // object
      p1.SetName("abc");
      Person *p2 = &p1;     // pointer to an object
      p2->SetName("def");   // same as (*p2).SetName("def")
      ```

   2. **Public:** Any code in the program can access these members with the `.` operator.
   3. **Private:** Code outside the class cannot access these members. Only the class's own member functions can touch them.

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

   4. **Getter and setter pattern:** Keep the data private. Expose small public functions to read it (`GetAge`) and write it (`SetAge`).
      - **Why:** The class stays in control of its own data.
      - **Example:** A setter can reject a negative age.
5. **Encapsulation**
   1. Encapsulation puts data and the operations on that data into one class.
   2. It also hides the functional details from whoever calls the object.
   3. **Example:** A car exposes the clutch, brake and accelerator to the driver. It hides the engine.

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

   4. C++ implements encapsulation with public and private members.
6. **Naming conventions** (Google C++ style, used throughout these notes)
   1. **Classes:** Names start with a capital letter, such as `Person` and `TextEditor`.
   2. **Functions:** There are three common styles.

      | Style | Example | Note |
      |-------|---------|------|
      | snake_case | `push_back()` | |
      | PascalCase | `PushBack()` | Used here for functions |
      | camelCase | `pushBack()` | |

   3. **Private data members:** Names end with an underscore, such as `int age_;`. This separates a member from a parameter with the same name (`age_ = age;`).
7. **Constructors**
   1. A constructor is a special member function. It is called automatically when an object is created. It sets up the object's initial state.
   2. Naming rules:
      1. A constructor must have the same name as the class, with the same capitalization.
      2. A constructor has no return type, not even `void`.
   3. **Access:** A constructor is normally public. If it is private, code outside the class cannot create an object. (Lecture 8, Singleton, makes the constructor private on purpose.)
   4. **Parameters:** Constructors can take parameters. Parameters can have default values.

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
   1. A destructor is a special member function. It is called automatically when an object is destroyed.
   2. Its job is cleanup before the object goes away. It frees memory, closes files and releases locks.
   3. Naming rules:
      1. Same name as the class, preceded by a tilde (`~`).
      2. It takes no arguments, so a class has exactly one destructor.
      3. It has no return type.
   4. **Default destructor:** If we do not write one, the compiler gives us one. It is equivalent to `~A() {}`.
      - It is called when the object is destroyed.
      - It does no cleanup of its own. For example, it will not `delete` memory the class allocated with `new`.

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
   1. A local object lives until the closing brace `}` of the scope it was created in. Its destructor runs at that brace.
   2. A function body is a scope.

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

   3. A bare pair of braces is also a scope. The sequence is the same (Con. A, Des. A, Con. B, Des. B). Everything defined inside the braces is destroyed when we leave them.

      ```cpp
      int main() {
          {
              A obj1(3);
          }
          B obj(5);
          return 0;
      }
      ```

   4. Objects in the **same** scope are destroyed in reverse order of creation. This works like a stack (last in, first out).

      ```cpp
      int main() {
          A obj1(3);
          B obj2(5);
          return 0;
      }
      // Const. A, Const. B, Dest. B, Dest. A
      ```

10. **Constructor member initializer list**
    1. The usual way for a constructor to set members is a member initializer list. It is written after a `:`.

       ```cpp
       class A {
       public:
           A(int a, int b) : a_(a), b_(b) {}
       private:
           int a_;
           int b_;
       };
       ```

    2. **Direct initialization:** Members get their values directly. They are not created first and assigned later in the body. For `const` members and reference members, this is the only option.
    3. **Order:** Members are always initialized in the order they are **declared in the class**. The order written in the list does not matter. Here `a_` is still initialized first.

       ```cpp
       A(int a, int b) : b_(b), a_(a) {}   // a_ first, then b_ (declaration order)
       ```

       1. This matters when one member is initialized from another. If `b_` is initialized from `a_`, then `a_` must be declared first.
       2. **Rule:** Write the list in the same order as the declarations. Compilers warn (`-Wreorder`) if you do not.
    4. **Body:** The constructor body runs **after** the initializer list. So the body is usually empty. It holds any extra setup work that is needed.
    5. **Brace initialization:** `A obj{4, 5};` passes the values straight to the constructor. It also works for many members, such as `A obj{a, b, c, d, e};`.
11. **Stack vs heap objects, and memory leaks**
    1. **Stack:** `A obj(3);` creates the object on the stack. It is destroyed automatically at the end of its scope.
    2. **Heap:** `new` creates the object on the heap and returns a pointer to it. It lives until someone calls `delete`.

       ```cpp
       A* ptr = new A(3, 4);   // allocated on heap
       delete ptr;             // destructor runs and memory is freed
       ```

    3. **Memory leak:** Suppose we forget `delete`. When the scope ends, only the pointer variable `ptr` (on the stack) is destroyed. The heap object stays allocated, but nothing points to it any more.
    4. **No garbage collector:** C++ has none, so raw pointers can cause memory leaks.
       - **Smart pointers:** Modern C++ uses `std::unique_ptr` and `std::shared_ptr`. They call `delete` automatically.
       - **Rust:** It goes further and enforces memory safety at compile time.
12. **Why inheritance comes next:** Classes rarely stand alone. Many classes share common data. A `Person` and an `Employee` both have a name and an age. Inheritance lets one class build on another instead of repeating those members.
