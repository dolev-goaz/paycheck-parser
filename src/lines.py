
def split_by_lines(words):
    # Group words into lines based on vertical (y0) proximity
    words = sorted(words, key=lambda w: (round(w[1], 1), -round(w[2], 1)))  # Sort by y0 and x0
    lines = []
    current_line = []
    previous_y = None
    line_height_threshold = 5  # Adjust the threshold for vertical proximity between words on the same line

    for word in words:
        y, text = word[1], word[4]
        
        # If it's the first word or part of the same line (close y0 value)
        if previous_y is None or abs(previous_y - y) < line_height_threshold:
            current_line.append(text)
        else:
            # New line detected; save the current line and start a new one
            lines.append(current_line)
            current_line = [text]

        # Update previous_y to the bottom of the current word (y1)
        previous_y = y
    
    lines.append(current_line)
    
    return lines

def join_underscores_star(line: list[str]):
    result = []
    i = 0
    while i < len(line):
        if '_' in line[i]:
            # If the current string is "_", join the previous and next string with "_"
            if line[i].startswith('_'):
                if i > 0 and i + 1 < len(line):
                    result[-1] += f"{line[i]}{line[i + 1]}"  # Join with underscore
                    i += 1  # Skip the next element since it's already joined
            elif i > 0:
                underscore_index = line[i].index('_')
                result[-1] += line[i][underscore_index:] + line[i][:underscore_index] # reverse the underscore
        elif line[i] in ["*", "-", '"']:
            current = "";
            if i > 0:
                current = result.pop();
            current += line[i]
            if i + 1 < len(line):
                current += line[i+1]
                i += 1
            result.append(current)
        elif line[i] in ["'"]:
            if i > 0:
                result[-1] += line[i]
            else:
                result.append(line[i])
        else:
            # If it's not an underscore or asterisk, just add the string to the result
            result.append(line[i])
        i += 1
    return result
