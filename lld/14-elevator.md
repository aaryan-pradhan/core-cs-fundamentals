# Lecture 14: Design an Elevator System

1. **Requirements**
   1. A building with multiple floors.
   2. Support for multiple elevators.
   3. Movement of an elevator: up, down or idle.
   4. External displays and buttons at every floor:
      1. Input: up or down.
      2. Display: the direction and current floor of the elevator.
   5. Internal display and buttons inside each elevator:
      1. Input: the destination floor number.
      2. Display: the direction and current floor.
   6. Maximum capacity: a weight limit per elevator.
   7. Door handling: the door opens at a stop and closes after a timeout.
2. **Entities**
   1. `ElevatorSystem`: the software that runs everything. It knows the building and the elevators, and decides which elevator goes where.
   2. `Building`: name, address and its floors.
   3. `Floor`: floor number, an external display, and up/down buttons.
   4. `Elevator`: current floor, movement, an internal display, floor buttons, a weight machine, and its own queue of stops.
   5. `Movement`: an enum with `UP`, `DOWN` and `IDLE`.
   6. `Display` (interface): with `ExternalDisplay` (on a floor) and `InternalDisplay` (in a car).
   7. `Button` (interface): with `FloorButton` (↑ ↓) and `ElevatorButton` (1, 2, 3, …). They are different kinds of input with one common shape.
   8. `WeightMachine`: reports the current load, so the elevator refuses to move when it is over the limit.
   9. `SchedulingStrategy` (interface): the algorithm that picks the next stop. There are several (FCFS, SCAN, LOOK, SSTF), and the system chooses one at runtime. This is the Strategy pattern from lecture 9.
3. **Relations**
   1. `Building` → `Floor`: **composition**. Floors don't exist without the building.
   2. `Floor` → `ExternalDisplay`, `FloorButton`: **composition**. Seen as software that drives the display, rather than the physical panel, this could also be argued as association.
   3. `Elevator` → `InternalDisplay`, `ElevatorButton`, `WeightMachine`: **composition**.
   4. `ElevatorSystem` → `Building`, `Elevator`: **association**. The software uses them, and they exist physically on their own.
   5. `ExternalDisplay` and `InternalDisplay` IS-A `Display`. `FloorButton` and `ElevatorButton` IS-A `Button`. Both are **inheritance** from an interface.
   6. `ElevatorSystem` → `SchedulingStrategy`: **aggregation**. The strategy can be swapped without touching the system.
4. **UML class diagram**

   ```mermaid
   classDiagram
       class ElevatorSystem {
           -Building* building_
           -vector~Elevator*~ elevators_
           -SchedulingStrategy* strategy_
           -queue~Request~ scheduler_queue_
           +HandleRequest(Request) void
       }
       class Building {
           -string name_
           -string address_
           -vector~Floor~ floors_
       }
       class Floor {
           -int floor_no_
           -ExternalDisplay display_
           -FloorButton buttons_
       }
       class Elevator {
           -int curr_floor_
           -Movement movement_
           -InternalDisplay display_
           -ElevatorButton buttons_
           -WeightMachine weight_machine_
           -queue~int~ dispatcher_queue_
           +Move(int floor) void
           +OpenDoor() void
       }
       class Movement {
           <<enum>>
           UP
           DOWN
           IDLE
       }
       class Display {
           <<interface>>
           +Show(int floor, Movement m) void
       }
       class Button {
           <<interface>>
           +Press() void
       }
       class SchedulingStrategy {
           <<interface>>
           +PickNext(int curr_floor, vector~Request~ pending) int
       }
       ElevatorSystem --> Building
       ElevatorSystem --> Elevator
       ElevatorSystem o-- SchedulingStrategy
       Building *-- Floor
       Floor *-- ExternalDisplay
       Floor *-- FloorButton
       Elevator *-- InternalDisplay
       Elevator *-- ElevatorButton
       Elevator *-- WeightMachine
       Elevator ..> Movement
       Display <|-- ExternalDisplay
       Display <|-- InternalDisplay
       Button <|-- FloorButton
       Button <|-- ElevatorButton
       SchedulingStrategy <|.. FCFS
       SchedulingStrategy <|.. LOOK
       SchedulingStrategy <|.. SSTF
   ```

