from typing import List
import typer
from tmachine import Machine

app = typer.Typer()


@app.command()
def main(
    program_path: str,
    number: List[int] = typer.Option(
        [],
        "--number",
        "-n",
        help="Numbers to initialize on the machine tape before program execution",
    ),
    tape_size: int = typer.Option(71, "--tape-size", "-s", help="Tape size"),
    origin: int = typer.Option(35, "--origin", "-o", help="Tape origin index"),
):
    """Run a program with turing machine"""
    m = Machine(tape_size)
    m.init(number, origin=origin)
    m.run(program_path)
