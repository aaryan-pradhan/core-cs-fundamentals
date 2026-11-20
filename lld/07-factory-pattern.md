# Lecture 7: Design Patterns and the Factory Pattern

1. **What is a design pattern?**
   1. A design pattern is a tried and tested solution to a problem that keeps coming up in software design. It is a recipe, not a library: you adapt it to your own classes.
   2. Every pattern in these notes is built from the same tools: interfaces, virtual functions, and pointers to a base class (lecture 3), arranged so that the SOLID principles (lecture 6) hold.
2. **Three groups of patterns**
   1. **Creational patterns** provide object creation mechanisms that increase flexibility and reuse of existing code. They answer "who creates the object, and how?"
      1. Factory pattern (this lecture)
      2. Singleton pattern (lecture 8)
   2. **Behavioral patterns** deal with how objects behave and divide work between them. They answer "who does what, and how can that be swapped?"
      1. Strategy pattern (lecture 9)
   3. **Structural patterns** help connect different pieces together to form a larger structure. They answer "how are objects composed?"
      1. Decorator pattern (lecture 10)
3. **Factory pattern: definition**
   1. Create objects without specifying the exact class of the object that will be created.
      1. The type of object is determined at **runtime**, for example from user input.
      2. You need a pointer or reference to a base class. Without polymorphism, the factory pattern can't be implemented.
   2. It provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created.
   3. The problem it solves: if `main` writes `new Square()` directly, `main` depends on `Square`. Every new shape means editing every place that creates shapes. A factory moves all the `new` calls into one class. The client only ever sees the interface.
4. **Example: a shape factory**

   ```cpp
   #include <iostream>
   #include <string>
   using namespace std;

   class ShapeInterface {   // interface
   public:
       virtual void Draw() = 0;
       virtual ~ShapeInterface() = default;
   };

   class Square : public ShapeInterface {
   public:
       void Draw() override { cout << "SQUARE" << endl; }
   };

   class Circle : public ShapeInterface {
   public:
       void Draw() override { cout << "CIRCLE" << endl; }
   };

   class Rectangle : public ShapeInterface {
   public:
       void Draw() override { cout << "RECTANGLE" << endl; }
   };

   class ShapeFactory {
   public:
       ShapeInterface* GetShape(string shape_name) {   // base pointer makes polymorphism work
           if (shape_name == "square") return new Square();
           if (shape_name == "circle") return new Circle();
           if (shape_name == "rectangle") return new Rectangle();
           return nullptr;   // unknown shape
       }
   };

   int main() {
       string shape_name = "circle";   // in practice: cin >> shape_name;

       ShapeFactory factory;
       ShapeInterface* shape = factory.GetShape(shape_name);
       if (shape) shape->Draw();   // CIRCLE
       delete shape;               // virtual destructor cleans up the real Circle
   }
   ```

   1. The shape that gets drawn depends on the runtime input `shape_name`. `main` never names `Square`, `Circle` or `Rectangle`.
   2. Adding a `Triangle` means one new class and one new `if` in the factory. No client code changes.
5. **How it follows SOLID**
   1. **S**: each class has one responsibility. Shapes draw themselves, and the factory only creates them.
   2. **O**: new shapes extend the system as new classes. The existing shapes are never modified.
   3. **L**: every shape can stand in wherever a `ShapeInterface*` is expected.
   4. **I**: the interface is very small (just `Draw`), so there is no need to segregate it.
   5. **D**: maintained through the interface. The client depends on `ShapeInterface`, not on concrete shapes.
6. **Rule of thumb**: whenever two classes are of the same type (both are shapes, both are payment methods), make a new abstract class above them. Both inherit from it, and the rest of the code talks to the abstract class.
7. **When is the factory pattern useful?**
   1. When a class has multiple subclasses, each providing a different implementation.
   2. When we have to decouple the client code from the concrete classes.
   3. When we need to extend the application by adding new types of objects without modifying existing code.
8. **Bigger version: a family of factories**
   1. The factory itself can be an interface too. A `TwoDShapeFactory` makes 2D shapes, and a `ThreeDShapeFactory` makes 3D shapes. The client picks a factory, then asks it for shapes, and never knows which concrete classes it gets.

   ```mermaid
   classDiagram
       class ShapeFactory {
           <<interface>>
           +GetShape(string) Shape*
       }
       class TwoDShapeFactory {
           +GetShape(string) Shape*
       }
       class ThreeDShapeFactory {
           +GetShape(string) Shape*
       }
       class Shape {
           <<interface>>
           +Draw() void
       }
       ShapeFactory <|-- TwoDShapeFactory
       ShapeFactory <|-- ThreeDShapeFactory
       Shape <|-- Square
       Shape <|-- Circle
       Shape <|-- Sphere
       Shape <|-- Cube
       TwoDShapeFactory ..> Square : creates
       TwoDShapeFactory ..> Circle : creates
       ThreeDShapeFactory ..> Sphere : creates
       ThreeDShapeFactory ..> Cube : creates
   ```

   ```cpp
   #include <iostream>
   #include <string>
   using namespace std;

   class Shape {
   public:
       virtual void Draw() = 0;
       virtual ~Shape() = default;
   };
   class Square : public Shape { public: void Draw() override { cout << "Square" << endl; } };
   class Circle : public Shape { public: void Draw() override { cout << "Circle" << endl; } };
   class Sphere : public Shape { public: void Draw() override { cout << "Sphere" << endl; } };
   class Cube   : public Shape { public: void Draw() override { cout << "Cube" << endl; } };

   class ShapeFactory {   // the factory is an interface too
   public:
       virtual Shape* GetShape(string name) = 0;
       virtual ~ShapeFactory() = default;
   };

   class TwoDShapeFactory : public ShapeFactory {
   public:
       Shape* GetShape(string name) override {
           if (name == "square") return new Square();
           if (name == "circle") return new Circle();
           return nullptr;
       }
   };

   class ThreeDShapeFactory : public ShapeFactory {
   public:
       Shape* GetShape(string name) override {
           if (name == "sphere") return new Sphere();
           if (name == "cube") return new Cube();
           return nullptr;
       }
   };

   void DrawFrom(ShapeFactory& factory, string name) {   // knows only the interfaces
       Shape* shape = factory.GetShape(name);
       if (shape) shape->Draw();
       delete shape;
   }

   int main() {
       TwoDShapeFactory two_d;
       ThreeDShapeFactory three_d;
       DrawFrom(two_d, "circle");    // Circle
       DrawFrom(three_d, "cube");    // Cube
   }
   ```

9. **Pros and cons**
   1. Pros:
      1. Avoids tight coupling between the creator and the concrete products. They are connected only through the interface and the factory.
      2. Single Responsibility Principle: product creation code lives in one place in the program, which makes it easier to support.
      3. Open/Closed Principle: new types of products can be introduced without breaking existing client code.
   2. Cons:
      1. The code may become more complicated, since the pattern introduces a lot of new subclasses. It fits best when a class hierarchy already exists.
10. Next: the factory controls *which* class gets created. Sometimes we need to control *how many* objects get created, exactly one. That is the Singleton pattern.
