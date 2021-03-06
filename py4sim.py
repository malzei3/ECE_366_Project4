import os
import math
import copy

# Global Var
debugMode = False
instructionsList = []
asmCopy = []
labelindex = []
labelname = []
Placement_Policy = "DM"
total_blk = 8   # 8 blocks in cache
word_offset = 0
set_offset = 0
mem_space = 1024
blocks = {}
menu = 0
programMode = "AP"

# This class keeps track of all the statistics needed for
# simulation results.
# Feel free to add any stats
class Statistic:
    def __init__(self, debugMode, programMode):
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
        self.programMode = programMode

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
                print("Cycle: " + str(self.cycle - 5) + "| PC:" + str(self.pc) + " ori $" + str(
                    self.p1) + ", $" + str(self.p2) + ", "+ str(
                    self.p3) + "   Taking 5 cycles\n\n")

                #Print updates cycle by cycles
                if (self.programMode == "MC"):
                    print("Cycle: 1 " + "| MemtoReg: x"  + "| MemWrite: x"  + "| Branch: x"
                          + "| ALUSrc: x" + "| RegDst: x" + "| RegWrite: x")
                    print("Cycle: 2 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")
                    print("Cycle: 3 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")
                    print("Cycle: 4 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")
                    print("Cycle: 5 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")

                #TODO
                if (self.programMode == "AP"):
                    print("Cycle: 1 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 2 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 3 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")

            elif self.name == "addi":
                print("Cycle: " + str(self.cycle - 5) + "| PC:" + str(self.pc) + " addi $" + str(
                    self.p1) + ", $" + str(self.p2) + ", " + str(
                    self.p3) + "   Taking 5 cycles")

                if (self.programMode == "MC"):
                    print("Cycle: 1 " + "| MemtoReg: x"  + "| MemWrite: x"  + "| Branch: x"
                          + "| ALUSrc: x" + "| RegDst: x" + "| RegWrite: x")
                    print("Cycle: 2 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")
                    print("Cycle: 3 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")
                    print("Cycle: 4 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")
                    print("Cycle: 5 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")

                if (self.programMode == "AP"):
                    print("Cycle: 1 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 2 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 3 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                
            elif self.name == "addu":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " addu $" + str(
                    self.p1) + ", $" + str(self.p2) + ", $" + str(
                    self.p3) + "   Taking 4 cycles")

                if (self.programMode == "MC"):
                    print("Cycle: 1 " + "| MemtoReg: x"  + "| MemWrite: x"  + "| Branch: x"
                          + "| ALUSrc: x" + "| RegDst: x" + "| RegWrite: x")
                    print("Cycle: 2 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")
                    print("Cycle: 3 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")
                    print("Cycle: 4 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")

                if (self.programMode == "AP"):
                    print("Cycle: 1 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 2 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 3 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")

            elif self.name == "beq":
                print("Cycle: " + str(self.cycle - 3) + "| PC:" + str(self.pc) + " beq $" + str(
                    self.p1) + ", " + str(self.p2) + ", " + str(
                    self.p3) + "   Taking 3 cycles")

                if (self.programMode == "MC"):
                    print("Cycle: 1 " + "| MemtoReg: x"  + "| MemWrite: x"  + "| Branch: x"
                          + "| ALUSrc: x" + "| RegDst: x" + "| RegWrite: x")
                    print("Cycle: 2 " + "| MemtoReg: x"  + "| MemWrite: 0"  + "| Branch: 1"
                          + "| ALUSrc: 0" + "| RegDst: x" + "| RegWrite: 0")
                    print("Cycle: 3 " + "| MemtoReg: x"  + "| MemWrite: 0"  + "| Branch: 1"
                          + "| ALUSrc: 0" + "| RegDst: x" + "| RegWrite: 0")


                if (self.programMode == "AP"):
                    print("Cycle: 1 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 2 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 3 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")


            elif self.name == "bne":
                print("Cycle: " + str(self.cycle - 3) + "| PC:" + str(self.pc) + " bne $" + str(
                    self.p1) + ", " + str(self.p2) + ", " + str(
                    self.p3) + "   Taking 3 cycles")

                if (self.programMode == "MC"):
                    print("Cycle: 1 " + "| MemtoReg: x"  + "| MemWrite: x"  + "| Branch: x"
                          + "| ALUSrc: x" + "| RegDst: x" + "| RegWrite: x")
                    print("Cycle: 2 " + "| MemtoReg: x"  + "| MemWrite: 0"  + "| Branch: 1"
                          + "| ALUSrc: 0" + "| RegDst: x" + "| RegWrite: 0")
                    print("Cycle: 3 " + "| MemtoReg: x"  + "| MemWrite: 0"  + "| Branch: 1"
                          + "| ALUSrc: 0" + "| RegDst: x" + "| RegWrite: 0")

                if (self.programMode == "AP"):
                    print("Cycle: 1 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 2 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 3 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")


            elif self.name == "sll":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " sll $" + str(
                    self.p1) + ", $" + str(self.p2) + ", " + str(
                    self.p3) + "   Taking 4 cycles")

                if (self.programMode == "MC"):
                    print("Cycle: 1 " + "| MemtoReg: x"  + "| MemWrite: x"  + "| Branch: x"
                          + "| ALUSrc: x" + "| RegDst: x" + "| RegWrite: x")
                    print("Cycle: 2 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")
                    print("Cycle: 3 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")
                    print("Cycle: 4 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")

                if (self.programMode == "AP"):
                    print("Cycle: 1 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 2 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 3 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")

            elif self.name == "sub":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " sub $" + str(
                    self.p1) + ", $" + str(self.p2) + ", $" + str(
                    self.p3) + "   Taking 4 cycles")

                if (self.programMode == "MC"):
                    print("Cycle: 1 " + "| MemtoReg: x"  + "| MemWrite: x"  + "| Branch: x"
                          + "| ALUSrc: x" + "| RegDst: x" + "| RegWrite: x")
                    print("Cycle: 2 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")
                    print("Cycle: 3 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")
                    print("Cycle: 4 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")


                if (self.programMode == "AP"):
                    print("Cycle: 1 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 2 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 3 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")

            elif self.name == "xor":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " xor $" + str(
                    self.p1) + ", $" + str(self.p2) + ", $" + str(
                    self.p3) + "   Taking 4 cycles")

                if (self.programMode == "MC"):
                    print("Cycle: 1 " + "| MemtoReg: x"  + "| MemWrite: x"  + "| Branch: x"
                          + "| ALUSrc: x" + "| RegDst: x" + "| RegWrite: x")
                    print("Cycle: 2 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")
                    print("Cycle: 3 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")
                    print("Cycle: 4 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")

                if (self.programMode == "AP"):
                    print("Cycle: 1 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 2 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 3 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")

            elif self.name == "slt":
                print("Cycle: " + str(self.cycle - 4) + "| PC:" + str(self.pc) + " slt $" + str(
                    self.p1) + ", $" + str(self.p2) + ", $" + str(
                    self.p3) + "   Taking 4 cycles")

                if (self.programMode == "MC"):
                    print("Cycle: 1 " + "| MemtoReg: x"  + "| MemWrite: x"  + "| Branch: x"
                          + "| ALUSrc: x" + "| RegDst: x" + "| RegWrite: x")
                    print("Cycle: 2 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")
                    print("Cycle: 3 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")
                    print("Cycle: 4 " + "| MemtoReg: 0"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 0" + "| RegDst: 1" + "| RegWrite: 1")

                if (self.programMode == "AP"):
                    print("Cycle: 1 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 2 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 3 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")


            #sb $t, offset($s)
            elif self.name == "sb":
                print("Cycle: " + str(self.cycle - 5) + "| PC:" + str(self.pc) + " sb $" + str(
                    self.p1) + ", " + str(self.p2) + "($" + str(
                    self.p3) + ")   Taking 5 cycles")

                if (self.programMode == "MC"):
                    print("Cycle: 1 x" + "| MemtoReg: x"  + "| MemWrite: x"  + "| Branch: x"
                          + "| ALUSrc: x" + "| RegDst: x" + "| RegWrite: x")
                    print("Cycle: 2 " + "| MemtoReg: x"  + "| MemWrite: 1"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: x" + "| RegWrite: 0")
                    print("Cycle: 3 " + "| MemtoReg: x"  + "| MemWrite: 1"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: x" + "| RegWrite: 0")
                    print("Cycle: 4 " + "| MemtoReg: x"  + "| MemWrite: 1"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: x" + "| RegWrite: 0")
                    print("Cycle: 5 " + "| MemtoReg: x"  + "| MemWrite: 1"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: x" + "| RegWrite: 0")

                if (self.programMode == "AP"):
                    print("Cycle: 1 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 2 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 3 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")


            #lw $t, offset($s)
            elif self.name == "lb":
                print("Cycle: " + str(self.cycle - 5) + "| PC:" + str(self.pc) + " lb $" + str(
                    self.p1) + ", " + str(self.p2) + "($" + str(
                    self.p3) + ")   Taking 5 cycles")

                if (self.programMode == "MC"):
                    print("Cycle: 1 " + "| MemtoReg: x"  + "| MemWrite: x"  + "| Branch: x"
                          + "| ALUSrc: x" + "| RegDst: x" + "| RegWrite: x")
                    print("Cycle: 2 " + "| MemtoReg: 1"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")
                    print("Cycle: 3 " + "| MemtoReg: x"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")
                    print("Cycle: 4 " + "| MemtoReg: 1"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")
                    print("Cycle: 5 " + "| MemtoReg: x"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")

                if (self.programMode == "AP"):
                    print("Cycle: 1 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 2 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 3 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")


            elif self.name == "sw":
                print("Cycle: " + str(self.cycle - 5) + "| PC:" + str(self.pc) + " sw $" + str(
                    self.p1) + ", " + str(self.p2) + "($" + str(
                    self.p3) + ")   Taking 5 cycles")

                if (self.programMode == "MC"):
                    print("Cycle: 1 x" + "| MemtoReg: x"  + "| MemWrite: x"  + "| Branch: x"
                          + "| ALUSrc: x" + "| RegDst: x" + "| RegWrite: x")
                    print("Cycle: 2 " + "| MemtoReg: x"  + "| MemWrite: 1"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: x" + "| RegWrite: 0")
                    print("Cycle: 3 " + "| MemtoReg: x"  + "| MemWrite: 1"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: x" + "| RegWrite: 0")
                    print("Cycle: 4 " + "| MemtoReg: x"  + "| MemWrite: 1"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: x" + "| RegWrite: 0")
                    print("Cycle: 5 " + "| MemtoReg: x"  + "| MemWrite: 1"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: x" + "| RegWrite: 0")

                if (self.programMode == "AP"):
                    print("Cycle: 1 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 2 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 3 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")


            elif self.name == "lw":
                print("Cycle: " + str(self.cycle - 5) + "| PC:" + str(self.pc) + " lw $" + str(
                    self.p1) + ", " + str(self.p2) + "($" + str(
                    self.p3) + ")   Taking 5 cycles")

                if (self.programMode == "MC"):
                    print("Cycle: 1 " + "| MemtoReg: x"  + "| MemWrite: x"  + "| Branch: x"
                          + "| ALUSrc: x" + "| RegDst: x" + "| RegWrite: x")
                    print("Cycle: 2 " + "| MemtoReg: 1"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")
                    print("Cycle: 3 " + "| MemtoReg: x"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")
                    print("Cycle: 4 " + "| MemtoReg: 1"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")
                    print("Cycle: 5 " + "| MemtoReg: x"  + "| MemWrite: 0"  + "| Branch: 0"
                          + "| ALUSrc: 1" + "| RegDst: 0" + "| RegWrite: 1")

                if (self.programMode == "AP"):
                    print("Cycle: 1 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 2 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")
                    print("Cycle: 3 " + "| Pipeline Stage: "  + "| Bubble Status: "
                          + "| Stall or Flush: " + "| Which Hazard:" + "| hazard information: ")

            else:
                print("")

    def exitSim(self):
        print("Total # of cycles: " + str(self.cycle))
        print("Dynamic instructions count: " + str(self.DIC))

        if (self.programMode == "MC"):
            print("Three Cycles: " + str(self.threeCycles) + " instructions take 3 cycles")
            print("Four Cycles: " + str(self.fourCycles) + " instructions take 4 cycles")
            print("Five Cycles: " + str(self.fiveCycles) + " instructions take 5 cycles")

        #TODO
        if (self.programMode == "AP"):
            print("Statistics of delays: " + str(self.delay))
            print("Statistics of forward-path usage: " + str(self.delay))

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -----------------------------------------------   Simulator Start   ------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #



def choosemode(mode):
    global blk_size
    global total_blk
    global N
    global Sets
    global word_offset
    global set_offset
    global Placement_Policy

    if mode == "a":
        Placement_Policy = "DM"
        blk_size = 16
        N = 1
        Sets = 4
        total_blk = 4
        set_offset = int(math.log(Sets, 2))
    elif mode == "b":
        Placement_Policy = "FA"
        blk_size = 8
        N = 8
        Sets = 1
        total_blk = 8
        set_offset = int(math.log(Sets, 2))
    elif mode == "c":
        Placement_Policy = "SA"
        blk_size = 8
        N = 2
        Sets = 4
        set_offset = int(math.log(N, 2))
    elif mode == "d":
        Placement_Policy = "SA"
        blk_size = 8
        N = 4
        Sets = 2
        set_offset = int(math.log(N, 2))
    else:
        Placement_Policy = input("Please select the Placement Policy type DM, SA, or FA:\n")
        print("Please enter a vaild inputs correspond to the selected Placement Policy:")

        #validate the input
        while True:
            try:
                blk_size = int(input("Please enter block size:\n"))
                N = int(input("Please enter number of ways:\n"))
                Sets = int(input("Please enter number of set:\n"))
                set_offset = int(math.log(Sets, 2))
            except ValueError:
                print("\n\nEnter a valid input!!! -_- \n\n")
                continue
            else:
                break
        


    word_offset = int(math.log(blk_size, 2))


def simulate():
    global instructionsList
    global debugMode
    global blk_size
    global Placement_Policy
    global menu
    global programMode

    stats = Statistic(debugMode, programMode)  # init. the statistic class, keeps track of debugmode as well

    Instruction = instructionsList.copy()

    Register = [0 for i in range(24)]  # initialie all registers to 0
    Memory = [0 for i in range(mem_space)]  # initialize all memory spaces to 0

    # initialie the following var for cache sim
    Cache = []
    LRUQueue = []
    waysQueue = []
    blocks = {}
    ways =  []
    Misses = 0
    Hits = 0

    if menu == 3:
        Cache = [[0 for j in range(blk_size)] for i in range(total_blk)]  # Cache data

        # initialie blocks and ways
        if(Placement_Policy == "SA"):
            blocks = {new_list: [0 for i in range(3)] for new_list in range(int(total_blk/N))}
            for i in range(N):
                f = {}
                f = copy.deepcopy(blocks)
                ways.append(f)

            for i in range(int(total_blk/N)):
                LRUQueue.append(i)

            for i in range(N):
                x = []
                x= copy.deepcopy(LRUQueue)
                waysQueue.append(x)
     
        else:
            blocks = {new_list: [0 for i in range(3)] for new_list in range(total_blk)} # dictionary to save every block information
        for i in range(total_blk):
            LRUQueue.append(i)

    PC = 0
    DIC = 0

    finished = False

    while not finished:
        DIC += 1
        if PC == len(instructionsList):
            break
        fetch = Instruction[PC]

        # ********************************************************************************************************* ADD
        if (fetch[0][0] == "add"):  # ADD
            PC += 1
            results = Register[int(fetch[1][1])] + Register[int(fetch[1][2])]
            results = checkResults(results)
            Register[int(fetch[1][0])] = results
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1], fetch[1][2], 4, PC*4)  # add instr, 4 cycles

        # ********************************************************************************************************* ADD
        elif (fetch[0][0] == "addu"):  # ADDU
            PC += 1
            results = Register[int(fetch[1][2])] + Register[int(fetch[1][1])]
            results = checkResults(results)
            Register[int(fetch[1][0])] = results
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1], fetch[1][2], 4, PC*4)  # addu instr, 4 cycles


        # ********************************************************************************************************* ori
        elif (fetch[0][0] == "ori"):  # ori
            PC += 1
            results = int(fetch[1][2]) | Register[int(fetch[1][1])]
            results = checkResults(results)
            Register[int(fetch[1][0])] = results
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1], fetch[1][2], 5, PC*4)  # ori instr, 5 cycles


        # ********************************************************************************************************* xor
        elif (fetch[0][0] == "xor"):  # xor
            PC += 1
            results = int(bin(Register[int(fetch[1][1])]).replace("0b",""),2) ^ int(bin(Register[int(fetch[1][2])]).replace("0b",""),2)
            results = checkResults(results)
            Register[int(fetch[1][0])] = results
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1], fetch[1][2], 4, PC*4)  # addu instr, 4 cycles


        # ********************************************************************************************************* sll
        elif (fetch[0][0] == "sll"):  # sll
            PC += 1
            var1 = Register[int(fetch[1][1])]
            var2 = int(fetch[1][2])
            results = (var1 <<  var2)
            results = checkResults(results)
            Register[int(fetch[1][0])] = results
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1], fetch[1][2], 4, PC*4)  # sll instr, 4 cycles

        # ********************************************************************************************************* SUB
        elif (fetch[0][0] == "sub"):  # SUB
            PC += 1
            results = Register[int(fetch[1][1])] - Register[int(fetch[1][2])]
            results = checkResults(results)
            Register[int(fetch[1][0])] = results
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1], fetch[1][2], 4, PC*4)  # addu instr, 4 cycles

        # ********************************************************************************************************* ADDI
        elif (fetch[0][0] == 'addi'):  # ADDI
            imm = int(fetch[1][2])
            PC += 1
            results = Register[int(fetch[1][1])] + imm
            results = checkResults(results)
            Register[int(fetch[1][0])] = results
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1], fetch[1][2], 5, PC*4)  # addu instr, 5 cycles

        # ********************************************************************************************************* BEQ
        elif (fetch[0][0] == 'beq'):  # BEQ
            x = PC + 1
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1], fetch[1][2], 3, PC*4)  # beq instr, 3 cycles
            if Register[int(fetch[1][0])] == Register[int(fetch[1][1])]:
                for i in range(len(labelname)):
                    if (labelname[i] == fetch[1][2]):
                        PC = labelindex[i]
            else:
                PC += 1
                x = PC

        # ********************************************************************************************************* BNE
        elif (fetch[0][0] == 'bne'):  # BNE
            x = PC + 1
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1], fetch[1][2], 3, PC*4)  # bne instr, 3 cycles
            if Register[int(fetch[1][0])] != Register[int(fetch[1][1])]:
                for i in range(len(labelname)):
                    if (labelname[i] == fetch[1][2]):
                        PC = labelindex[i]
            else:
                PC += 1
                x = PC

        # ********************************************************************************************************* SLT
        elif (fetch[0][0] == 'slt'):  # SLT
            PC += 1
            Register[int(fetch[1][0])] = 1 if Register[int(fetch[1][1])] < Register[int(fetch[1][2])] else 0
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1], fetch[1][2], 4, PC*4)  # slt instr, 4 cycles

        # ********************************************************************************************************* SLTU
        elif (fetch[0][0] == 'sltu'):  # SLTU
            PC += 1
            Register[int(fetch[1][0])] = 1 if Register[int(fetch[1][1])] < Register[int(fetch[1][2])] else 0
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1], fetch[1][2], 4, PC*4)  # sltu instr, 4 cycles

        # ********************************************************************************************************* SW
        elif (fetch[0][0] == 'sw'):  # SW

            if isinstance(fetch[1][1][1],str): 
                x= int(fetch[1][1][1]) 
            else: x = fetch[1][1][1]

            if isinstance(fetch[1][1][0],str): 
                y= int(fetch[1][1][0]) 
            else: y = fetch[1][1][0]

            address = y + Register[x] # The actual address store-word is accessing
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1][0], fetch[1][1][1], 5, PC*4)  # sw instr, 5 cycles
            Memory[address  - 8192] = Register[int(fetch[1][0])]

            PC += 1

            if menu == 3:
                #Store word first in memory. It's software don't care about cache :)
                addressBin = bin(address).replace('0b','').zfill(16)


                if(Placement_Policy == "DM"):
                    index = addressBin[16-word_offset-set_offset:16-word_offset] 

                    if(debugMode):
                        print("Address of StoreWord: ", address)
                        print("Set index",index)

                    index = int(index,2)
                    tag = addressBin[0:16-word_offset-set_offset]#tag 

                    if ( blocks[index][0] == 0 ): # Cache miss
                        Misses += 1
                        blocks[index][0] = 1    # Since we have cache miss, valid bit is now 1 after cache has updated value
                        blocks[index][1] = tag
                        blocks[index][2] = Memory[address - 8192]  # Load memory into cache data

                        if(debugMode):
                            print("Cache missed due to valid bit = 0")
                            print("Tag = " ,blocks[index][1])

                    else: # Valid bit is 1, now check if tag matches
                        if( blocks[index][1] == tag): # Cache hit             
                            Hits += 1
                            if(debugMode):
                                print("Cache hit")
                                print("Tag = ",blocks[index][1])

                        else: # Tag doesnt match, cache miss
                            Misses += 1
                            blocks[index][1] = tag
                            blocks[index][2] = Memory[address - 8192]  # store memory into cache data
                            if(debugMode):
                                print("Cache missed due to tag mismatch")
                                print("Tag = ",blocks[index][1])

                if(Placement_Policy == "FA"):
                    found = False
                    tag = addressBin[0:16-word_offset]   #tag

                    for i in range(total_blk):
                        if (blocks[i][0] == 1 and blocks[i][1] == tag): # Cache miss
                            Hits += 1
                            found = True
                            if(debugMode):
                                print("Cache hit")
                                print("Tag = ",blocks[i][1])
                            break

                    if(found == False):
                        for i in range(total_blk):
                            if (blocks[i][0] == 0):
                                Misses += 1
                                blocks[i][0] = 1
                                blocks[i][1] = tag
                                blocks[i][2] = Memory[address - 8192]  # Load memory into cache data
                                LRUQueue.pop(i)
                                LRUQueue.append(i)
                                found = True
                                if(debugMode):
                                    print("Cache missed")
                                    print("Tag = ",blocks[i][1])
                                break

                    if(found == False):
                        Misses += 1
                        i = LRUQueue.pop(0)
                        LRUQueue.append(i)
                        blocks[i][1] = tag
                        blocks[i][2] = Memory[address - 8192]  # Load memory into cache data
                        if(debugMode):
                                print("Cache missed")
                                print("Tag = ",blocks[i][1])

                if(Placement_Policy == "SA"):
                    index = addressBin[16-word_offset-set_offset:16-word_offset]
                    index = int(index,2)
                    tag = addressBin[0:16-word_offset-set_offset]#tag 

                    total_blkInWays = int(total_blk/N)

                    for i in range(total_blkInWays):
                        if (ways[index][i][0] == 1 and ways[index][i][1] == tag): # Cache miss
                            Hits += 1
                            found = True
                            if(debugMode):
                                print("Cache hit")
                                print("Tag = ",ways[index][i][1])
                            break
                
                    for i in range(total_blkInWays):
                        if (ways[index][i][0] == 0):
                            Misses += 1
                            waysQueue[index].pop(i)
                            waysQueue[index].append(i)
                            ways[index][i][0] = 1
                            ways[index][i][1] = tag
                            ways[index][i][2] = Memory[address - 8192]  # Load memory into cache data
                            found = True
                            if(debugMode):
                                print("Cache missed")
                                print("Tag = ",ways[index][i][1])
                            break

                    if(found == False):
                        Misses += 1
                        i = waysQueue[index].pop(0)
                        waysQueue[index].append(i)
                        ways[index][i][1] = tag
                        ways[index][i][2] = Memory[address - 8192]  # Load memory into cache data
                        if(debugMode):
                                print("Cache missed")
                                print("Tag = ",ways[index][i][1])
                
                if (debugMode):
                    printInfo(Register, DIC, PC, Memory, Misses, Hits, ways,stats)

            
        # *********************************************************************************************************LW
        elif (fetch[0][0] == 'lw'):  # ********LOAD WORD********

            if isinstance(fetch[1][1][1],str): 
                x= int(fetch[1][1][1]) 
            else: x = fetch[1][1][1]

            if isinstance(fetch[1][1][0],str): 
                y= int(fetch[1][1][0]) 
            else: y = fetch[1][1][0]

            address = y + Register[x] # The actual address load-word is accessing

            #Load word first from memory. It's software don't care about cache :)
            Register[int(fetch[1][0])] = Memory[address  - 8192]
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1][0], fetch[1][1][1], 5, PC*4)  # sw instr, 5 cycles

            PC += 1

            if menu == 3:
                addressBin = bin(address).replace('0b','').zfill(16)

                if(Placement_Policy == "DM"):
                    index = addressBin[16-word_offset-set_offset:16-word_offset] 

                    if(debugMode):
                        print("Address of loadword: ", address)
                        print("Set index",index)

                    index = int(index,2)
                    tag = addressBin[0:16-word_offset-set_offset]#tag 

                    if ( blocks[index][0] == 0 ): # Cache miss
                        Misses += 1
                        blocks[index][0] = 1    # Since we have cache miss, valid bit is now 1 after cache has updated value
                        blocks[index][1] = tag
                        blocks[index][2] = Memory[address - 8192]  # Load memory into cache data

                        if(debugMode):
                            print("Cache missed due to valid bit = 0")
                            print("Tag = " ,blocks[index][1])

                    else: # Valid bit is 1, now check if tag matches
                        if( blocks[index][1] == tag): # Cache hit             
                            Hits += 1
                            if(debugMode):
                                print("Cache hit")
                                print("Tag = ",blocks[index][1])

                        else: # Tag doesnt match, cache miss
                            Misses += 1
                            blocks[index][1] = tag
                            blocks[index][2] = Memory[address - 8192]  # Load memory into cache data
                            if(debugMode):
                                print("Cache missed due to tag mismatch")
                                print("Tag = ",Tag[index])

                if(Placement_Policy == "FA"):
                    found = False
                    tag = addressBin[0:16-word_offset]   #tag

                    for i in range(total_blk):
                        if (blocks[i][0] == 1 and blocks[i][1] == tag): # Cache miss
                            Hits += 1
                            found = True
                            if(debugMode):
                                print("Cache hit")
                                print("Tag = ",blocks[i][1])
                            break
                
                    for i in range(total_blk):
                        if (blocks[i][0] == 0):
                            Misses += 1
                            LRUQueue.pop(i)
                            LRUQueue.append(i)
                            blocks[i][0] = 1
                            blocks[i][1] = tag
                            blocks[i][2] = Memory[address - 8192]  # Load memory into cache data
                            found = True
                            if(debugMode):
                                print("Cache missed")
                                print("Tag = ",blocks[i][1])
                            break

                    if(found == False):
                        Misses += 1
                        i = LRUQueue.pop(0)
                        LRUQueue.append(i)
                        blocks[i][1] = tag
                        blocks[i][2] = Memory[address - 8192]  # Load memory into cache data
                        if(debugMode):
                                print("Cache missed")
                                print("Tag = ",blocks[i][1])

                if(Placement_Policy == "SA"):
                    index = addressBin[16-word_offset-set_offset:16-word_offset]
                    index = int(index,2)
                    tag = addressBin[0:16-word_offset-set_offset]#tag 

                    total_blkInWays = int(total_blk/N)

                    for i in range(total_blkInWays):
                        if (ways[index][i][0] == 1 and ways[index][i][1] == tag): # Cache miss
                            Hits += 1
                            found = True
                            if(debugMode):
                                print("Cache hit")
                                print("Tag = ",ways[index][i][1])
                            break
                
                    for i in range(total_blkInWays):
                        if (ways[index][i][0] == 0):
                            Misses += 1
                            waysQueue[index].pop(i)
                            waysQueue[index].append(i)
                            ways[index][i][0] = 1
                            ways[index][i][1] = tag
                            ways[index][i][2] = Memory[address - 8192]  # Load memory into cache data
                            found = True
                            if(debugMode):
                                print("Cache missed")
                                print("Tag = ",ways[index][i][1])
                            break

                    if(found == False):
                        Misses += 1
                        i = waysQueue[index].pop(0)
                        waysQueue[index].append(i)
                        ways[index][i][1] = tag
                        ways[index][i][2] = Memory[address - 8192]  # Load memory into cache data
                        if(debugMode):
                                print("Cache missed")
                                print("Tag = ",ways[index][i][1])

                    if (debugMode):
                        printInfo(Register, DIC, PC, Memory, Misses, Hits, ways,stats)


        if (debugMode):
            if(Placement_Policy == "SA"):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, ways,stats)
            else:
                printInfo(Register, DIC, PC, Memory, Misses, Hits, blocks,stats)

        # ********************************************************************************************************* SB
        elif (fetch[0][0] == 'sb'):  # SB

            if isinstance(fetch[1][1][1],str): 
                x= int(fetch[1][1][1]) 
            else: x = fetch[1][1][1]

            if isinstance(fetch[1][1][0],str): 
                y= int(fetch[1][1][0]) 
            else: y = fetch[1][1][0]

            address = y + Register[x] # The actual address store-word is accessing
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1][0], fetch[1][1][1], 5, PC*4)  # sw instr, 5 cycles
            Memory[address  - 8192] = Register[int(fetch[1][0])]

            PC += 1

            if menu == 3:
                #Store word first in memory. It's software don't care about cache :)
                addressBin = bin(address).replace('0b','').zfill(16)


                if(Placement_Policy == "DM"):
                    index = addressBin[16-word_offset-set_offset:16-word_offset] 

                    if(debugMode):
                        print("Address of StoreWord: ", address)
                        print("Set index",index)

                    index = int(index,2)
                    tag = addressBin[0:16-word_offset-set_offset]#tag 

                    if ( blocks[index][0] == 0 ): # Cache miss
                        Misses += 1
                        blocks[index][0] = 1    # Since we have cache miss, valid bit is now 1 after cache has updated value
                        blocks[index][1] = tag
                        blocks[index][2] = Memory[address - 8192]  # Load memory into cache data

                        if(debugMode):
                            print("Cache missed due to valid bit = 0")
                            print("Tag = " ,blocks[index][1])

                    else: # Valid bit is 1, now check if tag matches
                        if( blocks[index][1] == tag): # Cache hit             
                            Hits += 1
                            if(debugMode):
                                print("Cache hit")
                                print("Tag = ",blocks[index][1])

                        else: # Tag doesnt match, cache miss
                            Misses += 1
                            blocks[index][1] = tag
                            blocks[index][2] = Memory[address - 8192]  # store memory into cache data
                            if(debugMode):
                                print("Cache missed due to tag mismatch")
                                print("Tag = ",blocks[index][1])

                if(Placement_Policy == "FA"):
                    found = False
                    tag = addressBin[0:16-word_offset]   #tag

                    for i in range(total_blk):
                        if (blocks[i][0] == 1 and blocks[i][1] == tag): # Cache miss
                            Hits += 1
                            found = True
                            if(debugMode):
                                print("Cache hit")
                                print("Tag = ",blocks[i][1])
                            break

                    if(found == False):
                        for i in range(total_blk):
                            if (blocks[i][0] == 0):
                                Misses += 1
                                blocks[i][0] = 1
                                blocks[i][1] = tag
                                blocks[i][2] = Memory[address - 8192]  # Load memory into cache data
                                LRUQueue.pop(i)
                                LRUQueue.append(i)
                                found = True
                                if(debugMode):
                                    print("Cache missed")
                                    print("Tag = ",blocks[i][1])
                                break

                    if(found == False):
                        Misses += 1
                        i = LRUQueue.pop(0)
                        LRUQueue.append(i)
                        blocks[i][1] = tag
                        blocks[i][2] = Memory[address - 8192]  # Load memory into cache data
                        if(debugMode):
                                print("Cache missed")
                                print("Tag = ",blocks[i][1])

                if(Placement_Policy == "SA"):
                    index = addressBin[16-word_offset-set_offset:16-word_offset]
                    index = int(index,2)
                    tag = addressBin[0:16-word_offset-set_offset]#tag 

                    total_blkInWays = int(total_blk/N)

                    for i in range(total_blkInWays):
                        if (ways[index][i][0] == 1 and ways[index][i][1] == tag): # Cache miss
                            Hits += 1
                            found = True
                            if(debugMode):
                                print("Cache hit")
                                print("Tag = ",ways[index][i][1])
                            break
                
                    for i in range(total_blkInWays):
                        if (ways[index][i][0] == 0):
                            Misses += 1
                            waysQueue[index].pop(i)
                            waysQueue[index].append(i)
                            ways[index][i][0] = 1
                            ways[index][i][1] = tag
                            ways[index][i][2] = Memory[address - 8192]  # Load memory into cache data
                            found = True
                            if(debugMode):
                                print("Cache missed")
                                print("Tag = ",ways[index][i][1])
                            break

                    if(found == False):
                        Misses += 1
                        i = waysQueue[index].pop(0)
                        waysQueue[index].append(i)
                        ways[index][i][1] = tag
                        ways[index][i][2] = Memory[address - 8192]  # Load memory into cache data
                        if(debugMode):
                                print("Cache missed")
                                print("Tag = ",ways[index][i][1])
                
                if (debugMode):
                    printInfo(Register, DIC, PC, Memory, Misses, Hits, ways,stats)

            
        # *********************************************************************************************************LB
        elif (fetch[0][0] == 'lb'):  # ********LOAD WORD********

            if isinstance(fetch[1][1][1],str): 
                x= int(fetch[1][1][1]) 
            else: x = fetch[1][1][1]

            if isinstance(fetch[1][1][0],str): 
                y= int(fetch[1][1][0]) 
            else: y = fetch[1][1][0]

            address = y + Register[x] # The actual address load-word is accessing

            #Load word first from memory. It's software don't care about cache :)
            Register[int(fetch[1][0])] = Memory[address  - 8192]
            stats.log(asmCopy[PC], fetch[0][0], fetch[1][0], fetch[1][1][0], fetch[1][1][1], 5, PC*4)  # sw instr, 5 cycles

            PC += 1

            if menu == 3:
                addressBin = bin(address).replace('0b','').zfill(16)

                if(Placement_Policy == "DM"):
                    index = addressBin[16-word_offset-set_offset:16-word_offset] 

                    if(debugMode):
                        print("Address of loadword: ", address)
                        print("Set index",index)

                    index = int(index,2)
                    tag = addressBin[0:16-word_offset-set_offset]#tag 

                    if ( blocks[index][0] == 0 ): # Cache miss
                        Misses += 1
                        blocks[index][0] = 1    # Since we have cache miss, valid bit is now 1 after cache has updated value
                        blocks[index][1] = tag
                        blocks[index][2] = Memory[address - 8192]  # Load memory into cache data

                        if(debugMode):
                            print("Cache missed due to valid bit = 0")
                            print("Tag = " ,blocks[index][1])

                    else: # Valid bit is 1, now check if tag matches
                        if( blocks[index][1] == tag): # Cache hit             
                            Hits += 1
                            if(debugMode):
                                print("Cache hit")
                                print("Tag = ",blocks[index][1])

                        else: # Tag doesnt match, cache miss
                            Misses += 1
                            blocks[index][1] = tag
                            blocks[index][2] = Memory[address - 8192]  # Load memory into cache data
                            if(debugMode):
                                print("Cache missed due to tag mismatch")
                                print("Tag = ",Tag[index])

                if(Placement_Policy == "FA"):
                    found = False
                    tag = addressBin[0:16-word_offset]   #tag

                    for i in range(total_blk):
                        if (blocks[i][0] == 1 and blocks[i][1] == tag): # Cache miss
                            Hits += 1
                            found = True
                            if(debugMode):
                                print("Cache hit")
                                print("Tag = ",blocks[i][1])
                            break
                
                    for i in range(total_blk):
                        if (blocks[i][0] == 0):
                            Misses += 1
                            LRUQueue.pop(i)
                            LRUQueue.append(i)
                            blocks[i][0] = 1
                            blocks[i][1] = tag
                            blocks[i][2] = Memory[address - 8192]  # Load memory into cache data
                            found = True
                            if(debugMode):
                                print("Cache missed")
                                print("Tag = ",blocks[i][1])
                            break

                    if(found == False):
                        Misses += 1
                        i = LRUQueue.pop(0)
                        LRUQueue.append(i)
                        blocks[i][1] = tag
                        blocks[i][2] = Memory[address - 8192]  # Load memory into cache data
                        if(debugMode):
                                print("Cache missed")
                                print("Tag = ",blocks[i][1])

                if(Placement_Policy == "SA"):
                    index = addressBin[16-word_offset-set_offset:16-word_offset]
                    index = int(index,2)
                    tag = addressBin[0:16-word_offset-set_offset]#tag 

                    total_blkInWays = int(total_blk/N)

                    for i in range(total_blkInWays):
                        if (ways[index][i][0] == 1 and ways[index][i][1] == tag): # Cache miss
                            Hits += 1
                            found = True
                            if(debugMode):
                                print("Cache hit")
                                print("Tag = ",ways[index][i][1])
                            break
                
                    for i in range(total_blkInWays):
                        if (ways[index][i][0] == 0):
                            Misses += 1
                            waysQueue[index].pop(i)
                            waysQueue[index].append(i)
                            ways[index][i][0] = 1
                            ways[index][i][1] = tag
                            ways[index][i][2] = Memory[address - 8192]  # Load memory into cache data
                            found = True
                            if(debugMode):
                                print("Cache missed")
                                print("Tag = ",ways[index][i][1])
                            break

                    if(found == False):
                        Misses += 1
                        i = waysQueue[index].pop(0)
                        waysQueue[index].append(i)
                        ways[index][i][1] = tag
                        ways[index][i][2] = Memory[address - 8192]  # Load memory into cache data
                        if(debugMode):
                                print("Cache missed")
                                print("Tag = ",ways[index][i][1])

                    if (debugMode):
                        printInfo(Register, DIC, PC, Memory, Misses, Hits, ways,stats)


        if (debugMode):
            if(Placement_Policy == "SA"):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, ways,stats)
            else:
                printInfo(Register, DIC, PC, Memory, Misses, Hits, blocks,stats)

    print("***Finished simulation***")
    printInfo(Register, DIC, PC, Memory, Misses, Hits, blocks, stats)
    if(menu == 1 or menu == 2):
        stats.exitSim()

