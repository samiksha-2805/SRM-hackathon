from models import Faculty, Session


def get_faculty_input():
    faculty = []

    print("\n" + "=" * 45)
    print("ENTER FACULTY DETAILS")
    print("=" * 45)

    while True:
        faculty_id = input(
            "\nEnter Faculty ID (or 'done' to finish): "
        ).strip()

        if faculty_id.lower() == "done":
            break

        if not faculty_id:
            print("Faculty ID cannot be empty.")
            continue

        if any(f.id == faculty_id for f in faculty):
            print("Faculty ID already exists.")
            continue

        name = input("Enter Faculty Name: ").strip()

        while True:
            role = input(
                "Enter Role (SENIOR/JUNIOR): "
            ).strip().upper()

            if role in {"SENIOR", "JUNIOR"}:
                break

            print("Invalid role. Enter SENIOR or JUNIOR.")

        sessions_input = input(
            "Enter available Session IDs separated by spaces: "
        ).strip()

        available_sessions = set(
            sessions_input.split()
        ) if sessions_input else set()

        faculty.append(
            Faculty(
                id=faculty_id,
                name=name,
                role=role,
                available_sessions=available_sessions
            )
        )

        print(f"{faculty_id} added successfully.")

    return faculty


def get_session_input():
    sessions = []

    print("\n" + "=" * 45)
    print("ENTER SESSION DETAILS")
    print("=" * 45)

    while True:
        session_id = input(
            "\nEnter Session ID (or 'done' to finish): "
        ).strip()

        if session_id.lower() == "done":
            break

        if not session_id:
            print("Session ID cannot be empty.")
            continue

        if any(s.id == session_id for s in sessions):
            print("Session ID already exists.")
            continue

        while True:
            try:
                hall_count = int(
                    input("Enter number of halls: ")
                )

                if hall_count <= 0:
                    print("Number of halls must be greater than 0.")
                    continue

                break

            except ValueError:
                print("Enter a valid number.")

        halls = []

        for i in range(1, hall_count + 1):
            while True:
                hall_id = input(
                    f"Enter Hall ID {i}: "
                ).strip()

                if not hall_id:
                    print("Hall ID cannot be empty.")
                    continue

                if hall_id in halls:
                    print("Hall ID already exists in this session.")
                    continue

                halls.append(hall_id)
                break

        sessions.append(
            Session(
                id=session_id,
                halls=halls
            )
        )

        print(f"{session_id} added successfully.")

    return sessions