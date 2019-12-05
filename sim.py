import os
import math
import copy

debugMode = False


# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Mc Simulation.
def simMC():
    print("\n\nOption 1: Processor Simulation of MC\n\n")


def simAP():
    print("\n\nOption 2: Processor Simulation of AP\n\n")


# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------  Cache Simulator Start   ------------------------------------------------ #
# -------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

import math

# For simple example, let's have all settings as global-variables
# For simple example, let's have all settings as global-variables
mem_space = 1024

b = 0
N = 0
S = 0
word_offset = 0
set_offset = 0

def choosemode(mode):
    global b
    global N
    global S
    global word_offset
    global set_offset
    if mode == "a":
        b = 16
        N = 1
        S = 4
    elif mode == "b":
        b = 8
        N = 8
        S = 1
    elif mode == "c":
        b = 8
        N = 2
        S = 4
    elif mode == "d":
        b = 8
        N = 4
        S = 2
    else:
        b = int(input("Please enter block size:\n"))
        N = int(input("Please enter number of ways:\n"))
        S = int(input("Please enter number of set:\n"))

    word_offset = int(math.log(b, 2))
    set_offset = int(math.log(S, 2))

def readIn(fileN):
    text = ""
    with open(fileN, "r") as f:
        for line in f:
            if line != "\n" and line[0] != '#':
                text += line

    return text

def splitText(text):
    return text.split("\n")


def cache_simulate(L):
    global debugMode

    print("***Starting simulation***")
    print("Settings : ")
    print("Enter 'a' for a directly-mapped cache, block size of 16 Bytes, a total of 4 blocks")
    print("Enter 'b' for a fully-associated cache, block size of 8 Bytes, a total of 8 blocks")
    print("Enter 'c' for a 2-way set-associative cache, block size of 8 Bytes, 4 sets")
    print("Enter 'd' for a 4-way set-associative cache, block size of 8 Bytes, 2 sets")
    print("Press any key for entering block size, number of ways and number of sets of choice")
    mode = input("Choose preset mode or self set mode:\n")

    choosemode(mode)
    print("Cache block size: " + str(word_offset) + ' words')
    print("Number of blocks: " + str(S))
    Register = [0 for i in range(24)]  # initialie all registers to 0
    Memory = [0 for i in range(mem_space)]  # initialize all memory spaces to 0
    Valid = [0 for i in range(S)]  # valid bits and tag data
    Tag = ['0' for i in range(S)]
    Cache = [[0 for j in range(b)] for i in range(S)]  # Cache data
    Misses = 0
    Hits = 0
    PC = 0
    DIC = 0
    lineCount = 0
    
    
    
    while lineCount < len(L):
        DIC += 1
        line = L[lineCount]

        # ********************************************************************************************************* Finish
        if (line[0:32] == '00010000000000001111111111111111'):
            print("PC =" + str(PC * 4) + " Instruction: Deadloop. Ending program")
            finished = True

        # ********************************************************************************************************* ADD
        elif (line[0:3] == "add"):  # ADD
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + "add $" + str(
                    int(line[16:21], 2)) + ",$" + str(int(line[6:11], 2)) + ",$" + str(int(line[11:16], 2)))
            PC += 1
            Register[int(line[16:21], 2)] = Register[int(line[6:11], 2)] + Register[int(line[11:16], 2)]

        # ********************************************************************************************************* SUB
        elif (line[0:3] == "sub"):  # SUB
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + "sub $" + str(
                    int(line[16:21], 2)) + ",$" + str(int(line[6:11], 2)) + ",$" + str(int(line[11:16], 2)))
            PC += 1
            Register[int(line[16:21], 2)] = Register[int(line[6:11], 2)] - Register[int(line[11:16], 2)]

        # ********************************************************************************************************* ADDI
        elif (line[0:4] == 'addi'):  # ADDI
            imm = int(line[16:32], 2) if line[16] == '0' else -(65535 - int(line[16:32], 2) + 1)
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + "addi $" + str(
                    int(line[16:21], 2)) + ",$" + str(int(line[6:11], 2)) + ",$" + str(imm))
            PC += 1
            Register[int(line[11:16], 2)] = Register[int(line[6:11], 2)] + imm

        # ********************************************************************************************************* BEQ
        elif (line[0:3] == 'beq'):  # BEQ
            imm = int(line[16:32], 2) if line[16] == '0' else -(65535 - int(line[16:32], 2) + 1)
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + "beq $" + str(
                    int(line[6:11], 2)) + ",$" + str(int(line[11:16], 2)) + "," + str(imm))
            PC += 1
            PC = PC + imm if (Register[int(line[6:11], 2)] == Register[int(line[11:16], 2)]) else PC

        # ********************************************************************************************************* BNE
        elif (line[0:3] == 'bne'):  # BNE
            imm = int(line[16:32], 2) if line[16] == '0' else -(65535 - int(line[16:32], 2) + 1)
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + "bne $" + str(
                    int(line[6:11], 2)) + ",$" + str(int(line[11:16], 2)) + "," + str(imm))
            PC += 1
            PC = PC + imm if Register[int(line[6:11], 2)] != Register[int(line[11:16], 2)] else PC

        # ********************************************************************************************************* SLT
        elif (line[0:3] == 'slt'):  # SLT
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + "slt $" + str(
                    int(line[16:21], 2)) + ",$" + str(int(line[6:11], 2)) + ",$" + str(int(line[11:16], 2)))
            PC += 1
            Register[int(line[16:21], 2)] = 1 if Register[int(line[6:11], 2)] < Register[int(line[11:16], 2)] else 0

        # ********************************************************************************************************* SW
        elif (line[0:2] == 'sw'):  # SW
            # Sanity check for word-addressing
            if (int(line[30:32]) % 4 != 0):
                print("Runtime exception: line address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", hex(int(line, 2)))
                exit()
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + "sw $" + str(
                    int(line[6:11], 2)) + "," + str(imm + Register[int(line[6:11], 2)] - 8192) + "(0x2000)")
            PC += 1
            imm = int(line[16:32], 2)
            index = int(line[32 - set_offset - 2:32 - 2], 2)
            Memory[imm + Register[int(line[6:11], 2)] - 8192] = Register[int(line[11:16], 2)]

            # TODO: CACHE-ACCESS

        # *********************************************************************************************************LW
        elif (line[0:2] == 'lw'):  # ********LOAD WORD********
            # Sanity check for word-addressing
            if (int(line[30:32]) % 4 != 0):
                print("Runtime exception: line address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", hex(int(line, 2)))
                exit()
            imm = int(line[16:32], 2)

            PC += 1
            # Cache access:
            # First check cache for any hit based on valid bit and index of cache
            address = format(imm + Register[int(line[6:11], 2)], "016b")  # The actual address load-word is accessing
            wordIndex = address[16 - 2 - word_offset:16 - 2]  # how many bits needed to index word in each blocks

            if mode == "b":
                index = 0
            else:
                index = address[16 - 2 - word_offset - set_offset:16 - 2 - word_offset]  # how many bits needed for set indexing

            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + "lw $" + str(
                    int(line[11:16], 2)) + ",$" + str(int(line[6:11], 2)) + "(" + str(imm) + ")")
                print("Address of loadword: ", address)
                print("Word offset", wordIndex)
                print("Set index", index)
            wordIndex = int(wordIndex, 2)

            if mode != "b":
                index = int(index, 2)

            if (Valid[index] == 0):  # Cache miss
                Misses += 1
                for i in range(b):
                    Cache[index][i] = Memory[
                        imm + Register[int(line[6:11], 2)] - 8192 + i * 4]  # Load memory into cache data
                Register[int(line[11:16], 2)] = Memory[
                    imm + Register[int(line[6:11], 2)] - 8192]  # Load data into register as well
                Valid[index] = 1  # Since we have cache miss, valid bit is now 1 after cache has updated value
                Tag[index] = address[0:16 - 2 - word_offset - set_offset]
                if (debugMode):
                    print("Cache missed due to valid bit = 0")
                    print("Tag = ", Tag[index])
                    print("Cache", Cache)
            else:  # Valid bit is 1, now check if tag matches
                if (Tag[index] == address[0:16 - 2 - word_offset - set_offset]):  # Cache hit

                    Register[int(line[11:16], 2)] = Cache[index][wordIndex]
                    Hits += 1
                    if (debugMode):
                        print("Cache hit")
                        print("Tag = ", Tag[index])
                        print("Cache", Cache)
                else:  # Tag doesnt match, cache miss
                    Misses += 1
                    for i in range(b):
                        Cache[index][i] = Memory[
                            imm + Register[int(line[6:11], 2)] - 8192 + i * 4]  # Load memory into cache data
                    Register[int(line[11:16], 2)] = Memory[
                        imm + Register[int(line[6:11], 2)] - 8192]  # Load cache data into register
                    Tag[index] = address[0:16 - 2 - word_offset - set_offset]  # Update tag
                    if (debugMode):
                        print("Cache missed due to tag mismatch")
                        print("Tag = ", Tag[index])
                        print("Cache", Cache)
            print("")

    print("***Finished simulation***")
    print("Dynamic instructions count: " + str(DIC))
    print("Cache misses:" + str(Misses))
    print("Cache hits:" + str(Hits))
    print("Cache Hit Rate:" + str(100 * (float(Hits) / float(Hits + Misses))))
    print("Registers: " + str(Register))
    print("Cache data: " + str(Cache))


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
# ---- FUNCTION: function read in asm file and returns it as a list



