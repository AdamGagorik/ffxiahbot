from subprocess import run

from mkdocs_macros.plugin import MacrosPlugin


def define_env(env: MacrosPlugin) -> None:
    @env.macro
    def get_help_message(*args: str):
        command = ["uv", "run", "python", "-m", *args, "--help"]
        message = run(command, capture_output=True).stdout.decode("utf-8")
        return f"```bash\n➜  {' '.join(command)}\n{message}\n```"
