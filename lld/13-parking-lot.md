# Lecture 13: Design a Parking Lot

1. **Points to discuss (clarification questions)**
   1. **Floors:** Ask whether there are multiple floors.
   2. **Entry and exit points:** Ask whether there are multiple entry and exit points.
   3. **Vehicle types:** Ask which vehicle types must be supported.
   4. **Parking fees:** Ask how fees are charged (per hour, flat rate, different rates per spot type).
   5. **Payment methods:** Ask which methods customers use (cash, card, others).
   6. **Capacity:** Ask what happens when the lot is full.
   7. **Agreement:** In this design we agree on hourly fees that depend on the spot type. We agree on payment by cash or card. We agree on a "full" message when no matching spot is left.

2. **Requirements**
   1. **Floors:** The parking lot has multiple floors where customers can park their vehicles.
   2. **Entry and exit points:** The parking lot has multiple entry and exit points.
   3. **Ticket:** Customers collect a parking ticket at an entry point and use it to exit at an exit point.
   4. **Capacity:** The system must not allow more vehicles than the maximum capacity. If parking is full, it shows a message at the entrance panel and on the parking display board on the ground floor.
   5. **Spots:** Each floor has many parking spots. The system supports multiple types of spot: Compact, Large, Handicapped, Motorcycle.
   6. **Vehicles:** The system supports parking for different types of vehicles: car, truck, van, motorcycle.
   7. **Fees:** Fees are charged per hour by spot type. The customer pays at the exit by cash or card.

3. **Supporting use cases**
   1. **Car arrives:** A car arrives at entrance 1. The panel finds a free compact spot and issues a ticket. The display board's free count drops by one.
   2. **Lot full:** A truck arrives when every large spot is taken. The entrance panel and the ground-floor board both show "full". No ticket is issued.
   3. **Car leaves:** The car leaves through exit 2 after 3 hours. The exit panel reads the ticket and computes the fee. It takes payment by card and frees the spot.

4. **Entities**

   | Entity | Role |
   |--------|------|
   | `Vehicle` (abstract) | Has `Car`, `Truck`, `Van` and `Motorcycle` below it. Each vehicle knows which spot type it needs. |
   | `SpotType` | An enum with `COMPACT`, `LARGE`, `HANDICAPPED` and `MOTORCYCLE`. |
   | `ParkingSpot` | One spot, with an id, a type and the vehicle currently parked (or none). |
   | `ParkingFloor` | A floor number and its spots. |
   | `Ticket` | Ticket id, vehicle, spot and entry time. |
   | `EntrancePanel`, `ExitPanel` | The entry and exit points. There are several of each. |
   | `DisplayBoard` | Sits on the ground floor. It shows free spots per type, or "FULL". |
   | `PaymentStrategy` (interface) | Has `CashPayment` and `CardPayment` below it. |
   | `ParkingLot` | Owns the floors and the board, and keeps the active tickets. |

5. **Relations**

   | Relation | Type | Why |
   |----------|------|-----|
   | `Car`, `Truck`, `Van`, `Motorcycle` IS-A `Vehicle` | **Inheritance** | The lot asks any vehicle `GetSpotType()` through a base pointer (polymorphism, lecture 3). |
   | `ParkingLot` to `ParkingFloor` to `ParkingSpot` | **Composition** | Floors and spots are built with the lot and do not exist without it. |
   | `ParkingLot` to `DisplayBoard` | **Composition** | The board belongs to the lot. |
   | `ParkingSpot` to `Vehicle` | **Association** | A car comes and goes. Its life has nothing to do with the spot. |
   | `Ticket` to `Vehicle`, `ParkingSpot` | **Association** | The ticket refers to both. |
   | `EntrancePanel`, `ExitPanel` to `ParkingLot` | **Association** | Many panels use one lot. |
   | `ExitPanel` to `PaymentStrategy` | **Strategy pattern** (lecture 9) | The payment method is picked at runtime. Adding UPI later is a new class, and `ExitPanel` does not change. |

   - **Singleton:** There is only one parking lot, so `ParkingLot` could be a singleton (lecture 8). Here it is created once in `main` and passed to the panels. This keeps it easy to test.

6. **Algorithms**
   1. **Find a spot:** Go floor by floor from the ground up. Return the first free spot whose type matches the vehicle. If none is found, the lot is full for that vehicle type.
   2. **Capacity:** Never count vehicles separately. "Full" simply means "find a spot" found nothing. So the count can never drift from reality.
   3. **Fee:** Hours parked (at least 1) × the hourly rate for the spot type.
   4. **Display board:** After every entry and exit, recount the free spots per type and show them.

