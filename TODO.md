# Interview Coach — Feature Backlog

## ✅ Done

- [x] Java test runner — was 0/0, now appends full `Main` class with test harness
- [x] `public class Solution` collision with `public class Main` in Java — strip `public` from user's class
- [x] `expected_output` vs `expected` key mismatch in new questions — `_get_expected()` helper
- [x] Output panel invisible — Monaco filled 100% height, pushed output off-screen → fixed with LeetCode layout
- [x] Auto-coach trigger on submit — coach is now manual-only
- [x] **Interview timer** — 20/30/45/60 min presets, yellow < 10 min, red < 5 min, pauses on solve
- [x] **Next Question button** — random same-difficulty, shown in nav and in result banner
- [x] **Compilation error banner** — red ⚠️ header when Java/Python fails to compile
- [x] **Category pills on homepage** — one-click filter row above the question list
- [x] **LeetCode-style layout** — problem + output left, full-height editor right, resizable
- [x] **Study plan streak tracking** — 🔥 consecutive days, resets on skip
- [x] **Today's Mission card** — highlights today's problems with Solve → CTA
- [x] **On-track / behind status** — past-incomplete count with color-coded banner
- [x] **Color-coded timeline** — ✅ done · 🔶 partial · 🔴 overdue · ▶ today · ○ future
- [x] **Auto-mark complete on passing submit** — from study plan → all tests pass → checkbox auto-ticks
- [x] **Toggle completion** — unmark a done problem by clicking the checkbox again
- [x] **Back to study plan** context — "← Study Plan" when entering from plan
- [x] **Personal notes per question** — auto-saves 800 ms after typing, persists per question
- [x] **Keyboard shortcuts** — Ctrl/Cmd+Enter → Run, Ctrl/Cmd+Shift+Enter → Submit
- [x] **"Needs Review" flag** 🔖 — toggle in nav bar, shown on home page list
- [x] **Next button page reload bug** — React Router reused same component instance across query-param nav; fixed with `key={search}` wrapper in App.tsx
- [x] **Tiered hints** 💡 — 3 progressive hints, Claude-generated on first request and cached to disk; hidden in mock mode
- [x] **Test case breakdown** — submit result shows structured per-row table (✓/✗, input, expected, got)
- [x] **Submission history per question** 📋 — collapsible panel, all past attempts with date/language/pass rate
- [x] **Mock interview mode** 🎯 — 45-min locked timer, hints hidden, coach uses strict interviewer system prompt

---

## 🟠 High Priority — Coding Session UX

### 1. Personal Notes Per Question
A small text area per question for jotting approach notes, complexity, gotchas.
Saved locally per question. Visible below the problem statement.
**Why:** You'll forget your own insights. Notes make revision 10× faster.

### 2. "Needs Review" Flag
Let users mark questions they want to revisit (separate from pass/fail).
Show a 🔖 bookmark icon on the homepage for flagged questions.
**Why:** "I solved it but used O(n²) when O(n) was possible" — currently no way to track this.

### 3. Keyboard Shortcuts
- `Ctrl+Enter` → Run
- `Ctrl+Shift+Enter` → Submit
- `Ctrl+\`` → Focus editor
**Why:** Removes friction. Muscle memory matters in real interviews.

### 4. Submission History Viewer Per Question
Show past attempts for the current question in the left panel (expandable).
Each entry: date, language, pass rate, elapsed time.
**Why:** Lets you see how you've improved on a problem over time.

---

## 🟡 Medium Priority — Learning Quality

### 5. Reference Solution Reveal
After 3+ failed attempts (or explicit request), show a reference solution with explanation.
Collapsed behind a button. Could start with top 20 most common problems.
**Why:** There's a point where you need to see the answer to make progress.

### 6. Complexity Self-Report
After submitting, show a field: "Your time complexity:" / "Your space complexity:"
Coach can confirm or correct if open.
**Why:** Forces you to articulate it — exactly what happens in real interviews.

### 7. Difficulty Self-Rating After Solving
"How hard was this for you?" 😅 Hard / 😐 Medium / 😊 Easy
Used to tune which problems show up in spaced repetition.
**Why:** Objective difficulty (Easy/Medium/Hard) doesn't match your personal difficulty.

### 8. Spaced Repetition
Questions that failed come back sooner; passed ones space out.
Simple algorithm: failed → retry in 1 day, passed once → 3 days, passed twice → 7/14 days.
Show "Due today" count on homepage.

### 9. Mock Interview Mode
Full 45-min mock: random problem + coach plays interviewer role, asks clarifying questions,
gives hints only when stuck, scores communication + code quality at the end.
Uses the existing coach with a different system prompt.
**Why:** Most realistic practice for the actual interview format.

---

## 🟢 Nice to Have — Content & Polish

### 10. Company Tag Improvement
Company tags on 47 new questions are mostly empty.
Add standard company associations (Google → LRU Cache, Amazon → Two Sum, etc.).

### 11. "Similar Problems" Sidebar
When on a tree problem, show "3 other DFS problems you've solved".
Tag similar problems by pattern, not just category.

### 12. Timer History in Submissions
Save `time_taken_seconds` in each submission record.
Show "Solved in 23 min" on the homepage solved indicator.

### 13. Dark/Light Mode Toggle
Currently locked to dark mode.

---

## 🔵 Bigger Features (Later)

### 14. Export Progress Report
PDF / markdown summary: problems practiced, pass rates, time trends, weak areas.
Useful to review before an actual interview week.

### 15. LeetCode Import
Paste a LeetCode URL → auto-scrape problem and add to your bank.

### 16. Company-Specific Practice Mode
"Google loop prep" — only Google-tagged problems in frequency order.

### 17. Peer Comparison (Anonymous)
"X% of users solved this under 30 min" — synthetic / estimated for motivation.