5. **Two queues**
   1. **Scheduler queue**: the requests from external users (floor buttons, like "0 ↑" or "2 ↓"). It is shared by the whole system.
   2. **Dispatcher queue**: one per elevator. It holds the floors that this elevator has committed to stop at, including the destinations pressed inside it.
   3. Flow: a floor request enters the scheduler queue. The system hands it to one elevator, and it moves into that elevator's dispatcher queue. Once an elevator's dispatcher queue is empty, the elevator is free to serve another floor.
6. **Multiple elevators: synchronization**
   1. With several elevators reading the common scheduler queue, two of them could read the same request and both go to that floor, which is bad.
   2. Fix: after reading a request, pop it out of the queue first, and make "read + pop" one atomic step guarded by a **mutex** lock. Only one elevator can take a given request.

      ```cpp
      #include <mutex>
      #include <optional>
      #include <queue>
      using namespace std;

      struct Request { int floor; int time; };

      class SchedulerQueue {
      public:
          void Push(Request r) {
              lock_guard<mutex> lock(mtx_);
              q_.push(r);
          }
          optional<Request> Take() {          // read and pop under one lock
              lock_guard<mutex> lock(mtx_);
              if (q_.empty()) return nullopt;
              Request r = q_.front();
              q_.pop();
              return r;
          }
      private:
          queue<Request> q_;
          mutex mtx_;
      };

      int main() {
          SchedulerQueue sq;
          sq.Push({2, 0});
          auto r = sq.Take();   // only one elevator thread can get this request
          return r ? 0 : 1;
      }
      ```

7. **Scheduling algorithms**
   1. **FCFS (first come, first served)**: serve requests in arrival order (FIFO). It is the brute-force version.
      1. Example: two people get in at floor 0. One wants floor 2 and the other wants 5. At floor 2 a new person gets in and wants floor 4.
      2. FCFS goes 0 → 2 → 5 → 4. It passes floor 4 on the way up, then comes back down for it. Simple, but not optimal.
      3. A smarter elevator goes 0 → 2 → 4 → 5, picking up stops on its way up. This is what SCAN and LOOK do.
   2. **SCAN**: the elevator moves fully in one direction to the **end** (the top floor), serving every request on the way, then reverses and goes fully down. It is like a disk head sweeping. It is not very efficient, because it travels to the top even when nobody is there.
   3. **LOOK**: like SCAN, but it moves only until the **last request** in the current direction, then reverses. Once there are no more upward requests above it, it comes down and keeps going down while there are requests below. This avoids the empty trips to the ends.
   4. **SSTF (shortest seek time first)**: the elevator always serves the request with the shortest travel distance from where it is now.
      1. Disadvantage: **starvation**. If floors 1–3 are the most populated, the elevator keeps serving them, and a lone request at floor 10 may never be reached.
      2. Fix: a **waiting timeout** (for example 30 minutes, or a few seconds in the demo below). Once a request has waited longer than the timeout, it is served first, regardless of distance.
      3. For implementation, we can use a priority queue ordered by (timed out first, then distance). Distance changes as the elevator moves, so the queue must be rebuilt at each stop. For a handful of requests, a simple scan does the same job.
   5. Comparison:

   | Algorithm | Picks next | Good | Bad |
   |---|---|---|---|
   | FCFS | oldest request | simple, fair | lots of back-and-forth |
   | SCAN | next request in direction, goes to the end | no starvation | empty trips to top and bottom |
   | LOOK | next request in direction, turns at the last request | no empty trips | slightly more logic |
   | SSTF | nearest request | least travel | starvation without a timeout |

   6. Choosing between these algorithms is a research-level problem. In an interview, show that the algorithm is swappable (Strategy pattern) and explain the trade-offs. You don't need the perfect algorithm.
