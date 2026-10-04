"""Calculator session state and actions (connects core logic to Streamlit)."""

from __future__ import annotations

from typing import Any

import streamlit as st

from scientific_cal_core import auto_close_parentheses, evaluate_expression, format_result

_BINARY_TOKENS = frozenset({"+", "-", "×", "÷", " mod ", "^"})

STATE_DEFAULTS: dict[str, Any] = {
    "expression": "",
    "last_answer": 0.0,
    "history": [],
    "angle_mode": "DEG",
    "error": "",
    "immediate_unary_mode": False,
    "pending_unary": None,
}


def init_state() -> None:
    for key, value in STATE_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _apply_pending_unary() -> str:
    name = st.session_state.pending_unary
    if not name:
        raise ValueError("No function waiting for a value")
    arg = st.session_state.expression.strip()
    if not arg:
        raise ValueError(f"Enter a value for {name}")
    st.session_state.pending_unary = None
    return f"{name}({auto_close_parentheses(arg)})"


def append_token(token: str) -> None:
    st.session_state.error = ""
    if st.session_state.immediate_unary_mode and st.session_state.pending_unary:
        if token in _BINARY_TOKENS:
            closed = _apply_pending_unary()
            st.session_state.expression = closed
        else:
            st.session_state.expression = f"{st.session_state.expression}{token}"
            return
    expr = st.session_state.expression
    if token in _BINARY_TOKENS:
        expr = auto_close_parentheses(expr)
    st.session_state.expression = f"{expr}{token}"


def backspace() -> None:
    st.session_state.error = ""
    st.session_state.expression = st.session_state.expression[:-1]


def clear_expression() -> None:
    st.session_state.error = ""
    st.session_state.expression = ""
    st.session_state.pending_unary = None


def clear_entry() -> None:
    clear_expression()


def insert_function(name: str) -> None:
    st.session_state.error = ""
    if st.session_state.immediate_unary_mode:
        if st.session_state.pending_unary and st.session_state.expression.strip():
            try:
                closed = _apply_pending_unary()
                result = evaluate_expression(
                    closed,
                    st.session_state.angle_mode,
                    float(st.session_state.last_answer),
                )
                st.session_state.expression = format_result(result)
            except Exception as exc:  # noqa: BLE001
                st.session_state.error = str(exc)
                return
        st.session_state.pending_unary = name
        st.session_state.expression = ""
        return
    append_token(f"{name}(")


def calculate() -> None:
    st.session_state.error = ""
    try:
        if st.session_state.immediate_unary_mode and st.session_state.pending_unary:
            closed = _apply_pending_unary()
        else:
            closed = auto_close_parentheses(st.session_state.expression)
        st.session_state.expression = closed
        result = evaluate_expression(
            closed,
            st.session_state.angle_mode,
            float(st.session_state.last_answer),
        )
        formatted = format_result(result)
        entry = f"{closed} = {formatted}"
        st.session_state.history.insert(0, entry)
        st.session_state.history = st.session_state.history[:20]
        st.session_state.last_answer = result
        st.session_state.expression = formatted
    except Exception as exc:  # noqa: BLE001 — user-facing calculator errors
        st.session_state.error = str(exc)


def get_display_text() -> str:
    if st.session_state.immediate_unary_mode and st.session_state.pending_unary:
        if st.session_state.expression:
            return f"{st.session_state.pending_unary} {st.session_state.expression}"
        return str(st.session_state.pending_unary)
    return st.session_state.expression or "0"


def get_immediate_unary_mode() -> bool:
    return bool(st.session_state.immediate_unary_mode)


def set_immediate_unary_mode(enabled: bool) -> None:
    st.session_state.immediate_unary_mode = enabled
    if not enabled:
        st.session_state.pending_unary = None


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
