
def load_program():
    instructions = []
    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                opcode, operand = line.split(' ')
                operand = int(operand)
                instructions.append((opcode, operand))
    return instructions
                

class Machine:
    def __init__(self, code):
        self._acc = 0
        self._pc = 0
        self._code = code
    
    def run(self):
        visited = set()
        while not self.is_finished():
            if self._pc in visited:
                raise ValueError('Looping program')
            else:
                visited.add(self._pc)
                self.step()
        return self._acc

    def step(self):
        instruction, operand = self.fetch()
        self.dispatch(instruction, operand)

    def fetch(self):
        return self._code[self._pc]
    
    def dispatch(self, opcode, operand):
        if opcode == 'acc':
            self._acc += operand
            self._pc += 1
        elif opcode == 'jmp':
            self._pc += operand
        elif opcode == 'nop':
            self._pc += 1
        else:
            raise NotImplementedError(opcode)

    def is_finished(self):
        return self._pc == len(self._code)


def part1():
    code = load_program()
    m = Machine(code)
    try:
        m.run()
    except ValueError:
        print('Accumulator before looping:', m._acc)
    

def part2():
    original_code = load_program()

    for i, instruction in enumerate(original_code):
        opcode, operand = instruction

        # Do some patching:
        if opcode == 'jmp':
            opcode = 'nop'
        elif opcode == 'nop':
            opcode = 'jmp'
        else:
            continue

        modified_code = list(original_code)  # Create a copy to modify
        modified_code[i] = (opcode, operand)

        # print('try modify index', i)
        m = Machine(modified_code)
        try:
            result = m.run()
            print('Valid result:', result)
            break
        except ValueError as ex:
            # print('Too bad:', ex)
            pass


part1()
part2()
