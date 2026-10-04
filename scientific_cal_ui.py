"""Streamlit UI for the scientific calculator."""

from __future__ import annotations

import html
from collections.abc import Callable
from typing import Any

import streamlit as st

from scientific_cal_controller import (
    append_token,
    backspace,
    calculate,
    clear_entry,
    clear_expression,
    clear_history,
    get_angle_mode,
    get_display_text,
    get_error,
    get_history,
    get_immediate_unary_mode,
    init_state,
    insert_function,
    set_angle_mode,
    set_immediate_unary_mode,
)

STUDENT_NAME = "Muhammad Waseem"

CALC_STYLES = """
<style>
.block-container {
    max-width: 520px;
    padding-top: 3rem;
    padding-bottom: 2rem;
    margin-top: 1.25rem;
}
.calc-header {
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
}
.calc-student-name {
    text-align: center;
    font-size: 15px;
    font-weight: 600;
    color: #4338ca;
    margin-bottom: 1rem;
}
.calc-title {
    font-size: 28px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.25rem;
}
.calc-subtitle {
    text-align: center;
    color: #888;
    margin-bottom: 1.25rem;
    font-size: 14px;
}
.calc-display-wrap {
    background: linear-gradient(145deg, #1e1e2e 0%, #2d2d44 100%);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 1rem;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.35);
    min-height: 88px;
}
.calc-expression {
    color: #a0a0b8;
    font-size: 14px;
    font-family: ui-monospace, monospace;
    text-align: right;
    min-height: 20px;
    word-break: break-all;
}
.calc-result {
    color: #f0f0f5;
    font-size: 36px;
    font-weight: 600;
    font-family: ui-monospace, monospace;
    text-align: right;
    line-height: 1.2;
    word-break: break-all;
}
.calc-mode-badge {
    display: inline-block;
    background: #3d3d5c;
    color: #c4c4dc;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 999px;
    margin-top: 8px;
}
div.stButton > button {
    width: 100%;
    min-height: 52px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 10px;
    border: 1px solid #e0e0e8;
    touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
    user-select: none;
}
div.stButton > button:active {
    transform: scale(0.97);
}
div.stButton > button:hover {
    border-color: #6366f1;
    color: #4338ca;
}
</style>
"""

CALC_KEYBOARD_HTML = """
<script>
(function () {
  const KEY_TO_BUTTON = {
    "+": "+",
    "-": "−",
    "*": "×",
    "/": "÷",
    "(": "(",
    ")": ")",
    ".": ".",
    "^": "xʸ",
  };
  const LETTER_TO_BUTTON = {
    s: "sin",
    c: "cos",
    t: "tan",
    l: "log",
  };

  function isSidebarField(el) {
    return el && el.closest && el.closest('[data-testid="stSidebar"]');
  }

  function isTextField(el) {
    if (!el || !el.tagName) return false;
    if (el.tagName === "TEXTAREA") return true;
    if (el.tagName === "INPUT") {
      const type = (el.type || "text").toLowerCase();
      return type !== "button" && type !== "submit" && type !== "checkbox" && type !== "radio";
    }
    return false;
  }

  function clickButton(label) {
    for (const btn of document.querySelectorAll("button")) {
      if (btn.innerText.trim() === label) {
        btn.click();
        return true;
      }
    }
    return false;
  }

  if (window.__calcKeyboardListener) {
    document.removeEventListener("keydown", window.__calcKeyboardListener, true);
  }

  window.__calcKeyboardListener = function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (isSidebarField(e.target) || isTextField(e.target)) return;

    if (e.key === "Enter" || e.code === "NumpadEnter") {
      e.preventDefault();
      clickButton("=");
      return;
    }
    if (e.key === "Escape" || e.key === "Delete") {
      e.preventDefault();
      clickButton("C");
      return;
    }
    if (e.key === "Backspace") {
      e.preventDefault();
      clickButton("⌫");
      return;
    }
    if (e.key >= "0" && e.key <= "9") {
      e.preventDefault();
      clickButton(e.key);
      return;
    }
    if (Object.prototype.hasOwnProperty.call(KEY_TO_BUTTON, e.key)) {
      e.preventDefault();
      clickButton(KEY_TO_BUTTON[e.key]);
      return;
    }
    const letter = e.key.length === 1 ? e.key.toLowerCase() : "";
    if (letter && Object.prototype.hasOwnProperty.call(LETTER_TO_BUTTON, letter)) {
      e.preventDefault();
      clickButton(LETTER_TO_BUTTON[letter]);
    }
  };

  document.addEventListener("keydown", window.__calcKeyboardListener, true);
})();
</script>
"""

ButtonRow = tuple[str, str, Callable[..., None], tuple[Any, ...]]


def _render_button(
    label: str,
    action: str,
    callback: Callable[..., None],
    *args: Any,
    help_text: str | None = None,
) -> None:
    st.button(
        label,
        key=f"btn_{action}",
        help=help_text,
        use_container_width=True,
        on_click=callback,
        args=args,
    )


def _render_button_row(buttons: list[ButtonRow]) -> None:
    cols = st.columns(len(buttons))
    for col, (label, action, callback, args) in zip(cols, buttons, strict=True):
        with col:
            _render_button(label, action, callback, *args)


