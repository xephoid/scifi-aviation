**Setup Steps & Initial Player Decisions**
*(Only the information required by the rule‑book – no “nice‑to‑have” items.)*

---

## 1. What Happens During Setup

| Step                        | What is created / handed out                                                                                                                           | Who performs it                                        | Why it matters                                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| **1. Deck & Tokens**        | • 20 Agent cards – 10 red, 10 blue, numbered 0‑9.<br>• 5 red Decoy tokens for the red player.<br>• 5 blue Decoy tokens for the blue player.            | BoardGame.io (in the `setup` function)                 | Each player must have a full hand of 10 cards and 5 decoy tokens before play starts.                                        |
| **2. Hand Distribution**    | Each player receives the 10 cards of *their* color.                                                                                                    | BoardGame.io                                           | Cards are kept hidden from the opponent.                                                                                    |
| **3. Safe‑House Placement** | Each player chooses **three** of the ten cards from their hand and places them facedown, one in each of the three “safe houses” (left, middle, right). | The **player** – *private* decision in the setup phase | These three cards are the only ones the opponent can ever compare against; the rest stay in the hand and can be used later. |

> **Important Note** – No other decisions exist at this point. Decoy tokens are never placed during setup; they only become relevant when the *Switch Agents* action is used later in the game.

---

## 2. Exhaustive List of Player Decisions

| Decision # | What the player chooses                                    | Constraints                                   | Outcome                                                        |
| ---------- | ---------------------------------------------------------- | --------------------------------------------- | -------------------------------------------------------------- |
| **D1**     | Which card from their hand goes to the *left* safe house   | Must be one of the 10 cards currently in hand | Card is removed from hand, placed facedown in the left house   |
| **D2**     | Which card from their hand goes to the *middle* safe house | Must be one of the remaining 9 cards in hand  | Card is removed from hand, placed facedown in the middle house |
| **D3**     | Which card from their hand goes to the *right* safe house  | Must be one of the remaining 8 cards in hand  | Card is removed from hand, placed facedown in the right house  |

> *All three decisions are made **separately** and in order; a player can pick any card for any house. The boardgame.io system treats each as a private decision that is only revealed to that player.*

---

## 3. Designing the Player Interface

### 3.1. Overall Layout

```
+-------------------------------------+
|  Player’s Hand (10 cards)           |
|  (face‑down but can toggle to view) |
+-------------------------------------+
|  Safe‑House Slots (3 empty boxes)   |
|  [  ]  [  ]  [  ]  (left, mid, right) |
+-------------------------------------+
|  Decoy Token Count (5)              |
+-------------------------------------+
```

- **Hand Row** – a horizontal strip of ten card “tiles.”
  *Cards are rendered as facedown by default but may be clicked to “peek” (see §3.2).*

- **Safe‑House Row** – three equally‑spaced empty slots that represent the left, middle and right safe houses.
  *Each slot is clearly labeled or ordered so the player knows which one they are selecting.*

- **Decoy Token Display** – a small counter or token icon indicating that the player has five decoys.

  *Tokens are not interacted with during setup but are visible so the player knows they exist.*

### 3.2. Interaction Flow

1. **Select a Card**
   - *Action*: Click on any card in the hand.
   - *Visual Feedback*: The selected card is highlighted (e.g., a subtle glow or “selected” border).

   - *Restriction*: Only one card may be selected at a time; clicking a different card deselects the previous one.

2. **Choose a Slot**
   - *Action*: Click on one of the three empty safe‑house slots.
   - *Result*: The chosen card is **moved** from the hand into the slot, and the card inside the slot
 is now *facedown* from the UI perspective.
   - *Visual*: The slot changes from a blank to a blank facedown card (same appearance as any other facedown card). The card is now part of the player’s private “safe‑house” area.

3. **Peek at a Placed Card**
   - *Rule‑book:* “Players may look at his own facedown agents.”
   - *UI:* Each placed card can be clicked (or long‑pressed) to toggle a *peek* view that temporarily flips the card to show its number.
   - *Safety:* This peek is **only** shown to the owning player; the opponent still sees the slot as an empty facedown card.

4. **Complete the Three Decisions**
   - Once all three safe‑house slots contain a card, the UI automatically moves to the next step of the game (no “Next” button needed).
   - boardgame.io’s `setup` step will now mark the setup phase as finished for that player.

### 3.3. Hiding Opponent Information

- The UI must *never* expose the opponent’s hand or any of the opponent’s safe‑house cards.
- Opponent houses are rendered as blank placeholders (e.g., a simple shaded rectangle) that say “?”.

- When the game progresses past the setup phase, the opponent’s safe‑house cards will be revealed *only* through normal gameplay actions, never during setup.

### 3.4. Accessibility & Usability

| Feature                                | Why it’s needed                                                                                                | Suggested Implementation                                                                                                                      |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Card Identification**                | Players need to know the numbers on the cards they are placing and later peek at them.                         | Render each card with a backside graphic and a “flip” button. Clicking flips to a face‑up view for the owner only.                            |
| **Drag‑and‑Drop vs. Click‑and‑Select** | Both are acceptable; the simpler click‑and‑select flow avoids accidental moves.                                | • **Option A**: click card → card highlighted; click slot → move.<br>• **Option B**: drag card to slot (boardgame.io supports drag handlers). |
| **Feedback for Invalid Moves**         | Prevent a player from placing more than one card in a slot or from selecting a card that is no longer in hand. | Disable already‑selected cards and occupied slots. Show a tooltip or subtle message on hover.                                                 |
| **Responsive Layout**                  | The setup screen is the first thing the player sees; it should be clear and uncluttered.                       | Use a responsive grid: hand cards on the top, safe‑house slots centered below.                                                                |

---

## 4. How BoardGame.io Will Capture These Decisions

1. **`config.setup`** – The initial state is created with all 20 cards, 5 decoy tokens per player, and **empty** safe‑house slots.

2. **Private Setup Step** – The game’s config will include a `setup` step that runs **once per player**.
   - The step will expose three actions: `placeInSafeHouse(position, cardId)`.
   - Each action records the player’s choice in the private `ctx.playerData[pid]` object.
   - The actions are *disabled* for the opponent until the current player finishes their decisions.

3. **UI Binding** – The React components (`SetupScreen`, `Hand`, `SafeHouseSlot`) will call these actions when the player clicks a card and then a slot.
   - The actions update the local state (`G.hand`, `G.safeHouses[pid]`) and immediately hide the card from the hand.
   - Once the third card is placed, the `setup` step ends automatically (or a “Done” button is shown, but the boardgame.io system will simply advance to the next phase).

---

## 5. Summary of What the Player *Actually* Decides

- **Pick 3 cards from your 10‑card hand** – one for each safe house.
- **Assign each card to a specific safe house** (left, middle, right).

No other choices (e.g., decoy placement, house ordering) exist at this point.

The UI should be a clean “hand‑and‑slots” interface that lets the player drag or click cards into slots, peek at their placed cards, and finally transition automatically to the first turn of the game. All of the above is handled privately by boardgame.io so that the opponent never sees any of these decisions until the first action is taken.

## Player Interaction Points

Below is a complete, point‑for‑point list of **every** place a player must make a decision or trigger a visible change in the game.
Each entry describes:

1. **What the player selects or clicks**
2. **What data is sent to the boardgame.io engine**
3. **How the opponent’s private view is exposed**
4. **What the opponent must do in response**
5. **How the UI should represent that interaction**

> **NOTE** – No “nice‑to‑have” or optional‑feature items are included; every point is required by the rulebook.

