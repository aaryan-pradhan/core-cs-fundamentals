# Lecture 10: Decorator Pattern

1. **Structural patterns** connect different pieces into a larger structure. They define simple ways to compose objects to create new functionality.
   - **In this course:** Decorator is the structural pattern.

2. **Definition**

   1. The Decorator pattern adds behaviour to individual objects **dynamically**. Other objects of the same class are not affected.
   2. **The problem it solves:** A coffee shop sells simple coffee with any mix of milk, sugar, caramel and so on.
      - **Subclass per combination:** `MilkCoffee`, `MilkSugarCoffee`, `MilkSugarCaramelCoffee` and so on. The number of classes explodes.
      - **With decorators:** You build any combination at runtime by **wrapping** one object inside another.
   3. A decorator is a wrapper with two links to the component:
      1. **Is a `Coffee` (inheritance):** A decorated coffee can be used anywhere a plain coffee can.
      2. **Has a `Coffee*` (the object it wraps):** Each call is forwarded to the wrapped coffee. The decorator adds its own part on top.
   4. **Two levels of inheritance:** `Coffee`, then `CoffeeDecorator`, then `MilkDecorator` and `SugarDecorator`.

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

   1. **How a call travels:** `with_sugar.GetCost()` asks `with_milk`, which asks `simple`.
      - `simple` returns 5.0.
      - Milk adds 1.5.
      - Sugar adds 0.5.
      - The result is 7.
   2. **Free order:** The wrapping order is free. The same decorator can be applied twice (double sugar). No new class is needed for any combination.
   3. **Individual objects:** `simple` itself is unchanged. Other `SimpleCoffee` objects are unaffected. This is the "individual objects" part of the definition.

4. **Decorator vs inheritance vs strategy**

   | Pattern | What it does |
   |---------|--------------|
   | Inheritance | Adds behaviour to a whole class, fixed at compile time. |
   | Decorator | Adds behaviour to one object, at runtime. It **adds layers** around an object. It keeps the original behaviour and extends it. |
   | Strategy | **Replaces** the algorithm inside an object. |

5. **Pros and cons**

   | Pros | Cons |
   |------|------|
   | A flexible alternative to subclassing. Behaviour can be added or removed dynamically, without modifying the original object or class. | The design can get complex. As decorators grow in number, the system is harder to understand and debug. |
   | Each decorator has a single responsibility. The code is easier to manage, extend and keep modular. | All decorators must implement the same interface as the component they decorate. If that interface changes, every decorator must be updated. |
   | Decorators combine in many ways to give different behaviours. You do not need a large number of subclasses. | Maintaining many decorators is labour-intensive. You need careful testing to make sure they all work together. |

6. **Next:** You now have the full toolkit: OOP, relationships, UML, SOLID and four patterns. The rest of the notes apply it the way an interview does. They start with a step-by-step approach to any LLD question.
