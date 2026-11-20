# Lecture 8: Singleton Pattern

1. **Definition**
   1. Singleton is a creational design pattern that lets you ensure that:
      1. a class has only **one instance** (object), while
      2. providing a **global access point** to this instance, like a pointer that any part of the program can get.
   2. Typical uses: a logger, a configuration manager, a database connection pool. Each of these is one shared thing that every part of the program should use, never a second copy.
   3. Building one needs the `static` keyword, so that comes first.
2. **Static local variables**

   ```cpp
   #include <iostream>
   using namespace std;

   void Print() {
       static int a = 0;   // initialized only once, on the first call
       a++;
       cout << a << endl;
   }

   int main() {
       Print();   // 1
       Print();   // 2: the same a, changed again
       Print();   // 3
   }
   ```

   1. A normal local variable is created fresh on every call. A `static` local keeps the same memory across calls, and its initialization runs only once.
   2. Static variables are like global variables, but visible only within their scope.
3. **Static members of a class**
   1. Static members of a class are associated with the **class**, not with any object. All objects share one copy.
   2. A normal data member (`int cnt_ = 0;`) belongs to each object separately.
   3. A static member function can be called without any object, as `A::Print()`. Because there is no object, it can use only static members.

      ```cpp
      #include <iostream>
      using namespace std;

      class A {
      public:
          static void Print() {
              cnt_++;
              cout << cnt_ << endl;
          }
          static int cnt_;   // declaration
      };

      int A::cnt_ = 0;   // definition: must be written once outside the class

      int main() {
          A obj;
          A::Print();                  // 1 (called on the class)
          cout << obj.cnt_ << endl;    // 1 (the same shared variable)
          obj.Print();                 // 2 (can also be called through an object)
      }
      ```

      1. A static data member is declared inside the class and defined (given memory and an initial value) outside it.
4. **How to implement a singleton**
   1. Make the default constructor **private**. This stops other code from creating objects with `new A()` or `A a;`.
   2. Create a **static creation method** (`GetInstance`) that acts as the constructor.
      1. The first time it is called, it creates the object and saves it in a static pointer.
      2. Every later call returns that same saved pointer.
   3. Also delete the copy constructor and copy assignment. Otherwise `A copy = *A::GetInstance();` would quietly make a second object.

   ```cpp
   #include <iostream>
   using namespace std;

   class A {
   public:
       static A* GetInstance() {
           if (ptr_ == nullptr) {
               ptr_ = new A();   // created only on the first request
           }
           return ptr_;          // later calls get the same pointer
       }
       A(const A&) = delete;              // no copies
       A& operator=(const A&) = delete;   // no copy assignment
       void ShowMessage() { cout << "Hello from the only A" << endl; }
   private:
       A() = default;   // private: nobody outside can construct an A
       static A* ptr_;
   };

   A* A::ptr_ = nullptr;

   int main() {
       A* ptr1 = A::GetInstance();
       A* ptr2 = A::GetInstance();   // pointer is non-null now, so it is simply returned
       cout << (ptr1 == ptr2) << endl;   // 1: both point to the same object
       ptr1->ShowMessage();
       return 0;
   }
   ```

   4. Since there is only one object, a change made through one pointer is visible everywhere.
5. **Thread safety**
   1. The version above has a race. If two threads call `GetInstance()` at the same moment, both can see `nullptr` and both can call `new`. Then two instances exist.
   2. The simplest fix in C++11 and later is a static local variable (the "Meyers singleton"). The language guarantees that a static local is initialized exactly once, even when many threads arrive together.

      ```cpp
      #include <iostream>
      using namespace std;

      class A {
      public:
          static A& GetInstance() {
              static A instance;   // created once, on first call, thread-safe
              return instance;
          }
          A(const A&) = delete;
          A& operator=(const A&) = delete;
      private:
          A() { cout << "A created" << endl; }
      };

      int main() {
          A& a1 = A::GetInstance();   // A created
          A& a2 = A::GetInstance();   // nothing printed: same object
          cout << (&a1 == &a2) << endl;   // 1
      }
      ```

      1. This also fixes the leak in the pointer version, which never calls `delete`. The static object is destroyed automatically when the program ends.
6. **Example: a logger**
   1. A program should write all its logs to one file through one logger. Two loggers writing to the same file would mix up and overwrite each other's lines.
   2. The constructor does the setup work once: it creates the text file and makes sure the file size stays limited.

   ```cpp
   #include <iostream>
   #include <string>
   using namespace std;

   class Logger {
   public:
       static Logger* GetLogger() {
           static Logger logger;   // the only Logger
           return &logger;
       }
       Logger(const Logger&) = delete;
       Logger& operator=(const Logger&) = delete;

       void Log(string logs) {
           // real version: write logs to the file
           cout << "[log " << ++count_ << "] " << logs << endl;
       }
   private:
       Logger() {
           // real version: create the text file, limit its size
       }
       int count_ = 0;
   };

   int main() {
       Logger* logger = Logger::GetLogger();
       logger->Log("Hello world!");          // [log 1] Hello world!
       Logger::GetLogger()->Log("Again");    // [log 2] Again: same logger, count continues
       return 0;
   }
   ```

   3. Singleton is suggested only where an object really should be initialized once. It is rarely the right answer, so use it sparingly.
7. **Pros and cons**
   1. Pros:
      1. You can be sure that a class has only a single instance.
      2. You gain a global access point to that instance.
      3. The singleton object is initialized only when it is requested for the first time (lazy initialization).
   2. Cons:
      1. Violates the Single Responsibility Principle. The class solves two problems at once: its real job, and controlling its own creation, like a factory and a class combined.
      2. It can mask bad design, for instance when components of the program know too much about each other. A global object is easy to reach from everywhere, so everything starts depending on it.
      3. It needs special treatment in a multithreaded environment, so that multiple threads don't create the object several times.
      4. It can be difficult to unit test the client code of a singleton. Tests can't swap in a fake instance, and state left over from one test leaks into the next.
8. Next: Factory and Singleton control how objects are created. The next pattern is behavioral: it lets an object change *how it does its job* at runtime by swapping in a different algorithm.