7. **UML class diagram**

   ```mermaid
   classDiagram
       class Vehicle {
           <<abstract>>
           -string plate_
           +GetSpotType() SpotType
       }
       Vehicle <|-- Car
       Vehicle <|-- Truck
       Vehicle <|-- Van
       Vehicle <|-- Motorcycle
       class SpotType {
           <<enum>>
           COMPACT
           LARGE
           HANDICAPPED
           MOTORCYCLE
       }
       class ParkingSpot {
           -int id_
           -SpotType type_
           -Vehicle* vehicle_
           +IsFree() bool
           +Park(Vehicle*) void
           +Free() void
       }
       class ParkingFloor {
           -int floor_no_
           -vector~ParkingSpot~ spots_
           +FindFreeSpot(SpotType) ParkingSpot*
           +FreeCount(SpotType) int
       }
       class Ticket {
           -int ticket_id_
           -Vehicle* vehicle_
           -ParkingSpot* spot_
           -int entry_hour_
       }
       class DisplayBoard {
           +Show(vector~ParkingFloor~) void
       }
       class ParkingLot {
           -vector~ParkingFloor~ floors_
           -DisplayBoard board_
           -map~int,Ticket~ active_tickets_
           +Park(Vehicle*, int hour) Ticket*
           +Unpark(int ticket_id, int hour) double
       }
       class EntrancePanel {
           -int id_
           -ParkingLot* lot_
           +Enter(Vehicle*, int hour) Ticket*
       }
       class ExitPanel {
           -int id_
           -ParkingLot* lot_
           +Exit(int ticket_id, int hour, PaymentStrategy&) void
       }
       class PaymentStrategy {
           <<interface>>
           +Pay(double amount) void
       }
       PaymentStrategy <|.. CashPayment
       PaymentStrategy <|.. CardPayment
       ParkingLot *-- ParkingFloor
       ParkingFloor *-- ParkingSpot
       ParkingLot *-- DisplayBoard
       ParkingLot o-- Ticket
       ParkingSpot --> Vehicle
       Ticket --> Vehicle
       Ticket --> ParkingSpot
       EntrancePanel --> ParkingLot
       ExitPanel --> ParkingLot
       ExitPanel ..> PaymentStrategy
       ParkingSpot ..> SpotType
   ```

