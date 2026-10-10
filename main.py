from sample_data import get_sample_faculty, get_sample_sessions
from large_sample_data import (
    get_large_sample_faculty,
    get_large_sample_sessions
)
from input_handler import get_faculty_input, get_session_input
from roster_generator import RosterGenerator


def display_header():
    print("\n" + "=" * 50)
    print("             EXAM DUTY ROSTER")
    print("=" * 50)


def display_menu():
    print("\n1. Load Sample Data")
    print("2. Load Large Sample Data")
    print("3. Enter Faculty Details")
    print("4. Enter Session Details")
    print("5. Display Current Data")
    print("6. Check Feasibility")
    print("7. Generate Roster")
    print("8. Exit")


def display_data(faculty, sessions):
    if not faculty and not sessions:
        print("\nNo data available.")
        return

    print("\nFaculty")
    print("-" * 50)

    if faculty:
        print(f"Total Faculty: {len(faculty)}")

        for f in faculty:
            available = ", ".join(sorted(f.available_sessions))

            if not available:
                available = "None"

            print(
                f"{f.id:<8}"
                f"{f.name:<20}"
                f"{f.role:<10}"
                f"Available: {available}"
            )
    else:
        print("No faculty entered.")

    print("\nSessions")
    print("-" * 50)

    if sessions:
        print(f"Total Sessions: {len(sessions)}")

        for session in sessions:
            print(
                f"{session.id:<8}"
                f"Halls: {', '.join(session.halls)}"
            )
    else:
        print("No sessions entered.")


def display_roster(roster):
    print("\n" + "=" * 50)
    print("FINAL EXAM DUTY ROSTER")
    print("=" * 50)

    print(f"\nSession: {roster.session_id}")

    print(
        f"Chief Invigilator: "
        f"{roster.chief.id} - {roster.chief.name}"
    )

    print("\nHall Assignments")
    print("-" * 50)

    for hall, faculty in roster.hall_assignments.items():
        print(
            f"{hall:<8}"
            f"{faculty.id} - {faculty.name}"
        )

    print("\nStatus: FEASIBLE")
    print("=" * 50)


def check_feasibility(faculty, sessions):
    if not faculty:
        print("\nNo faculty data available.")
        return

    if not sessions:
        print("\nNo session data available.")
        return

    generator = RosterGenerator(faculty)

    large_dataset = len(faculty) >= 100 or len(sessions) >= 200

    feasible_count = 0
    infeasible_count = 0

    for session in sessions:
        feasible, reason = generator.check_feasibility(session)

        if feasible:
            feasible_count += 1
        else:
            infeasible_count += 1

            if not large_dataset:
                print(f"\nSession: {session.id}")
                print("Status: INFEASIBLE")
                print(f"Reason: {reason}")

    if large_dataset:
        print("\n" + "=" * 50)
        print("LARGE DATASET FEASIBILITY")
        print("=" * 50)

        print(f"\nTotal Faculty:       {len(faculty)}")
        print(f"Total Sessions:      {len(sessions)}")
        print(f"Feasible Sessions:   {feasible_count}")
        print(f"Infeasible Sessions: {infeasible_count}")

        if infeasible_count == 0:
            print("\nStatus: FEASIBLE")
        else:
            print("\nStatus: PARTIALLY FEASIBLE")

        print("=" * 50)

    else:
        print("\n" + "=" * 50)
        print("FEASIBILITY CHECK")
        print("=" * 50)

        print(f"\nFeasible Sessions:   {feasible_count}")
        print(f"Infeasible Sessions: {infeasible_count}")

        if infeasible_count == 0:
            print("\nStatus: FEASIBLE")
        else:
            print("\nStatus: PARTIALLY FEASIBLE")

        print("=" * 50)


def generate_rosters(faculty, sessions):
    if not faculty:
        print("\nNo faculty data available.")
        return

    if not sessions:
        print("\nNo sessions available.")
        return

    generator = RosterGenerator(faculty)

    large_dataset = len(faculty) >= 100 or len(sessions) >= 200

    generated = 0
    infeasible = 0

    for session in sessions:
        roster, message = generator.generate(session)

        if roster is None:
            infeasible += 1

            if not large_dataset:
                print(f"\nSession: {session.id}")
                print("Status: INFEASIBLE")
                print(f"Reason: {message}")

        else:
            generated += 1

            if not large_dataset:
                display_roster(roster)

    if large_dataset:
        print("\n" + "=" * 50)
        print("LARGE DATASET RESULT")
        print("=" * 50)

        print(f"\nTotal Faculty:       {len(faculty)}")
        print(f"Total Sessions:      {len(sessions)}")
        print(f"Rosters Generated:   {generated}")
        print(f"Infeasible Sessions: {infeasible}")

        if infeasible == 0:
            print("\nStatus: FEASIBLE")
        else:
            print("\nStatus: PARTIALLY FEASIBLE")

        print("=" * 50)

    else:
        print(f"\nGenerated rosters: {generated}/{len(sessions)}")


def main():
    faculty = []
    sessions = []

    while True:
        display_header()
        display_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            faculty = get_sample_faculty()
            sessions = get_sample_sessions()

            print("\nSample data loaded successfully.")
            print(f"Faculty: {len(faculty)}")
            print(f"Sessions: {len(sessions)}")

        elif choice == "2":
            faculty = get_large_sample_faculty()
            sessions = get_large_sample_sessions()

            print("\nLarge sample data loaded successfully.")
            print(f"Faculty: {len(faculty)}")
            print(f"Sessions: {len(sessions)}")

        elif choice == "3":
            new_faculty = get_faculty_input()
            faculty.extend(new_faculty)

            print(f"\nFaculty records added: {len(new_faculty)}")
            print(f"Total Faculty: {len(faculty)}")

        elif choice == "4":
            new_sessions = get_session_input()
            sessions.extend(new_sessions)

            print(f"\nSession records added: {len(new_sessions)}")
            print(f"Total Sessions: {len(sessions)}")

        elif choice == "5":
            display_data(faculty, sessions)

        elif choice == "6":
            check_feasibility(faculty, sessions)

        elif choice == "7":
            generate_rosters(faculty, sessions)

        elif choice == "8":
            print("\nExiting Exam Duty Roster.")
            break

        else:
            print("\nInvalid choice. Please select an option from 1 to 8.")


if __name__ == "__main__":
    main()