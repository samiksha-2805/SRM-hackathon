import unittest

from models import Faculty, Session
from roster_generator import RosterGenerator


class TestRosterSystem(unittest.TestCase):

    def setUp(self):
        self.session = Session(
            id="S1",
            halls=["H1", "H2"]
        )

    def test_valid_roster(self):
        faculty = [
            Faculty("F1", "Faculty 1", "SENIOR", {"S1"}),
            Faculty("F2", "Faculty 2", "JUNIOR", {"S1"}),
            Faculty("F3", "Faculty 3", "JUNIOR", {"S1"}),
        ]

        generator = RosterGenerator(faculty)

        roster, message = generator.generate(self.session)

        self.assertIsNotNone(roster)
        self.assertEqual(roster.chief.role, "SENIOR")
        self.assertEqual(len(roster.hall_assignments), 2)

        assigned = [
            f.id for f in roster.hall_assignments.values()
        ]

        self.assertEqual(len(assigned), len(set(assigned)))

    def test_no_senior(self):
        faculty = [
            Faculty("F1", "Faculty 1", "JUNIOR", {"S1"}),
            Faculty("F2", "Faculty 2", "JUNIOR", {"S1"}),
            Faculty("F3", "Faculty 3", "JUNIOR", {"S1"}),
        ]

        generator = RosterGenerator(faculty)

        roster, message = generator.generate(self.session)

        self.assertIsNone(roster)
        self.assertIn("No SENIOR", message)

    def test_insufficient_faculty(self):
        faculty = [
            Faculty("F1", "Faculty 1", "SENIOR", {"S1"}),
            Faculty("F2", "Faculty 2", "JUNIOR", {"S1"}),
        ]

        generator = RosterGenerator(faculty)

        roster, message = generator.generate(self.session)

        self.assertIsNone(roster)

    def test_no_available_faculty(self):
        faculty = [
            Faculty("F1", "Faculty 1", "SENIOR", set()),
            Faculty("F2", "Faculty 2", "JUNIOR", set()),
            Faculty("F3", "Faculty 3", "JUNIOR", set()),
        ]

        generator = RosterGenerator(faculty)

        roster, message = generator.generate(self.session)

        self.assertIsNone(roster)
        self.assertIn("No SENIOR", message)

    def test_unavailable_faculty_not_assigned(self):
        faculty = [
            Faculty("F1", "Faculty 1", "SENIOR", {"S1"}),
            Faculty("F2", "Faculty 2", "JUNIOR", {"S1"}),
            Faculty("F3", "Faculty 3", "JUNIOR", set()),
            Faculty("F4", "Faculty 4", "JUNIOR", {"S1"}),
        ]

        generator = RosterGenerator(faculty)

        roster, message = generator.generate(self.session)

        self.assertIsNotNone(roster)

        assigned = [
            f.id for f in roster.hall_assignments.values()
        ]

        self.assertNotIn("F3", assigned)

    def test_no_duplicate_hall_assignment(self):
        faculty = [
            Faculty("F1", "Faculty 1", "SENIOR", {"S1"}),
            Faculty("F2", "Faculty 2", "JUNIOR", {"S1"}),
            Faculty("F3", "Faculty 3", "JUNIOR", {"S1"}),
        ]

        generator = RosterGenerator(faculty)

        roster, message = generator.generate(self.session)

        self.assertIsNotNone(roster)

        assigned = [
            f.id for f in roster.hall_assignments.values()
        ]

        self.assertEqual(
            len(assigned),
            len(set(assigned))
        )

    def test_chief_must_be_senior(self):
        faculty = [
            Faculty("F1", "Faculty 1", "JUNIOR", {"S1"}),
            Faculty("F2", "Faculty 2", "JUNIOR", {"S1"}),
            Faculty("F3", "Faculty 3", "JUNIOR", {"S1"}),
        ]

        generator = RosterGenerator(faculty)

        roster, message = generator.generate(self.session)

        self.assertIsNone(roster)

    def test_all_halls_are_assigned(self):
        faculty = [
            Faculty("F1", "Faculty 1", "SENIOR", {"S1"}),
            Faculty("F2", "Faculty 2", "JUNIOR", {"S1"}),
            Faculty("F3", "Faculty 3", "JUNIOR", {"S1"}),
        ]

        generator = RosterGenerator(faculty)

        roster, message = generator.generate(self.session)

        self.assertIsNotNone(roster)

        self.assertEqual(
            set(roster.hall_assignments.keys()),
            {"H1", "H2"}
        )

    def test_multiple_sessions(self):
        sessions = [
            Session("S1", ["H1", "H2"]),
            Session("S2", ["H3", "H4"])
        ]

        faculty = [
            Faculty("F1", "Faculty 1", "SENIOR", {"S1", "S2"}),
            Faculty("F2", "Faculty 2", "JUNIOR", {"S1", "S2"}),
            Faculty("F3", "Faculty 3", "JUNIOR", {"S1", "S2"}),
            Faculty("F4", "Faculty 4", "JUNIOR", {"S1", "S2"}),
        ]

        generator = RosterGenerator(faculty)

        for session in sessions:
            roster, message = generator.generate(session)

            self.assertIsNotNone(roster)

            self.assertEqual(
                len(roster.hall_assignments),
                len(session.halls)
            )

    def test_large_input(self):
        faculty = []

        for i in range(100):
            role = "SENIOR" if i < 10 else "JUNIOR"

            faculty.append(
                Faculty(
                    f"F{i + 1}",
                    f"Faculty {i + 1}",
                    role,
                    {"S1"}
                )
            )

        session = Session(
            "S1",
            [f"H{i + 1}" for i in range(50)]
        )

        generator = RosterGenerator(faculty)

        roster, message = generator.generate(session)

        self.assertIsNotNone(roster)

        self.assertEqual(
            len(roster.hall_assignments),
            50
        )

        assigned = [
            f.id for f in roster.hall_assignments.values()
        ]

        self.assertEqual(
            len(assigned),
            len(set(assigned))
        )

    def test_200_sessions(self):
        faculty = []

        for i in range(100):
            role = "SENIOR" if i < 10 else "JUNIOR"

            faculty.append(
                Faculty(
                    f"F{i + 1}",
                    f"Faculty {i + 1}",
                    role,
                    {f"S{j + 1}" for j in range(200)}
                )
            )

        sessions = [
            Session(
                f"S{i + 1}",
                [f"H{i + 1}_1", f"H{i + 1}_2"]
            )
            for i in range(200)
        ]

        generator = RosterGenerator(faculty)

        for session in sessions:
            roster, message = generator.generate(session)

            self.assertIsNotNone(roster)

            self.assertEqual(
                len(roster.hall_assignments),
                2
            )

            assigned = [
                f.id for f in roster.hall_assignments.values()
            ]

            self.assertEqual(
                len(assigned),
                len(set(assigned))
            )

    def test_senior_chief_reuse(self):
        sessions = [
            Session("S1", ["H1", "H2"]),
            Session("S2", ["H3", "H4"])
        ]

        faculty = [
            Faculty("F1", "Faculty 1", "SENIOR", {"S1", "S2"}),
            Faculty("F2", "Faculty 2", "SENIOR", {"S1", "S2"}),
            Faculty("F3", "Faculty 3", "JUNIOR", {"S1", "S2"}),
            Faculty("F4", "Faculty 4", "JUNIOR", {"S1", "S2"}),
            Faculty("F5", "Faculty 5", "JUNIOR", {"S1", "S2"}),
        ]

        generator = RosterGenerator(faculty)

        roster1, message1 = generator.generate(sessions[0])
        roster2, message2 = generator.generate(sessions[1])

        self.assertIsNotNone(roster1)
        self.assertIsNotNone(roster2)

        self.assertEqual(
            roster1.chief.id,
            roster2.chief.id
        )

        self.assertEqual(
            len(generator.used_chief_ids),
            1
        )

    def test_new_senior_when_previous_unavailable(self):
        sessions = [
            Session("S1", ["H1", "H2"]),
            Session("S2", ["H3", "H4"])
        ]

        faculty = [
            Faculty("F1", "Faculty 1", "SENIOR", {"S1"}),
            Faculty("F2", "Faculty 2", "SENIOR", {"S2"}),
            Faculty("F3", "Faculty 3", "JUNIOR", {"S1", "S2"}),
            Faculty("F4", "Faculty 4", "JUNIOR", {"S1", "S2"}),
            Faculty("F5", "Faculty 5", "JUNIOR", {"S1", "S2"}),
        ]

        generator = RosterGenerator(faculty)

        roster1, message1 = generator.generate(sessions[0])
        roster2, message2 = generator.generate(sessions[1])

        self.assertIsNotNone(roster1)
        self.assertIsNotNone(roster2)

        self.assertEqual(roster1.chief.id, "F1")
        self.assertEqual(roster2.chief.id, "F2")

        self.assertEqual(
            len(generator.used_chief_ids),
            2
        )


if __name__ == "__main__":
    unittest.main()