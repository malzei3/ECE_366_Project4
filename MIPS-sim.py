import time
instructions = []

# This class keeps track of all the statistics needed for
# simulation results.
# Feel free to add any stats
class Statistic:
    def __init__(self, debugMode):
        self.I = ""  # Current instr being executed
        self.name = ""  # name of the instruction
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

    def log(self, I, name, cycle, pc):
        self.I = I
        self.name = name
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
        if (self.debugMode):
            print("\n")
            print("Instruction: " + self.I)
            if (self.name == "add"):
                print("Cycle: " + str(self.cycle - 4) + "|PC: " + str(self.pc * 4) + " add $" + str(
                    int(self.I[16:21], 2)) + ",$" + str(int(self.I[6:11], 2)) + ",$" + str(
                    int(self.I[11:16], 2)) + "   Taking 4 cycles")
            elif (self.name == "addi"):
                print("Cycle: " + str(self.cycle - 4) + "|PC: " + str(self.pc * 4) + " addi $" + str(
                    int(self.I[16:21], 2)) + ",$" + str(int(self.I[6:11], 2)) + "," + str(imm) + "   Taking 4 cycles")
            elif (self.name == "beq"):
                print("Cycle: " + str(self.cycle - 3) + "|PC: " + str(self.pc * 4) + " beq $" + str(
                    int(self.I[6:11], 2)) + ",$" + str(int(self.I[11:16], 2)) + "," + str(imm) + "   Taking 3 cycles")
            elif (self.name == "slt"):
                print("Cycle: " + str(self.cycle - 4) + "|PC: " + str(self.pc * 4) + " slt $" + str(
                    int(self.I[16:21], 2)) + ",$" + str(int(self.I[6:11], 2)) + ",$" + str(
                    int(self.I[11:16], 2)) + "   Taking 4 cycles")
            elif (self.name == "sw"):
                print("Cycle: " + str(self.cycle - 4) + "|PC :" + str(self.pc * 4) + " sw $" + str(
                    int(self.I[6:11], 2)) + "," + str(int(self.I[16:32], 2) - 8192) + "($" + str(
                    int(self.I[6:11], 2)) + ")" + "   Taking 4 cycles")
            else:
                print("")

    def exitSim(self):
        print("***Finished simulation***")
        print("Total # of cycles: " + str(self.cycle))
        print("Dynamic instructions count: " + str(self.DIC) + ". Break down:")
        print("                    " + str(self.threeCycles) + " instructions take 3 cycles")
        print("                    " + str(self.fourCycles) + " instructions take 4 cycles")
        print("                    " + str(self.fiveCycles) + " instructions take 5 cycles")


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
    print(text)
    return text.split("\n")


def simulate(lisIns, debugMode):
    start_time = time.time()
    print("***Starting simulation***")
    Register = [0 for i in range(24)]  # initialize registers from $0-$24, but
    # only utilize $8 - $23 as stated in guideline
    Memory = [0 for i in range(1024)]
    stats = Statistic(debugMode)  # init. the statistic class, keeps track of debugmode as well

    PC = 0
    lineCount = 0

    finished = False
    while lineCount < len(lisIns):
        line = lisIns[lineCount]

        if (line[0:32] == '00010000000000001111111111111111'):
            finished = True
            print("PC = " + str(PC * 4) + "  Instruction: " + instructions[PC] + " : Deadloop. Exiting simulation")

        elif (line[0:3] == 'add'):
            line = line.replace("add", "").replace("$", "").split(",")
            PC += 4
            Register[int(line[0])] = Register[int(line[1])] + Register[int(line[2])]
            stats.log(line, "add", 4, PC)  # ADD instr, 4 cycles
            lineCount += 1

        else:
            print("Instruction " + str(lisIns[lineCount]) + " not supported. Exiting")
            exit()

        if (not (finished)):
            #print("Test")
            #stats.prints()
            print(PC, lisIns[lineCount])

    if (finished):
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
