from position import Position

def convert_lsystem_to_hpgl(path, step_size, start_x, start_y):
    body = []
    heading = -90
    pen_down = False

    # initialize plotter position
    curr_pos = Position(start_x, start_y, heading)
    body.append('PA{},{};'.format(curr_pos.x, curr_pos.y).encode())

    for c in path:
        if c.isupper():
            if not pen_down:
                body.append(b'PD;')
                pen_down = True
            curr_pos = curr_pos.move(step_size)
            body.append('PA{},{};'.format(curr_pos.x, curr_pos.y).encode())
        elif c.islower():
            if pen_down:
                body.append(b'PU;')
                pen_down = False
            curr_pos = curr_pos.move(step_size)
            body.append('PA{},{};'.format(curr_pos.x, curr_pos.y).encode())
        elif c == "+":
            curr_pos.heading -= heading
        elif c == "-":
            curr_pos.heading += heading
        else:
            continue

    return body
