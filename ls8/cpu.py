"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""
        program = []

        if len(sys.argv) != 2:
            print("Usage: file.py filename", file=sys.stderr)
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.find("#")
                    if comment_split >= 0:
                        line = line[:comment_split]

                    if len(line) > 1:
                        line = line.strip()
                        program.append(line)

                    # if line == "":
                    #     continue # Ignore blank lines

                    # # x = int(num, 2)
                    # print(f"{x:08b}: {x:d}")

                    # program.append(line)

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000, 
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram[address] = int(instruction, 2)
            address += 1
 
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, value, index):
        self.ram[index] = value

    def HLT(self, address):
        pass

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)

        loop = True

        while loop:

            ir = self.ram[self.pc]
            print("IR", ir)
            
            if ir == 0b10000010:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == 0b01000111:
                print(self.reg[0])
                self.pc += 2

            elif ir == 0b00000001:
                sys.exit()
                loop = False

            else:
                self.pc += 1



