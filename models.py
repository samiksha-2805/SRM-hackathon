from dataclasses import dataclass, field


@dataclass
class Faculty:
    id: str
    name: str
    role: str
    available_sessions: set[str] = field(default_factory=set)

    def is_available(self, session_id):
        return session_id in self.available_sessions

    def is_senior(self):
        return self.role.upper() == "SENIOR"


@dataclass
class Session:
    id: str
    halls: list[str]


@dataclass
class Roster:
    session_id: str
    chief: Faculty | None = None
    hall_assignments: dict[str, Faculty] = field(default_factory=dict)

    def add_hall_assignment(self, hall, faculty):
        self.hall_assignments[hall] = faculty