def _render_sidebar() -> None:
    with st.sidebar:
        st.header("Settings")
        mode = st.radio(
            "Angle mode",
            options=["DEG", "RAD"],
            index=0 if get_angle_mode() == "DEG" else 1,
            horizontal=True,
        )
        set_angle_mode(mode)

        immediate = st.toggle(
            "Immediate function mode",
            value=get_immediate_unary_mode(),
            help="sin → type 90 → = gives 1 without showing sin(",
        )
        set_immediate_unary_mode(immediate)

        st.divider()
        st.subheader("History")
        if st.button("Clear history", use_container_width=True):
            clear_history()
        history = get_history()
        if history:
            for item in history:
                st.caption(item)
        else:
            st.caption("No calculations yet.")

        st.divider()
        st.markdown(
            """
**Keyboard**
- **0–9**, `+`, `-`, `*`, `/`, `(`, `)`, `.`, `^` map to the keypad
- **s** → sin · **c** → cos · **t** → tan · **l** → log (then type the rest via buttons)
- **Enter** = calculate · **Backspace** · **Esc** clear
- On-screen buttons work with **mouse** and **touch**

**Function modes**
- **Off (default):** `sin(` then value then **=** (adds `)` for you)
- **Immediate on:** **sin** → **90** → **=** (shows `sin` then `sin 90`, result **1**)

**Tips**
- Use `^` for powers · `log` is base 10 · `ln` is natural log
- `ANS` inserts the last result · `*` and `/` work like × and ÷
"""
        )


def _render_display() -> None:
    display_text = html.escape(get_display_text())
    st.markdown(
        f"""
<div class="calc-display-wrap">
  <div class="calc-expression">&nbsp;</div>
  <div class="calc-result">{display_text}</div>
  <span class="calc-mode-badge">{html.escape(get_angle_mode())}</span>
  {"<span class='calc-mode-badge'>IMM</span>" if get_immediate_unary_mode() else ""}
</div>
""",
        unsafe_allow_html=True,
    )
    error = get_error()
    if error:
        st.error(error)


def _render_keypad() -> None:
    st.caption("Scientific functions")
    _render_button_row(
        [
            ("sin", "sin", insert_function, ("sin",)),
            ("cos", "cos", insert_function, ("cos",)),
            ("tan", "tan", insert_function, ("tan",)),
            ("√", "sqrt", insert_function, ("sqrt",)),
            ("xʸ", "append_pow", append_token, ("^",)),
        ]
    )
    _render_button_row(
        [
            ("asin", "asin", insert_function, ("asin",)),
            ("acos", "acos", insert_function, ("acos",)),
            ("atan", "atan", insert_function, ("atan",)),
            ("log", "log", insert_function, ("log",)),
            ("ln", "ln", insert_function, ("ln",)),
        ]
    )
    _render_button_row(
        [
            ("exp", "exp", insert_function, ("exp",)),
            ("|x|", "abs", insert_function, ("abs",)),
            ("n!", "fact", insert_function, ("factorial",)),
            ("π", "append_pi", append_token, ("pi",)),
            ("e", "append_e", append_token, ("e",)),
        ]
    )

    st.divider()
    st.caption("Keypad")
    _render_button_row(
        [
            ("(", "append_lparen", append_token, ("(",)),
            (")", "append_rparen", append_token, (")",)),
            ("C", "clear", clear_expression, ()),
            ("CE", "clear_entry", clear_entry, ()),
            ("⌫", "backspace", backspace, ()),
        ]
    )
    _render_button_row(
        [
            ("7", "append_7", append_token, ("7",)),
            ("8", "append_8", append_token, ("8",)),
            ("9", "append_9", append_token, ("9",)),
            ("÷", "append_div", append_token, ("÷",)),
            ("ANS", "append_ans", append_token, ("ANS",)),
        ]
    )
    _render_button_row(
        [
            ("4", "append_4", append_token, ("4",)),
            ("5", "append_5", append_token, ("5",)),
            ("6", "append_6", append_token, ("6",)),
            ("×", "append_mul", append_token, ("×",)),
            ("mod", "append_mod", append_token, (" mod ",)),
        ]
    )
    _render_button_row(
        [
            ("1", "append_1", append_token, ("1",)),
            ("2", "append_2", append_token, ("2",)),
            ("3", "append_3", append_token, ("3",)),
            ("−", "append_minus", append_token, ("-",)),
            ("+", "append_plus", append_token, ("+",)),
        ]
    )
    _render_button_row(
        [
            ("0", "append_0", append_token, ("0",)),
            (".", "append_dot", append_token, (".",)),
            ("=", "equals", calculate, ()),
        ]
    )


def _render_keyboard_helper() -> None:
    st.html(CALC_KEYBOARD_HTML, unsafe_allow_javascript=True)


def run_calculator_app() -> None:
    st.set_page_config(
        page_title="Scientific Calculator",
        page_icon="🧮",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    st.markdown(CALC_STYLES, unsafe_allow_html=True)

    init_state()
    _render_sidebar()

    student_line = html.escape(f"Student Name = {STUDENT_NAME}")
    st.markdown(
        f"""
<div class="calc-header">
  <div class="calc-student-name">{student_line}</div>
  <div class="calc-title">Scientific Calculator</div>
  <div class="calc-subtitle">Streamlit · HCCDA learning project</div>
</div>
""",
        unsafe_allow_html=True,
    )

    _render_display()
    _render_keypad()
    _render_keyboard_helper()