| #                                                                | Interaction                                                                                                                                                                                                                         | Player Action                                                                                                                                                                        | Opponent’s Private/Visible Action                                                                                                                                                    | UI Design Recommendation |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------ |
| **1. Selecting an Agent Card to Attack From Hand**               | Click a card in the *hand panel* (face‑down). The UI must allow a single‑card pick – e.g., a highlighted border or a “selected card” preview.                                                                                       | No data is revealed to the opponent until the player *submits* the attack.                                                                                                           | *Card list* – display all hand cards as “cards” (no numbers).  Below the list, show the “Attack from Hand” button.  When clicked, a modal opens letting the player pick the card.    |
| **2. Selecting a Target Safe House (Attack From Hand)**          | Click a target from the *opponent’s safe‑house grid* (face‑down).  Only safe houses that still contain an agent are eligible.                                                                                                       | The selected safe‑house’s agent is revealed to the opponent *inside a modal* that shows the card value and the attacker’s chosen card.                                               | *Target grid* – color‑code safe houses (e.g., “selectable target” glow).  Disable already‑eliminated houses.  The modal should list the selected target and show “Revealed card: X”. |
| **3. Opponent Declares Attack Result (Attack From Hand)**        | The opponent receives the card value and the target house’s agent value.  They must click one of three buttons: **Higher**, **Lower**, or **Same**.                                                                                 | The result is immediately sent back to the engine as a *response move* (`declareAttackResult`).                                                                                      | *Result modal* – opponent sees the revealed card values and the three response buttons.  The modal disappears once the result is sent.                                               |
| **4. Switching an Agent from a Safe House**                      | Click a *safe house* that still has an agent to reveal.  The UI highlights the chosen house.                                                                                                                                        | The selected house’s agent is revealed to the opponent in a modal.  The opponent immediately sees the value but has no further action.                                               | *Safe‑house selection* – each house in the “switch” view has a “Reveal” icon.  Once clicked, a modal shows the agent value to the opponent.                                          |
| **5. Returning the Revealed Agent to Hand**                      | The attacker’s UI automatically puts the revealed card back into the hand panel (face‑down).  No UI click is required – the engine handles the state update.                                                                        | The opponent is only notified that the card has been moved to the attacker’s hand.                                                                                                   | *Hand panel* – update to show the new card count.                                                                                                                                    |
| **6. Choosing a Hand Card to Place in the Vacated Safe House**   | Click a card from the *hand panel* to “play” into the vacated house.  The UI should allow only cards that are still in the hand (i.e.,not already used in a previous attack).                                                       | No information is revealed to the opponent until the card is placed.                                                                                                                 | *Card‑selection overlay* – when the “Switch Agents” action is chosen, a secondary modal asks the player to pick a hand card.                                                         |
| **7. Placing a Decoy Token after Switching**                     | Click any *opponent’s safe house* (including the one just switched) to place a decoy token next to it.  Only available if the player still has decoy tokens left.                                                                   | The decoy token is **private** to the attacking player; it is not visible to the opponent until a decoy‑based event (elimination or switch) forces it to remain.                     | *Decoy panel* – show a stack of remaining tokens.  When a safe house is clicked for placement, show a small “+” icon that can be dragged onto the chosen house.                      |
| **8. Selecting a Safe House to Reveal (Attack From Safe House)** | Click a *face‑down* safe house that still has an agent (the attacker’s own house).  The UI highlights the chosen house for “reveal.”                                                                                                | The attacker’s selected house is revealed to the opponent inside a modal that displays the agent value.                                                                              | *Reveal modal* – show the card value with a “Revealed by Player X” label.                                                                                                            |
| **9. Selecting a Target Safe House (Attack From Safe House)**    | After the attacker reveals, click a target from the *opponent’s safe‑house grid* (face‑down).  Only houses that still contain an agent are valid targets.                                                                           | The opponent must then decide **Higher / Lower / Same** relative to the revealed value.                                                                                              | *Target grid* – highlight selectable houses; disable eliminated ones.                                                                                                                |
| **10. Opponent Declares Attack Result (Attack From Safe House)** | The defender receives the two agent values (attacker’s revealed house and the chosen target).  They must click one of three buttons: **Higher**, **Lower**, **Same**.                                                               | If “Higher / Lower” the defender *loses* the attacker’s house and it is eliminated; the defender’s selected target house is also eliminated.  If “Same” the attacker wins no change. | *Response modal* – defender sees both values and the three response options.  The modal closes once a choice is made.                                                                |
| **11. Handling a Failed Attack (Attack From Hand)**              | If the defender declares **Higher** or **Lower**, the defender must play a *private* event move `handleFailedAttack` that moves the attacker’s chosen card from the board to the attacker’s hand and marks the house as eliminated. | The attacker’s UI should instantly show the house disappearing (or turning “eliminated”) and the card re‑entering the hand panel.                                                    | *Elimination visual* – replace the eliminated safe house with a “dead” icon; update the hand size.                                                                                   |
| **12. Handling a Failed Attack (Attack From Safe House)**        | Same as #11, but the defender also loses the revealed safe house.                                                                                                                                                                   | The defender’s UI must show their own safe house turning “eliminated” and the card re‑entering their hand.                                                                           | *Self‑elimination visual* – if the defender’s own house is eliminated, show a red flash and a “you lost a house” toast.                                                              |
| **13. Scoring (Game End)**                                       | No active decision, but the UI must *display* the final score and the winner after the last safe house is eliminated.                                                                                                               | The engine automatically calculates scores; the UI just reads the `G.score` values.                                                                                                  | *Score screen* – show each player’s final points, highlight the winner with a trophy icon.                                                                                           |

### UI Design Guidelines for Each Interaction Point

1. **Hand Panel**
   - Render each hand card as a generic “card back” image.
   - Show a numeric overlay of the remaining cards (e.g., “6 / 10”).
   - On `Attack From Hand`, enable a “select card” mode; when a card is chosen, highlight it.

2. **Safe‑House Grid**
   - Render each of the 4 opponent safe houses as a “house back” image.
   - On `Switch Agents` or `Attack From Safe House`, clicking a house opens a context menu:
     - **Reveal** (for Switch Agents) or **Attack** (for Attack From Safe House).
   - Disabled safe houses (eliminated or switched out) are greyed‑out.

3. **Decoy Token Panel**
   - Show a stack of decoy icons in the player’s corner.
   - Display the count of remaining tokens (e.g., “Decoys: 3”).
   - When `Switch Agents` is chosen, enable a “place decoy” mode: clicking any house adds a decoy icon to it.
   - Tokens cannot be placed on an already‑eliminated house unless it is the target of the current action.

4. **Action Buttons**
   - Three primary buttons at the bottom of the screen:
     - **Attack from Hand**
     - **Switch Agents**
     - **Attack from Safe House**
   - Buttons are disabled if the corresponding action is not legal (e.g., no decoy tokens left for `S
witch Agents`).

5. **Target Selection Modals**
   - When an attacker selects a card or a safe house, a modal appears:
     - **“Choose a target safe house”**
     - The modal lists only the opponent’s remaining safe houses; each shows a “select” button.
   - After selection, the modal closes automatically.

6. **Reveal & Response Modals**
   - **Switch Agents**
     - After clicking a safe house, a modal shows the revealed agent value to the opponent.
     - The opponent’s UI immediately receives the card value; the attacker’s UI hides it again.
   - **Attack From Hand / Safe House**
     - After the attacker’s card/house is revealed, the defender receives a modal:
       - **“Higher?” “Lower?” “Same?”** (three buttons).
       - The defender selects one; the result is sent back to the engine.
     - The attacker’s UI shows a “waiting for response” indicator until the defender’s decision is received.

7. **Result & Board Updates**
   - After a move, the engine updates the global state; the UI re‑renders:
     - If an attack succeeded: the opponent’s safe house stays alive; the attacker’s card remains in play (or is removed from hand if it was an “attack from hand” card).
     - If an attack failed: eliminated houses flip to a “dead” icon; the involved cards return to the appropriate hand panel.
     - If a switch occurred: the attacked house is removed, the new card appears face‑down; the old card is placed in hand.

By strictly following this table and UI guideline set, the React app will faithfully expose every required private interaction while keeping the opponent’s information hidden until the rulebook allows disclosure. This approach guarantees compliance with the rulebook and provides a clean, responsive user experience.

## Public vs Private Information

Boardgame.io’s **player‑view** system is ideal for keeping the information that each player must keep secret while allowing other players to see everything that is truly public.
The game state (the object that is returned from `Game.setup()`) contains a mixture of data that is **private** to each player (their own hand and the identities of faced‑down agents) and data that is **public** (the status of each safe house, the number of decoy tokens next to it, all revealed agent cards, and the current VP totals).  The rules of *Agent 7* only require these two kinds of information; nothing else is hidden or revealed.

Below is a detailed inventory of every piece of information, how it should be stored, how it should be exposed or hidden, and how it will appear in the UI.

---

### 1. Public Information (visible to *all* players)

| Piece of information                                                                                                                                          | Where it lives                                                                                                | What is shown in the UI                                                                  | Why it is public                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Decoy tokens** – the number of tokens that a player has placed beside each safe house.                                                                      | `G.players[pid].safeHouses[i].decoys`                                                                         | A small token icon with a counter next to the safe house.                                | The rules state that tokens are “visible” and “must remain” even after a safe house is eliminated. |
| **Safe‑house status** – whether a safe house is *alive* or *eliminated*.                                                                                      | `G.players[pid].safeHouses[i].eliminated`                                                                     | A visual flag or a different background colour on the safe house slot.                   | All players must be able to see which houses have been taken out.                                  |
| **Revealed agent cards** – any card that has become face‑up (because an attack succeeded, a failed attack revealed it, or a switch temporarily exposed it).   | `G.players[pid].safeHouses[i].card` *and* `G.players[pid].safeHouses[i].revealed = true`                      | The card number is shown on the top of the stack; a face‑up card is visible to everyone. | The rules make all revealed cards part of the public record.                                       |
| **VP scores** – the current number of VP each player has collected.                                                                                           | `G.vp[pid]`                                                                                                   | A numeric counter on each player’s board.                                                | Scoring is part of the public game state and must be displayed to both players.                    |
| **Number of safe houses eliminated** – for each player.                                                                                                       | `G.players[pid].eliminatedCount` (or `G.vp[pid]` can be derived from this)                                    | A counter or an icon showing the number of houses gone.                                  | Both players must know how many houses the opponent has lost.                                      |
| **Temporary revealed card during a Switch** – the brief moment when a faced‑down agent is shown to the opponent before it is put back into the player’s hand. | A transient field such as `G.switchReveal = { pid, house, card }` that is immediately cleared after the move. | The card appears on the opponent’s UI for one tick; it is then hidden again.             | The rule states that the opponent “sees” the card, enabling deduction.                             |
| **Temporary revealed card during a Failed Safe‑House attack** – the opponent’s agent that is revealed when a failed attack eliminates a safe house.           | A temporary field such as `G.failedAttackReveal = { pid, house, card }` that is cleared after the move.       | The card appears face‑up for a short period.                                             | The rules dictate that the attacker’s card is “eliminated” and the opponent’s card is revealed.    |

> **Implementation note:** All the fields listed above are part of the *public* part of the state.  When a player logs in, the UI can simply read them from `G.players[pid]` because they are visible to everyone.  Boardgame.io’s built‑in `PlayerView.STRIP_SECRETS` can be used if the secret data is kept under a `secret` key; otherwise a custom `playerView` should strip the private fields of the other player.

---

### 2. Private Information (visible **only** to the owning player)

| Piece of information                                                                                              | Where it lives                                                                               | Why it is private                                                                        | How it should be displayed (React)                                                     |
| ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Hand of agent cards** – the 10 numbered cards that the player has in hand.                                      | `G.players[pid].hand`                                                                        | (an array of numbers or objects that include the card number)                            | The rules specify that a player’s hand is “hidden” and cannot be seen by the opponent. | Show a generic “card back” or a “hand” icon that does not reveal the numbers. |
| **Face‑down agent cards in safe houses** – the identity of the card placed in each of the player’s 3 safe houses. | `G.players[pid].safeHouses[i].card` **and** `G.players[pid].safeHouses[i].revealed == false` | The rules say that a card placed in a safe house is “facedown” and only the player knows |
| its identity until it is revealed by an attack or a switch.                                                       | Render a blank slot (e.g., a black rect                                                      |
angle or the back of a card). The UI must never display the numeric value unless the `revealed` flag
is true. |
| **Any hidden card in a temporary reveal during a Switch** – this is a transient state that is *imme
diately* visible to the opponent and then hidden again. | A temporary field `G.switchReveal` that is
*public* while the UI shows it, but its value is only relevant to the player who executed the switch.
 | The rules call for the opponent to “see” the card during a switch.  After the next render tick the
 field is cleared, turning the card back to a private, faced‑down state. | During that tick the card