# -------------------------------------------------------------------------------------------------------------------- #
# ---- FUNCTION: Prints the registers information when the debug mode is on.
def printInfo(_register, _DIC, _PC,_Mem,_Misses,_Hits,_Cache, _stats):
    global menu
    global debugMode

    print('\n************** Instruction Number ' + str(_PC) + '. ' + asmCopy[_PC-1] + ' : **************\n')
    print('Registers $0 - $23: \n', _register)
    x = 64/4
    printWords = [sum(_Mem[i:i+4]) for i in range(0, len(_Mem), 4)]
    print('Memory start from 8192 (Words): \n', printWords[0:100])
    print('\nDynamic instructions count: ', _DIC)
    print('PC = ', _PC*4)

    if menu == 1 and debugMode == True:
        print("\n***MC Info***")
        _stats.prints()

    if menu == 2 and debugMode == True:
        print("\n***AP Info***")
        _stats.prints()

    if menu == 3:
        print("\n***Cache Info***")
        print("Cache misses:" + str(_Misses))
        print("Cache hits:" + str(_Hits))
        if(_Hits + _Misses == 0):
            print("Cache Hit Rate:" + str(0))
        else:
            print("Cache Hit Rate:" + str(100 * (float(_Hits) / float(_Hits + _Misses))))
        print("Blocks info (contains index, valid, tag, and data): " + str(_Cache))

    if debugMode:
        print('\nPress enter to continue.......')
        input()

# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------  Cache Simulator End   -------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------------------------------- #
# ---- FUNCTION: Ask user to enter the file name. If user press enter the applicaiton will take the default file.
def SelectFile(defaultFile):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

    # Select  file, default is prog.asm
    while True:
        cktFile = defaultFile
        print("\nRead asm file: use " + cktFile + "?" + " Enter to accept or type filename: ")
        userInput = input()
        if userInput == "":
            userInput = defaultFile
            return userInput
        else:
            cktFile = os.path.join(script_dir, userInput)
            if not os.path.isfile(cktFile):
                print("File does not exist. \n")
            else:
                return userInput

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Takes hex and return int
def CheckandConvertHexToInt(_line):

    if "(" in _line:
      _line = _line.replace(")","")
      _line = _line.split("(")
      if "0x" in _line[0]:
        _line[0] = _line[0].replace('0x','')
        _line[0] = int(_line[0], 16)

    if "0x" in _line:
        _line = _line.replace('0x','')
        _line = int(_line, 16)   
        
    return _line

# -------------------------------------------------------------------------------------------------------------------- #
#---- FUNCTION: Convert an instruction to 
def convertAsmToBin(line):

    if isinstance(line[1][1][0], str):
        line[1][1][0] = int(line[1][1][0])

    if(line[0][0] == 'lw'):
        rt = format(int(line[1][0]), '05b').zfill(5)
        rs = format(int(line[1][1][1]),'05b').zfill(5)
        offset = format(line[1][1][0],'016b') if (int(line[1][1][0]) >= 0) else format(65536 + int(line[1][1][0]),'016b')
        bin = "100011" + rs + rt + offset.zfill(16)

    elif(line[0][0] == 'sw'):
        rt = format(int(line[1][0]), '05b').zfill(5)
        rs = format(int(line[1][1][1]),'05b').zfill(5)
        offset = format(line[1][1][0],'016b') if (int(line[1][1][0]) >= 0) else format(65536 + int(line[1][1][0]),'016b')
        bin = "101011" + rs + rt + offset.zfill(16)

    return bin

