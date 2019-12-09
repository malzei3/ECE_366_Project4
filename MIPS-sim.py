import time

instructions = []
labelindex = []
labelname = []
labeladdr = []
regname = []

# This class keeps track of all the statistics needed for
# simulation results.
# Feel free to add any stats
class Statistic:
    def __init__(self, debugMode):
        self.I = ""  # Current instr being executed
        self.name = ""  # name of the instruction
        self.p1 = 0
        self.p2 = 0
        self.p3 = 0
        self.cycle = 0  # Total cycles in simulation
        self.DIC = 0  # Total Dynamic Instr Count
        self.threeCycles = 0  # How many instr that took 3 cycles to execute
        self.fourCycles = 0  # 4 cycles
        self.fiveCycles = 0  # 5 cycles
        #MC
        self.MemtoReg = 0
        self.MemWrite = 0
        self.Branch = 0
        self.ALUSrc = 0
        self.RegDst = 0
        self.RegWrite = 0
        self.debugMode = debugMode

        #AP
        self.DataHazard = 0     # Helpful statistics needed for slow-pipe, fast-pipe implementation
        self.ControlHazard = 0  #
        self.NOPcount = 0       #
        self.flushCount = 0     #
        self.stallCount = 0     #
        self.delay = 0

    def log(self, I, name, p1, p2, p3, cycle, pc):
        self.I = I
        self.name = name
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.cycle = self.cycle + cycle
        self.pc = pc
        self.DIC += 1
        self.threeCycles += 1 if (cycle == 3) else 0
        self.fourCycles += 1 if (cycle == 4) else 0
        self.fiveCycles += 1 if (cycle == 5) else 0

        # Student TO-DO:
        # update data + control hazards, NOP, flush, stall statistics

    # Since the self.cycle has the updated cycles, need to substract x cycles for correct printing , i.e (self.cycle - x)
    def prints(self):
        #imm = int(self.I[16:32], 2) if self.I[16] == '0' else -(65535 - int(self.I[16:32], 2) + 1)
        if (self.debugMode):
            print("\n")
            print("Instruction: " + self.I)
            if self.name == "ori":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " ori $" + str(
                    self.p1) + ", $" + str(self.p2) + ", "+ str(
                    self.p3) + "   Taking 4 cycles")

            elif self.name == "addi":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " addi $" + str(
                    self.p1) + ", $" + str(self.p2) + ", " + str(
                    self.p3) + "   Taking 4 cycles")
            elif self.name == "addu":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " addu $" + str(
                    self.p1) + ", $" + str(self.p2) + ", $" + str(
                    self.p3) + "   Taking 4 cycles")
            elif self.name == "beq":
                print("Cycle: " + str(self.cycle - 3) + "| PC:" + str(self.pc) + " beq $" + str(
                    self.p1) + ", " + str(self.p2) + ", " + str(
                    self.p3) + "   Taking 4 cycles")
            elif self.name == "bne":
                print("Cycle: " + str(self.cycle - 3) + "| PC:" + str(self.pc) + " bne $" + str(
                    self.p1) + ", " + str(self.p2) + ", " + str(
                    self.p3) + "   Taking 4 cycles")
            elif self.name == "sll":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " sll $" + str(
                    self.p1) + ", $" + str(self.p2) + ", " + str(
                    self.p3) + "   Taking 4 cycles")
            elif self.name == "sub":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " sub $" + str(
                    self.p1) + ", $" + str(self.p2) + ", $" + str(
                    self.p3) + "   Taking 4 cycles")
            elif self.name == "xor":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " xor $" + str(
                    self.p1) + ", $" + str(self.p2) + ", $" + str(
                    self.p3) + "   Taking 4 cycles")
            elif self.name == "slt":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " slt $" + str(
                    self.p1) + ", $" + str(self.p2) + ", $" + str(
                    self.p3) + "   Taking 4 cycles")
            #sb $t, offset($s)
            elif self.name == "sb":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " sb $" + str(
                    self.p1) + ", " + str(self.p2) + "($" + str(
                    self.p3) + ")   Taking 4 cycles")
            #lw $t, offset($s)
            elif self.name == "lb":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " lb $" + str(
                    self.p1) + ", " + str(self.p2) + "($" + str(
                    self.p3) + ")   Taking 4 cycles")

            elif self.name == "sw":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " sw $" + str(
                    self.p1) + ", " + str(self.p2) + "($" + str(
                    self.p3) + ")   Taking 4 cycles")
            elif self.name == "lw":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " lw $" + str(
                    self.p1) + ", " + str(self.p2) + "($" + str(
                    self.p3) + ")   Taking 4 cycles")

            else:
                print("")

    def exitSim(self):
        print("***Finished simulation***")
        print("Total # of cycles: " + str(self.cycle))
        print("Dynamic instructions count: " + str(self.DIC) + ". Break down:")
        print("                    " + str(self.threeCycles) + " instructions take 3 cycles")
        print("                    " + str(self.fourCycles) + " instructions take 4 cycles")
        print("                    " + str(self.fiveCycles) + " instructions take 5 cycles")