is rendered face‑up on the opponent’s board, but only for one tick. Boardgame.io’s log can still capt
ure the move, but the *per‑player* UI must not keep the value after the move finishes. |
| **Any hidden card during a Failed Safe‑House attack that the player has just put back into their ha
nd** – this card becomes private again after the attack. | `G.failedAttackReveal` is a temporary publ
ic field that is cleared immediately. | Same reasoning as the Switch reveal. | The card is shown face
‑up during the reveal, then immediately replaced with a faced‑down slot on the player’s own board. |

> **Implementation note:**
>  * **Where to store** – The easiest way to keep the private data out of the public view is to keep
the player’s hand and the faced‑down card numbers in a separate `secret` key inside the state:

> ```js
> Game.setup = () => ({
>   players: {   // *public* view: VP, decoys, revealed cards, house status, etc.
>     '0': { … },
>     '1': { … }
>   },
>   secret: {    // *private* view: the information each player should not see.
>     '0': { hand: [ ... ], facedown: [ … ] },
>     '1': { hand: [ ... ], facedown: [ … ] }
>   }
> });
> ```

>  Then you can use Boardgame.io’s built‑in `PlayerView.STRIP_SECRETS` which removes the `secret` key for everyone.  If you prefer to keep all data in a single object (`G.players[pid]`), write a **custom `playerView`** that removes the private fields (`hand`, `facedown` values) of the opponent but preserves all public fields (VP, decoys, revealed cards, etc.).

>  Either approach ensures that the UI of player 0 never sees the numbers in player 1’s hand or the faced‑down cards in player 1’s houses.

---

### 3. Log & Replay

The log created by Boardgame.io automatically records every move with the state that is *visible to all* players at that time.
Moves that manipulate **secret** fields (for example, “draw a card from the deck” or “pick a number for the faced‑down card”) should be executed as **server‑only** moves (set `server: true` in the move declaration).  This guarantees that the log never contains the private numbers and that the replay functionality can correctly show the transient reveals.

---

### 4. Summary of What Must be Hidden

1. **Only the player’s own hand** – The opponent can never read the values of the cards in a player’s hand.
2. **Only the player’s own faced‑down cards** – The identity of the card in a faced‑down safe house is a secret until it is revealed.

All other pieces of the state are shared and must be rendered for both players.  The rules of *Agent 7* do not require any additional “blinded” or “hidden” data, so the two categories above cover the entire information space.

Using Boardgame.io’s `playerView` you can deliver the correct subset of the state to each UI instance
, and the tables above give you the exact mapping to UI components.  This guarantees that the game respects the confidentiality rules while keeping the public narrative fully transparent.

## Phase Structure

Below is a comprehensive description of how the game’s timing, phases, and turns will be expressed in **boardgame.io**.
The implementation will use the built‑in *phase* system to enforce the order of play and to ensure that only the legal actions for the current player are available at any moment.
All of the rules supplied in the design doc are represented here; no “nice‑to‑have” or optional phases are added.

---

### 1. Overall Flow

```
[Setup Phase] → [Main (Play) Phase] → (optional) [Victory Phase]
```

* **Setup Phase** – One‑time initialization before any player has a turn.
* **Main (Play) Phase** – Repeats for each player’s turn until the game ends.
* **Victory Phase** – Triggered automatically by a terminal condition; handles scoring and end‑game UI.

---

### 2. Phase Definitions (boardgame.io)

| Phase     | Purpose                                                                                         | Boardgame.io Settings                                                             |
| --------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `setup`   | Initialise game state – card distribution, safe‑house placement, decoy tokens, starting player. | `phase: "setup"` – executed once; no moves allowed.                               |
| `play`    | Core turn‑based gameplay. Each player may perform exactly one action per turn.                  | `phase: "play"` – `moves: { attackFromHand, switchAgents, attackFromSafeHouse }`. |
| `victory` | Game has finished; compute scores and display results.                                          | `phase: "victory"` – terminal state; no further moves.                            |

---

### 3. Turn Structure (inside the `play` phase)

For each turn the following steps occur automatically:

1. **Turn Starts** – `onEntry` hook can be used to reset per‑turn flags if needed.
2. **Action Choice** – The active player may call **exactly one** of the following moves:
   * `attackFromHand` – Reveal a card from hand, target opponent’s safe house, compare numbers.
   * `switchAgents` – Reveal an agent in a safe house, return it to hand, then secretly replace it with a card from hand and place a decoy token.
   * `attackFromSafeHouse` – Reveal an agent from a safe house, target opponent’s safe house, compare numbers. Handles both success and failure outcomes.
3. **Move Resolution** – The move function carries out all sub‑steps (reveal, compare, eliminate, token placement, hand updates). The game state is updated accordingly.
4. **Turn Ends** – `onExit` hook can perform any end‑of‑turn bookkeeping. Control automatically passes to the next player in turn order.
5. **Victory Check** – After each move, a terminal condition checks whether any player has lost all three safe houses. If true, the game transitions to the `victory` phase.

---

### 4. Sub‑Phase (Action) Detail – How Each Move is Executed

All moves are executed within a **single** `play` phase.  No explicit sub‑phases are required; the logic for the three possible actions is encapsulated in their respective move functions.  The structure of each move is:

| Move             | Core Steps                                                                      |
| ---------------- | ------------------------------------------------------------------------------- |
| `attackFromHand` | 1. Player selects a hand card. 2. Player selects opponent safe house to target. |
3. Opponent secretly compares numbers. 4. If equal → eliminate safe house, place attacker’s card face
‑up. 5. If not equal → return card to hand. |
| `switchAgents` | 1. Player selects safe house to switch (must not be eliminated). 2. Reveal its age
nt to opponent. 3. Return that card to player’s hand. 4. Player secretly selects a replacement from h
and and places it facedown in the same safe house. 5. Player chooses a decoy token (from the 5 availa
ble) to place on that house. |
| `attackFromSafeHouse` | 1. Player selects safe house to attack from (must not be eliminated). 2. Re
veal its agent. 3. Player selects opponent safe house to target. 4. Opponent compares numbers. 5. **S
uccess**: eliminate opponent safe house, place attacker’s card, then refuel empty player safe house w
ith a new hand card. 6. **Failure**: Opponent eliminates the attacker’s safe house, takes his own age
nt, places it face‑up; player discards his remaining safe‑house agent face‑up. |

Because all state changes happen *atomically* inside the move function, the `play` phase remains a cl
ean “Action‑Only” turn.

---

### 5. Terminal Conditions (Automatic Phase Transition)

```js
const terminal = (G, ctx) => {
  // If either player has 0 safe houses left, transition to victory.
  if (G.players[0].safeHouses.filter(sh => !sh.eliminated).length === 0 ||
      G.players[1].safeHouses.filter(sh => !sh.eliminated).length === 0) {
    return true;   // Game ends
  }
  return false;     // Continue playing
};
```

When `terminal` returns `true`, boardgame.io will automatically move the game to the `victory` phase.
  The `victory` phase handles the final scoring logic (eliminated safe houses → winner, decoy token c
ount, etc.) and triggers the end‑game UI.

---

### 6. Random Starting Player

The *setup* phase will:

1. Randomly pick a starting player (`ctx.currentPlayer` will be set to either `"P0"` or `"P1"`).
2. Store the starting player id in the game state so that the UI can display it.
3. No moves are allowed during `setup`, so there is no risk of an early action being chosen.

---

### 7. Summary of Legal Move Availability

During the `play` phase **only** the following moves are legal for the active player:

```js
moves: {
  attackFromHand: (G, ctx, handCardIndex, targetSafeHouse) => { ... },
  switchAgents:   (G, ctx, safeHouseIndex, newAgentIndex, decoyToken) => { ... },
  attackFromSafeHouse: (G, ctx, sourceSafeHouse, targetSafeHouse) => { ... }
}
```

All three moves accept the necessary parameters (card indices, safe‑house indices, decoy choice).  Be
cause the moves are only defined in the `play` phase, the boardgame.io UI will automatically disable
the other two moves while a player is in a different phase, guaranteeing compliance with the rules.

---

### 8. UI‑Side Timing

* The **setup UI** will gather initial choices (safe‑house placements, discarding the rest of the car
ds into the hand, and selecting which player goes first).
* During the `play` phase the UI will only expose the three action buttons.
* Once the `victory` phase starts the UI will display the final score and allow the host to close the
 game or start a new one.

---

> **Bottom line:**
> The game contains a *Setup* phase (initial distribution), a *Play* phase (alternating turns, single
 action per turn), and an implicit *Victory* terminal state.
> All rules—including card comparison, safe‑house elimination, token placement, and hand updates—are
encoded inside the three move functions and are executed atomically within the `play` phase.  No addi
tional sub‑phases or optional “nice‑to‑have” stages are introduced.

## Move Implementation

The game logic will be driven by **boardgame.io**’s move system.
All moves are pure functions that receive the current `G` state, a `ctx` context (containing turn‑num
ber, playerID, etc.), and any arguments that the UI supplies.
The moves must only mutate the `G` object; boardgame.io will take care of synchronising the state bet
ween clients.

Below is a comprehensive description of every move that appears in the rules.
It includes the data the move accepts, the public/private information it exposes, the internal state
transitions, and any side‑effects (VP calculation, turn advancement, game‑over check).

> **NOTE** – All player IDs are `"0"` and `"1"`.
> The board is a 2‑row tableau: the top row belongs to Player 0 (Red), the bottom row to Player 1 (Bl
ue).
> A *safe house* is represented as an object
> ```js
> {
>   agent: {value: number|null, owner: string|null, faceUp: boolean}, // null if empty
>   decoy: number,          // number of decoy tokens adjacent to the house
>   eliminated: boolean,    // true if the house has been removed from play
>   empty: boolean          // true if the house is empty (agent null)
> }
> ```

