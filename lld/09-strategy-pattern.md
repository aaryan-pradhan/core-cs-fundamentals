# Lecture 9: Strategy Pattern

1. **Behavioral patterns** take care of effective communication and the assignment of responsibilities between objects. Strategy is the behavioral pattern in this course.
2. **Definition**
   1. The Strategy pattern defines a family of interchangeable algorithms and allows them to be used interchangeably within a context.
   2. It lets the algorithm be selected at **runtime**, which gives flexibility and promotes code reuse.
   3. Three roles:
      1. **Strategy interface**: the common shape of every algorithm, for example `Sort(vector<int>&)`.
      2. **Concrete strategies**: one class per algorithm, such as `BubbleSort`, `QuickSort` and `MergeSort`.
      3. **Context**: the class that uses an algorithm, here `Sorter`. It holds a pointer to the strategy interface and never knows which concrete algorithm is behind it.
   4. The problem it solves: without the pattern, `Sorter::Sort` would be one big `if (type == "bubble") ... else if (type == "quick") ...`. Every new algorithm would mean editing `Sorter`, which breaks the open-closed principle (lecture 6).
3. **Example: a sorter**

   ```mermaid
   classDiagram
       class Sorter {
           -SortingStrategy* strategy_
           +Sorter(SortingStrategy* strategy)
           +SetStrategy(SortingStrategy* strategy) void
           +Sort(vector~int~& data) void
       }
       class SortingStrategy {
           <<interface>>
           +Sort(vector~int~& data) void
       }
       Sorter o-- SortingStrategy
       SortingStrategy <|.. BubbleSort
       SortingStrategy <|.. QuickSort
       SortingStrategy <|.. MergeSort
   ```

   ```cpp
   #include <algorithm>
   #include <iostream>
   #include <vector>
   using namespace std;

   class SortingStrategy {   // strategy interface
   public:
       virtual void Sort(vector<int>& data) const = 0;
       virtual ~SortingStrategy() = default;
   };

   class BubbleSort : public SortingStrategy {
   public:
       void Sort(vector<int>& data) const override {
           int n = data.size();
           for (int i = 0; i < n - 1; ++i)
               for (int j = 0; j < n - i - 1; ++j)
                   if (data[j] > data[j + 1]) swap(data[j], data[j + 1]);
       }
   };

   class QuickSort : public SortingStrategy {
   public:
       void Sort(vector<int>& data) const override {
           Quicksort(data, 0, (int)data.size() - 1);
       }
   private:
       void Quicksort(vector<int>& data, int low, int high) const {
           if (low < high) {
               int pi = Partition(data, low, high);
               Quicksort(data, low, pi - 1);
               Quicksort(data, pi + 1, high);
           }
       }
       int Partition(vector<int>& data, int low, int high) const {
           int pivot = data[high];
           int i = low - 1;
           for (int j = low; j < high; ++j)
               if (data[j] < pivot) swap(data[++i], data[j]);
           swap(data[i + 1], data[high]);
           return i + 1;
       }
   };

   class MergeSort : public SortingStrategy {
   public:
       void Sort(vector<int>& data) const override {
           stable_sort(data.begin(), data.end());   // the standard library's stable sort is a merge sort
       }
   };

   class Sorter {   // context
   public:
       explicit Sorter(SortingStrategy* strategy) : strategy_(strategy) {}
       void SetStrategy(SortingStrategy* strategy) { strategy_ = strategy; }   // swap at runtime
       void Sort(vector<int>& data) const { strategy_->Sort(data); }          // delegate
   private:
       SortingStrategy* strategy_;
   };

   void Print(const vector<int>& data) {
       for (int num : data) cout << num << " ";
       cout << endl;
   }

   int main() {
       vector<int> data = {34, 7, 23, 32, 5, 62};

       BubbleSort bubble_sort;
       Sorter sorter(&bubble_sort);
       sorter.Sort(data);
       Print(data);   // 5 7 23 32 34 62

       data = {34, 7, 23, 32, 5, 62};   // reset
       QuickSort quick_sort;
       sorter.SetStrategy(&quick_sort);   // same sorter, new algorithm
       sorter.Sort(data);
       Print(data);   // 5 7 23 32 34 62
   }
   ```

   1. `Sorter` has a strategy (aggregation: it holds a pointer, and the strategy object lives outside it). It also delegates the real work to that strategy.
   2. Adding `HeapSort` means one new class. `Sorter` is never touched.
   3. Compare with the open-closed `TextEditor` (lecture 6): it is the same idea. There the strategy was passed into each call. Here it is stored in the context and can be changed with `SetStrategy`.
   4. Other everyday examples: payment methods (card, UPI, wallet) at checkout, route planning (fastest, shortest, avoid tolls), and the elevator scheduling algorithms in lecture 14.
4. **Pros and cons**
   1. Pros:
      1. Strategies can be swapped at runtime without changing the context that uses them. This allows behaviour to change dynamically.
      2. Each algorithm is encapsulated in its own class, which makes the code more maintainable and easier to understand.
      3. Each strategy class handles a single algorithm. This gives cleaner, more modular code where each class has a single responsibility.
      4. Since strategies are encapsulated, they can be reused in different parts of the codebase without duplicating code.
      5. Each strategy can be tested independently, which makes unit testing easier.
   2. Cons:
      1. It involves creating many strategy classes, which increases the number of classes and objects in the codebase.
      2. Clients must be aware of the different strategies and pick the most appropriate one. This adds complexity to client code.
      3. Managing and configuring strategies can become complex if there are many of them or they have complex dependencies.
5. Next: Strategy swaps *one* behaviour for another. Sometimes we want to *stack* extra behaviour on top of an object instead (milk, then sugar, on a coffee). That is the Decorator pattern.
