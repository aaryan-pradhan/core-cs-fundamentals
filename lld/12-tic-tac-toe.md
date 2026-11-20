# Lecture 12: Design Tic-Tac-Toe

1. **Points to discuss (clarification questions)**
   1. Game description: how the game is played.
   2. Rules:
      1. Winner: three of the same mark in a row, column or diagonal.
      2. Loser: the other player.
      3. Draw: the board is full and nobody has won.
      4. Illegal moves: a cell that is out of range or already taken.
      5. Timeouts? What happens if a player doesn't move.
      6. First move: who starts.
   3. Generalizing to an N×N board.
   4. Leaderboard.
   5. Player ratings.
   6. Settle these in the first 3–5 minutes. In this design we agree on 3×3, a toss for the first move, and no timeouts, leaderboard or ratings.
2. **Requirements**
   1. Game setup: the game initializes a 3×3 board.
   2. Players: two players take turns.
   3. Moves: a player places their mark (X or O) on the board.
   4. Win conditions: the game checks whether a player has won.
   5. Draw condition: the game checks for a draw when the board is full.
   6. Game flow: the game alternates between players until there is a win or a draw.
   7. Validation: moves must be valid, for example the chosen cell must be empty.
   8. User interface: display the board and prompt players for their moves.
   9. First move: the game starts with a toss to decide which player goes first.
3. **Entities**
   1. `User`: a real person, with id, name and country. A user exists before and after any game.
   2. `GamePlayer`: a user's role in one game, meaning the user plus their symbol (X or O).
   3. `Board`: the 3×3 grid. It applies moves, validates them and judges the result.
   4. `GameStatus`: an enum with `WIN`, `DRAW` and `NOT_ENDED`.
   5. `GameDisplay`: everything printed on screen.
   6. `PlayerInput`: where moves come from (keyboard, network, a test script).
   7. `Game`: ties it all together and runs the turns.
4. **Relations**
   1. `GamePlayer` → `User`: **aggregation**. A game player has a user, but the user outlives the game.
   2. `Game` → `GamePlayer`: **composition**. Players are created for this game and end with it.
   3. `Game` → `Board`: **composition**. The board belongs to one game and dies with it.
   4. `Game` → `GameDisplay`, `PlayerInput`: **association**. The game uses them, but they are created outside and could serve many games.
   5. `Board` → `GameStatus`: `Judge()` returns one.
   6. Keeping display and input separate from `Board` is the single responsibility principle in action. The same board logic works with a console, a web page or a test script.
5. **Algorithms**
   1. **Start**:
      1. Toss: `rand() % 2` decides who is first.
      2. Decide the first and second player.
      3. Display the empty board.
      4. Run turns until the game ends.
   2. **One turn**:
      1. Display whose turn it is.
      2. The player gives a move (r, c).
      3. Validate the move. If it is invalid, show an error and ask again.
      4. `PlayTurn(r, c, symbol)` places the mark.
      5. Check for a win or a draw. If the game is not over, switch players.
   3. **Judge**: check all 3 rows, 3 columns and 2 diagonals for three equal non-empty marks. If one is found, it is a `WIN` for the player who just moved. If not, and the board is full, it is a `DRAW`. Otherwise the game is `NOT_ENDED`.
6. **UML class diagram**

   ```mermaid
   classDiagram
       class User {
           -int user_id_
           -string name_
           -string country_
           +GetId() int
           +GetName() string
       }
       class GamePlayer {
           -char symbol_
           -User* user_
           +GetSymbol() char
           +GetUser() User*
       }
       class Board {
           -char board_[3][3]
           +PlayTurn(int r, int c, char symbol) void
           +IsValidMove(int r, int c) bool
           +Judge() GameStatus
       }
       class GameStatus {
           <<enum>>
           WIN
           DRAW
           NOT_ENDED
       }
       class GameDisplay {
           +DisplayBoard(Board) void
           +DisplayPlayerTurn(GamePlayer) void
           +AnnounceWinner(GamePlayer) void
           +AnnounceDraw() void
           +DisplayInvalidMove(GamePlayer) void
       }
       class PlayerInput {
           +GetMove() pair~int,int~
       }
       class Game {
           -Board board_
           -GamePlayer player1_
           -GamePlayer player2_
           -GameDisplay* display_
           -PlayerInput* input_
           +Start() void
       }
       GamePlayer o-- User
       Game *-- GamePlayer
       Game *-- Board
       Game --> GameDisplay
       Game --> PlayerInput
       Board ..> GameStatus
   ```