8. **Code: swappable scheduling, with SSTF and a starvation timeout**

   ```cpp
   #include <cstdlib>
   #include <iostream>
   #include <vector>
   using namespace std;

   struct Request { int floor; int time; };   // time = when the button was pressed

   class SchedulingStrategy {
   public:
       // pending is in arrival order; returns the index of the request to serve next
       virtual size_t PickNext(int curr_floor, const vector<Request>& pending, int now) = 0;
       virtual ~SchedulingStrategy() = default;
   };

   class FCFS : public SchedulingStrategy {
   public:
       size_t PickNext(int, const vector<Request>&, int) override { return 0; }   // oldest
   };

   class SSTF : public SchedulingStrategy {
   public:
       explicit SSTF(int timeout) : timeout_(timeout) {}
       size_t PickNext(int curr_floor, const vector<Request>& pending, int now) override {
           for (size_t i = 0; i < pending.size(); ++i)          // oldest first
               if (now - pending[i].time >= timeout_) return i; // waited too long: serve it now
           size_t best = 0;
           for (size_t i = 1; i < pending.size(); ++i)
               if (abs(pending[i].floor - curr_floor) < abs(pending[best].floor - curr_floor))
                   best = i;
           return best;                                         // nearest floor
       }
   private:
       int timeout_;
   };

   class Elevator {
   public:
       Elevator(int floor, SchedulingStrategy* strategy) : curr_floor_(floor), strategy_(strategy) {}

       // Requests arrive over time; the elevator moves one floor per time unit.
       void Run(vector<Request> incoming) {
           vector<Request> pending;
           size_t next_in = 0;
           int now = 0;
           cout << "Stops:";
           while (next_in < incoming.size() || !pending.empty()) {
               while (next_in < incoming.size() && incoming[next_in].time <= now)
                   pending.push_back(incoming[next_in++]);   // new button presses
               if (pending.empty()) { now = incoming[next_in].time; continue; }   // idle

               size_t i = strategy_->PickNext(curr_floor_, pending, now);
               now += abs(pending[i].floor - curr_floor_);   // travel time
               curr_floor_ = pending[i].floor;
               cout << " " << curr_floor_ << "(t=" << now << ")";
               pending.erase(pending.begin() + i);
           }
           cout << endl;
       }
   private:
       int curr_floor_;
       SchedulingStrategy* strategy_;   // swappable at runtime
   };

   int main() {
       // From floor 0: requests for 5 and 2 at t=0, then 4 at t=1.
       vector<Request> simple = {{5, 0}, {2, 0}, {4, 1}};
       FCFS fcfs;
       SSTF sstf(1000);   // effectively no timeout
       Elevator(0, &fcfs).Run(simple);   // Stops: 5(t=5) 2(t=8) 4(t=10)
       Elevator(0, &sstf).Run(simple);   // Stops: 2(t=2) 4(t=4) 5(t=5)

       // Starvation: floor 10 asks at t=0, while floors 1-3 keep calling.
       vector<Request> busy = {{10, 0}};
       for (int i = 0; i < 40; ++i) busy.push_back({1 + i % 3, i / 2});   // two calls per time unit
       SSTF no_timeout(1000), with_timeout(8);
       Elevator(1, &no_timeout).Run(busy);     // 10 is served last, after every other request
       Elevator(1, &with_timeout).Run(busy);   // 10 is served once it has waited 8 time units
   }
   ```

   1. `Elevator` never knows which algorithm it runs. Swapping `FCFS` for `SSTF`, or adding `LOOK`, changes only the object passed in.
   2. The first two runs show the 0 → 2 → 5 → 4 example: FCFS needs 10 time units, and SSTF needs 5.
   3. The last two runs show starvation and its fix. Without a timeout, floor 10 waits until the busy floors go quiet. With a timeout, it jumps the queue once it has waited long enough.
9. **Wrapping up the course**
   1. All three case studies use the same toolkit:
      1. Classes with one job each (lectures 1 and 6).
      2. Relationships chosen by the composition, aggregation and association rules (lecture 4).
      3. A UML diagram before code (lecture 5).
      4. An interface wherever behaviour varies, with a pattern when it fits: strategy for payments and scheduling, singleton for the one shared lot or logger (lectures 7–10).
   2. For more practice, take Snake & Ladder or a booking system through the steps in lecture 11.
