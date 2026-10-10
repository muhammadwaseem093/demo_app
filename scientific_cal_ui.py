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
.stApp {
    background:
        radial-gradient(900px 420px at 8% -10%, rgba(99, 102, 241, 0.28), transparent 60%),
        radial-gradient(700px 380px at 100% 0%, rgba(244, 114, 182, 0.22), transparent 55%),
        radial-gradient(800px 480px at 80% 100%, rgba(45, 212, 191, 0.22), transparent 60%),
        linear-gradient(165deg, #eef2ff 0%, #fdf2f8 48%, #ecfeff 100%);
}
[data-testid="stMain"] .block-container {
    max-width: 520px;
    padding-top: 2.25rem;
    padding-bottom: 2rem;
    margin-top: 1.25rem;
}
.calc-header {
    margin-top: 0.25rem;
    margin-bottom: 0.5rem;
}
.calc-student-name {
    text-align: center;
    font-size: 15px;
    font-weight: 700;
    color: #4f46e5;
    margin-bottom: 0.85rem;
    letter-spacing: 0.01em;
}
.calc-title {
    font-size: 28px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.25rem;
    background: linear-gradient(90deg, #4f46e5 0%, #0d9488 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.calc-subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 1.1rem;
    font-size: 14px;
}
.calc-section {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #475569;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin: 0.15rem 0 0.35rem;
}
.calc-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    display: inline-block;
}
.calc-dot-sci { background: #6366f1; }
.calc-dot-key { background: #f97316; }
.calc-display-wrap {
    background: linear-gradient(145deg, #1e1b4b 0%, #312e81 58%, #0f766e 140%);
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 1rem;
    box-shadow: 0 12px 28px rgba(49, 46, 129, 0.28);
    min-height: 88px;
}
.calc-expression {
    color: #c4b5fd;
    font-size: 14px;
    font-family: ui-monospace, monospace;
    text-align: right;
    min-height: 20px;
    word-break: break-all;
}
.calc-result {
    color: #f8fafc;
    font-size: 36px;
    font-weight: 700;
    font-family: ui-monospace, monospace;
    text-align: right;
    line-height: 1.2;
    word-break: break-all;
}
.calc-mode-badge {
    display: inline-block;
    background: #f59e0b;
    color: #1e1b4b;
    font-size: 11px;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 999px;
    margin-top: 8px;
    margin-right: 6px;
}
.calc-mode-badge-imm {
    background: #2dd4bf;
    color: #134e4a;
}
[data-testid="stMain"] hr {
    border: none;
    height: 3px;
    border-radius: 999px;
    background: linear-gradient(90deg, #818cf8, #22d3ee, #fb923c);
    margin: 0.85rem 0 0.65rem;
}
div.stButton > button {
    width: 100%;
    min-height: 52px;
    font-size: 16px;
    font-weight: 700;
    border-radius: 12px;
    border: 1px solid transparent;
    touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
    user-select: none;
    transition: transform 0.08s ease, filter 0.08s ease;
}
div.stButton > button:active {
    transform: scale(0.97);
}
div.stButton > button:focus-visible {
    outline: 2px solid #4f46e5;
    outline-offset: 2px;
}

div.st-key-btn_sin div.stButton > button,
div.st-key-btn_cos div.stButton > button,
div.st-key-btn_tan div.stButton > button,
div.st-key-btn_sqrt div.stButton > button,
div.st-key-btn_abs div.stButton > button,
div.st-key-btn_fact div.stButton > button {
    background: #dbeafe !important;
    color: #1d4ed8 !important;
    border-color: #93c5fd !important;
}
div.st-key-btn_asin div.stButton > button,
div.st-key-btn_acos div.stButton > button,
div.st-key-btn_atan div.stButton > button {
    background: #ede9fe !important;
    color: #6d28d9 !important;
    border-color: #c4b5fd !important;
}
div.st-key-btn_log div.stButton > button,
div.st-key-btn_ln div.stButton > button,
div.st-key-btn_exp div.stButton > button {
    background: #ccfbf1 !important;
    color: #0f766e !important;
    border-color: #5eead4 !important;
}
div.st-key-btn_append_pow div.stButton > button,
div.st-key-btn_append_pi div.stButton > button,
div.st-key-btn_append_e div.stButton > button {
    background: #fef9c3 !important;
    color: #a16207 !important;
    border-color: #fde047 !important;
}
div.st-key-btn_append_lparen div.stButton > button,
div.st-key-btn_append_rparen div.stButton > button,
div.st-key-btn_append_0 div.stButton > button,
div.st-key-btn_append_1 div.stButton > button,
div.st-key-btn_append_2 div.stButton > button,
div.st-key-btn_append_3 div.stButton > button,
div.st-key-btn_append_4 div.stButton > button,
div.st-key-btn_append_5 div.stButton > button,
div.st-key-btn_append_6 div.stButton > button,
div.st-key-btn_append_7 div.stButton > button,
div.st-key-btn_append_8 div.stButton > button,
div.st-key-btn_append_9 div.stButton > button,
div.st-key-btn_append_dot div.stButton > button {
    background: #ffffff !important;
    color: #312e81 !important;
    border-color: #c7d2fe !important;
}
div.st-key-btn_append_div div.stButton > button,
div.st-key-btn_append_mul div.stButton > button,
div.st-key-btn_append_minus div.stButton > button,
div.st-key-btn_append_plus div.stButton > button {
    background: #ffedd5 !important;
    color: #c2410c !important;
    border-color: #fdba74 !important;
}
div.st-key-btn_clear div.stButton > button,
div.st-key-btn_clear_entry div.stButton > button {
    background: #ffe4e6 !important;
    color: #be123c !important;
    border-color: #fda4af !important;
}
div.st-key-btn_backspace div.stButton > button {
    background: #fef3c7 !important;
    color: #b45309 !important;
    border-color: #fcd34d !important;
}
div.st-key-btn_equals div.stButton > button {
    background: linear-gradient(90deg, #4f46e5 0%, #0d9488 100%) !important;
    color: #ffffff !important;
    border-color: transparent !important;
    font-size: 20px;
    box-shadow: 0 8px 18px rgba(79, 70, 229, 0.28);
}
div.st-key-btn_equals div.stButton > button:hover,
div.st-key-btn_sin div.stButton > button:hover,
div.st-key-btn_cos div.stButton > button:hover,
div.st-key-btn_tan div.stButton > button:hover,
div.st-key-btn_sqrt div.stButton > button:hover,
div.st-key-btn_abs div.stButton > button:hover,
div.st-key-btn_fact div.stButton > button:hover,
div.st-key-btn_asin div.stButton > button:hover,
div.st-key-btn_acos div.stButton > button:hover,
div.st-key-btn_atan div.stButton > button:hover,
div.st-key-btn_log div.stButton > button:hover,
div.st-key-btn_ln div.stButton > button:hover,
div.st-key-btn_exp div.stButton > button:hover,
div.st-key-btn_append_pow div.stButton > button:hover,
div.st-key-btn_append_pi div.stButton > button:hover,
div.st-key-btn_append_e div.stButton > button:hover,
div.st-key-btn_append_lparen div.stButton > button:hover,
div.st-key-btn_append_rparen div.stButton > button:hover,
div.st-key-btn_append_0 div.stButton > button:hover,
div.st-key-btn_append_1 div.stButton > button:hover,
div.st-key-btn_append_2 div.stButton > button:hover,
div.st-key-btn_append_3 div.stButton > button:hover,
div.st-key-btn_append_4 div.stButton > button:hover,
div.st-key-btn_append_5 div.stButton > button:hover,
div.st-key-btn_append_6 div.stButton > button:hover,
div.st-key-btn_append_7 div.stButton > button:hover,
div.st-key-btn_append_8 div.stButton > button:hover,
div.st-key-btn_append_9 div.stButton > button:hover,
div.st-key-btn_append_dot div.stButton > button:hover,
div.st-key-btn_append_div div.stButton > button:hover,
div.st-key-btn_append_mul div.stButton > button:hover,
div.st-key-btn_append_minus div.stButton > button:hover,
div.st-key-btn_append_plus div.stButton > button:hover,
div.st-key-btn_clear div.stButton > button:hover,
div.st-key-btn_clear_entry div.stButton > button:hover,
div.st-key-btn_backspace div.stButton > button:hover {
    filter: brightness(0.96);
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
- `*` and `/` work like × and ÷
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
  {"<span class='calc-mode-badge calc-mode-badge-imm'>IMM</span>" if get_immediate_unary_mode() else ""}
</div>
""",
        unsafe_allow_html=True,
    )
    error = get_error()
    if error:
        st.error(error)


def _render_keypad() -> None:
    st.markdown(
        '<div class="calc-section"><span class="calc-dot calc-dot-sci"></span>Scientific functions</div>',
        unsafe_allow_html=True,
    )
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
    st.markdown(
        '<div class="calc-section"><span class="calc-dot calc-dot-key"></span>Keypad</div>',
        unsafe_allow_html=True,
    )
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
            ("×", "append_mul", append_token, ("×",)),
        ]
    )
    _render_button_row(
        [
            ("4", "append_4", append_token, ("4",)),
            ("5", "append_5", append_token, ("5",)),
            ("6", "append_6", append_token, ("6",)),
            ("−", "append_minus", append_token, ("-",)),
            ("+", "append_plus", append_token, ("+",)),
        ]
    )
    _render_button_row(
        [
            ("1", "append_1", append_token, ("1",)),
            ("2", "append_2", append_token, ("2",)),
            ("3", "append_3", append_token, ("3",)),
            ("0", "append_0", append_token, ("0",)),
            (".", "append_dot", append_token, (".",)),
        ]
    )
    _render_button_row(
        [
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
