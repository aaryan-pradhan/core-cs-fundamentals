# Lecture 11: How to Approach LLD Questions

1. An LLD interview question is short and open. Examples are "Design Tic-Tac-Toe" and "Design a parking lot".

   > **Interview:** The interviewer judges the **process** as much as the final code. Follow the steps below in order.

2. **The steps**

   1. **Listen:** Hear exactly what problem statement they give you. Do not start designing in your head halfway through.

   2. **Clarification questions:** The statement is vague on purpose. Ask about scope, rules and edge cases. Spend at least 3 to 5 minutes understanding the problem clearly.
      1. **Tic-Tac-Toe example:** Is the board always 3×3, or N×N? How is the first move decided? Is a leaderboard needed?

   3. **Requirements:** Write down the agreed list of what the system must do. This list is the contract for everything after it.

   4. **Supporting use cases:** Walk through the system from the user's point of view. Each use case must be covered by the design.
      1. **Example:** "A player places X at (1, 1). The board shows it. The turn passes to O."
      2. **Marks:** Steps 1 to 4 together carry a big share of the marks, roughly 30%, before any class is drawn.

   5. **Entities:** Pick out the nouns from the requirements. They become the classes: `Board`, `Player`, `Game`, `ParkingSpot`, `Ticket`, `Elevator`.

   6. **Relations between entities:** For each pair, decide the relation. Lecture 4's rules settle each case.

      | Relation | Meaning |
      |----------|---------|
      | IS-A | Inheritance |
      | Part of | Composition |
      | Has a | Aggregation |
      | Uses a | Association |

   7. **Algorithms:** Name the non-trivial logic and how it works. Examples: how a winner is checked, how a free spot is found, which elevator answers a request.

   8. **UML class diagram:** Draw the classes with attributes, methods and relationship arrows (lecture 5). This is the main deliverable.

   9. **Code:** Implement the core classes and the main flow.
      - **Payoff:** If the interview reaches code with a clean diagram behind it, you have most likely already cleared it.

3. **Habits that help at every step**

   1. **Single responsibility (S):** Keep each class to one responsibility. Put interfaces wherever behaviour varies (O, D).
   2. **Patterns only when needed:** Reach for a pattern only when the problem asks for it.

      | Problem says | Use |
      |--------------|-----|
      | Create one of many types | Factory |
      | Swap the algorithm | Strategy |
      | Exactly one shared thing | Singleton |
      | Stack optional extras | Decorator |

   3. **Trade-offs:** Say them out loud. A slightly worse design that is explained clearly scores better than a silent perfect one.

4. **Important LLDs to practise**

   1. Design Tic-Tac-Toe (lecture 12)
   2. Design a Parking Lot (lecture 13)
   3. Design an Elevator system (lecture 14)
   4. Implement a Logger singleton (lecture 8)
   5. Design Snake & Ladder
   6. Design a Booking system (movie tickets, hotel rooms)

5. **More worked designs**

   1. https://github.com/prasadgujar/low-level-design-primer/tree/master
   2. https://github.com/tssovi/grokking-the-object-oriented-design-interview

6. **Next:** The steps applied end to end, on the classic warm-up question: Tic-Tac-Toe.
