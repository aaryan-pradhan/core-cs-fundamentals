# Lecture 6: SOLID Principles

1. Software development principles are guidelines to follow while building software, so that it is easier to scale and maintain. The five SOLID principles were made popular by the software engineer Robert C. Martin ("Uncle Bob").
   1. **S**: Single Responsibility
   2. **O**: Open-Closed
   3. **L**: Liskov Substitution
   4. **I**: Interface Segregation
   5. **D**: Dependency Inversion
2. **S: Single Responsibility Principle**
   1. A class should have a single responsibility: it performs one particular job.
   2. Put another way, a class should have only **one reason to change**.
   3. So we segregate different responsibilities into different classes. Whenever we feel a class needs to perform two different tasks, we split it into two classes.
   4. Example: storing income data and calculating tax are two jobs, so they get two kinds of classes.

      ```cpp
      #include <iostream>
      using namespace std;

      class IndiaIncome {          // only job: hold India's income data
      public:
          IndiaIncome(double avg_income) : avg_income_(avg_income) {}
          double GetAvgIncome() const { return avg_income_; }
      private:
          double avg_income_;
      };

      class USIncome {             // only job: hold US income data
      public:
          USIncome(double avg_income) : avg_income_(avg_income) {}
          double GetAvgIncome() const { return avg_income_; }
      private:
          double avg_income_;
      };

      class AvgIncomeTaxCalculator {   // only job: calculate tax
      public:
          double GetAverageIncomeTax(const IndiaIncome& indian_income) {
              return indian_income.GetAvgIncome() / 15;
          }
          double GetAverageIncomeTax(const USIncome& us_income) {
              return us_income.GetAvgIncome() / 10;
          }
      };

      int main() {
          AvgIncomeTaxCalculator calc;
          cout << calc.GetAverageIncomeTax(IndiaIncome(150000)) << endl;   // 10000
          cout << calc.GetAverageIncomeTax(USIncome(50000)) << endl;       // 5000
      }
      ```

      1. If tax rules change, only the calculator changes. If the income data format changes, only the income classes change. Each class has one reason to change.
3. **O: Open-Closed Principle**
   1. Classes should be **open for extension, but closed for modification**.
   2. Why: a class that is well tested and live in production should not be edited to add a new feature. The edit could break the functions already in the class. Instead, we extend its functionality by creating a new class.
   3. Bad version: every new kind of formatting means editing `TextEditor` itself.

      ```cpp
      class TextEditor {
      public:
          string Format(string str1, string str2) {
              return str1 + str2;   // want reverse-append too? edit this class again
          }
      };
      ```

   4. Good version: put an interface between the editor and the formatting. A new kind of formatting is a new class, and `TextEditor` never changes.

      ```cpp
      #include <iostream>
      #include <string>
      using namespace std;

      class StringFnctn {   // interface
      public:
          virtual string Edit(string str1, string str2) = 0;   // pure virtual
          virtual ~StringFnctn() = default;
      };

      class AppendFnctn : public StringFnctn {
      public:
          string Edit(string str1, string str2) override { return str1 + str2; }
      };

      class ReverseAppendFnctn : public StringFnctn {
      public:
          string Edit(string str1, string str2) override { return str2 + str1; }
      };

      class TextEditor {   // closed for modification
      public:
          string Format(string str1, string str2, StringFnctn& func) {
              return func.Edit(str1, str2);
          }
      };

      int main() {
          TextEditor editor;
          string str1 = "ab", str2 = "cd";
          AppendFnctn append_fnctn;
          cout << editor.Format(str1, str2, append_fnctn) << endl;       // abcd
          ReverseAppendFnctn rev_append_fnctn;
          cout << editor.Format(str1, str2, rev_append_fnctn) << endl;   // cdab
      }
      ```

      1. This works because of polymorphism (lecture 3): `Format` takes a base reference, and the virtual call reaches the right `Edit`.
4. **L: Liskov Substitution Principle**
   1. If S is a subtype of T, then objects of type T in a program may be replaced with objects of type S without altering any of the desirable properties of that program.
   2. In simple words: wherever a function expects a base class, passing any derived class must still work correctly, through virtual functions. A derived class must not narrow down the functionality of the base class.
   3. Good example (cat and dog): `PlaySound(Animal&)` from lecture 3 works for an `Animal`, a `Cat` or a `Dog`. Each one makes a sound, so each is a valid substitute.
   4. Violation: a subclass that can't do what the base promises.

      ```cpp
      class Bird {
      public:
          virtual void Fly() { cout << "Flying" << endl; }
      };

      class Penguin : public Bird {
      public:
          void Fly() override { throw logic_error("Penguins can't fly"); }   // narrows Bird
      };

      void MakeItFly(Bird& bird) { bird.Fly(); }   // breaks when given a Penguin
      ```

   5. Fix: model the hierarchy on what each class really can do. Put `Fly()` only on a `FlyingBird` subclass, so `Penguin` inherits from `Bird` and never promises to fly.
   6. Quick test: if a derived class has to throw "not supported", do nothing, or need a type check (`if (dynamic_cast<Penguin*>(...))`) to behave, it is breaking Liskov.