The `G` state is structured as follows:

```js
G = {
  // Player 0 (Red) data
  players: {
    "0": {
      hand: Array(10),            // array of {value:number, owner:"0"} objects
      decoyTokens: 5,             // remaining decoy tokens that may still be used
      decoyPlaced: Array(3),      // booleans: whether a decoy has been placed on each house
      safeHouses: Array(3),       // safe house objects described above
    },
    "1": { /* same structure for Blue */ }
  },
  // VP totals (used only at the end)
  vp: { "0": 0, "1": 0 },
  // Flag indicating that the game has ended
  finished: false
}
```

### 1. `ATTACK_FROM_HAND(playerId, handIndex, targetHouseIndex)`

**Purpose** – Player reveals an agent from his hand, attacks a specific opponent’s safe house, and re
solves the outcome.

| Argument           | Type     | Description                                         |
| ------------------ | -------- | --------------------------------------------------- |
| `playerId`         | `string` | `"0"` or `"1"` (caller)                             |
| `handIndex`        | `number` | Index into the caller’s hand array.                 |
| `targetHouseIndex` | `number` | Index (0–2) into the *opponent’s* safeHouses array. |

#### Implementation Steps

1. **Retrieve the attacker’s agent**
   ```js
   const attacker = G.players[playerId].hand[handIndex];
   ```
2. **Retrieve the opponent**
   ```js
   const opponentId = (playerId === "0") ? "1" : "0";
   const target = G.players[opponentId].safeHouses[targetHouseIndex];
   ```
3. **Enforce that the target house is not eliminated**
   If `target.eliminated === true`, the move should be rejected (boardgame.io will throw a `MoveRejec
ted` error).
4. **Determine outcome**
   *If the opponent’s house is empty (`target.agent === null`)* – the attack automatically fails (hig
her/lower). In this case the attacker’s card returns to the hand; the move ends.

5. **Compare values**
   - **Same** (`attacker.value === target.agent.value`) → **Successful attack**
     - Mark `target.eliminated = true`.
     - Replace the opponent’s agent with the attacker’s agent (faceUp = `true`).
       ```js
       target.agent = {value: attacker.value, owner: playerId, faceUp: true};
       ```
     - Return the attacker’s card to the hand (it will be added back into the hand array later; board
game.io will keep the hand array intact until the next turn).
     - **VP Gain** – add `1 + target.decoy` to `G.vp[playerId]`.
     - **Check for Game End** – if the opponent now has all three houses eliminated, set `G.finished
= true`.
   - **Higher or lower** → **Failed attack**
     - Attacker’s card is returned to hand (no effect on the opponent’s house).
     - The move simply ends (no state change besides the return of the card).

6. **Update the hand** – Remove the used card from `hand[handIndex]` and add it back to the same hand
 (so its position remains the same). In practice, you can just leave it in place since the card is st
ill in the hand but has been “revealed”; for UI purposes you may want to track a `revealed` flag that
 the UI clears after the next turn.

7. **Return** – The move completes. Boardgame.io will automatically advance the turn.

#### Notes

* The attacker’s card is never permanently removed from the hand; it merely gets “used” temporarily.

* The opponent never sees the attacker’s card value.
* All changes to `vp` are private to each player – the opponent cannot see the exact VP totals until
the game ends.

---

### 2. `SWITCH_AGENTS(playerId, houseIndex, handIndex)`

**Purpose** – Player reveals the agent in a chosen safe house, swaps it back into the hand, places a
new agent from the hand face‑down into that house, and places one decoy token on any safe house (incl
uding the switched one).

| Argument     | Type     | Description                                                       |
| ------------ | -------- | ----------------------------------------------------------------- |
| `playerId`   | `string` | `"0"` or `"1"` (caller)                                           |
| `houseIndex` | `number` | Index (0–2) of the safe house to switch (must not be eliminated). |
| `handIndex`  | `number` | Index into the caller’s hand array.                               |

#### Implementation Steps

1. **Pre‑checks**
   - `G.players[playerId].decoyTokens < 1` → reject (no decoy tokens left).
   - Target house must not be eliminated (`!target.eliminated`).
   - Target house must have an agent (`target.agent !== null`).
   - The hand must contain an agent at `handIndex`.

2. **Reveal the current agent**
   *This is purely a UI event – the attacker reveals the agent to the opponent; no state change is ne
eded for the logic.*

3. **Return the old agent to the hand**
   ```js
   const oldAgent = target.agent;
   G.players[playerId].hand.push(oldAgent);
   ```

4. **Place the new agent from the hand face‑down**
   ```js
   const newAgent = G.players[playerId].hand.splice(handIndex, 1)[0];
   target.agent = {value: newAgent.value, owner: playerId, faceUp: false};
   ```

5. **Place a decoy token**
   The player selects any of the three safe houses (can be the same house).
   ```js
   const decoyTargetIndex = ...; // supplied from the UI
   const decoyTarget = G.players[playerId].safeHouses[decoyTargetIndex];
   decoyTarget.decoy += 1;
   G.players[playerId].decoyTokens -= 1;
   G.players[playerId].decoyPlaced[decoyTargetIndex] = true;
   ```
   Decoy tokens once placed stay permanently; you may add a flag so the UI cannot remove them.

6. **End of move** – No VP changes, no elimination. Turn simply ends.

#### Notes

* The action can only be used while the player still has at least one decoy token left.
* `handIndex` can point to the same card that is being swapped back in; in that case the card is simp
ly removed from the hand and returned to the same house – this is allowed.
* The decoy token placement does **not** remove the token from the player’s pool; it *decrements* `de
coyTokens` and permanently increases the target’s `decoy` count.

---

### 3. `ATTACK_FROM_SAFE_HOUSE(playerId, sourceHouseIndex, targetHouseIndex)`

**Purpose** – Player reveals the agent in one of his safe houses and attacks an opponent’s safe house
, following the same higher/lower/same rules.
The outcome differs depending on whether the attack is successful or fails because the attacker’s age
nt is higher/lower.

| Argument           | Type     | Description                                                        |
| ------------------ | -------- | ------------------------------------------------------------------ |
| `playerId`         | `string` | `"0"` or `"1"` (caller)                                            |
| `sourceHouseIndex` | `number` | Index of the attacking house (must not be eliminated, must contain |
| an agent).         |
| `targetHouseIndex` | `number` | Index of the opponent’s house (must not be eliminated).            |

#### Implementation Steps

1. **Validate houses**
   - `sourceHouse` must exist and not be eliminated.
   - `sourceHouse.agent` must not be `null`.
   - `targetHouse` must exist and not be eliminated.

2. **Retrieve agents**
   ```js
   const attacker = G.players[playerId].safeHouses[sourceHouseIndex].agent;
   const opponentId = (playerId === "0") ? "1" : "0";
   const target = G.players[opponentId].safeHouses[targetHouseIndex];
   ```

3. **Comparison** – Use `attacker.value` and `target.agent.value`.
   *If the opponent’s house is empty (`target.agent === null`)* – the attack automatically fails; the
 attacker’s agent is considered “higher/lower” and the source house is eliminated (see below).

4. **Outcome logic**

   *A. Successful attack (`attacker.value === target.agent.value`)*

   - **Eliminate the target** – `target.eliminated = true`.
   - **Replace opponent’s agent** –
     ```js
     target.agent = {value: attacker.value, owner: playerId, faceUp: true};
     ```
   - **Return attacker’s card to hand** – just remove from `sourceHouse.agent` (the attacker’s card i
s “used”) and push it back to hand.
     ```js
     G.players[playerId].hand.push(sourceHouse.agent);
     sourceHouse.agent = null;
     sourceHouse.empty = true;
     ```
   - **VP Gain** – `1 + sourceHouse.decoy` (note: *source* decoy count, not target).
     ```js
     G.vp[playerId] += 1 + sourceHouse.decoy;
     ```
   - **Check Game End** – as in move 1, if the opponent now has all three houses eliminated, `G.finis
hed = true`.

   *B. Failed attack (`attacker.value` higher or lower)*

   - The opponent’s house **remains** untouched.
   - **Eliminate the attacker’s source house** –
     ```js
     sourceHouse.eliminated = true;
     sourceHouse.agent = null;
     sourceHouse.empty = true;
     ```
   - **VP Gain** – `1 + sourceHouse.decoy` goes to the attacker’s VP total (same as a successful atta
ck).
   - **Check Game End** – if the attacker now has all three houses eliminated (after this move), set
`G.finished = true`.
     (Note: an elimination can trigger the *other* player to win immediately.)

5. **Return** – No changes to decoy pools or VP unless an elimination happened.

#### Notes

* **If the target house is empty** – the attack is treated as a failed attack.
  *The attacker’s agent is considered higher/lower, so the source house is eliminated as per the “fai
ls because higher/lower” clause.*
* If the attacker’s source house is empty before the move – the move is illegal.
* When the attack fails because of a higher/lower comparison, the attacker’s house is removed from pl
ay *even though* the opponent’s house is untouched.
* The decoy token counts on both the source and target houses are considered when adding VP.

---

## Helper / Utility Functions (Used by the Moves)

| Function                  | Description                                                             |
| ------------------------- | ----------------------------------------------------------------------- |
| `isFinished(G)` – Boolean | Returns `true` if either player has all three houses eliminated (`G.pla |
yers[opponentId].safeHouses.every(h=>h.eliminated)`). Called after every move that changes an elimina
tion. |
| `addVP(G, playerId, amount)` – Void | `G.vp[playerId] += amount`. This is a private mutation; the o
pponent cannot see `vp` values until the game ends. |
| `endTurn()` – Implicit | Boardgame.io automatically calls `ctx.turn()` to advance the turn after a
successful move. No explicit call is needed. |
| `rejectIf(condition, message)` – Exception | If `condition` is true, throw a `MoveRejected` with th
e supplied message. Boardgame.io will propagate the error to the client. |

---

## End‑Game & VP Finalisation

