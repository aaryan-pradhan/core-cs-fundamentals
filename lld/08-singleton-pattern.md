# Lecture 8: Singleton Pattern

1. **Definition**
   1. Singleton is a creational design pattern. It ensures two things:
      1. **One instance:** The class has only one instance (object).
      2. **Global access point:** The instance has a global access point. This is like a pointer that any part of the program can get.
   2. **Typical uses:** A logger, a configuration manager, a database connection pool. Each is one shared thing that every part of the program uses, never a second copy.
   3. **Needs `static`:** Building one needs the `static` keyword, so it comes first.
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

   1. **Normal local:** It is created fresh on every call.
   2. **Static local:** It keeps the same memory across calls. Its initialization runs only once.
   3. **Like globals:** Static variables are like global variables, but visible only within their scope.
3. **Static members of a class**
   1. **Shared copy:** Static members are associated with the **class**, not with any object. All objects share one copy.
   2. **Normal data member:** A member like `int cnt_ = 0;` belongs to each object separately.
   3. **Static member function:** You can call it without any object, as `A::Print()`. There is no object, so it can use only static members.

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

      1. **Declaration and definition:** A static data member is declared inside the class. It is defined (given memory and an initial value) outside the class.
4. **How to implement a singleton**
   1. Make the default constructor **private**. This stops other code from creating objects with `new A()` or `A a;`.
   2. Create a **static creation method** (`GetInstance`) that acts as the constructor.
      1. The first call creates the object and saves it in a static pointer.
      2. Every later call returns that same saved pointer.
   3. Delete the copy constructor and copy assignment too. Otherwise `A copy = *A::GetInstance();` quietly makes a second object.

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

   4. **One object:** A change made through one pointer is visible everywhere.
5. **Thread safety**
   1. **Race:** The version above has a race. Two threads can call `GetInstance()` at the same moment. Both can see `nullptr`, and both can call `new`. Then two instances exist.
   2. **Simplest fix:** In C++11 and later, use a static local variable (the "Meyers singleton"). The language guarantees that a static local is initialized exactly once, even when many threads arrive together.

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

      1. **No leak:** This also fixes the leak in the pointer version, which never calls `delete`. The static object is destroyed automatically when the program ends.
6. **Example: a logger**
   1. **Why one logger:** A program writes all its logs to one file through one logger. Two loggers writing to the same file would mix up and overwrite each other's lines.
   2. **Constructor:** It does the setup work once. It creates the text file and keeps the file size limited.

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

   3. **Use sparingly:** Singleton is suggested only where an object really should be initialized once. It is rarely the right answer.
7. **Pros and cons**
   1. **Pros:**
      1. **Single instance:** You can be sure that a class has only one instance.
      2. **Global access:** You gain a global access point to that instance.
      3. **Lazy initialization:** The singleton object is initialized only when it is requested for the first time.
   2. **Cons:**
      1. **Breaks Single Responsibility:** The class solves two problems at once. It does its real job, and it controls its own creation, like a factory and a class combined.
      2. **Masks bad design:** Components of the program may know too much about each other. A global object is easy to reach from everywhere, so everything starts depending on it.
      3. **Threads:** It needs special treatment in a multithreaded environment, so that multiple threads do not create the object several times.
      4. **Hard to unit test:** Tests cannot swap in a fake instance. State left over from one test leaks into the next.
8. **Next:** Factory and Singleton control how objects are created. The next pattern is behavioral. It lets an object change *how it does its job* at runtime by swapping in a different algorithm.
