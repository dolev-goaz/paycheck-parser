import fitz
from lines import split_by_lines, join_underscores_star

def read_rects(page, *rects: list[float]):
    lines = []
    for rect_coords in rects:
        rect = fitz.Rect(*rect_coords)
        words = page.get_text("words", clip=rect)
        
        temp_lines = split_by_lines(words)
        lines.extend([join_underscores_star(line) for line in temp_lines])
    
    return lines