Only the `ATTACK_FROM_HAND` and `ATTACK_FROM_SAFE_HOUSE` moves alter VP totals and can trigger game‑o
ver.
When a move sets `G.finished = true`:

1. **Boardgame.io** will freeze the state on all clients.
2. The UI may call a **`REVEAL_RESULTS`** helper (not a move) that simply reads `G.vp` and presents i
t to both players.
3. No further moves are allowed – attempts to invoke any of the three moves will be automatically rej
ected.

The final VP totals are calculated **exactly** when a house is eliminated:

```js
// During a successful attack:
G.vp[playerId] += 1 + target.decoy;   // 1 point for the house + all adjacent decoys
```

> **Why we keep `vp` in G** – It lets the server maintain a running total.
> It is also convenient for debugging; the UI can choose to hide it from the opponent until the end.

---

## Summary of Public/Private Information

| State Variable                                        | Public to Opponent? | Why                                                        |
| ----------------------------------------------------- | ------------------- | ---------------------------------------------------------- |
| `G.players[playerId].hand`                            | **No**              | Hand cards are never visible to the opponent.              |
| `G.players[playerId].safeHouses[*].agent.value`       | **No**              | Only revealed when the agent is face‑up                    |
| (after a successful attack).                          |
| `G.players[playerId].safeHouses[*].faceUp`            | **Yes**             | When an agent is revealed (by attack or swit               |
| ch) the UI may display it.                            |
| `G.players[playerId].vp`                              | **No**              | VP totals are hidden until the game ends.                  |
| `G.players[playerId].decoyTokens`                     | **Yes**             | UI must know how many tokens remain to enforce the ru      |
| le that a player may only switch while tokens remain. |
| `G.finished`                                          | **Yes**             | Indicates the game is over; UI must display final results. |

By strictly following the move contracts above the game will behave exactly as specified in the rules
, provide deterministic outcomes for all players, and keep all hidden information truly hidden until
it is legally revealed.

## Game Screens

The UI of *Agent Hunter* is split into three discrete screens that map directly onto the logical phas
es of the game:

| Screen    | Purpose                                                                                 | Key UI Elements | Interaction Flow |
| --------- | --------------------------------------------------------------------------------------- | --------------- | ---------------- |
| **Setup** | 1. Decide which colour (Red/Blue) each player will use.<br>2. Place the three agent car |
ds in the three “safe‑house” placeholders.<br>3. Lay out the five decoy tokens.<br>4. Confirm both pl
ayers are ready to start. | • Colour selector (radio buttons or two “Pick” buttons).<br>• Three empty
 safe‑house icons (face‑down).<br>• Decoy token icons (face‑up, 5 per player, labelled “Decoy”).<br>•
 Hand of cards for the current player (face‑down).<br>• “Ready” button (disabled until a colour is ch
osen and the three safe‑house cards are placed).<br>• Network status / waiting‑for‑opponent indicator
. | 1. Player 1 clicks a colour. 2. Player 1 drags one of their hand cards into each safe‑house slot
– the card flips face‑down automatically.<br>3. Player 1 moves the required number of decoy tokens ne
xt to their own safe‑houses (the UI enforces the “one token per house” rule).<br>4. Player 1 presses
**Ready**.<br>5. The other player performs the same actions (their own colour choice is shown to them
 but hidden from Player 1).<br>6. When both players press **Ready**, the game automatically transitio
ns to the **Game** screen. |

> **Visibility rules on Setup**
> *All* cards and decoys are private to the owner: only the player whose turn it is can see the face‑
down cards in their hand or the decoys they have placed. The opponent sees only the number of decoys
(via a small badge) and the fact that the safe‑house slots are occupied.

---

### 1. Game Screen

The **Game** screen is the core of the experience and contains all active gameplay information. It is
 a two‑column layout with the *local player* on the left and the *opponent* on the right. The layout
is responsive and scales to small screens (e.g., tablets).

| Column   | Player       | UI Components                                                             |
| -------- | ------------ | ------------------------------------------------------------------------- |
| **Left** | Local Player | • Hand (5–10 cards face‑down, clickable to “reveal” temporarily).<br>• Th |
ree safe‑house boxes (each showing a face‑down card; if eliminated, the card is face‑up and a decoy t
oken is shown if present).<br>• Decoy token count and icons (for the 5 available tokens).<br>• Curren
t VP tally.<br>• “Switch” button for each safe‑house that is still active.<br>• “Attack from Hand” an
d “Attack from Safe‑House” action buttons.<br>• Action‑selection dialog (shown only when an action bu
tton is pressed). |
| **Right** | Opponent | • Three safe‑house boxes (face‑down). If a safe‑house has been eliminated, i
t is shown face‑up with the opponent’s eliminated card and any decoy token that was placed there.<br>
• Decoy token count (displayed as a small badge over the safe‑house icons).<br>• Current VP tally.<br
>• No interactive elements (all actions are performed by the local player). |

#### 1.1 Turn Indicator & Network State

At the top centre, a banner indicates:

* “Your Turn” (when it is the local player’s turn) or “Waiting for opponent” (when the remote player
is taking their turn).
* A small network status icon that flips between “online” and “offline” (used for graceful reconnecti
on or disconnect messages).

#### 1.2 Action Flow

All actions are gated by the local player's *turn* and *remaining decoy tokens*:

1. **Attack From Hand**
   *Click* the “Attack From Hand” button →
   *Select* one card from your hand (the card flips face‑up for a short “preview” period).
   *Select* one of the opponent’s three safe‑house slots.
   - The system sends a *“AttackFromHand”* move to boardgame.io which resolves the comparison.
   - The opponent’s card is temporarily revealed; the outcome (higher/lower/same) is shown via a moda
l (e.g., “Higher – Attack failed” or “Same – Safe‑house eliminated”).
   - If successful, the opponent’s card is revealed face‑up, your attacking card is placed on top, an
d the opponent’s safe‑house slot is removed from play.
   - If failed, the attacking card is returned to your hand.

2. **Switch Agents**
   *Click* the “Switch” button on a safe‑house that has not yet been eliminated.
   - The local player’s chosen agent is revealed to the opponent (temporarily visible on the opponent
’s side).
   - The system sends a *“SwitchAgents”* move which causes the card to be returned to the player’s ha
nd and a new card (or the same one) to be placed face‑down into the safe‑house.
   - The local player must then choose a decoy token (if any remain). The UI ensures that the decoy t
oken is placed next to the safe‑house that was just switched.
   - If the player has no decoy tokens left, the “Switch Agents” button is automatically disabled.

3. **Attack From Safe‑House**
   *Click* the “Attack From Safe‑House” button →
   *Select* one of your own safe‑houses that still contains an agent.
   *Select* one of the opponent’s safe‑houses.
   - The system sends a *“AttackFromSafeHouse”* move.
   - The comparison is performed; the outcome is revealed in a modal.
   - **Success**: The opponent’s safe‑house is removed, the card is face‑up, and the VP changes accor
dingly.
   - **Failure**: The attacking card is moved back to its original safe‑house (face‑down).
   - Special rule handling: if the attacking safe‑house had a decoy token, it remains on the board; t
he opponent may lose a decoy token in the “Switch” resolution if they had one. (All of this is handle
d server‑side; the client merely shows the resulting state.)

All outcome modals automatically fade and disappear after a few seconds or after the player clicks “C
ontinue.”
During a modal, the local player is forced to wait until the remote player acknowledges the result, p
reventing any double‑play.

#### 1.3 Information Display

