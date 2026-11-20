# Lecture 9: Strategy Pattern

1. **Behavioral patterns** handle communication and the split of responsibilities between objects.
   - **In this course:** Strategy is the behavioral pattern.

2. **Definition**

   1. The Strategy pattern defines a family of interchangeable algorithms. A context can use any of them.
   2. It lets you pick the algorithm at **runtime**. This gives flexibility and promotes code reuse.
   3. It has three roles:

      | Role | Meaning | Example |
      |------|---------|---------|
      | **Strategy interface** | The common shape of every algorithm. | `Sort(vector<int>&)` |
      | **Concrete strategies** | One class per algorithm. | `BubbleSort`, `QuickSort`, `MergeSort` |
      | **Context** | The class that uses an algorithm. It holds a pointer to the strategy interface. It never knows which concrete algorithm is behind it. | `Sorter` |

   4. **The problem it solves:** Without the pattern, `Sorter::Sort` is one big `if (type == "bubble") ... else if (type == "quick") ...`.
      - **Cost:** Every new algorithm means editing `Sorter`.
      - **Rule broken:** This breaks the open-closed principle (lecture 6).

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

   1. **Aggregation:** `Sorter` has a strategy. It holds a pointer, and the strategy object lives outside it.
   2. **Delegation:** `Sorter` hands the real work to the strategy.
   3. **Extending:** Adding `HeapSort` means one new class. `Sorter` is never touched.
   4. **Compare with `TextEditor` (lecture 6):** It is the same open-closed idea.
      - **There:** The strategy was passed into each call.
      - **Here:** The strategy is stored in the context. You change it with `SetStrategy`.
   5. **Other everyday examples:**
      - Payment methods (card, UPI, wallet) at checkout.
      - Route planning (fastest, shortest, avoid tolls).
      - The elevator scheduling algorithms in lecture 14.

4. **Pros and cons**

   | Pros | Cons |
   |------|------|
   | Strategies swap at runtime without changing the context. Behaviour can change dynamically. | Many strategy classes increase the number of classes and objects in the codebase. |
   | Each algorithm is encapsulated in its own class. The code is easier to maintain and understand. | Clients must know the different strategies and pick the right one. This adds complexity to client code. |
   | Each strategy class handles one algorithm. The code is cleaner and more modular. Each class has a single responsibility. | Managing and configuring strategies gets complex if there are many of them or they have complex dependencies. |
   | Strategies are encapsulated, so they can be reused in other parts of the codebase without duplicating code. | |
   | Each strategy can be tested independently. Unit testing is easier. | |

5. **Next:** Strategy swaps one behaviour for another. Sometimes you want to stack extra behaviour on an object instead, like milk, then sugar, on a coffee. That is the Decorator pattern.