# -------------------------------------------------------------------------------------------------------------------- #
#---- FUNCTION: function read in asm file and returns it as a list
def insertMipsFile():
    global asmCopy
    global labelindex
    global labelname

    lineCount = 0

    I_file = open(SelectFile("prog.asm"),"r")

    Instruction = []    # array containing all instructions to execute         

    for line in I_file:
        if (line == "\n" or line[0] =='#'):              # empty lines,comments ignored
            continue
        line = line.replace('\n','')
        line = line.replace(' ','')
        if ":" in line:
            labelname.append(line[0:line.index(":")]) # append the label name
            labelindex.append(lineCount) # append the label's index\
            continue
        lineCount += 1
        asmCopy.append(line)
        line = line.split('$',1)
        for item in line:
            ind = line.index(item)
            item = item.replace('$','')
            line[ind] = item.split(',')
        
        if(line[0][0] == 'lw' or line[0][0] == 'sw'):
            line[1][1] = CheckandConvertHexToInt(line[1][1])
        else:
            line[1][2] = str(CheckandConvertHexToInt(line[1][2]))
        Instruction.append(line)

    return Instruction
            
# -------------------------------------------------------------------------------------------------------------------- #
#---- FUNCTION: function read in asm file and returns it as a list
def checkResults(_num):
    x= str(bin(_num)).replace("0b","")
    if len(x)>32:
        n = len(x) - 31
        x = x[n:]
        b = int(x[15:],2)
        a = x[:15]
        reg1 = int(a,2) * 65536
        reg1 = format(reg1 | b, "032b")
        return int(reg1,2)
    else:
        return _num


