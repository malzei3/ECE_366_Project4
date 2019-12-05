import os
import math
import copy

debugMode = False
instructionsList = []
asmCopy = []

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
blk_size = 4  # each block is 64bytes, or 2 words

total_blk = 8  # 8 blocks in cache

mem_space = 1024

b = 0
N = 0
S = 0
word_offset = int(math.log(blk_size, 2))
set_offset = int(math.log(total_blk, 2))

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
        set_offset = int(math.log(S, 2))
    elif mode == "b":
        b = 8
        N = 8
        S = 1
        set_offset = int(math.log(N, 2))
    elif mode == "c":
        b = 8
        N = 2
        S = 4
        set_offset = int(math.log(S, 2))
    elif mode == "d":
        b = 8
        N = 4
        S = 2
        set_offset = int(math.log(S, 2))
    else:
        b = int(input("Please enter block size:\n"))
        N = int(input("Please enter number of ways:\n"))
        S = int(input("Please enter number of set:\n"))
        set_offset = int(math.log(S, 2))

    word_offset = int(math.log(b, 2))


def cache_simulate():
    global instructionsList
    global debugMode

    Instruction = instructionsList.copy()

    print("***************************Starting Cache Simulation********************************")
    print("\nSettings : \n")
    print("Enter 'a' for a directly-mapped cache, block size of 16 Bytes, a total of 4 blocks")
    print("Enter 'b' for a fully-associated cache, block size of 8 Bytes, a total of 8 blocks")
    print("Enter 'c' for a 2-way set-associative cache, block size of 8 Bytes, 4 sets")
    print("Enter 'd' for a 4-way set-associative cache, block size of 8 Bytes, 2 sets")
    print("Press any key for entering block size, number of ways and number of sets of choice")
    mode = input("Choose preset mode or self set mode:")


    choosemode(mode)
    print("Cache block size: " + str(b) + ' words')
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
    finished = False
    while not finished:
        DIC += 1
        fetch = Instruction[PC]
        x = fetch[0][0]
        # ********************************************************************************************************* Finish
        if (fetch[0:32] == '00010000000000001111111111111111'):
            print("PC =" + str(PC * 4) + " Instruction: Deadloop. Ending program")
            finished = True

        # ********************************************************************************************************* ADD
        elif (fetch[0][0] == "add"):  # ADD
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + str(asmCopy[PC]))
            PC += 1
            Register[int(fetch[1][0])] = Register[int(fetch[1][1])] + Register[int(fetch[1][2])]

        # ********************************************************************************************************* ADD
        elif (fetch[0][0] == "ori"):  # ori
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + str(asmCopy[PC]))
            PC += 1
            Register[int(fetch[1][0])] = int(fetch[1][2]) | Register[int(fetch[1][1])]

        # ********************************************************************************************************* ADD
        elif (fetch[0][0] == "sll"):  # sll
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + str(asmCopy[PC]))
            var = format(register[fetch[1][1]], '032b')

            PC += 1
            Register[int(fetch[1][0])] = int(fetch[1][2]) | Register[int(fetch[1][1])]

        # ********************************************************************************************************* SUB
        elif (fetch[0][0] == "sub"):  # SUB
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + str(asmCopy[PC]))
            PC += 1
            Register[int(fetch[1][0])] = Register[int(fetch[1][1])] - Register[int(fetch[1][2])]

        # ********************************************************************************************************* ADDI
        elif (fetch[0][0] == 'addi'):  # ADDI
            imm = int(fetch[1][2])
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + str(asmCopy[PC]))
            PC += 1
            Register[int(fetch[1][0])] = Register[int(fetch[1][1])] + imm

        # ********************************************************************************************************* BEQ
        elif (fetch[0][0] == 'beq'):  # BEQ
            imm = int(fetch[1][2])
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + str(asmCopy[PC]))
            PC += 1
            PC = PC + imm if (Register[int(fetch[1][0])] == Register[int(fetch[1][1])]) else PC

        # ********************************************************************************************************* BNE
        elif (fetch[0][0] == 'bne'):  # BNE
            imm = int(fetch[1][2])
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + str(asmCopy[PC]))
            PC += 1
            PC = PC + imm if Register[int(fetch[1][0])] != Register[int(fetch[1][1])] else PC

        # ********************************************************************************************************* SLT
        elif (fetch[0][0] == 'slt'):  # SLT
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + str(asmCopy[PC]))
            PC += 1
            Register[int(fetch[1][0])] = 1 if Register[int(fetch[1][1])] < Register[int(fetch[1][2])] else 0

        # ********************************************************************************************************* SLTU
        elif (fetch[0][0] == 'sltu'):  # SLTU
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + str(asmCopy[PC]))
            PC += 1
            Register[int(fetch[1][0])] = 1 if Register[int(fetch[1][1])] < Register[int(fetch[1][2])] else 0

        # ********************************************************************************************************* SW
        elif (fetch[0][0] == 'sw'):  # SW
            x = fetch[1][1].split('(')
            x[1] = x[1].replace(')',"")
            x[0] = "{0:08b}".format(int(x[0].replace('0x',""), 16)).zfill(16)
            fetch.append("101011" + intToBin(int(x[1]), 5) + intToBin(int(fetch[1][0]), 5) + x[0])

            # Sanity check for word-addressing
            if (int(fetch[2][30:32]) % 4 != 0):
                print("Runtime exception: fetch address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", str(asmCopy[PC]))
                exit()
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + str(asmCopy[PC]))
            PC += 1
            imm = int(fetch[2][16:32])
            index = int(fetch[2][32 - set_offset - 2:32 - 2], 2)
            Memory[imm + Register[int(fetch[2][6:11], 2)] - 8192] = Register[int(fetch[2][11:16], 2)]

            # TO-DO: CACHE-ACCESS
            
        # *********************************************************************************************************LW
        elif (fetch[0][0] == 'lw'):  # ********LOAD WORD********
            x = fetch[1][1].split('(')
            x[1] = x[1].replace(')',"")
            x[0] = "{0:08b}".format(int(x[0].replace('0x',""), 16)).zfill(16)
            fetch.append("101011" + intToBin(int(x[1]), 5) + intToBin(int(fetch[1][0]), 5) + x[0]) 
            # Sanity check for word-addressing
            if (int(fetch[2][30:32]) % 4 != 0):
                print("Runtime exception: fetch address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", str(asmCopy[PC]))
                exit()
            imm = int(fetch[2][16:32], 2)

            PC += 1
            # Cache access:
            # First check cache for any hit based on valid bit and index of cache
            address = format(imm + Register[int(fetch[2][6:11], 2)], "016b")  # The actual address load-word is accessing
            wordIndex = address[16 - 2 - word_offset:16 - 2]  # how many bits needed to index word in each blocks
            index = address[
                    16 - 2 - word_offset - set_offset:16 - 2 - word_offset]  # how many bits needed for set indexing
            if (debugMode):
                print("PC =" + str(PC * 4) + " Instruction:" + str(asmCopy[PC]))
                print("Address of loadword: ", address)
                print("Word offset", wordIndex)
                print("Set index", index)
            wordIndex = int(wordIndex, 2)
            index = int(index, 2)
            if (Valid[index] == 0):  # Cache miss
                Misses += 1
                for i in range(blk_size):
                    Cache[index][i] = Memory[
                        imm + Register[int(fetch[2][6:11], 2)] - 8192 + i * 4]  # Load memory into cache data
                Register[int(fetch[2][11:16], 2)] = Memory[
                    imm + Register[int(fetch[2][6:11], 2)] - 8192]  # Load data into register as well
                Valid[index] = 1  # Since we have cache miss, valid bit is now 1 after cache has updated value
                Tag[index] = address[0:16 - 2 - word_offset - set_offset]
                if (debugMode):
                    print("Cache missed due to valid bit = 0")
                    print("Tag = ", Tag[index])
                    print("Cache", Cache)
            else:  # Valid bit is 1, now check if tag matches
                if (Tag[index] == address[0:16 - 2 - word_offset - set_offset]):  # Cache hit

                    Register[int(fetch[2][11:16], 2)] = Cache[index][wordIndex]
                    Hits += 1
                    if (debugMode):
                        print("Cache hit")
                        print("Tag = ", Tag[index])
                        print("Cache", Cache)
                else:  # Tag doesnt match, cache miss
                    Misses += 1
                    for i in range(blk_size):
                        Cache[index][i] = Memory[
                            imm + Register[int(fetch[2][6:11], 2)] - 8192 + i * 4]  # Load memory into cache data
                    Register[int(fetch[2][11:16], 2)] = Memory[
                        imm + Register[int(fetch[2][6:11], 2)] - 8192]  # Load cache data into register
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
# FUNCTION: Takes int and return bin
def intToBin(intNum, bits):
    s = bin(intNum & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Takes hex and return int
def ConvertHexToInt(_line):
    i = ""
    for item in _line:
        if "0x" in item:
            ind = _line.index(item)
            if "(" in item:
                i = item.find("(")
                i = item[i:]
                item = item.replace(i,"")
            item = str(int(item, 0))
            item = item + i
            _line[ind]=item
            
    return _line

# -------------------------------------------------------------------------------------------------------------------- #
#---- FUNCTION: function read in asm file and returns it as a list
def insertMipsFile():
    global asmCopy
    I_file = open(SelectFile("prog.asm"),"r")

    Instruction = []    # array containing all instructions to execute         

    for line in I_file:
        if (line == "\n" or line[0] =='#'):              # empty lines,comments ignored
            continue
        line = line.replace('\n','')
        line = line.replace(' ','')
        asmCopy.append(line)
        line = line.split('$',1)
        for item in line:
            ind = line.index(item)
            item = item.replace('$','')
            line[ind] = item.split(',')
        
        Instruction.append(line)

    return Instruction
            
def main():

    global instructionsList
    global debugMode

    ## Keeps loop until user hits Exit.
    while True:

        print("Choose what you’d like to do (1, 2, or 3): ", "1: Processor Simulation of MC ","2: Processor Simulation of AP ","3: Data Cache Simulator ","4: Exit", sep="\n\n")
        
        while True:
            Input = input()
            ## Input validater 
            if Input != '1' and Input != '2' and Input != '3' and Input != '4' :
                print("\n\nEnter a valid input!!! -_-\n\n")
            else:
                break

        menu = int(Input)

        ## -------------------------------------------------------------------------------------------------------------------- #
        ## Test Vector Generation Part 1
        if menu == 1:
            ## Debug mode or normal mode
            print("\nWould you like to run simulator in debug mode ?")
            debugMode =True if  int(input("\n1: debug mode \n\n2: normal execution\n")) == 1 else False
            instructionsList = insertMipsFile()
            simMC()
            
         
        ## -------------------------------------------------------------------------------------------------------------------- #
        ## Fault Coverage Simulation Part 2
        elif menu == 2:
            ## Debug mode or normal mode
            print("\nWould you like to run simulator in debug mode ?")
            debugMode =True if  int(input("\n1: debug mode \n\n2: normal execution\n")) == 1 else False
            instructionsList = insertMipsFile()
            simAP()
            
        ## -------------------------------------------------------------------------------------------------------------------- #
        ##  Avg Fault Coverage data generation Part 3
        elif menu == 3:
            ## Debug mode or normal mode
            print("\nWould you like to run simulator in debug mode ?")
            debugMode =True if  int(input("\n1: debug mode \n\n2: normal execution\n")) == 1 else False
            instructionsList = insertMipsFile()
            cache_simulate()

        
        ## -------------------------------------------------------------------------------------------------------------------- #
        ##  Exit 
        elif menu == 4:
            break

        else:
            print("\n\nEnter a valid input!!! -_- \n\n")



if __name__ == "__main__":
    main()
