from machineclient import MachineClient

import argparse


def parse_line(machine, position, line):
    line_number, *instructions = line.split()
    linear_move = False
    moves = []
    for ins in instructions:
        code = ins[0]
        value = ins[1:]
        if code == 'F':
            machine.set_feed_rate(float(value))
        elif code == 'G':
            value = int(value)
            if value == 0:
                linear_move = False
            elif value == 1:
                linear_move = True
            elif value == 17:
                # XY plane selection
                pass
            elif value == 21:
                # Programming in millimeters
                pass
            elif value == 28:
                machine.home()
            elif value == 40:
                # Tool radius compensation off
                pass
            elif value == 49:
                # Tool length offset compensation cancel
                pass
            elif value == 54:
                # Work coordinate systems (WCSs)
                pass
            elif value == 80:
                # Cancel canned cycle
                pass
            elif value == 90:
                # Absolute programming
                pass
            elif value == 91:
                # Incremental programming
                pass
            elif value == 94:
                # Feedrate per minute
                pass
            else:
                print(f'Unknown instruction {ins}')
        elif code == 'M':
            value = int(value)
            if value == 3:
                # Spindle on (clockwise rotation)
                pass
            elif value == 5:
                machine.set_spindle_speed(0)
            elif value == 6:
                # Automatic tool change (ATC)
                pass
            elif value == 9:
                machine.coolant_off()
            elif value == 30:
                # End of program, with return to program top
                pass
            else:
                print(f'Unknown instruction {ins}')
        elif code == 'S':
            machine.set_spindle_speed(int(value))
        elif code == 'T':
            machine.change_tool(value)
        elif code in 'XYZ':
            value = float(value)
            position['XYZ'.index(code)] = value
            moves.append([code, value])
        else:
            print(f'Unknown instruction {ins}')
            
    if linear_move:
        machine.move(*position)
    else:
        for dir, value in moves:
            if dir == 'X':
                machine.move_x(value)
            elif dir == 'Y':
                machine.move_y(value)
            elif dir == 'Z':
                machine.move_z(value)


def read_gcode(path):
    machine = MachineClient()
    position = [0.0, 0.0, 0.0]
    
    with open(path) as file:
        for line in file.readlines():
            line = line.strip()
            
            if line == '%':
                continue
                
            if line[0] == '(' and line[-1] == ')':
                continue
                
            parse_line(machine, position, line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='G-Code file path')
    args = parser.parse_args()
    read_gcode(args.path)


if __name__ == '__main__':
    main()
