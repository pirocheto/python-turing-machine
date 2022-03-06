from typing import List

from colorama import Back, Fore
from tabulate import tabulate


class Pile(list):
    def append(self, start: int, end: int) -> None:
        return super().append(slice(start, end))

    def pop(self, __index):
        return super().pop(__index).stop - 1


class Machine:
    def __init__(self, tape_size: int = 71):
        self._tape = [0 for _ in range(tape_size)]
        self._head = 0
        self._pile = Pile()

    def init(self, args: List[int], origin: int = 35):
        """Init turing machine tape with numbers given as arguments"""

        self._origin = origin
        self._head = origin
        for n in args:
            for _ in range(n + 1):
                self._write(1)
                self._move(">")
            self._move(">")
        self._head = origin

    def _move(self, direction: str):
        """Move the reading head"""
        if direction == ">":
            self._head += 1
        if direction == "<":
            self._head -= 1

    def _write(self, element):
        """Write a element on the tape (0 or 1) at current location of the reading head"""
        self._tape[self._head] = int(element)

    def __str__(self):
        """Print current machine state (Del Vigna's machine like)"""

        tape_str = [
            f"{Fore.LIGHTYELLOW_EX}{str(ele)}{Fore.RESET}" if ele == 1 else str(ele)
            for ele in self._tape
        ]
        tape_str[self._head] = Back.LIGHTBLACK_EX + tape_str[self._head] + Back.RESET

        tape_str.insert(0, " ")
        tape_str.append(" ")

        # border_top = "-" * len(tape_str)
        # border_bottom = "-" * len(tape_str)

        head_str = [" " for _ in self._tape]
        head_str[self._head] = Fore.LIGHTBLACK_EX + "↓" + Fore.RESET
        head_str.insert(0, " ")
        head_str.append(" ")

        unit_str = ["┴" if i % 5 == 0 else "─" for i in range(len(self._tape))]
        unit_str[self._origin] = "┼"
        unit_str.insert(0, Fore.LIGHTBLACK_EX + " ")
        unit_str.append(" " + Fore.RESET)

        origin_str = [" " for _ in self._tape]
        origin_str[self._origin] = Fore.LIGHTBLACK_EX + "0" + Fore.RESET
        origin_str.insert(0, " ")
        origin_str.append(" ")

        return f'{"".join(head_str)}\n{"".join(tape_str)}\n{"".join(unit_str)}\n{"".join(origin_str)}\n'

    def _endif(self, condition: int) -> bool:
        """Checks if exit condition is true"""
        return self._tape[self._head] == int(condition)

    def _get_endloop(self, prog, start: int):
        """Get end index of a loop from its start index"""
        end = start
        pile_size = len(self._pile) + 1
        while len(prog) != end and (
            prog[end].startswith("\t" * pile_size)
            or prog[end].startswith(" " * 4 * pile_size)
        ):
            end += 1
        return end

    def _loop(self, prog, i):
        # ==== Foncionnement d'une boucle =============================

        i += 1
        # 1.
        # On cherche l'adresse de la première instruction et l'adresse
        # de la dernière instruction de la boucle que l'on ajoute à la
        # pile.
        self._pile.append(i, self._get_endloop(prog, i))

        # 2.
        # On exécute la même fonction avec les indices stockés dans le
        # dernier élément de la pile. Puisque c'est une boucle :
        # on indique boucle=True pour lancer la récursivité.
        self._run_script(
            prog,
            start=self._pile[-1].start,
            end=self._pile[-1].stop,
            inloop=True,
        )
        # 3.
        # La boucle est terminée donc on dépile. Le dernier élément de
        # la pile est donc retirée. On renvoie l'indice de la dernière
        # ligne de l'instruction de la dernière instruction de la
        # dernière boucle.
        i = self._pile.pop(-1)

        # 4.
        # On remet à jour la limite des instructions à éxécuter.
        # On reprend donc l'indice de la dernière instruction de la
        # boucle parent ou la dernière instruction du programme si
        # la pile est vide.
        # if self._pile != []:
        #     end = self._pile[-1].stop
        # else:
        #     end = len(prog)

        return i
        # =============================================================

    def _run_script(self, prog, start, end, inloop=False):
        """Run a instruction list from start index to end index with recusivity option"""

        i = start

        while i != end:

            line = prog[i]

            if "<" in line or ">" in line:
                self._move(line[-1])
            elif "write" in line:
                self._write(int(line[-2]))
            elif "print" in line:
                print(self)
            elif "loop:" in line:
                i = self._loop(prog, i)

            elif "endif" in line:
                # Si on rencontre un out(0|1) valide alors on arrête la
                # récursivité et on sort de la boucle. Permet également de
                # quitter le programme si nous ne sommes pas dans une boucle.
                if self._endif(int(line[-2])):
                    inloop = False
                    break
                # =============================================================

            # On augmente notre indice pour chaque instruction traitée.
            i += 1

        # Si nous sommes dans une boucle alors elle est éxécutée tant que nous
        # ne rencontrons pas de out(0|1) valide.
        if inloop:
            self._run_script(prog, start=start, end=end, inloop=True)

    def run(self, prog_path):
        """Run a program from path"""
        with open(prog_path, "r", encoding="utf8") as sc:
            prog = sc.read().split("\n")
        self._run_script(prog, start=0, end=len(prog))
