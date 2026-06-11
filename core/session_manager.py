

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class SessionManager:
    """
    Scan session manager.

    Responsibilities:
    -----------------
    - Create scan sessions
    - Track scan status
    - Save phase progress
    - Support resume scans
    - Store session metadata
    """

    def __init__(
        self,
        session_dir: str | Path = "outputs/sessions",
    ):
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(parents=True, exist_ok=True)

    def create_session(
        self,
        target: str,
        mode: str = "normal",
    ) -> Dict[str, Any]:

        session_id = str(uuid.uuid4())

        session = {
            "session_id": session_id,
            "target": target,
            "mode": mode,
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed_phases": [],
            "current_phase": None,
            "results": {},
        }

        self.save_session(session)

        return session

    def get_session_path(
        self,
        session_id: str,
    ) -> Path:

        return self.session_dir / f"{session_id}.json"

    def save_session(
        self,
        session: Dict[str, Any],
    ) -> Path:

        session["updated_at"] = datetime.now().isoformat()

        path = self.get_session_path(
            session["session_id"]
        )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                session,
                f,
                indent=4,
                ensure_ascii=False,
            )

        return path

    def load_session(
        self,
        session_id: str,
    ) -> Dict[str, Any] | None:

        path = self.get_session_path(session_id)

        if not path.exists():
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception:
            return None

    def update_status(
        self,
        session_id: str,
        status: str,
    ) -> bool:

        session = self.load_session(session_id)

        if not session:
            return False

        session["status"] = status

        self.save_session(session)

        return True

    def set_current_phase(
        self,
        session_id: str,
        phase_name: str,
    ) -> bool:

        session = self.load_session(session_id)

        if not session:
            return False

        session["current_phase"] = phase_name
        session["status"] = "running"

        self.save_session(session)

        return True

    def mark_phase_complete(
        self,
        session_id: str,
        phase_name: str,
        result: Any = None,
    ) -> bool:

        session = self.load_session(session_id)

        if not session:
            return False

        completed = session.get("completed_phases", [])

        if phase_name not in completed:
            completed.append(phase_name)

        session["completed_phases"] = completed
        session["current_phase"] = None

        if result is not None:
            session.setdefault("results", {})
            session["results"][phase_name] = result

        self.save_session(session)

        return True

    def is_phase_completed(
        self,
        session_id: str,
        phase_name: str,
    ) -> bool:

        session = self.load_session(session_id)

        if not session:
            return False

        return phase_name in session.get(
            "completed_phases",
            [],
        )

    def get_results(
        self,
        session_id: str,
    ) -> Dict[str, Any]:

        session = self.load_session(session_id)

        if not session:
            return {}

        return session.get("results", {})

    def complete_session(
        self,
        session_id: str,
    ) -> bool:

        session = self.load_session(session_id)

        if not session:
            return False

        session["status"] = "completed"
        session["completed_at"] = datetime.now().isoformat()
        session["current_phase"] = None

        self.save_session(session)

        return True

    def fail_session(
        self,
        session_id: str,
        reason: str,
    ) -> bool:

        session = self.load_session(session_id)

        if not session:
            return False

        session["status"] = "failed"
        session["failed_at"] = datetime.now().isoformat()
        session["failure_reason"] = reason
        session["current_phase"] = None

        self.save_session(session)

        return True

    def list_sessions(self) -> list[Dict[str, Any]]:

        sessions = []

        for file in self.session_dir.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    sessions.append(json.load(f))
            except Exception:
                continue

        return sorted(
            sessions,
            key=lambda item: item.get("updated_at", ""),
            reverse=True,
        )


session_manager = SessionManager()