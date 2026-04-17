# Interview Coach — Feature Backlog

## 🔴 Bugs / Must Fix
- [x] Java test runner — was 0/0 because no runner was appended
- [x] `public class Solution` collision with `public class Main` in Java
- [x] `expected_output` vs `expected` key mismatch in new questions
- [x] Output panel invisible (Monaco filled 100% height, pushed output off-screen)
- [x] Auto-coach trigger on submit (now coach is manual only)

---

## 🟠 High Priority — Core Coding UX

### 1. Interview Timer
Start a countdown when you begin a problem. Real interviews are 45 min.
- Visible countdown in the header (e.g. `⏱ 38:22`)
- Optional — user sets duration (30 / 45 / 60 min)
- Turns red in last 5 min
- Records time taken in submission history

### 2. "Next Question" Button
After submitting, show "Next →" (next in study plan or random same difficulty).
No need to go back to the home page between problems.

### 3. Compilation Error UX
When Java/Python has a syntax error, show a red "Compilation Error" banner
at the top of the output panel instead of just dumping stderr.

### 4. Category Quick-Filter on Homepage
Currently categories are in the filter dropdown but users still scroll through 79.
Add a horizontal category pill row (Array · Tree · DP · Graph · …) that one-click
filters the list.

---

## 🟡 Medium Priority — Progress & Study

### 5. Interview Timer History
Save `time_taken_seconds` in each submission. Show it on the submission record
and on the homepage (e.g. "Solved in 23 min").

### 6. "Needs Review" Flag
Let users mark questions they want to revisit (separate from pass/fail).
Show a 🔖 icon on the homepage for flagged questions.
Useful for: "I solved it but used a suboptimal approach."

### 7. Personal Notes Per Question
A small text area per question for jotting approach notes or gotchas.
Saved locally (JSON). Visible when you reopen the question.

### 8. Spaced Repetition in Study Plans
Questions that failed come back sooner.
Simple algorithm: failed → retry in 1 day, passed → retry in 3/7/14 days.
Show a "Due today" count on the homepage.

### 9. Streak Tracker
Track daily practice streak (consecutive days with at least 1 submission).
Show streak on homepage: 🔥 7-day streak.

---

## 🟢 Nice to Have — Content & Polish

### 10. Reference Solution Reveal
After 3+ failed attempts, offer to show a reference solution with explanation.
Pre-written (no API credits needed). Collapsed by default behind a button.
Could start with just the top 20 most common problems.

### 11. Complexity Annotation
After submitting, show a text field: "Your time/space complexity is: ___"
User self-reports. Coach can verify if open.

### 12. Difficulty Rating After Solving
"How hard was this for you?" 😅 Hard / 😐 Medium / 😊 Easy
Used to tune study plan suggestions.

### 13. Company Tag Filtering Improvement
Current company tags on the new 47 questions are missing (they defaulted to empty).
Add company tags for the standard Blind 75 problems (e.g. Google asks LRU Cache, Amazon asks Two Sum).

### 14. Dark/Light Mode Toggle
Currently locked to dark mode.

### 15. Keyboard Shortcuts
- `Ctrl+Enter` → Run
- `Ctrl+Shift+Enter` → Submit  
- `Ctrl+\`` → Focus editor

---

## 🔵 Bigger Features (Later)

### 16. Mock Interview Mode
Full 45-min mock: random problem + coach plays interviewer, asks clarifying
questions, gives hints only when stuck, scores at the end.
Uses the existing coach but with a different system prompt.

### 17. Peer Comparison (Anonymous)
"X% of users solved this in under 30 min" — motivational context.
Could be synthetic/estimated at first.

### 18. Export Progress Report
PDF / markdown summary of what you've practiced, pass rates, weak areas.
Useful before an actual interview week.

### 19. LeetCode Import
Paste a LeetCode URL → auto-scrape problem and add to your bank.
(Would need a scraper or the unofficial LeetCode API.)

### 20. Company-Specific Practice Mode
"Google loop prep" — pulls only Google-tagged problems in likely frequency order.
