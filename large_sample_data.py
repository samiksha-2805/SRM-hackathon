from models import Faculty, Session


def get_large_sample_faculty():
    faculty = []

    for i in range(1, 21):
        faculty.append(
            Faculty(
                id=f"F{i}",
                name=f"Faculty {i}",
                role="SENIOR",
                available_sessions={
                    f"S{j}" for j in range(1, 201)
                    if (i + j) % 5 != 0
                }
            )
        )

    for i in range(21, 101):
        faculty.append(
            Faculty(
                id=f"F{i}",
                name=f"Faculty {i}",
                role="JUNIOR",
                available_sessions={
                    f"S{j}" for j in range(1, 201)
                    if (i + j) % 7 != 0
                }
            )
        )

    return faculty


def get_large_sample_sessions():
    sessions = []

    for i in range(1, 201):
        sessions.append(
            Session(
                id=f"S{i}",
                halls=[
                    f"H{i}_1",
                    f"H{i}_2"
                ]
            )
        )

    return sessions