# -------------------------------------------------------------------------------------------------------------------- #
#---- FUNCTION: Main
def main():

    global instructionsList
    global debugMode
    global menu
    global blk_size
    global Sets
    global total_blk
    global programMode

    ## Keeps loop until user hits Exit.
    while True:

        print("\nChoose what you’d like to do (1, 2, or 3): ", "1: Processor Simulation of MC", "2: Processor Simulation of AP", "3: Data Cache Simulator ","4: Exit", sep="\n\n")
        
        while True:
            Input = input()
            ## Input validater 
            if Input != '1' and Input != '2' and Input != '3':
                print("\n\nEnter a valid input!!! -_-\n\n")
            else:
                break

        menu = int(Input)

        ## -------------------------------------------------------------------------------------------------------------------- #
        ## AP
        if menu == 1:
            ## Debug mode or normal mode
            programMode = "MC"
            print("\nWould you like to run simulator in debug mode ?")
            debugMode =True if  int(input("\n1: debug mode \n\n2: normal execution\n")) == 1 else False
            instructionsList = insertMipsFile()
            simulate()

        ## -------------------------------------------------------------------------------------------------------------------- #
        ## MC
        if menu == 2:
            ## Debug mode or normal mode
            programMode = "AP"
            print("\nWould you like to run simulator in debug mode ?")
            debugMode =True if  int(input("\n1: debug mode \n\n2: normal execution\n")) == 1 else False
            instructionsList = insertMipsFile()
            simulate()
            
        ## -------------------------------------------------------------------------------------------------------------------- #
        ##  Cache
        elif menu == 3:
            ## Debug mode or normal mode
            print("\nWould you like to run simulator in debug mode ?")
            debugMode =True if  int(input("\n1: debug mode \n\n2: normal execution\n")) == 1 else False
            instructionsList = insertMipsFile()
            print("***************************Starting Cache Simulation********************************")
            print("\nSettings : \n")
            print("Enter 'a' for a directly-mapped cache, block size of 16 Bytes, a total of 4 blocks")
            print("Enter 'b' for a fully-associated cache, block size of 8 Bytes, a total of 8 blocks")
            print("Enter 'c' for a 2-way set-associative cache, block size of 8 Bytes, 4 sets")
            print("Enter 'd' for a 4-way set-associative cache, block size of 8 Bytes, 2 sets")
            print("Press any key for entering block size, number of ways and number of sets of choice")
            mode = input("Choose preset mode or self set mode:")


            choosemode(mode)
            print("Cache block size: " + str(blk_size) + " words")
            print("Number of Sets: " + str(Sets))
            print("Total number of blocks: " + str(total_blk))
            simulate()
        ## -------------------------------------------------------------------------------------------------------------------- #
        ##  Exit 
        elif menu == 4:
            break

        else:
            print("\n\nEnter a valid input!!! -_- \n\n")



if __name__ == "__main__":
    main()
