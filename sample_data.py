from models import Faculty, Session


def get_sample_faculty():
    return [
        Faculty(
            id="F1",
            name="Faculty 1",
            role="SENIOR",
            available_sessions={"S1"}
        ),
        Faculty(
            id="F2",
            name="Faculty 2",
            role="JUNIOR",
            available_sessions={"S1"}
        ),
        Faculty(
            id="F3",
            name="Faculty 3",
            role="JUNIOR",
            available_sessions={"S1"}
        ),
        Faculty(
            id="F4",
            name="Faculty 4",
            role="JUNIOR",
            available_sessions=set()
        )
    ]


def get_sample_sessions():
    return [
        Session(
            id="S1",
            halls=["H1", "H2"]
        )
    ]