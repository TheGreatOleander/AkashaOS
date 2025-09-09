
from typing import List
def spiral(size: int = 7) -> str:
    if size < 3: size = 3
    grid: List[List[str]] = [["·" for _ in range(size)] for _ in range(size)]
    mid = size // 2
    grid[mid][mid] = "@"
    for i in range(size):
        grid[i][i] = "*"
        grid[i][size - i - 1] = "*"
    return "\n".join(" ".join(row) for row in grid)
