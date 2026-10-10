def is_available(faculty, session_id):
    return faculty.is_available(session_id)


def is_senior(faculty):
    return faculty.is_senior()


def can_assign_to_hall(faculty, session_id, assigned_faculty):
    if not is_available(faculty, session_id):
        return False

    if faculty.id in assigned_faculty:
        return False

    return True


def can_be_chief(faculty, session_id):
    if not is_available(faculty, session_id):
        return False

    if not is_senior(faculty):
        return False

    return True


def all_halls_assigned(session, hall_assignments):
    return len(hall_assignments) == len(session.halls)


def validate_roster(roster, session):
    if roster.chief is None:
        return False, "No Chief Invigilator assigned."

    if not roster.chief.is_available(session.id):
        return False, "Chief Invigilator is not available for this session."

    if not roster.chief.is_senior():
        return False, "Chief Invigilator must be SENIOR."

    if len(roster.hall_assignments) != len(session.halls):
        return False, "Not all halls have been assigned."

    assigned_ids = set()

    for hall in session.halls:
        if hall not in roster.hall_assignments:
            return False, f"Hall {hall} has no invigilator."

        faculty = roster.hall_assignments[hall]

        if not faculty.is_available(session.id):
            return False, f"{faculty.id} is unavailable for {session.id}."

        if faculty.id in assigned_ids:
            return False, f"{faculty.id} is assigned to multiple halls."

        assigned_ids.add(faculty.id)

    return True, "Roster is valid."