8. **Code**

   ```cpp
   #include <iostream>
   #include <map>
   #include <string>
   #include <vector>
   using namespace std;

   enum class SpotType { COMPACT, LARGE, HANDICAPPED, MOTORCYCLE };
   const vector<SpotType> kAllTypes = {SpotType::COMPACT, SpotType::LARGE,
                                       SpotType::HANDICAPPED, SpotType::MOTORCYCLE};

   string Name(SpotType t) {
       switch (t) {
           case SpotType::COMPACT: return "Compact";
           case SpotType::LARGE: return "Large";
           case SpotType::HANDICAPPED: return "Handicapped";
           case SpotType::MOTORCYCLE: return "Motorcycle";
       }
       return "";
   }

   double HourlyRate(SpotType t) {
       switch (t) {
           case SpotType::COMPACT: return 20;
           case SpotType::LARGE: return 40;
           case SpotType::HANDICAPPED: return 10;
           case SpotType::MOTORCYCLE: return 10;
       }
       return 0;
   }

   // ---------- vehicles ----------
   class Vehicle {
   public:
       explicit Vehicle(string plate) : plate_(plate) {}
       virtual ~Vehicle() = default;
       virtual SpotType GetSpotType() const = 0;
       string GetPlate() const { return plate_; }
   private:
       string plate_;
   };

   class Car : public Vehicle {
   public:
       Car(string plate, bool handicapped = false) : Vehicle(plate), handicapped_(handicapped) {}
       SpotType GetSpotType() const override {
           return handicapped_ ? SpotType::HANDICAPPED : SpotType::COMPACT;
       }
   private:
       bool handicapped_;
   };

   class Truck : public Vehicle {
   public:
       using Vehicle::Vehicle;
       SpotType GetSpotType() const override { return SpotType::LARGE; }
   };

   class Van : public Vehicle {
   public:
       using Vehicle::Vehicle;
       SpotType GetSpotType() const override { return SpotType::LARGE; }
   };

   class Motorcycle : public Vehicle {
   public:
       using Vehicle::Vehicle;
       SpotType GetSpotType() const override { return SpotType::MOTORCYCLE; }
   };

   // ---------- spots and floors ----------
   class ParkingSpot {
   public:
       ParkingSpot(int id, SpotType type) : id_(id), type_(type) {}
       bool IsFree() const { return vehicle_ == nullptr; }
       void Park(Vehicle* v) { vehicle_ = v; }
       void Free() { vehicle_ = nullptr; }
       int GetId() const { return id_; }
       SpotType GetType() const { return type_; }
   private:
       int id_;
       SpotType type_;
       Vehicle* vehicle_ = nullptr;   // association
   };

   class ParkingFloor {
   public:
       ParkingFloor(int floor_no, map<SpotType, int> spots_per_type) : floor_no_(floor_no) {
           int id = floor_no * 100;
           for (auto [type, count] : spots_per_type)
               for (int i = 0; i < count; ++i) spots_.emplace_back(++id, type);
       }
       ParkingSpot* FindFreeSpot(SpotType type) {
           for (auto& spot : spots_)
               if (spot.GetType() == type && spot.IsFree()) return &spot;
           return nullptr;
       }
       int FreeCount(SpotType type) const {
           int n = 0;
           for (auto& spot : spots_) n += (spot.GetType() == type && spot.IsFree());
           return n;
       }
       int GetFloorNo() const { return floor_no_; }
   private:
       int floor_no_;
       vector<ParkingSpot> spots_;   // composition
   };

   // ---------- ticket, board, payment ----------
   struct Ticket {
       int ticket_id;
       Vehicle* vehicle;
       ParkingSpot* spot;
       int entry_hour;
   };

   class DisplayBoard {   // on the ground floor
   public:
       void Show(const vector<ParkingFloor>& floors) {
           cout << "  [Board]";
           for (SpotType t : kAllTypes) {
               int free = 0;
               for (auto& f : floors) free += f.FreeCount(t);
               cout << " " << Name(t) << ": " << (free ? to_string(free) : "FULL");
           }
           cout << endl;
       }
   };

   class PaymentStrategy {
   public:
       virtual void Pay(double amount) = 0;
       virtual ~PaymentStrategy() = default;
   };
   class CashPayment : public PaymentStrategy {
   public:
       void Pay(double amount) override { cout << "  Paid Rs " << amount << " in cash" << endl; }
   };
   class CardPayment : public PaymentStrategy {
   public:
       void Pay(double amount) override { cout << "  Paid Rs " << amount << " by card" << endl; }
   };

   // ---------- the lot ----------
   class ParkingLot {
   public:
       explicit ParkingLot(vector<ParkingFloor> floors) : floors_(floors) {}

       Ticket* Park(Vehicle* v, int hour) {
           for (auto& floor : floors_) {   // ground floor first
               if (ParkingSpot* spot = floor.FindFreeSpot(v->GetSpotType())) {
                   spot->Park(v);
                   int id = next_ticket_id_++;
                   active_tickets_[id] = {id, v, spot, hour};
                   board_.Show(floors_);
                   return &active_tickets_[id];
               }
           }
           board_.Show(floors_);   // shows FULL for this type
           return nullptr;
       }

       double Unpark(int ticket_id, int hour) {
           auto it = active_tickets_.find(ticket_id);
           if (it == active_tickets_.end()) return -1;   // unknown ticket
           Ticket t = it->second;
           int hours = max(1, hour - t.entry_hour);
           double fee = hours * HourlyRate(t.spot->GetType());
           t.spot->Free();
           active_tickets_.erase(it);
           board_.Show(floors_);
           return fee;
       }
   private:
       vector<ParkingFloor> floors_;   // composition
       DisplayBoard board_;            // composition
       map<int, Ticket> active_tickets_;
       int next_ticket_id_ = 1;
   };

   // ---------- entry and exit points ----------
   class EntrancePanel {
   public:
       EntrancePanel(int id, ParkingLot* lot) : id_(id), lot_(lot) {}
       Ticket* Enter(Vehicle* v, int hour) {
           cout << "Entrance " << id_ << ": " << v->GetPlate() << endl;
           Ticket* t = lot_->Park(v, hour);
           if (t) cout << "  Ticket " << t->ticket_id << ", spot " << t->spot->GetId() << endl;
           else cout << "  Parking full for " << Name(v->GetSpotType()) << endl;
           return t;
       }
   private:
       int id_;
       ParkingLot* lot_;   // association
   };

   class ExitPanel {
   public:
       ExitPanel(int id, ParkingLot* lot) : id_(id), lot_(lot) {}
       void Exit(int ticket_id, int hour, PaymentStrategy& payment) {
           cout << "Exit " << id_ << ": ticket " << ticket_id << endl;
           double fee = lot_->Unpark(ticket_id, hour);
           if (fee < 0) cout << "  Invalid ticket" << endl;
           else payment.Pay(fee);
       }
   private:
       int id_;
       ParkingLot* lot_;
   };

   int main() {
       ParkingLot lot({
           ParkingFloor(0, {{SpotType::COMPACT, 2}, {SpotType::LARGE, 1}, {SpotType::HANDICAPPED, 1}}),
           ParkingFloor(1, {{SpotType::COMPACT, 2}, {SpotType::MOTORCYCLE, 2}}),
       });
       EntrancePanel entrance1(1, &lot), entrance2(2, &lot);
       ExitPanel exit1(1, &lot), exit2(2, &lot);

       Car car("KA-01-1234");
       Truck truck("KA-02-5678");
       Van van("KA-03-9999");

       Ticket* car_ticket = entrance1.Enter(&car, 9);   // 9 am
       entrance2.Enter(&truck, 10);                     // takes the only large spot
       entrance1.Enter(&van, 11);                       // full for Large

       CardPayment card;
       exit2.Exit(car_ticket->ticket_id, 12, card);     // 3 hours * Rs 20
   }
   ```

   1. **Read order:** `car_ticket` is read before `Exit` because `Unpark` erases the ticket from the map. The pointer is invalid after that.
   2. **New vehicle type:** An electric car needing a charging spot means one new `SpotType` value and one new `Vehicle` subclass. The floors, panels and lot do not change.
9. **Next:** The last case study is the most algorithm-heavy: an elevator system, where the hard part is deciding which elevator goes where.
