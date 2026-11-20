# Lecture 10: Decorator Pattern

1. **Structural patterns** help connect different pieces together to form a larger structure. They define simple ways to compose objects to create new functionality. Decorator is the structural pattern in this course.
2. **Definition**
   1. The Decorator pattern allows behaviour to be added to individual objects **dynamically**, without affecting the behaviour of other objects from the same class.
   2. The problem it solves: a coffee shop sells simple coffee with any mix of milk, sugar, caramel, and so on. One subclass per combination (`MilkCoffee`, `MilkSugarCoffee`, `MilkSugarCaramelCoffee`, ...) explodes in number. Decorators let us build any combination at runtime by **wrapping** one object inside another.
   3. A decorator is a "wrapper" with two links to the component:
      1. It **is a** `Coffee` (inheritance), so a decorated coffee can be used anywhere a plain coffee can.
      2. It **has a** `Coffee*` (the object it wraps). Each call is forwarded to the wrapped coffee, and the decorator adds its own bit on top.
   4. This gives two levels of inheritance: `Coffee` → `CoffeeDecorator` → `MilkDecorator` / `SugarDecorator`.
3. **Example: coffee**

   ```mermaid
   classDiagram
       class Coffee {
           <<interface>>
           +GetDescription() string
           +GetCost() double
       }
       class CoffeeDecorator {
           #Coffee* coffee_
           +GetDescription() string
           +GetCost() double
       }
       Coffee <|-- SimpleCoffee
       Coffee <|-- SpecialCoffee
       Coffee <|-- CoffeeDecorator
       CoffeeDecorator o-- Coffee : wraps
       CoffeeDecorator <|-- MilkDecorator
       CoffeeDecorator <|-- SugarDecorator
   ```

   ```cpp
   #include <iostream>
   #include <string>
   using namespace std;

   class Coffee {   // component interface
   public:
       virtual string GetDescription() const = 0;
       virtual double GetCost() const = 0;
       virtual ~Coffee() = default;
   };

   class SimpleCoffee : public Coffee {   // concrete component
   public:
       string GetDescription() const override { return "Simple Coffee"; }
       double GetCost() const override { return 5.0; }
   };

   class SpecialCoffee : public Coffee {  // another concrete component
   public:
       string GetDescription() const override { return "Special Coffee"; }
       double GetCost() const override { return 8.0; }
   };

   class CoffeeDecorator : public Coffee {   // is a Coffee...
   public:
       explicit CoffeeDecorator(Coffee* coffee) : coffee_(coffee) {}
       string GetDescription() const override { return coffee_->GetDescription(); }
       double GetCost() const override { return coffee_->GetCost(); }
   protected:
       Coffee* coffee_;   // ...and has a Coffee
   };

   class MilkDecorator : public CoffeeDecorator {
   public:
       explicit MilkDecorator(Coffee* coffee) : CoffeeDecorator(coffee) {}
       string GetDescription() const override { return coffee_->GetDescription() + ", Milk"; }
       double GetCost() const override { return coffee_->GetCost() + 1.5; }
   };

   class SugarDecorator : public CoffeeDecorator {
   public:
       explicit SugarDecorator(Coffee* coffee) : CoffeeDecorator(coffee) {}
       string GetDescription() const override { return coffee_->GetDescription() + ", Sugar"; }
       double GetCost() const override { return coffee_->GetCost() + 0.5; }
   };

   void Print(const Coffee& coffee) {
       cout << "Cost: " << coffee.GetCost() << "; Description: " << coffee.GetDescription() << endl;
   }

   int main() {
       SimpleCoffee simple;
       Print(simple);                    // Cost: 5; Description: Simple Coffee

       MilkDecorator with_milk(&simple);
       Print(with_milk);                 // Cost: 6.5; Description: Simple Coffee, Milk

       SugarDecorator with_sugar(&with_milk);
       Print(with_sugar);                // Cost: 7; Description: Simple Coffee, Milk, Sugar

       SpecialCoffee special;
       SugarDecorator special_sugar(&special);
       Print(special_sugar);             // Cost: 8.5; Description: Special Coffee, Sugar
   }
   ```

   1. How a call travels: `with_sugar.GetCost()` asks `with_milk`, which asks `simple`. Then `simple` returns 5.0, milk adds 1.5, and sugar adds 0.5, giving 7.
   2. The wrapping order is free, and the same decorator can be applied twice (double sugar). No new class is needed for any combination.
   3. `simple` itself is unchanged. Other `SimpleCoffee` objects are unaffected, which is exactly the "individual objects" part of the definition.
4. **Decorator vs inheritance vs strategy**
   1. Inheritance adds behaviour to a whole class, fixed at compile time. A decorator adds it to one object, at runtime.
   2. Strategy **replaces** the algorithm inside an object. A decorator **adds layers** around an object, keeping the original behaviour and extending it.
5. **Pros and cons**
   1. Pros:
      1. A flexible alternative to subclassing for extending functionality. Behaviour can be added or removed dynamically, without modifying the original object or class.
      2. Each decorator has a single responsibility, which makes the code easier to manage, extend and keep modular.
      3. Decorators can be combined in many ways to produce different behaviours, without creating a large number of subclasses.
   2. Cons:
      1. It can make the design complex. As the number of decorators grows, the system gets harder to understand and debug.
      2. All decorators must implement the same interface as the component they decorate. If that interface changes, every decorator must be updated.
      3. Maintaining many decorators is labour-intensive. Making sure they all work correctly together needs careful testing.
6. Next: we now have the full toolkit: OOP, relationships, UML, SOLID and four patterns. The rest of the notes apply it the way an interview does, starting with a step-by-step approach to any LLD question.
