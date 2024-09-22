import re
from subprocess import run

from mkdocs_macros.plugin import MacrosPlugin

# fmt: off
# https://stackoverflow.com/questions/14693701
ANSI_ESCAPE_8BIT = re.compile(
    r"""
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
    """,
    re.VERBOSE,
)
# fmt: on


def define_env(env: MacrosPlugin) -> None:
    @env.macro
    def get_help_message(*args: str):
        command = ["uv", "run", "python", "-m", *args, "--help"]
        message = run(command, capture_output=True).stdout.decode("utf-8")
        message = ANSI_ESCAPE_8BIT.sub("", message)
        return f"```bash\n➜  {' '.join(command)}\n{message}\n```"
