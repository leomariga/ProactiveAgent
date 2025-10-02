"""
Beautiful terminal chat example

Renders:
- User and AI messages as left-aligned chat bubbles
- Agent "thoughts" (decision and sleep time) as right-aligned dim notes

No third-party dependencies are required (pure stdlib rendering).
"""

import shutil
import sys
import textwrap
import time
import threading
from typing import List

from proactiveagent import ProactiveAgent, OpenAIProvider


# ANSI styles
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"

FG_CYAN = "\033[36m"
FG_GREEN = "\033[32m"
FG_GREY = "\033[90m"


def get_terminal_width(default: int = 100) -> int:
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return default


def wrap_lines(text: str, max_width: int) -> List[str]:
    wrapped = []
    for paragraph in text.splitlines() or [""]:
        if not paragraph:
            wrapped.append("")
            continue
        wrapped.extend(textwrap.wrap(paragraph, width=max_width, replace_whitespace=False))
    return wrapped if wrapped else [""]


def render_bubble(text: str, *, align_right: bool, color: str) -> str:
    # Layout
    term_width = max(40, get_terminal_width())
    max_content_width = min(68, term_width - 10)  # keep readable width

    lines = wrap_lines(text, max_content_width)
    content_width = max((len(line) for line in lines), default=0)

    # Bubble borders
    top = f"╭{'─' * (content_width + 2)}╮"
    bottom = f"╰{'─' * (content_width + 2)}╯"

    body_lines = []
    for line in lines:
        padding = " " * (content_width - len(line))
        # color only the content, keep borders neutral to avoid width calc drift
        colored = f"{color}{line}{RESET}"
        body_lines.append(f"│ {colored}{padding} │")

    bubble_lines = [top, *body_lines, bottom]

    # Right alignment by left-padding all lines equally
    if align_right:
        bubble_width = content_width + 4
        left_pad = max(0, term_width - bubble_width - 2)
        pad = " " * left_pad
        bubble_lines = [pad + l for l in bubble_lines]

    return "\n".join(bubble_lines)


def render_right_note(text: str, *, color: str) -> str:
    # A borderless, right-aligned note for "thoughts"
    term_width = max(40, get_terminal_width())
    max_content_width = min(68, term_width - 10)

    lines = wrap_lines(text, max_content_width)
    rendered = []
    for line in lines:
        pad = max(0, term_width - len(line) - 2)
        rendered.append(" " * pad + f"{color}{line}{RESET}")
    return "\n".join(rendered)


def render_left_block(text: str, *, color: str) -> str:
    # A borderless, left-aligned block for user/AI messages
    term_width = max(40, get_terminal_width())
    max_content_width = min(68, term_width - 6)

    lines = wrap_lines(text, max_content_width)
    rendered = []
    for line in lines:
        rendered.append("  " + f"{color}{line}{RESET}")
    return "\n".join(rendered)


class TerminalChatRenderer:
    def __init__(self) -> None:
        self.last_print_newline = True

    def _print_label(self, label: str, *, align_right: bool, style: str = DIM) -> None:
        term_width = get_terminal_width()
        text = f"{style}{label}{RESET}"
        if align_right:
            # subtract a small margin
            pad = max(0, term_width - len(label) - 2)
            sys.stdout.write(" " * pad + text + "\n")
        else:
            sys.stdout.write(text + "\n")

    def print_user(self, message: str) -> None:
        self._print_label("You", align_right=False)
        sys.stdout.write(render_left_block(message, color=FG_CYAN) + "\n\n")
        sys.stdout.flush()

    def print_ai(self, message: str) -> None:
        self._print_label("🤖 AI", align_right=False)
        sys.stdout.write(render_left_block(message, color=FG_GREEN) + "\n\n")
        sys.stdout.flush()

    def print_thought(self, message: str) -> None:
        self._print_label("🧠 Thought", align_right=True, style=f"{DIM}{ITALIC}")
        dim_grey = f"{DIM}{ITALIC}{FG_GREY}"
        sys.stdout.write(render_right_note(message, color=dim_grey) + "\n\n")
        sys.stdout.flush()


renderer = TerminalChatRenderer()


_prompt_lock = threading.Lock()
_prompting: bool = False


def _print_immediate(kind: str, message: str):
    global _prompting
    with _prompt_lock:
        if _prompting:
            # Clear current input line, print message, then redraw prompt
            sys.stdout.write("\r\033[2K")  # clear current line
            sys.stdout.flush()
            if kind == "ai":
                renderer.print_ai(message)
            else:
                renderer.print_thought(message)
            # redraw prompt without newline
            sys.stdout.write("You: ")
            sys.stdout.flush()
            return
    # Not prompting, print normally
    if kind == "ai":
        renderer.print_ai(message)
    else:
        renderer.print_thought(message)


def on_ai_response(response: str):
    _print_immediate("ai", response)


def on_sleep_time_calculated(sleep_time: int, reasoning: str):
    thought = f"⏰ Sleep time: {sleep_time}s — {reasoning}"
    _print_immediate("thought", thought)


def on_decision_made(should_respond: bool, reasoning: str):
    decision = "✅ RESPOND" if should_respond else "❌ NO RESPONSE"
    thought = f"{decision} — {reasoning}"
    _print_immediate("thought", thought)


def main():
    # Provider
    provider = OpenAIProvider(
        model="gpt-5-nano",
    )

    # Agent
    agent = ProactiveAgent(
        provider=provider,
        system_prompt=(
            "You are a casual young person bored and texting on WhatsApp. "
            "Use informal language, emojis, abbreviations; keep responses very short."
        ),
        decision_config={
            "wake_up_pattern": (
                "This is a normal WhatsApp conversation; adapt response frequency to user."
            ),
            "engagement_high_threshold": 2,
            "engagement_medium_threshold": 1,
        },
        # log_level="DEBUG",
    )

    # Callbacks
    agent.add_callback(on_ai_response)
    agent.add_sleep_time_callback(on_sleep_time_calculated)
    agent.add_decision_callback(on_decision_made)

    agent.start()

    sys.stdout.write(f"{BOLD}Chat started! Type your messages. Type 'quit' to exit.{RESET}\n\n")
    sys.stdout.flush()

    try:
        while True:
            # indicate we are prompting; callbacks will buffer
            with _prompt_lock:
                global _prompting
                _prompting = True
            user_input = input("You: ").strip()
            # stop prompting state as soon as we have the input string
            with _prompt_lock:
                _prompting = False

            if not user_input:
                # clear the prompt line (best effort)
                sys.stdout.write("\033[F\033[2K")
                sys.stdout.flush()
                continue

            if user_input.lower() in {"quit", "exit"}:
                # clear prompt line before exiting loop
                sys.stdout.write("\033[F\033[2K")
                sys.stdout.flush()
                break

            # clear the echoed input line to avoid duplication
            sys.stdout.write("\033[F\033[2K")  # move up one line, clear it
            sys.stdout.flush()

            # now render user's message and send
            renderer.print_user(user_input)
            agent.send_message(user_input)
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        agent.stop()
        sys.stdout.write("\nChat ended!\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()


