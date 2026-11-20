# Lecture 7: Design Patterns and the Factory Pattern

1. **What is a design pattern?**
   1. A design pattern is a tried and tested solution to a problem that keeps coming up in software design.
   2. **Recipe, not library:** You adapt it to your own classes.
   3. **Same tools:** Every pattern in these notes uses interfaces, virtual functions, and pointers to a base class (lecture 3). They are arranged so that the SOLID principles (lecture 6) hold.
2. **Three groups of patterns**

   | Group | What it does | Question it answers | Patterns |
   |-------|--------------|---------------------|----------|
   | **Creational** | Provides object creation mechanisms that increase flexibility and reuse of existing code | "Who creates the object, and how?" | Factory (lecture 7), Singleton (lecture 8) |
   | **Behavioral** | Takes care of effective communication and the assignment of responsibilities between objects | "Who does what, and how can that be swapped?" | Strategy (lecture 9) |
   | **Structural** | Helps connect different pieces together to form a larger structure | "How are objects composed?" | Decorator (lecture 10) |

3. **Factory pattern: definition**
   1. It creates objects without specifying the exact class of the object that will be created.
      - **Runtime:** The type of object is determined at **runtime**, for example from user input.
      - **Base pointer:** You need a pointer or reference to a base class. Without polymorphism, the factory pattern cannot be implemented.
   2. It provides an interface for creating objects in a superclass. Subclasses can alter the type of objects that will be created.
   3. **Problem it solves:**
      - If `main` writes `new Square()` directly, `main` depends on `Square`.
      - Every new shape means editing every place that creates shapes.
      - A factory moves all the `new` calls into one class. The client only ever sees the interface.
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

   1. **Runtime input:** The shape that gets drawn depends on the input `shape_name`. `main` never names `Square`, `Circle` or `Rectangle`.
   2. **Adding a shape:** A `Triangle` needs one new class and one new `if` in the factory. No client code changes.
5. **How it follows SOLID**
   1. **S:** Each class has one responsibility. Shapes draw themselves, and the factory only creates them.
   2. **O:** New shapes extend the system as new classes. The existing shapes are never modified.
   3. **L:** Every shape can stand in wherever a `ShapeInterface*` is expected.
   4. **I:** The interface is very small (just `Draw`), so there is no need to segregate it.
   5. **D:** It is maintained through the interface. The client depends on `ShapeInterface`, not on concrete shapes.
6. **Rule of thumb:** Whenever two classes are of the same type (both are shapes, both are payment methods), make a new abstract class above them. Both inherit from it. The rest of the code talks to the abstract class.
7. **When is the factory pattern useful?**
   1. A class has multiple subclasses, each providing a different implementation.
   2. You have to decouple the client code from the concrete classes.
   3. You need to extend the application with new types of objects without modifying existing code.
8. **Bigger version: a family of factories**
   1. The factory itself can be an interface too.
   2. A `TwoDShapeFactory` makes 2D shapes. A `ThreeDShapeFactory` makes 3D shapes.
   3. The client picks a factory, then asks it for shapes. It never knows which concrete classes it gets.

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
   1. **Pros:**
      1. **Loose coupling:** The creator and the concrete products are connected only through the interface and the factory.
      2. **Single Responsibility Principle:** Product creation code lives in one place in the program. This makes it easier to support.
      3. **Open/Closed Principle:** New types of products can be introduced without breaking existing client code.
   2. **Cons:**
      1. **More complexity:** The pattern introduces a lot of new subclasses. It fits best when a class hierarchy already exists.
10. **Next:** The factory controls *which* class gets created. Sometimes we need to control *how many* objects get created, exactly one. That is the Singleton pattern.