def main():
    ## Keeps loop until user hits Exit.
    while True:

        print("Choose what you’d like to do (1, 2, or 3): ", "1: Processor Simulation of MC ",
              "2: Processor Simulation of AP ", "3: Data Cache Simulator ", "4: Exit", sep="\n\n")

        while True:
            Input = input()
            ## Input validater
            if Input != '1' and Input != '2' and Input != '3' and Input != '4':
                print("\n\nEnter a valid input!!! -_-\n\n")
            else:
                break

        ## Debug mode or normal mode
        print("\nWould you like to run simulator in debug mode ?")
        debugMode = True if int(input("\n1: debug mode \n\n2: normal execution\n")) == 1 else False

        file_name = input("Enter file name to simulate")

        try:
            f = open(file_name)
            f.close()
            good_in = True
        except FileNotFoundError:
            print('File does not exist')
        text = readIn(file_name)
        t = splitText(text)

        menu = int(Input)

        ## -------------------------------------------------------------------------------------------------------------------- #
        ## Test Vector Generation Part 1
        if menu == 1:
            simMC()


        ## -------------------------------------------------------------------------------------------------------------------- #
        ## Fault Coverage Simulation Part 2
        elif menu == 2:
            simAP()

        ## -------------------------------------------------------------------------------------------------------------------- #
        ##  Avg Fault Coverage data generation Part 3
        elif menu == 3:
            cache_simulate(t)


        ## -------------------------------------------------------------------------------------------------------------------- #
        ##  Exit
        elif menu == 4:
            break

        else:
            print("\n\nEnter a valid input!!! -_- \n\n")


main()
