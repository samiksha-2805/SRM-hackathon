from models import Roster
from hopcroft_karp import HopcroftKarp
from constraints import can_assign_to_hall, can_be_chief, validate_roster


class RosterGenerator:

    def __init__(self, faculty):
        self.faculty = faculty
        self.used_chief_ids = set()

    def get_available_faculty(self, session_id):
        return [
            f for f in self.faculty
            if f.is_available(session_id)
        ]

    def build_graph(self, session, faculty_list):
        return {
            faculty.id: session.halls.copy()
            for faculty in faculty_list
        }

    def check_feasibility(self, session):
        available = self.get_available_faculty(session.id)

        if not available:
            return False, (
                f"No faculty is available for session {session.id}. "
                "No SENIOR faculty is available to act as Chief Invigilator."
            )

        senior_available = [
            f for f in available
            if can_be_chief(f, session.id)
        ]

        if not senior_available:
            return False, (
                "No SENIOR faculty is available to act as Chief Invigilator."
            )

        if len(available) < len(session.halls) + 1:
            return False, (
                f"Insufficient faculty. "
                f"{len(session.halls)} hall invigilators and "
                f"1 Chief are required, but only "
                f"{len(available)} faculty are available."
            )

        for chief in senior_available:

            remaining_faculty = [
                f for f in available
                if f.id != chief.id
            ]

            graph = self.build_graph(
                session,
                remaining_faculty
            )

            matcher = HopcroftKarp(graph)
            matching = matcher.maximum_matching()

            if matching == len(session.halls):
                return True, "Feasible"

        return False, (
            f"Unable to assign {len(session.halls)} halls "
            f"without assigning a faculty member to multiple halls."
        )

    def generate(self, session):
        feasible, reason = self.check_feasibility(session)

        if not feasible:
            return None, reason

        available = self.get_available_faculty(session.id)

        senior_faculty = [
            f for f in available
            if can_be_chief(f, session.id)
        ]

        senior_faculty.sort(
            key=lambda f: f.id not in self.used_chief_ids
        )

        for chief in senior_faculty:

            roster = Roster(
                session.id,
                chief
            )

            remaining_faculty = [
                f for f in available
                if f.id != chief.id
            ]

            if self.backtrack(
                session,
                remaining_faculty,
                roster
            ):
                valid, message = validate_roster(
                    roster,
                    session
                )

                if valid:
                    self.used_chief_ids.add(chief.id)
                    return roster, "Roster generated successfully."

        return None, "Unable to generate a valid roster."

    def backtrack(self, session, faculty_list, roster):

        if len(roster.hall_assignments) == len(session.halls):
            return True

        hall = self.select_hall(
            session,
            faculty_list,
            roster
        )

        if hall is None:
            return False

        used_ids = {
            faculty.id
            for faculty in roster.hall_assignments.values()
        }

        for faculty in faculty_list:

            if not can_assign_to_hall(
                faculty,
                session.id,
                used_ids
            ):
                continue

            roster.add_hall_assignment(
                hall,
                faculty
            )

            if self.forward_check(
                session,
                faculty_list,
                roster
            ):
                if self.backtrack(
                    session,
                    faculty_list,
                    roster
                ):
                    return True

            del roster.hall_assignments[hall]

        return False

    def select_hall(self, session, faculty_list, roster):

        remaining_halls = [
            hall
            for hall in session.halls
            if hall not in roster.hall_assignments
        ]

        if not remaining_halls:
            return None

        used_ids = {
            faculty.id
            for faculty in roster.hall_assignments.values()
        }

        best_hall = None
        best_count = float("inf")

        for hall in remaining_halls:

            count = 0

            for faculty in faculty_list:

                if can_assign_to_hall(
                    faculty,
                    session.id,
                    used_ids
                ):
                    count += 1

            if count < best_count:
                best_count = count
                best_hall = hall

        if best_count == 0:
            return None

        return best_hall

    def forward_check(
        self,
        session,
        faculty_list,
        roster
    ):

        used_ids = {
            faculty.id
            for faculty in roster.hall_assignments.values()
        }

        for hall in session.halls:

            if hall in roster.hall_assignments:
                continue

            possible = False

            for faculty in faculty_list:

                if can_assign_to_hall(
                    faculty,
                    session.id,
                    used_ids
                ):
                    possible = True
                    break

            if not possible:
                return False

        return True