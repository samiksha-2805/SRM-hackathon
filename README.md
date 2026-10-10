# SRM-hackathon
# Exam Duty Roster Generation System

## Overview

The Exam Duty Roster Generation System generates examination duty rosters based on faculty availability, sessions, halls, and faculty seniority.

For each session:
- Every hall gets exactly one invigilator.
- One available SENIOR faculty member is assigned as Chief Invigilator.
- A faculty member cannot be assigned to multiple halls in the same session.
- Unavailable faculty cannot be assigned.
- The system checks feasibility before generating a roster.

## Features

- Faculty and session management
- Faculty availability checking
- Chief Invigilator assignment
- Hall-wise invigilator assignment
- Feasibility checking
- Hopcroft–Karp matching
- Backtracking with forward checking
- Infeasible-case detection
- Large dataset support
- Automated testing
- Manual input support

## Technologies Used

- Python 3
- Lists, Sets and Dictionaries
- Hopcroft–Karp Algorithm
- Backtracking with Forward Checking
- Python unittest

## Project Structure

EXAM-DUTY-ROSTER/
│
├── models.py
├── hopcroft_karp.py
├── constraints.py
├── roster_generator.py
├── sample_data.py
├── large_sample_data.py
├── input_handler.py
├── main.py
│
└── tests/
    └── test_roster.py

## How It Works

1. Faculty availability and session details are provided as input.
2. The system checks whether a valid assignment is possible.
3. Hopcroft–Karp is used to check hall-faculty matching feasibility.
4. Backtracking with forward checking generates the roster.
5. The final roster is validated before being displayed.

## Algorithms

### Hopcroft–Karp

Faculty and halls are represented as a bipartite graph.

- Left side: Faculty
- Right side: Halls
- Edge: Faculty can be assigned to the session

It is used to check whether all halls can be assigned distinct faculty members.

### Backtracking with Forward Checking

Backtracking tries possible faculty assignments and goes back when a branch fails.

Forward checking verifies that every remaining hall still has at least one possible faculty member, helping eliminate invalid branches early.

## Time Complexity

Let:
- F = number of faculty
- H = number of halls
- E = number of edges

Hopcroft–Karp:

O(E √(F + H))

Backtracking:

O(F^H) in the worst case.

Forward checking reduces the practical search space by pruning invalid assignments.

## Space Complexity

Hopcroft–Karp:

O(V + E)

where V = F + H.

Roster generation additionally requires approximately:

O(F + H)

for assignment and recursion state.

## Conclusion

The system provides a practical solution for examination duty allocation while satisfying faculty availability, hall assignment, and Chief Invigilator constraints. It combines Hopcroft–Karp matching with backtracking and forward checking to generate valid rosters.