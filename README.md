## 🔍 Strategy Concept: "B. Rufsen"

This strategy:

- Cooperates initially to test the opponent.
- Detects if the opponent is cooperative or exploitative.
- Punishes repeated defection but forgives occasional mistakes.
- Adapts its behavior depending on how far into the game it is, if `rounds` is known.

---

### ✅ Key Behaviors:

- **First 3 rounds**: Always cooperate.
- **After that**:
  - If opponent defected **more than 60%** of the time recently (last 5 moves), **defect**.
  - If opponent has been mostly nice (**less than 30% defections**), **cooperate**.
  - Otherwise: **mirror opponent's last move**.
- If `rounds` is known and the game is **near the end (e.g., 90% done)**, become **greedy and defect**.