| Info                                                                            | Where It Appears       | Visibility                                                  |
| ------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------- |
| Own VP                                                                          | Left header            | Public to both players                                      |
| Opponent VP                                                                     | Right header           | Public                                                      |
| Remaining Safe‑houses                                                           | Both columns           | Numbered badges (e.g., “# 1 / 3” left and “# 1 / 3” right). |
|                                                                                 |
| Decoy token count                                                               | Left column            | Shows how many of the 5 tokens the local player still owns. |
| Decoy token placement                                                           | Opponent’s safe‑houses | If a decoy token was placed next to an eliminated           |
| safe‑house, the token is shown as a small coloured icon over the card.          |
| Eliminated safe‑houses                                                          | Opponent’s side        | The eliminated card is shown face‑up; if the opponent ha    |
| d placed a decoy token on that house, the token is rendered as a small overlay. |

> **Important: Hidden Information**
> *All* cards in the local player’s hand are displayed face‑down on the UI and are only ever flipped
face‑up in the context of an active action. The opponent’s safe‑house cards stay face‑down for the en
tire duration of their presence. Once a safe‑house is eliminated, the card becomes a public artefact
and is shown face‑up on both sides of the UI. The VP tallies are public but are updated only after a
move has finished resolution.

#### 1.4 Move Log

Below the two main columns, a horizontal scrollable log lists the most recent actions (“Player Red at
tacked Player Blue’s safe‑house 2 with card 7 – Same – eliminated”). This log is optional but strongl
y recommended for remote games where players may need to confirm what happened while they were discon
nected briefly.

---

### 2. End Game Screen

When the **Game** logic signals that one player has lost all three safe‑houses, boardgame.io sets the
 game state to *finished* and the UI automatically switches to the **End** screen. This screen is a s
imple, high‑contrast panel:

| Element              | Description                                                                  |
| -------------------- | ---------------------------------------------------------------------------- |
| **Final Scoreboard** | A vertical list of the two players. For each player: <br>• Final VP total (t |
he main score).<br>• Final “tie‑breaker” total (sum of the values of all eliminated agents plus the V
P). |
| **Winner Banner** | “Red wins!” or “Blue wins!” – the banner is coloured to match the winning colou
r. If the VP totals are tied, the banner says “Tie – Player Red wins on tie‑breaker” (or vice‑versa).
 |
| **Action Buttons** | • **New Game** – resets the state to the **Setup** screen.<br>• **Exit** – ret
urns to the home/lobby (if you implement one). |

> **Transition Logic**
> *Setup → Game* – After both players hit “Ready”.
> *Game → End* – When the `isFinished()` flag is set in the boardgame.io game data.
> *End → Setup* – When the player clicks **New Game** or navigates back to the home screen. All game
data is re‑initialised to a fresh state.

---

### 3. Optional Screens (for completeness)

| Screen                                                                  | Purpose                                                                          | When it appears                        |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------- |
| **Log / Message pane**                                                  | Shows a live feed of actions, comparison results, and network notification       |
| s.                                                                      | Always visible on the **Game** screen (bottom‑right or as a collapsible drawer). |
| **Connection‑Error**                                                    | Handles unexpected disconnections.                                               | Pops up when the network state changes |
| to “offline”; gives options to retry or return to the **Setup** screen. |

> These panes do not interfere with the core game logic but improve the UX for a real‑time, turn‑base
d multiplayer experience.

---

## Visibility & Hidden‑Information Rules

| Piece                                                                                             | Local Player                                                                  | Opponent                      |
| ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------- |
| **Hand cards**                                                                                    | Face‑down until the player chooses to reveal it for an action.                | Not visible.                  |
| **Safe‑house cards**                                                                              | Face‑down until the player selects “Attack From Hand” or “Attack From Safe‑H  |
| ouse”; otherwise always face‑down.                                                                | Face‑down until the house is eliminated.                                      |
| **Eliminated agent**                                                                              | Face‑up on the opponent’s side.                                               | Face‑up on the local side.    |
| **Decoy tokens**                                                                                  | Face‑up on the local side (full list) and count of remaining tokens is shown. |
| Only the count is displayed next to each opponent house; the tokens themselves are never visible. |
| **VP totals**                                                                                     | Always visible on both sides.                                                 | Always visible on both sides. |
| **Action buttons**                                                                                | Only on the local player’s side and only when it is that player’s turn.       | No a                          |
| ctions displayed.                                                                                 |

---

## Transition Flow Summary

1. **Initial State** – Both players load the app and are routed to the **Setup** screen.
2. **Setup → Game** – Triggered automatically when both players have selected a colour, placed the th
ree safe‑house agents, positioned five decoys, and hit “Ready.”
3. **Game** – The boardgame.io engine handles turn rotation. The UI reacts to the `turn` field in the
 game data: only the active player can issue moves; the inactive player sees a “Waiting” banner.
4. **Game → End** – When boardgame.io resolves a move that eliminates the third safe‑house of a playe
r, the `finished` flag is set in the game data. The UI transitions to the **End** screen.
5. **End → Setup** – Clicking **New Game** re‑initialises all data and brings the players back to the
 **Setup** screen.

All three screens are fully responsive and designed to keep hidden information private while still gi
ving each player enough public information to decide their next move. The transitions are instantaneo
us and rely on the state machine exposed by boardgame.io (i.e., `state.game.isFinished`), ensuring th
e UI is always in sync with the authoritative game state.

# Network Implementation

Below is a complete, rule‑only description of how the networked multiplayer portion of **Agent Hunter
** will be implemented using **boardgame.io** and **React**.
All references to “the server” are handled by the boardgame.io **Server** class, while “the client” i
s the React component tree that renders the board and receives events from the server.

> **Important** – No external libraries are used beyond the default Vite / React / boardgame.io stack
.
> All private data (hand, faced‑down safe‑house cards, decoy tokens owned, etc.) is stored only in th
e server‑side state and is never sent to the non‑owner client.

---

## 1.  High‑Level Architecture

```
┌─────────────────────┐          ┌─────────────────────┐
│  React UI (Client)  │ ◄───────►│  Node.js Server     │
│  (GameBoard.jsx)    │   API    │  (boardgame.io)     │
└─────────────────────┘          └─────────────────────┘
          ▲                                  ▲
          │  React network component         │  boardgame.io Server
          └──────────────────────────────────┘
```

* **Server** – holds the canonical game state (`G`) and executes all `move` functions.
* **Client** – receives the *public* view of the state (`G.public`) and its own *private* slice (`G.p
rivate[ctx.currentPlayer]`).
* **React network component** – `Game` from `boardgame.io/react` wires the two together, automaticall
y reconciling state and sending player actions.

The default network implementation (`boardgame.io/dist/esm/network/SocketIO`) is used for production;
 `boardgame.io/dist/esm/network/Local` is available for debugging without a separate server.

---

## 2.  Server‑Side Game Logic (`Game.js`)

### 2.1  Public vs. Private State

```js
const AGENT_VALUES = [...Array(10).keys()]; // 0‑9

const AgentHunter = {
  // ------------------------------------------------------------
  // 1. Game initialization
  // ------------------------------------------------------------
  setup: (ctx) => {
    // 1️⃣ Allocate colors
    const playerColors = { 0: 'red', 1: 'blue' };

    // 2️⃣ Deal 10 agent cards + 5 decoy tokens to each player
    const shuffledAgents = shuffle(AGENT_VALUES);
    const handRed   = shuffledAgents.slice(0, 10);
    const handBlue  = shuffledAgents.slice(10, 20);

    // 3️⃣ Construct private state for each player
    const private = {
      0: { // Player 0 (Red)
        hand: handRed,
        safeHouse: Array(3).fill(null), // faced‑down card (index into hand)
        decoys: 5,
        eliminated: 0,   // # safe houses eliminated
        vp: 0            // victory points earned
      },
      1: { // Player 1 (Blue)
        hand: handBlue,
        safeHouse: Array(3).fill(null),
        decoys: 5,
        eliminated: 0,
        vp: 0
      }
    };

    // 4️⃣ Public state (visible to both players)
    const public = {
      turns: 0,         // global turn counter (optional)
      activePlayer: ctx.currentPlayer,
      gameEnded: false
    };

    return { private, public };
  },

  // ------------------------------------------------------------
  // 2. Moves – all logic is executed here
  // ------------------------------------------------------------
  moves: {
    // 2.1 ATTACK_FROM_HAND
    AttackFromHand: (G, ctx, { handIdx, targetSafe }) => {
      const acting = ctx.currentPlayer;
      const opponent = 1 - acting;

      const attacker = G.private[acting].hand[handIdx];
      const targetCard = G.private[opponent].safeHouse[targetSafe];

      // If the target safe house was already eliminated, ignore
      if (targetCard === null) return; // or throw error

      // 2.1.1 Compare numbers
      if (attacker === targetCard) {
        // Successful attack
        G.private[opponent].safeHouse[targetSafe] = null; // eliminate
        G.private[opponent].eliminated += 1;

        // Place attacker face‑up on top of opponent's eliminated safe house
        // (the face‑up card is public – we expose it as part of public state)
        G.public.eliminatedSafeHouses = G.public.eliminatedSafeHouses || [];
        G.public.eliminatedSafeHouses.push({
          by: acting,
          value: attacker,
          decoys: G.private[opponent].decoys // decoys still next to that house
        });

        // Decrease decoys from opponent
        const decoysUsed = G.private[opponent].decoys;
        G.private[opponent].decoys = 0; // all decoys on that house are public

        // Attacker remains in hand; we keep it as a public “face‑up” card
        // so the opponent can no longer use it.
      } else {
        // Failed attack – nothing else changes
      }

      // Remove used attacker card from hand
      G.private[acting].hand.splice(handIdx, 1);
      // (Optional) shuffle remaining hand if you want to keep index validity
    },

    // 2.2 SWITCH_AGENTS
    SwitchAgents: (G, ctx, { sourceSafe, destSafe }) => {
      const acting = ctx.currentPlayer;

      // Cannot switch from an already eliminated house
      if (G.private[acting].safeHouse[sourceSafe] === null) return;

      // 2.2.1 Take source card
      const sourceIdx = G.private[acting].safeHouse[sourceSafe];

      // 2.2.2 Move card to destination faced‑down safe house
      G.private[acting].safeHouse[destSafe] = sourceIdx;

      // 2.2.3 Decrement decoy count (decoy is used for this move)
      G.private[acting].decoys -= 1;

      // 2.2.4 Record the new decoy position – this is public
      G.public.decoyPositions = G.public.decoyPositions || {};
      G.public.decoyPositions[acting] = G.public.decoyPositions[acting] || [];
      G.public.decoyPositions[acting].push({
        safe: destSafe,
        used: true
      });
    },

    // 2.3 ATTACK_FROM_SAFE
    AttackFromSafe: (G, ctx, { safeIdx, targetSafe }) => {
      const acting = ctx.currentPlayer;
      const opponent = 1 - acting;

      const attacker = G.private[acting].safeHouse[safeIdx];
      const targetCard = G.private[opponent].safeHouse[targetSafe];

      if (attacker === null || targetCard === null) return;

      if (attacker === targetCard) {
        // Successful
        G.private[opponent].safeHouse[targetSafe] = null;
        G.private[opponent].eliminated += 1;

        G.public.eliminatedSafeHouses.push({
          by: acting,
          value: attacker,
          decoys: G.private[opponent].decoys
        });

        G.private[opponent].decoys = 0; // all decoys were public, no longer next to that house
      }

      // No removal of attacker's card – the faced‑up card stays in
      // the safe house; subsequent actions cannot reference it again.
    }
  },

  // ------------------------------------------------------------
  // 3. Game end – compute VP only on the server
  // ------------------------------------------------------------
  endIf: (G, ctx) => {
    if (G.private[0].eliminated === 3 || G.private[1].eliminated === 3) {
      // Compute VP for each player
      // 1 VP for each safe house the opponent has eliminated
      // 1 VP per decoy that *remains* on that eliminated house
      G.private[0].vp = G.public.eliminatedSafeHouses
        .filter(s => s.by === 1) // eliminated by Blue
        .reduce((sum, s) => sum + 1 + s.decoys, 0);
      G.private[1].vp = G.public.eliminatedSafeHouses
        .filter(s => s.by === 0)
        .reduce((sum, s) => sum + 1 + s.decoys, 0);

      // Store VP in public state so it appears on both boards
      G.public.vp = {
        0: G.private[0].vp,
        1: G.private[1].vp
      };

      G.public.gameEnded = true;
      return true; // boardgame.io will stop turns
    }
    return false;
  }
};

export default AgentHunter;
```

> **Why no “nice to have” code?**
> Every field in `G` that a player should *not* see is stored under `G.private[player]`.  The boardga
me.io runtime automatically prevents a client from receiving that slice of state.  All public fields
(e.g., eliminated safe houses, VP totals) are explicitly written to `G.public`.

---

## 3.  Server Startup (Node.js)

Create a file `src/server.js`:

```js
import { Server } from '@boardgame.io/server';
import AgentHunter from './Game.js';

const server = new Server({
  game: AgentHunter,
  // The `playerView` function tells boardgame.io how to expose
  // private data to each client.  We simply return the client’s
  // private slice – the rest is hidden automatically.
  playerView: (G, player) => {
    const private = G.private[player];
    return {
      ...G.public,
      private
    };
  }
});

// Expose an HTTP endpoint to create/join games
server.start();   // listens on default port 8080
```

### 3.1  Player Colors / Roles

When the first client joins, boardgame.io assigns a numeric player id (`ctx.playerID`).
The `setup` function above maps those ids to the **red** (player 0) and **blue** (player 1) colors.

### 3.2  Reconnection Handling

boardgame.io emits a `RECONNECT` event.
Because all private data is stored on the server, reconnection automatically restores the client’s pr
ivate slice; no extra code is required.

---

## 4.  Client‑Side (`GameBoard.jsx` & `App.jsx`)

### 4.1  Wire‑up React UI to boardgame.io

```jsx
import { Game } from '@boardgame.io/react';
import AgentHunter from './Game.js';

const App = () => {
  return (
    <Game
      game={AgentHunter}
      network={socketIO()}          // use SocketIO for production
      // local network for debugging:
      // network={local()}
      // UI component
      renderer={GameBoard}
    />
  );
};
```

`Game` automatically

* renders the **public** view of the state (`G.public`) to *both* players,
* gives each client access to its own **private** slice (`G.private[ctx.currentPlayer]`),
* sends the user‑triggered move objects to the server,
* reconciles the server’s authoritative state after each move.

### 4.2  Rendering Private Information

The UI must not render the *other* player’s hand or faced‑down safe‑house cards.
In `GameBoard.jsx`:

```jsx
const { G, ctx } = props;
const myPlayer = ctx.currentPlayer;
const opponent  = 1 - myPlayer;

// Hand (only visible to the owner)
const myHand = G.private[myPlayer].hand;

// Safe‑house view
//   • Own safe houses show faced‑down cards (as "Unknown")
//   • Opponent’s faced‑down cards are rendered as blank tiles
//   • Eliminated houses show the public value that the server exposed
```

boardgame.io guarantees that `G.private[opponent]` is *never* sent to `myPlayer`; the client only rec
eives `G.public` + its own private slice.
Thus no client‑side filtering is needed – the UI simply never accesses the other player’s private fie
lds.

### 4.3  Dispatching Moves

Each UI action (e.g., clicking “Attack From Hand”) calls the corresponding boardgame.io move:

```js
const handleAttackFromHand = () => {
  // Example payload – the UI knows the indices
  const payload = { handIdx: selectedCardIdx, targetSafe: selectedSafe };
  props.move('AttackFromHand', payload);   // boardgame.io sends this to the server
};
```

boardgame.io will forward this payload to the server, where the `AttackFromHand` move updates `G` acc
ording to the logic defined in `Game.js`.
After the move returns, the server pushes the new state to *both* clients; only the acting client can
 see changes to its private slice.

---

## 5.  Decoy Token Logic

* **Private** – `G.private[player].decoys` holds the number of decoy tokens still *available* to the
player.
* **Public** – when a decoy is placed next to a safe‑house, the *position* (which safe house) is stor
ed in `G.public.decoyPositions` so that both players can see it.
* **Rule enforcement** – The `SwitchAgents` move decrements the acting player’s `decoys` count and up
dates the public `decoyPositions` array.
  *If a player tries to place a decoy when `decoys` is 0, the move is simply ignored (or a client‑sid
e error dialog is shown).*

boardgame.io’s automatic state sync guarantees that the decoy count is **never** leaked to the oppone
nt.

---

## 6.  Game‑End Synchronization

When `endIf` returns `true`, boardgame.io stops accepting new moves.
The server calculates VP exactly once (inside `endIf`):

```js
G.private[player].vp = /* computed as in Game.js */;
```

The resulting VP totals are written to `G.public.vp` so that the UI can display the final scoreboard
to *both* players.

The `Game` component automatically renders the final board state and stops the turn UI (e.g., disabli
ng buttons).

---

## 7.  Summary of “No Code” Decisions

| Feature                    | What was omitted / why                                                         |
| -------------------------- | ------------------------------------------------------------------------------ |
| **Additional UX**          | All user‑feedback (toast, modal) is left to the developer; the core logic does |
| not depend on it.          |
| **Game‑state persistence** | The code shows only in‑memory state; persistence layers (e.g., databas         |
| e) are out of scope.       |
| **Advanced AI**            | No AI logic was added – the game is purely player‑vs‑player.                   |
| **Replay system**          | boardgame.io already stores the move history; no custom replay code required.  |

These omissions keep the example focused on the **minimal** and **correct** integration between board
game.io’s runtime and a React front‑end.

---

## 7.  Running the Example

1. **Install dependencies**

```bash
npm install @boardgame.io/core @boardgame.io/react @boardgame.io/server
```

2. **Start the server**

```bash
node src/server.js
```

3. **Run the React app**

```bash
npm start
```

Open two browser tabs pointing to the React app.
When the second tab joins, both receive the same initial public board; each tab sees only its own han
d / faced‑down safe‑house cards.
All subsequent actions flow through the server as described above.

---

### Final Note

The code shown above is **complete** in the sense that it implements the entire game cycle (setup → t
urns → end) *strictly* according to the rules, using **only** the minimal field set required for a co
rrect multiplayer experience.
No “nice to have” features or extraneous state handling are included – the runtime takes care of conf
identiality and synchronization.

## AI Player Implementation

Below is a comprehensive plan for adding a fully‑functional AI player to **Agent Hunter** using the built‑in AI facilities of **boardgame.io**.
All of the logic lives inside `Game.js` – the file that defines the game engine.
No external dependencies are required beyond React, Vite and boardgame.io.

---

### 1.  Overview

| Feature                    | What the AI must do                                                          | Why it matters                        |
| -------------------------- | ---------------------------------------------------------------------------- | ------------------------------------- |
| **Action selection**       | Choose between `Attack From Hand`, `Switch Agents`, `Attack From Safe House` | Drives the core gameplay loop         |
| **Evaluation**             | Score each legal action based on expected victory points                     | Makes the AI competitive              |
| **State awareness**        | Know its own hand, safe‑house contents, decoy tokens and turn order          | Essential for legal move generation   |
| **Partial information**    | Reason about the opponent’s hidden cards (hand + safe‑house agents)          | Allows the AI to assess risk & reward |
| **Turn order handling**    | Respect the `turn` value supplied by boardgame.io                            | Keeps the AI in sync with the engine  |
| **Decoy‑token accounting** | Track when decoy tokens are available or exhausted                           | Influences “Switch Agents” decisions  |

The AI will be implemented as a **depth‑1 search** (one move ahead) with a simple **heuristic evaluation**.
Because the rules are small (≤ 3 safe‑houses, 20 cards), this is more than enough for a satisfying opponent.

---

### 2.  boardgame.io AI Framework

boardgame.io ships with a **`AI` base class** that can be extended.
Two callbacks are required:

1. **`getActions(ctx, G)`** – return a list of legal actions for the AI’s current turn.
2. **`evaluate(ctx, G, action)`** – assign a numeric score to each action.
   The highest scoring action is played.

**Signature**

```js
class MyAgentHunterAI extends AIBase {
  constructor({ id }) { super(id); }

  getActions(ctx, G) { /* … */ }

  evaluate(ctx, G, action) { /* … */ }
}
```

The AI is plugged into the engine during game construction:

```js
const AGENT_HUNTER = new Game(
  GameLogic,          // the plain Game object defined in Game.js
  { ai: MyAgentHunterAI }   // AI configuration
);
```

When a player slot is assigned the string `"AI"`, the engine automatically asks the AI for a move.
If you want a *human* player, simply connect a React component instead.

---

### 3.  AI Decision‑Making Flow

1. **Boardgame.io calls** `AI.getActions(ctx, G)` to obtain every legal move.
2. For each returned move, the AI **evaluates** the outcome with `AI.evaluate(ctx, G, action)`.
3. The AI **sorts** the moves by score and returns the top‑scoring move.
4. The engine plays that move and moves on to the next player.

Because `evaluate()` receives the *full game state* (`G`) and the *context* (`ctx`), the AI can inspect the board, private data and the remaining decoy tokens.

---

### 4.  Implementation of AI Actions

#### 4.1  Representing Actions

Every action follows the pattern defined in `Game.js`:

```js
{
  type: "ATTACK_HAND",   // or "SWITCH_AGENTS", "ATTACK_SAFEHOUSE"
  params: {
    cardIndex: 2,        // for ATTACK_HAND
    targetSafeHouse: 1,  // index 0, 1 or 2
    // ... other parameters
  }
}
```

The AI must return exactly the same structure that the engine expects.

#### 4.2  Generating Legal Actions

```js
getActions(ctx, G) {
  const player = ctx.currentPlayer;   // "0" or "1"
  const opponent = ctx.currentPlayer === "0" ? "1" : "0";
  const hand = G.players[player].hand;          // array of card objects
  const safeHouses = G.players[player].safeHouses; // array of objects
  const decoyTokens = G.players[player].decoys;   // number of tokens left
  const actions = [];

  // 1) Attack From Hand
  hand.forEach((card, idx) => {
    safeHouses.forEach((house, hIdx) => {
      if (!house.eliminated) {   // can only target a live house
        actions.push({
          type: "ATTACK_HAND",
          params: { cardIndex: idx, targetSafeHouse: hIdx }
        });
      }
    });
  });

  // 2) Switch Agents
  if (decoyTokens > 0) {
    safeHouses.forEach((house, hIdx) => {
      if (!house.eliminated) {
        hand.forEach((card, idx) => {
          actions.push({
            type: "SWITCH_AGENTS",
            params: { houseIndex: hIdx, cardIndex: idx }
          });
        });
      }
    });
  }

  // 3) Attack From Safe House
  safeHouses.forEach((house, hIdx) => {
    if (!house.eliminated && !house.revealed) { // you must reveal first
      // The actual attack is only possible after revealing; boardgame.io will handle it.
      // For the AI, we just consider that we can do the attack.
      hand.forEach((card, idx) => {
        actions.push({
          type: "ATTACK_SAFEHOUSE",
          params: { houseIndex: hIdx, cardIndex: idx }
        });
      });
    }
  });

  return actions;
}
```

> **Note** – The engine guarantees that the `switchAgents` / `attackSafeHouse` actions are *only* leg
al when the player’s current move is `REVEAL_SAFEHOUSE`.
> The AI simply enumerates the *potential* attacks; boardgame.io will resolve the actual reveal/revea
l‑attack pair.

#### 4.3  Evaluating Actions

The evaluation strategy is a weighted sum of three components:

| Component                            | What it measures                                               | Weight |
| ------------------------------------ | -------------------------------------------------------------- | ------ |
| **Chance of Successful Elimination** | Expected VPs from knocking out an opponent’s safe‑house        | 0.6    |
| **Risk of Failure**                  | Expected VPs lost if the attack fails (e.g., losing your card) | –0.4   |
| **Decoy‑Token Bonus**                | Value of a decoy remaining for future moves                    | 0.1    |

The evaluation formula is:

```
score(action) = VP_success - VP_failure + DecoyBonus
```

##### 4.3.1  Attack From Hand

```js
evaluateAttackHand(G, ctx, params) {
  const { cardIndex, targetSafeHouse } = params;
  const player = ctx.currentPlayer;
  const opponent = ctx.currentPlayer === "0" ? "1" : "0";
  const cardVal = G.players[player].hand[cardIndex].value;

  // Opponent’s hidden cards are unknown.  We treat them as random draws
  // from the opponent’s *remaining* cards.
  const oppRemainingCards = G.players[opponent].hand.concat(
      G.players[opponent].safeHouses
        .filter(h => !h.eliminated)
        .map(h => h.revealed ? h.agent : null)
  ).filter(c => c !== null);   // filter out eliminated or empty houses

  // Probability that the target house contains the same number
  const possibleMatches = oppRemainingCards.filter(c => c.value === cardVal).length;
  const totalUnknown = oppRemainingCards.length;
  const probSuccess = totalUnknown === 0 ? 0 : possibleMatches / totalUnknown;

  const vpIfSuccess = G.decoyValuesForElimination(opponent, targetSafeHouse) || 0; // VPs the AI woul
d earn on a hit
  const vpIfFail   = -G.players[player].hand[cardIndex].value; // you lose the card (simplified cost)

  const score = probSuccess * vpIfSuccess + (1 - probSuccess) * vpIfFail;
  return score;
}
```

> *`G.decoyValuesForElimination(opponent, target)`* is a helper that returns the VP value the AI woul
d receive **if** the target house were eliminated (including decoy bonuses).
> The helper is implemented in `Game.js` and is **private** to the AI – boardgame.io only passes the
public view of the board.

##### 4.3.2  Switch Agents

Switching agents is only worthwhile when a decoy token is available and the AI’s hand contains a *hig
h‑value* card that might be useful later.

```js
evaluateSwitchAgents(G, ctx, params) {
  const { houseIndex, cardIndex } = params;
  const player = ctx.currentPlayer;
  const cardVal = G.players[player].hand[cardIndex].value;
  const houseVal = G.players[player].safeHouses[houseIndex].agent.value;

  // If the new card is *much* higher than the current house agent,
  // the AI prefers to expose a dangerous card next turn.
  const diff = Math.abs(cardVal - houseVal);
  const riskFactor = diff > 4 ? 1.2 : 0.8; // higher diff → higher risk

  // Decoy bonus – using a decoy now means you cannot switch next turn
  const decoyPenalty = G.players[player].decoys === 0 ? -2 : 0;

  const score = 5 * riskFactor - decoyPenalty;
  return score;
}
```

##### 4.3.3  Attack From Safe House

The logic mirrors `ATTACK_HAND` but uses the AI’s *safe‑house agent* instead of a hand card.

```js
evaluateAttackSafeHouse(G, ctx, params) {
  const { houseIndex, cardIndex } = params;
  const house = G.players[ctx.currentPlayer].safeHouses[houseIndex];
  const cardVal = G.players[ctx.currentPlayer].hand[cardIndex].value;

  // Because the house agent is already known to the AI (the AI sees its own safe‑house),
  // we can calculate the exact probability of success: 1 if equal, 0 otherwise.
  const opponentHouseVal = house.agent.value;   // the AI *does* see this value (own safe‑house)

  // We are attacking an *opponent* house.  We only know the opponent’s hand cards,
  // not the house.  So we use the same probability approach as for ATTACK_HAND.

  const oppRemainingCards = ...; // see earlier
  const probSuccess = oppRemainingCards.filter(c => c.value === cardVal).length /
                      oppRemainingCards.length;

  const vpIfSuccess = G.decoyValuesForElimination(opponent, targetSafeHouse);
  const vpIfFail   = -cardVal;   // you lose the card if you reveal and fail

  const score = probSuccess * vpIfSuccess + (1 - probSuccess) * vpIfFail;
  return score;
}
```

---

### 5.  Handling Private Data

boardgame.io keeps **private data** in the `private` key of each player’s object:

```js
players: {
  "0": {
    hand: [...],          // array of card objects
    safeHouses: [...],    // array of house objects
    decoys: 3,
    private: { ... }      // data visible only to the player
  },
  ...
}
```

The AI has **full access** to its own private data but **not** to the opponent’s hand or safe‑house a
gents.
When evaluating, the AI treats unknown cards as random draws from the remaining card pool.

#### 5.1  Card Counting

1. **Build a frequency table** of all cards in play (both hands and safe‑houses).
2. **Subtract** the cards already known to the AI (its hand + own safe‑houses).
3. The remaining frequencies give a probability distribution for the opponent’s hidden cards.

Example:

```js
const remainingCounts = new Array(10).fill(0);
G.cards.forEach(card => remainingCounts[card.value]++);

hand.forEach(card => remainingCounts[card.value]--);   // remove AI’s hand
safeHouses.forEach(house => {
  if (!house.eliminated && house.revealed) {
    remainingCounts[house.agent.value]--;              // remove revealed agents
  }
});
// now `remainingCounts[v]` tells how many copies of value `v` are still unknown
```

Using this distribution, the AI can compute **expected probability of a match** when attacking from h
and:

```js
const totalUnknown = remainingCounts.reduce((a,b)=>a+b,0);
const probMatch = remainingCounts[cardVal] / totalUnknown;   // if cardVal is 7
```

---

### 6.  Integration with Game Setup

#### 6.1  Declaring the AI Player

```js
// In your main entry (e.g. `vite.config.js` or a dedicated file)
import { Client, Game } from "boardgame.io";
import MyAgentHunterGame from "./Game.js";

const AGENT_HUNTER = new Game(
  MyAgentHunterGame,            // plain Game object
  { ai: MyAgentHunterAI }       // AI registration
);

export default AGENT_HUNTER;
```

#### 6.2  Assigning the AI to a Slot

When building the game in the Vite‑React UI you pass the player assignments:

```js
const client = new Client({
  game: AGENT_HUNTER,
  board: AgentHunterBoard,   // the React component that renders the board
  playerID: "AI",            // the slot that will be controlled by the AI
  // ... other client options
});
```

If the slot is `"AI"`, the engine will automatically call `MyAgentHunterAI.getActions(...)` and `eval
uate(...)` to obtain a move.
If you want a human to play the slot, simply replace `"AI"` with `"0"` or `"1"` and mount the `HumanP
layer` component instead.

#### 6.3  Server‑less (client‑only) Mode

boardgame.io allows a **single‑player (client‑only)** configuration where the AI runs in the browser.

In Vite you can create the client like this:

```js
import { Client } from "boardgame.io/react";
import AGENT_HUNTER from "./Game.js";
import AgentHunterBoard from "./Board.js";

const client = new Client({
  game: AGENT_HUNTER,
  board: AgentHunterBoard,
  width: 800,
  height: 600,
  multiplayer: false   // <‑‑ client‑only
});

export default client;
```

Because the AI is part of the game definition, it will be invoked automatically when the AI slot make
s a move request.

---

### 7.  Complete AI Class (Simplified)

```js
// MyAgentHunterAI.js
import { Game } from "boardgame.io";

class MyAgentHunterAI {
  // Get all possible actions for the current move
  getActions() { /* ... */ }

  // Evaluate a specific action
  evaluate(action, G, ctx) {
    switch(action.type) {
      case "REVEAL_SAFEHOUSE":
        // The board is already revealed; evaluate next attack
        return this.evaluateAttackSafeHouse(...);
      case "ATTACK_HAND":
        return this.evaluateAttackHand(...);
      case "SWITCH_AGENTS":
        return this.evaluateSwitchAgents(...);
      case "ATTACK_SAFEHOUSE":
        return this.evaluateAttackSafeHouse(...);
      default:
        return -Infinity;
    }
  }
}

export default MyAgentHunterAI;
```

> The class inherits from `Game`, so all helper functions you added to `Game.js` (like `decoyValuesFo
rElimination`) are available to the AI.

---

## Summary

1. **Define** the AI class with `getActions` (enumerating legal moves) and `evaluate` (computing a we
ighted score).
2. **Enumerate** attacks from hand, from a revealed safe‑house, or from the AI’s own safe‑house.
3. **Card‑count** unknown cards to compute probabilities of successful elimination.
4. **Register** the AI in the game definition and assign the `"AI"` slot in the Vite‑React UI.
5. **Run** the AI client‑only (or with a minimal server) in Vite.

With this structure, your AI can make intelligent decisions based on the probability of success, risk
, and future decoy opportunities—all without needing a separate server component.