def saveJumpLabel(asm):
    lineCount = 0
    global labelindex
    global labelname
    global labeladdr
    for line in asm:
        line = line.replace(" ","")
        if line.count(":"):
            labelname.append(line[0:line.index(":")]) # append the label name
            labelindex.append(lineCount) # append the label's index\
            labeladdr.append(lineCount*4)
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')


def readIn(s):
    text = ""
    global instructions
    inst = []
    with open(s, "r") as f:
        for line in f:
            if line != "\n" and line[0] != '#':
                inst.append(line)
                line.replace("$", "")
                line.replace(" ", "")
                line.replace("zero", "0")
                text += line

    instructions = inst
    return text


def splitText(text):
    return text.split("\n")


def simulate(lisIns, debugMode):
    start_time = time.time()
    print("***Starting simulation***")
    Register = [0 for i in range(24)]  # initialize registers from $0-$24, but
    # only utilize $8 - $23 as stated in guideline
    Memory = [0 for i in range(60000)]
    stats = Statistic(debugMode)  # init. the statistic class, keeps track of debugmode as well


    PC = 0
    lineCount = 0
    saveJumpLabel(lisIns)

    finished = False
    while lineCount < len(lisIns):
        line = lisIns[lineCount]

        if (":" in line):
            lineCount += 1

        elif line[0:3] == "ori":
            linete = line.replace("ori", "").replace(" ", "").replace("$", "").split(",")
            PC += 4
            Register[int(linete[0])] = Register[int(linete[1])] | int(linete[2])
            stats.log(line, "ori", str(linete[0]), str(linete[1]), str(linete[2]), 4, PC)  # ori instr, 4 cycles
            lineCount += 1

        elif line[0:4] == "addu":
            linete = line.replace("addu", "").replace(" ", "").replace("$", "").replace("0x", "").split(",")
            PC += 4
            Register[int(linete[0])] = abs(Register[int(linete[1])]) + abs(Register[int(linete[2])])
            stats.log(line, "addu", str(linete[0]), str(linete[1]), str(linete[2]), 4, PC)  # addi instr, 4 cycles
            lineCount += 1

        elif line[0:4] == "addi":
            linete = line.replace("addi", "").replace(" ", "").replace("$", "").replace("0x", "").split(",")
            PC += 4
            Register[int(linete[0])] = Register[int(linete[1])] + int(linete[2])
            stats.log(line, "addi", str(linete[0]), str(linete[1]), str(linete[2]), 4, PC)  # addi instr, 4 cycles
            lineCount += 1

        elif line[0:3] == "sub":
            linete = line.replace("sub", "").replace(" ", "").replace("$", "").split(",")
            PC += 4
            Register[int(linete[0])] = Register[int(linete[1])] - Register[int(linete[2])]
            stats.log(line, "sub", str(linete[0]), str(linete[1]), str(linete[2]), 4, PC)  # sub instr, 4 cycles
            lineCount += 1

        elif line[0:3] == "xor":
            linete = line.replace("xor", "").replace(" ", "").replace("$", "").split(",")
            PC += 4
            Register[int(linete[0])] = int(Register[int(linete[1])]) ^ int(Register[int(linete[2])])
            stats.log(line, "xor", str(linete[0]), str(linete[1]), str(linete[2]), 4, PC)  # xor instr, 4 cycles
            lineCount += 1

        elif line[0:3] == "sll":
            linete = line.replace("sll", "").replace(" ", "").replace("$", "").split(",")
            PC += 4
            Register[int(linete[0])] = Register[int(linete[1])] << int(linete[2])
            stats.log(line, "sll", str(linete[0]), str(linete[1]), str(linete[2]), 4, PC)  # sll instr, 4 cycles
            lineCount += 1

        elif line[0:3] == "slt":
            linete = line.replace("slt", "").replace(" ", "").replace("$", "").split(",")
            PC += 4
            if Register[int(linete[1])] < Register[int(linete[2])]:
                Register[int(linete[0])] = 1
            else:
                Register[int(linete[0])] = 0

            stats.log(line, "slt", str(linete[0]), str(linete[1]), str(linete[2]), 4, PC)  # sll instr, 4 cycles
            lineCount += 1

        elif line[0:2] == "sw":
            linete = line.replace("sw", "").replace("$", "").replace(" ", "").replace("(", ",").replace(")", "").replace("0x", "")
            PC += 4
            linete = linete.split(",")
            if (int(Register[int(linete[2])]) + int(linete[1]) % 4) == 0:
                Memory[Register[int(linete[2])] + int(linete[1])] = Register[int(linete[0])]
                stats.log(line, "sw", str(linete[0]), str(linete[1]), str(linete[2]), 4, PC)  # sb instr, 4 cycles
                lineCount += 1
            else:
                lineCount += 1
                print("Memory address incorrect, return.\n")

        elif line[0:2] == "lw":
            linete = line.replace("sw", "").replace("$", "").replace(" ", "").replace("(", ",").replace(")","").replace("0x", "")
            PC += 4
            linete = linete.split(",")
            if (int(linete[2]) + int(linete[1]) % 4) == 0:
                Register[int(linete[0])] = Memory[Register[int(linete[2])] + int(linete[1])]
                stats.log(line, "lw", str(linete[0]), str(linete[1]), str(linete[2]), 4, PC)  # sb instr, 4 cycles
                lineCount += 1
                stats.NOPcount += 1
            else:
                lineCount += 1
                print("Memory address incorrect, return.\n")

        elif line[0:2] == "sb":
            linete = line.replace("sb", "").replace("$", "").replace(" ", "").replace("(", ",").replace(")","").replace("0x", "")
            PC += 4
            linete = linete.split(",")
            Memory[Register[int(linete[2])] + int(linete[1])] = Register[int(linete[0])]
            stats.log(line, "sb", str(linete[0]), str(linete[1]), str(linete[2]), 4, PC)  # sb instr, 4 cycles
            lineCount += 1

        elif line[0:2] == "lb":
            linete = line.replace("sw", "").replace("$", "").replace(" ", "").replace("(", ",").replace(")","").replace("0x", "")
            PC += 4
            linete = linete.split(",")
            Register[int(linete[0])] = Memory[Register[int(linete[2])] + int(linete[1])]
            stats.log(line, "lb", str(linete[0]), str(linete[1]), str(linete[2]), 4, PC)  # sb instr, 4 cycles
            lineCount += 1

        elif line[0:3] == "bne":
            linete = line.replace("bne", "").replace("$", "").split(",")
            if Register[int(linete[0])] != Register[int(linete[1])]:
                if linete[2].isdigit():
                    PC = linete[2] * 4
                    lineCount = lineCount[2]
                    stats.log(line, "bne", str(linete[0]), str(linete[1]), str(linete[2]), 3, PC)  # ADD instr, 4 cycles
                    lineCount += 1
                    stats.NOPcount += 3
                else:
                    for i in range(len(labelname)):
                        if labelname[i] == lisIns[2]:
                            PC = labeladdr[i]
                            lineCount = labelindex[i]
                            stats.log(line, "bne", str(linete[0]), str(linete[1]), str(linete[2]), 3, PC)
                            stats.NOPcount += 3
                continue
            print("No change in registers. \n")

        elif line[0:3] == "beq":
            linete = line.replace("beq", "").replace("$", "").split(",")
            if Register[int(linete[0])] == Register[int(linete[1])]:
                if linete[2].isdigit():
                    PC = linete[2] * 4
                    lineCount = lineCount[2] + 1
                    stats.log(line, "beq", str(linete[0]), str(linete[1]), str(linete[2]), 3, PC)  # ADD instr, 4 cycles
                else:
                    for i in range(len(labelname)):
                        if labelname[i] == lisIns[2]:
                            PC = labeladdr[i]
                            lineCount = labelindex[i]
                            stats.log(line, "beq", str(linete[0]), str(linete[1]), str(linete[2]), 3, PC)
                continue
            print("No change in registers. \n")

        elif line == "":
            finished = True

        else:
            print("Instruction " + str(lisIns[lineCount]) + " not supported. Exiting")
            lineCount += 1
            exit()

        if not finished:
            stats.prints()

    if finished:
        elapsed_time = time.time() - start_time
        stats.exitSim()
        print("Registers: " + str(Register))
        print("Total elapsed time: " + str(elapsed_time) + " seconds")


def main():
    print("Welcome to ECE366 Advanced MIPS Simulator.  Please choose the mode of running: ")
    debugMode = True if int(input(" 1 = Debug Mode         2 = Normal Execution \n")) == 1 else False
    if (debugMode):
        print("Debug Mode\n")
    else:
        print("Normal Execution \n")

    isFile = False
    while (not isFile):
        fileN = input("Enter file name: ")
        try:
            f = open(fileN)
            f.close()
            isFile = True
        except FileNotFoundError:
            print("File does not exist.\n")

    text = readIn(fileN)
    t = splitText(text)

    simulate(t, debugMode)


main()
