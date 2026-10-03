"""Calculator session state and actions (connects core logic to Streamlit)."""

from __future__ import annotations

from typing import Any

import streamlit as st

from scientific_cal_core import evaluate_expression, format_result

STATE_DEFAULTS: dict[str, Any] = {
    "expression": "",
    "last_answer": 0.0,
    "history": [],
    "angle_mode": "DEG",
    "error": "",
}


def init_state() -> None:
    for key, value in STATE_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def append_token(token: str) -> None:
    st.session_state.error = ""
    st.session_state.expression = f"{st.session_state.expression}{token}"


def backspace() -> None:
    st.session_state.error = ""
    st.session_state.expression = st.session_state.expression[:-1]


def clear_expression() -> None:
    st.session_state.error = ""
    st.session_state.expression = ""


def clear_entry() -> None:
    clear_expression()


def insert_function(name: str) -> None:
    append_token(f"{name}(")


def calculate() -> None:
    st.session_state.error = ""
    try:
        result = evaluate_expression(
            st.session_state.expression,
            st.session_state.angle_mode,
            float(st.session_state.last_answer),
        )
        formatted = format_result(result)
        entry = f"{st.session_state.expression} = {formatted}"
        st.session_state.history.insert(0, entry)
        st.session_state.history = st.session_state.history[:20]
        st.session_state.last_answer = result
        st.session_state.expression = formatted
    except Exception as exc:  # noqa: BLE001 — user-facing calculator errors
        st.session_state.error = str(exc)


def get_display_text() -> str:
    return st.session_state.expression or "0"


def get_angle_mode() -> str:
    return str(st.session_state.angle_mode)


def set_angle_mode(mode: str) -> None:
    st.session_state.angle_mode = mode


def get_error() -> str:
    return str(st.session_state.error)


def get_history() -> list[str]:
    return list(st.session_state.history)


def clear_history() -> None:
    st.session_state.history = []
