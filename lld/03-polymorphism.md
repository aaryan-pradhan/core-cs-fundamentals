# Lecture 3: Polymorphism, Virtual Functions and Abstraction

1. **What is polymorphism?**
   1. Polymorphism means "many forms": the same message (function call) behaves differently depending on the object that receives it.
   2. Example: `animal.Sound()` prints "Meow" for a cat and "Bark" for a dog, even though the calling code only knows it has "an animal".
   3. To get there we need two tools: references and pointers to a base class, and `virtual` functions.
2. **References and pointers (quick recap)**
   1. A reference is another name for an existing variable. Changing it changes the original.
   2. A pointer stores the address of a variable. `*ptr` reaches the original.

      ```cpp
      int a = 10;
      int *ptr = &a;
      int &b = a;
      cout << a << " " << b << endl;   // 10 10
      b = 15;
      cout << a << " " << b << endl;   // 15 15 (b is a, so both change)
      *ptr = 20;
      cout << a << " " << b << " " << *ptr << endl;   // 20 20 20
      ```

   3. Differences:
      1. A pointer can be reassigned to point somewhere else (`ptr = &c;`). A reference is bound once, at creation, and can never be rebound.
      2. A reference must be initialized when declared. A pointer can be `nullptr`.
   4. Passing by reference (`Animal &animal`) lets a function work on the caller's original object, with no copy. That is why the functions below take `Animal&`.
   5. Stack vs heap objects can both be passed this way:

      ```cpp
      Animal animal;               // object on the stack
      Animal *ptr = new Animal();  // object on the heap
      PlaySound(animal);
      PlaySound(*ptr);             // dereference to get the object
      ```

3. **A base reference only sees the base part**
   1. Picture a `Derived` object as two stacked boxes. The top box is the Base part, with `A()`, `B()`, `C()`. The bottom box is the Derived part, with `A()`, `E()`, `F()`.
   2. `Base &B = D;` is allowed, because a Derived IS-A Base. But `B` points only to the Base box.

      ```cpp
      int main() {
          Derived D;
          Base &B = D;
          B.B();   // fine, B() is in Base
          B.A();   // runs Base::A(), not Derived::A()
          B.E();   // compile error: E() is not in the Base part
      }
      ```

   3. Without anything extra, the compiler picks the function from the **type of the reference** (Base), not from the real object (Derived). This is decided at compile time.
4. **Virtual functions**
   1. Mark the base function `virtual`. Now a call through a base reference or pointer runs the version of the **actual object**, decided at runtime.

      ```cpp
      #include <iostream>
      using namespace std;

      class Animal {
      public:
          virtual void Sound() { cout << "No Sound" << endl; }
          virtual ~Animal() = default;
      };

      class Cat : public Animal {
      public:
          void Sound() override { cout << "Meow" << endl; }
      };

      class Dog : public Animal {
      public:
          void Sound() override { cout << "Bark" << endl; }
      };

      void PlaySound(Animal &animal) {
          animal.Sound();   // which Sound()? decided by the real object
      }

      int main() {
          Cat cat;
          Dog dog;
          PlaySound(cat);
          PlaySound(dog);
      }
      // Output:
      // Meow
      // Bark
      ```

      1. `Animal &animal = cat` refers to the Animal (base) part of `cat`. Without `virtual`, both calls would print "No Sound".
      2. With `virtual`, the most derived `Sound()` is performed, so `PlaySound` automatically does the right thing for a cat and for a dog.
      3. `PlaySound` never has to change when we add a `Cow` class. That is the payoff of polymorphism.
   2. In a chain `Top → Middle → Bottom`, if `Top::A()` is virtual, a call through a `Top&` reaches the most derived override, `Bottom::A()`. This happens even if `virtual` isn't written again in `Middle`, because once virtual, always virtual.
   3. Same idea through pointers:

      ```cpp
      Cat *cat_ptr = new Cat();
      Animal &animal_ref = *cat_ptr;    // refers to the Animal part
      Animal *animal_ptr = &animal_ref; // also points to the Animal part
      animal_ptr->Sound();              // Meow, because Sound() is virtual
      ```

      1. `cat_ptr` sees the whole object. `animal_ref` and `animal_ptr` see only the Animal part, yet the call still reaches `Cat::Sound()`.
   4. How it works (good to know): every class with virtual functions gets a table of function pointers (the **vtable**). Each object carries a hidden pointer to its class's vtable. A virtual call looks up the right function in that table at runtime.
5. **`override` and `final`**
   1. `override` on a derived function tells the compiler "this is meant to override a virtual base function". If it doesn't (wrong name, wrong parameters, base not virtual), it is a compile-time error. This catches silent typos like `Sound(int)`.
   2. `final` on a virtual function means derived classes may not override it any further, or it is a compile-time error. `final` on a class (`class Cat final : public Animal`) means nobody can inherit from it.
6. **Virtual destructors**
   1. Problem: deleting a derived object through a base pointer.

      ```cpp
      Animal *animal_ptr = new Cat();
      delete animal_ptr;
      ```

   2. If `~Animal()` is not virtual, only the Animal destructor runs. The Cat part is never cleaned up, so anything Cat allocated leaks. Formally, this is undefined behaviour.
   3. With `virtual ~Animal()`, `delete` runs `~Cat()` first, then `~Animal()`, as it should.
7. **Best practices**
   1. Use the `virtual` keyword on virtual functions in the base class.
   2. Use the `override` specifier (and not `virtual`) on overriding functions in derived classes. This includes virtual destructors.
   3. Whenever you are dealing with inheritance, make any explicit destructor virtual.
8. **Object slicing**
   1. Slicing happens when a derived object is **copied** into a base object, not referenced.

      ```cpp
      Derived D;
      Base B = D;   // a new Base object, not a reference
      B.A();        // always Base::A(), even if A() is virtual
      ```

   2. `D` has both parts, Base and Derived. `B` is a brand-new Base object, so only the Base part is copied and the Derived part is sliced off.
   3. Polymorphism works only through references and pointers, never through copies. So pass `Animal&` or `Animal*`, never plain `Animal`.
9. **Pure virtual functions, abstract classes and interfaces**
   1. A **pure virtual function** has no body at all. It is a placeholder that derived classes are meant to redefine.

      ```cpp
      class Animal {
      public:
          virtual void Sound() = 0;   // pure virtual: always supposed to be overridden
      };
      ```

   2. An **abstract base class** is any class with one or more pure virtual functions. It cannot be instantiated:

      ```cpp
      Animal animal;   // compile error: Animal is abstract
      ```

      1. A derived class that overrides every pure virtual function becomes concrete, so `Cat cat;` works. If it leaves even one, it is still abstract.
      2. Pointers and references to an abstract class are fine: `Animal *a = new Cat();`.
   3. An **interface class** is a class with no member variables, where all functions are pure virtual.
      1. Interfaces define what derived classes must implement, and leave how entirely up to the derived class.
      2. Give it a virtual destructor too: `virtual ~ShapeInterface() = default;`.
   4. **Abstraction**, the fourth pillar of OOP, is exactly this: callers depend on what an object can do (the interface), not how it does it. `PlaySound` knows only that an `Animal` has `Sound()`.
   5. Interfaces are the building block of everything ahead. SOLID's D principle and every design pattern in these notes are built on "depend on an interface, plug in a concrete class".
10. Next: so far one class inherits from another (IS-A). Objects also contain and use other objects, like a person and their heart or a doctor and their patients. These HAS-A relationships come next.
