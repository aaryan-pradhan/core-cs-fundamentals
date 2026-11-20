# Lecture 11: How to Approach LLD Questions

1. An LLD interview question is short and open, like "Design Tic-Tac-Toe" or "Design a parking lot". The interviewer judges the **process** as much as the final code. Follow these steps in order.
2. **The steps**
   1. **Listen**: hear exactly what problem statement they are giving. Don't start designing in your head halfway through.
   2. **Clarification questions**: the statement is vague on purpose. Ask about scope, rules and edge cases. Spend at least 3–5 minutes understanding the problem clearly.
      1. Example for Tic-Tac-Toe: always 3×3, or N×N? How is the first move decided? Is a leaderboard needed?
   3. **Requirements**: write down the agreed list of what the system must do. This list is the contract for everything after it.
   4. **Supporting use cases**: walk through the system from the user's point of view. "A player places X at (1, 1). The board shows it. The turn passes to O." Each use case must be covered by the design.
      1. Steps 1–4 together carry a big share of the marks (roughly 30%), before any class has been drawn.
   5. **Entities**: pick out the nouns from the requirements. They become the classes: `Board`, `Player`, `Game`, `ParkingSpot`, `Ticket`, `Elevator`.
   6. **Relations between entities**: for each pair, decide IS-A (inheritance), part of (composition), has a (aggregation), or uses a (association). Lecture 4's rules settle each case.
   7. **Algorithms**: name the non-trivial logic and how it will work. Examples: how a winner is checked, how a free spot is found, which elevator answers a request.
   8. **UML class diagram**: draw the classes with attributes, methods and the relationship arrows (lecture 5). This is the main deliverable.
   9. **Code**: implement the core classes and the main flow. If the interview reaches code with a clean diagram behind it, you have most likely already cleared it.
3. **Habits that help at every step**
   1. Keep each class to one responsibility (S), and put interfaces wherever behaviour varies (O, D).
   2. Reach for a pattern only when the problem asks for it. Use a factory for "create one of many types", strategy for "swap the algorithm", singleton for "exactly one shared thing", and decorator for "stack optional extras".
   3. Say your trade-offs out loud. A slightly worse design that is explained clearly scores better than a silent perfect one.
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
6. Next: the steps applied end to end, on the classic warm-up question: Tic-Tac-Toe.