5. **I: Interface Segregation Principle**
   1. Clients should not be forced to depend on methods that they do not use.
   2. Problem: one fat interface for every shape.

      ```cpp
      class ShapeInterface {
      public:
          virtual double GetArea() = 0;
          virtual double GetVol() = 0;   // a square has no volume
      };

      class Square : public ShapeInterface {
      public:
          Square(int len) : len_(len) {}
          double GetArea() override { return len_ * len_; }
          // no GetVol(): Square is still abstract, so `Square sq(2);` won't compile
      private:
          int len_;
      };
      ```

      1. `Square` is forced to implement `GetVol()`. It must either fake it (return 0, which is a lie) or stay abstract and unusable.
   3. Solution: segregate `ShapeInterface` into two smaller interfaces. Each class implements only what it really supports.

      ```cpp
      #include <iostream>
      using namespace std;

      class TwoDimensionShapeInterface {
      public:
          virtual double GetArea() = 0;
          virtual ~TwoDimensionShapeInterface() = default;
      };

      class ThreeDimensionShapeInterface {
      public:
          virtual double GetArea() = 0;   // surface area
          virtual double GetVol() = 0;
          virtual ~ThreeDimensionShapeInterface() = default;
      };

      class Square : public TwoDimensionShapeInterface {
      public:
          Square(int len) : len_(len) {}
          double GetArea() override { return len_ * len_; }
      private:
          int len_;
      };

      class Sphere : public ThreeDimensionShapeInterface {
      public:
          Sphere(int r) : r_(r) {}
          double GetArea() override { return 4 * 3.14 * r_ * r_; }
          double GetVol() override { return 4.0 / 3 * 3.14 * r_ * r_ * r_; }
      private:
          int r_;
      };

      int main() {
          Square sq(2);
          Sphere sp(1);
          cout << sq.GetArea() << " " << sp.GetArea() << " " << sp.GetVol() << endl;
      }
      ```

6. **D: Dependency Inversion Principle**
   1. High-level modules should not depend on low-level modules. Both should depend on the abstraction.
   2. Abstractions should not depend on details. Details should depend on abstractions.
   3. Picture it: a high-level class A (business logic) used to point straight at a low-level class B (a concrete detail). Cross that arrow out. Now A depends on an interface, and B implements that interface. The dependency arrow from B now points up to the abstraction. That reversal is the "inversion".
   4. Example: a laptop shouldn't be hard-wired to one mouse model. It depends on `MouseInterface` and `KeyboardInterface`. Wired and wireless devices implement those interfaces.

   ```mermaid
   classDiagram
       class Laptop {
           -MouseInterface* mouse_
           -KeyboardInterface* keyboard_
       }
       class MouseInterface {
           <<interface>>
           +Click() void
       }
       class KeyboardInterface {
           <<interface>>
           +Type() void
       }
       Laptop o-- MouseInterface
       Laptop o-- KeyboardInterface
       MouseInterface <|.. WiredMouse
       MouseInterface <|.. WirelessMouse
       KeyboardInterface <|.. WiredKeyboard
       KeyboardInterface <|.. WirelessKeyboard
   ```

   ```cpp
   #include <iostream>
   using namespace std;

   class MouseInterface {
   public:
       virtual void Click() = 0;
       virtual ~MouseInterface() = default;
   };
   class WiredMouse : public MouseInterface {
   public:
       void Click() override { cout << "Wired click" << endl; }
   };
   class WirelessMouse : public MouseInterface {
   public:
       void Click() override { cout << "Wireless click" << endl; }
   };

   class KeyboardInterface {
   public:
       virtual void Type() = 0;
       virtual ~KeyboardInterface() = default;
   };
   class WiredKeyboard : public KeyboardInterface {
   public:
       void Type() override { cout << "Wired typing" << endl; }
   };
   class WirelessKeyboard : public KeyboardInterface {
   public:
       void Type() override { cout << "Wireless typing" << endl; }
   };

   class Laptop {   // high-level module: knows only the interfaces
   public:
       Laptop(MouseInterface* mouse, KeyboardInterface* keyboard)
           : mouse_(mouse), keyboard_(keyboard) {}
       void Use() {
           mouse_->Click();
           keyboard_->Type();
       }
   private:
       MouseInterface* mouse_;
       KeyboardInterface* keyboard_;
   };

   int main() {
       WirelessMouse mouse;
       WiredKeyboard keyboard;
       Laptop laptop(&mouse, &keyboard);   // plug in any implementation
       laptop.Use();
   }
   ```

   5. The concrete devices are passed in from outside through the constructor. This is called **dependency injection**, and it is the usual way to apply D. Swapping a wired mouse for a wireless one changes `main`, never `Laptop`.
7. **One idea under all five**: depend on interfaces, keep each class small and single-purpose, and add features by adding classes. Design patterns are ready-made recipes that apply exactly these principles, starting with the Factory pattern.
