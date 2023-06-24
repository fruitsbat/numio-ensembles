"""
helpers for pretty printing
"""


from typing import List, Tuple
import rich
from rich.panel import Panel
from rich.columns import Columns


def print_boxes(
    title: str,
    list_items: List[Tuple[str, str]],
) -> None:
    """
    pretty prints a list of strings as boxes
    """

    def box_tuple(to_be_boxed: Tuple[str, str]) -> Panel:
        """
        puts a tuple of strings into a panel
        """
        return Panel.fit(
            to_be_boxed[0],
            title=to_be_boxed[1],
            border_style="yellow",
            style="cyan",
        )

    rich.print(
        Columns(
            map(box_tuple, list_items),
            title=title,
        ),
    )