7. **Code**

   ```cpp
   #include <cstdlib>
   #include <ctime>
   #include <iostream>
   #include <sstream>
   #include <string>
   #include <utility>
   using namespace std;

   enum class GameStatus { WIN, DRAW, NOT_ENDED };

   class User {
   public:
       User(int user_id, string name, string country)
           : user_id_(user_id), name_(name), country_(country) {}
       int GetId() const { return user_id_; }
       string GetName() const { return name_; }
   private:
       int user_id_;
       string name_;
       string country_;
   };

   class GamePlayer {
   public:
       GamePlayer(char symbol, User* user) : symbol_(symbol), user_(user) {}
       char GetSymbol() const { return symbol_; }
       User* GetUser() const { return user_; }
   private:
       char symbol_;
       User* user_;   // aggregation: the user outlives the game
   };

   class Board {
   public:
       Board() {
           for (auto& row : board_)
               for (char& cell : row) cell = '.';
       }
       bool IsValidMove(int r, int c) const {
           return r >= 0 && r < 3 && c >= 0 && c < 3 && board_[r][c] == '.';
       }
       void PlayTurn(int r, int c, char symbol) { board_[r][c] = symbol; }
       char Get(int r, int c) const { return board_[r][c]; }

       GameStatus Judge() const {
           for (int i = 0; i < 3; ++i) {
               if (Line(board_[i][0], board_[i][1], board_[i][2])) return GameStatus::WIN;   // row
               if (Line(board_[0][i], board_[1][i], board_[2][i])) return GameStatus::WIN;   // column
           }
           if (Line(board_[0][0], board_[1][1], board_[2][2])) return GameStatus::WIN;      // diagonal
           if (Line(board_[0][2], board_[1][1], board_[2][0])) return GameStatus::WIN;      // anti-diagonal
           for (auto& row : board_)
               for (char cell : row)
                   if (cell == '.') return GameStatus::NOT_ENDED;
           return GameStatus::DRAW;   // full board, no winner
       }
   private:
       static bool Line(char a, char b, char c) { return a != '.' && a == b && b == c; }
       char board_[3][3];
   };

   class GameDisplay {
   public:
       void DisplayBoard(const Board& board) {
           for (int r = 0; r < 3; ++r) {
               for (int c = 0; c < 3; ++c) cout << board.Get(r, c) << ' ';
               cout << endl;
           }
       }
       void DisplayPlayerTurn(const GamePlayer& p) {
           cout << p.GetUser()->GetName() << " (" << p.GetSymbol() << "), your move (r c): " << endl;
       }
       void AnnounceWinner(const GamePlayer& p) { cout << p.GetUser()->GetName() << " wins!" << endl; }
       void AnnounceDraw() { cout << "It's a draw." << endl; }
       void DisplayInvalidMove(const GamePlayer& p) {
           cout << "Invalid move by " << p.GetUser()->GetName() << ", try again." << endl;
       }
   };

   class PlayerInput {
   public:
       explicit PlayerInput(istream& in) : in_(in) {}   // cin for a real game
       pair<int, int> GetMove() {
           int r, c;
           in_ >> r >> c;
           return {r, c};
       }
   private:
       istream& in_;
   };

   class Game {
   public:
       Game(User* u1, User* u2, GameDisplay* display, PlayerInput* input)
           : player1_('X', u1), player2_('O', u2), display_(display), input_(input) {}

       void Start() {
           GamePlayer* current = (rand() % 2 == 0) ? &player1_ : &player2_;   // toss
           GamePlayer* other = (current == &player1_) ? &player2_ : &player1_;
           display_->DisplayBoard(board_);

           while (true) {
               display_->DisplayPlayerTurn(*current);
               auto [r, c] = input_->GetMove();
               if (!board_.IsValidMove(r, c)) {
                   display_->DisplayInvalidMove(*current);
                   continue;   // same player tries again
               }
               board_.PlayTurn(r, c, current->GetSymbol());
               display_->DisplayBoard(board_);

               GameStatus status = board_.Judge();
               if (status == GameStatus::WIN) { display_->AnnounceWinner(*current); return; }
               if (status == GameStatus::DRAW) { display_->AnnounceDraw(); return; }
               swap(current, other);
           }
       }
   private:
       Board board_;           // composition
       GamePlayer player1_;    // composition
       GamePlayer player2_;
       GameDisplay* display_;  // association
       PlayerInput* input_;    // association
   };

   int main() {
       srand(time(nullptr));
       User alice(1, "Alice", "India"), bob(2, "Bob", "India");

       // Scripted moves so the demo runs by itself; pass cin to play for real.
       // The first player takes the left column and wins on their third move.
       istringstream moves("0 0  0 1  1 0  1 1  2 0");
       PlayerInput input(moves);
       GameDisplay display;

       Game game(&alice, &bob, &display, &input);
       game.Start();
   }
   ```

   1. **Generalizing to N×N** only changes `Board`. It needs an `n_` size and a `vector<vector<char>>` grid, and `Judge` loops over `n` instead of 3. `Game`, `GameDisplay` and `PlayerInput` don't change. That is the payoff of keeping the rules inside `Board`.
   2. A **leaderboard** would be a new class that `Game` reports results to, which is another association. Nothing existing needs editing.
8. Next: a bigger real-world system with many object types and a capacity rule: the parking lot.
