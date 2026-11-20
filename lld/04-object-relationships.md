# Lecture 4: Object Relationships

1. Inheritance gives IS-A. Most real designs are built from HAS-A and USES-A relationships between objects instead. There are three kinds.
   1. **Composition**
   2. **Aggregation**
   3. **Association**
2. In each one, one side is the **object** (the class, the whole). The other side is the **member** (the part).
3. **Composition** ("part of")
   1. To qualify as a composition, an object and a part must have this relationship.
      1. The part (member) is part of the object (class).
      2. The part can only belong to one object at a time.
      3. The object manages the part's existence. The part is created with the object and destroyed with it.
      4. The part does not know about the existence of the object.
   2. **Example:** A body (object) and a heart (part).
      - A heart belongs to exactly one body. It lives and dies with that body.
      - The heart does not know whose body it is in.
      - The object can have other parts too, like kidneys.
   3. **In C++:** The part is a plain member variable (not a pointer). It is constructed with the object and destroyed with it automatically.

      ```cpp
      #include <iostream>
      #include <string>
      using namespace std;

      class Heart {
      public:
          Heart(string person_name) : person_name_(person_name) {}
          ~Heart() { cout << "~Heart of " << person_name_ << endl; }
      private:
          string person_name_;
      };

      class Person {
      public:
          Person(string person_name) : heart_(person_name) {}
          ~Person() { cout << "~Person" << endl; }
      private:
          Heart heart_;   // composition: a member, owned by Person
      };

      int main() {
          Person person("A");    // each object gets its own heart
          Person person2("B");
      }
      // Output:
      // ~Person
      // ~Heart of B
      // ~Person
      // ~Heart of A
      ```

      1. `person2` is destroyed first. Objects in one scope are destroyed last in, first out (lecture 1).
      2. For each person, the `~Person` body runs first. Then its members are destroyed. So the heart dies with its owner.
4. **Aggregation** ("has a")
   1. To qualify as an aggregation, a whole object and its parts must have this relationship.
      1. The part (member) is part of the object (class).
      2. The part can (if desired) belong to more than one object at a time.
      3. The object does **not** manage the part's existence.
      4. The part does not know about the existence of the object.
   2. **Example:** A person and their home address.
      - An address can belong to several people at once.
      - If a person dies, the address still exists.
      - The home is the part. The person is the object.
   3. **In C++:** The part is held by **pointer** (or reference). It is created outside and passed in. So its lifetime is separate from the object's.

      ```cpp
      #include <iostream>
      #include <string>
      using namespace std;

      class Heart {
      public:
          Heart(string person_name) : person_name_(person_name) {}
          ~Heart() { cout << "~Heart of " << person_name_ << endl; }
      private:
          string person_name_;
      };

      class Home {
      public:
          Home(string add) : add_(add) {}
          ~Home() { cout << "~Home of add: " << add_ << endl; }
          string add_;
      };

      class Person {
      public:
          Person(string person_name, Home *home)
              : heart_(person_name), home_(home), person_name_(person_name) {}
          ~Person() { cout << "~Person " << person_name_ << endl; }
          string GetAdd() { return home_->add_; }
      private:
          Heart heart_;         // composition (owned member)
          Home *home_;          // aggregation (pointer, not owned)
          string person_name_;
      };

      int main() {
          Home home("home");
          Person *p1 = new Person("A", &home);
          Person *p2 = new Person("B", &home);   // two persons share one home
          delete p1;
          cout << p2->GetAdd() << endl;           // home still exists after p1 is gone
          delete p2;
          return 0;
      }
      // Output:
      // ~Person A       p1 deleted
      // ~Heart of A     its heart goes with it (composition)
      // home            the home is still there
      // ~Person B
      // ~Heart of B
      // ~Home of add: home   destroyed only at main's closing brace
      ```

      1. `p1`, `p2` and `home` all have different lifetimes. That is the mark of aggregation.
      2. **Why a pointer and not a reference:** The only real difference is that a pointer can be reassigned (`ptr = &B;`). A reference member can never be rebound, so a person could never move house.
5. **Association** ("uses a")
   1. To qualify as an association, an object and another object must have this relationship.
      1. The associated object (member) is otherwise unrelated to the object. It is not a part/whole relationship.
      2. The associated object can belong to more than one object at a time.
      3. The object does not manage the associated object's existence.
      4. The associated object may or may not know about the existence of the object.
   2. **Example:** Doctors and patients.
      - A doctor sees many patients in a day.
      - A patient can see many doctors (a second opinion, or different specialists).
      - Neither is part of the other. Neither one's lifespan is tied to the other.
   3. **Difference from aggregation:** Rule 1 (not a whole/part) and rule 4 (it can know about the other side). So association can be **bidirectional**. Both sides hold pointers to each other.
   4. **Example:** A person can own many homes. A home can have many persons. Each side keeps a list of the other.
      1. **Problem:** `Home` needs `Person`, and `Person` needs `Home`. Whichever class we write first, the other is not defined yet, so it will not compile. Swapping the order does not help.
      2. **Fix:** A **forward declaration**. Declare `class Person;` first. This tells the compiler "this type exists, its definition comes later". A forward-declared type can be used as a pointer (`Person*`) before it is defined.

      ```cpp
      #include <iostream>
      #include <string>
      #include <vector>
      using namespace std;

      class Person;   // declare now, define later

      class Home {
      public:
          Home(string add) : add_(add) {}
          void AddPerson(Person *person) { persons_.push_back(person); }
      private:
          string add_;
          vector<Person*> persons_;   // association
      };

      class Person {   // definition after declaration
      public:
          Person(string name) : name_(name) {}
          void AddHome(Home *home) { homes_.push_back(home); }
      private:
          string name_;
          vector<Home*> homes_;       // association
      };

      int main() {
          Home home1("delhi"), home2("bengaluru"), home3("mumbai");
          Person p1("A"), p2("B");

          p1.AddHome(&home1); home1.AddPerson(&p1);
          p1.AddHome(&home2); home2.AddPerson(&p1);
          p2.AddHome(&home2); home2.AddPerson(&p2);   // home2 shared by A and B
          p2.AddHome(&home3); home3.AddPerson(&p2);
      }
      ```

6. **Summary**

   | Property | Composition | Aggregation | Association |
   |---|---|---|---|
   | Relationship type | whole/part | whole/part | otherwise unrelated |
   | Member can belong to multiple classes | No | Yes | Yes |
   | Member's existence managed by the class | Yes | No | No |
   | Directionality | Unidirectional | Unidirectional | Uni or bidirectional |
   | Relationship verb | part of | has a | uses a |
   | Typical C++ form | plain member | pointer member | pointers (often both sides) |

7. **Why UML comes next:** In interviews we do not write all this code first. We draw it. UML class diagrams are the standard picture of classes and these relationships.
