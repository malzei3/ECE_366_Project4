import os
import math
import copy

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

debugMode = False
instructionsList = []
asmCopy = []

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
        if PC == (len(instructionsList)-1):
            finished = True
        # ********************************************************************************************************* Finish
        #if (fetch[0:32] == '00010000000000001111111111111111'):
        #   print("PC =" + str(PC * 4) + " Instruction: Deadloop. Ending program")
        #   finished = True

        # ********************************************************************************************************* ADD
        if (fetch[0][0] == "add"):  # ADD
            PC += 1
            Register[int(fetch[1][0])] = Register[int(fetch[1][1])] + Register[int(fetch[1][2])]
            if (debugMode):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, Cache)

        # ********************************************************************************************************* ADD
        elif (fetch[0][0] == "addu"):  # ADDU
            PC += 1
            Register[int(fetch[1][0])] = abs(Register[int(fetch[1][1])]) + abs(Register[int(fetch[1][2])])
            if (debugMode):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, Cache)

        # ********************************************************************************************************* ori
        elif (fetch[0][0] == "ori"):  # ori
            PC += 1
            Register[int(fetch[1][0])] = int(fetch[1][2]) | Register[int(fetch[1][1])]
            if (debugMode):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, Cache)

        # ********************************************************************************************************* xor
        elif (fetch[0][0] == "xor"):  # xor
            PC += 1
            var = int(bin(int(fetch[1][1])).replace("0b","")) ^ int(bin(int(fetch[1][1])).replace("0b",""))
            Register[int(fetch[1][0])] = var
            if (debugMode):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, Cache)


        # ********************************************************************************************************* sll
        elif (fetch[0][0] == "sll"):  # sll
            PC += 1
            var1 = Register[int(fetch[1][1])]
            var2 = int(fetch[1][2])
            Register[int(fetch[1][0])] = (var1 <<  var2) & (0xFFFFFFFF)
            if (debugMode):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, Cache)

        # ********************************************************************************************************* SUB
        elif (fetch[0][0] == "sub"):  # SUB
            PC += 1
            Register[int(fetch[1][0])] = Register[int(fetch[1][1])] - Register[int(fetch[1][2])]
            if (debugMode):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, Cache)

        # ********************************************************************************************************* ADDI
        elif (fetch[0][0] == 'addi'):  # ADDI
            imm = int(fetch[1][2])
            PC += 1
            Register[int(fetch[1][0])] = Register[int(fetch[1][1])] + imm
            if (debugMode):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, Cache)

        # ********************************************************************************************************* BEQ
        elif (fetch[0][0] == 'beq'):  # BEQ
            imm = int(fetch[1][2])
            PC += 1
            PC = PC + imm if (Register[int(fetch[1][0])] == Register[int(fetch[1][1])]) else PC
            if (debugMode):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, Cache)

        # ********************************************************************************************************* BNE
        elif (fetch[0][0] == 'bne'):  # BNE
            imm = int(fetch[1][2])
            PC += 1
            PC = PC + imm if Register[int(fetch[1][0])] != Register[int(fetch[1][1])] else PC
            if (debugMode):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, Cache)

        # ********************************************************************************************************* SLT
        elif (fetch[0][0] == 'slt'):  # SLT
            PC += 1
            Register[int(fetch[1][0])] = 1 if Register[int(fetch[1][1])] < Register[int(fetch[1][2])] else 0
            if (debugMode):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, Cache)

        # ********************************************************************************************************* SLTU
        elif (fetch[0][0] == 'sltu'):  # SLTU
            PC += 1
            Register[int(fetch[1][0])] = 1 if Register[int(fetch[1][1])] < Register[int(fetch[1][2])] else 0
            if (debugMode):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, Cache)

        # ********************************************************************************************************* SW
        elif (fetch[0][0] == 'sw'):  # SW
            line = convertAsmToBin(fetch)
            # Sanity check for word-addressing
            if (int(line[30:32]) % 4 != 0):
                print("Runtime exception: fetch address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", str(asmCopy[PC]))
                exit()
            PC += 1
            imm = int(line[16:32], 2)
            index = int(line[32 - set_offset - 2:32 - 2], 2)
            Memory[imm + Register[int(line[6:11], 2)] - 8192] = Register[int(line[11:16], 2)]
            address = format(imm + Register[int(line[6:11], 2)], "016b")  # The actual address load-word is accessing
            wordIndex = address[16 - 2 - word_offset:16 - 2]  # how many bits needed to index word in each blocks

            if (debugMode):
                print("Address of Store Word: ", address)
                print("Word offset", wordIndex)
                print("Set index", index)
                input()

            if (Valid[index] == 0):  # Cache miss
                Misses += 1
                Valid[index] = 1  # Since we have cache miss, valid bit is now 1 after cache has updated value
                Tag[index] = address[0:16 - 2 - word_offset - set_offset]
                Cache[index][int(wordIndex, 2)] = Register[int(line[11:16], 2)] 

                if (debugMode):
                    print("Cache missed due to valid bit = 0")
                    print("Tag = ", Tag[index])
                    print("Cache", Cache)
                    input()
            else:
                if (Tag[index] == address[0:16 - 2 - word_offset - set_offset]):  # Cache hit
                    Hits += 1
                    if (debugMode):
                        print("Cache hit")
                        print("Tag = ", Tag[index])
                        print("Cache", Cache)
                        input()

            if (debugMode):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, Cache)

            # TO-DO: CACHE-ACCESS
            
        # *********************************************************************************************************LW
        elif (fetch[0][0] == 'lw'):  # ********LOAD WORD********
            line = convertAsmToBin(fetch)
            # Sanity check for word-addressing
            if (int(line[30:32]) % 4 != 0):
                print("Runtime exception: fetch address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", str(asmCopy[PC]))
                exit()

            imm = int(line[16:32], 2)
            PC += 1

            #Cache access:
            #First check cache for any hit based on valid bit and index of cache
            address = format(imm + Register[int(line[6:11], 2)], "016b")  # The actual address load-word is accessing
            wordIndex = address[16 - 2 - word_offset:16 - 2]  # how many bits needed to index word in each blocks
            index = address[16 - 2 - word_offset - set_offset:16 - 2 - word_offset]  # how many bits needed for set indexing

            if (debugMode):
                print("Address of loadword: ", address)
                print("Word offset", wordIndex)
                print("Set index", index)
                input()

            wordIndex = int(wordIndex, 2)
            index = int(index, 2)

            if (Valid[index] == 0):  # Cache miss
                Misses += 1
                for i in range(blk_size):
                    Cache[index][i] = Memory[
                        imm + Register[int(line[6:11], 2)] - 8192 + i * 4]  # Load memory into cache data

                Register[int(line[11:16], 2)] = Memory[imm + Register[int(line[6:11], 2)] - 8192]  # Load data into register as well
                Valid[index] = 1  # Since we have cache miss, valid bit is now 1 after cache has updated value
                Tag[index] = address[0:16 - 2 - word_offset - set_offset]
                Cache[index][wordIndex] = Register[int(line[11:16], 2)]

                if (debugMode):
                    print("Cache missed due to valid bit = 0")
                    print("Tag = ", Tag[index])
                    print("Cache", Cache)
                    input()

            else:  # Valid bit is 1, now check if tag matches
                if (Tag[index] == address[0:16 - 2 - word_offset - set_offset]):  # Cache hit

                    Register[int(line[11:16], 2)] = Cache[index][wordIndex]
                    Hits += 1
                    if (debugMode):
                        print("Cache hit")
                        print("Tag = ", Tag[index])
                        print("Cache", Cache)
                        input()


                else:  # Tag doesnt match, cache miss
                    Misses += 1
                    for i in range(blk_size):
                        Cache[index][i] = Memory[imm + Register[int(fetch[2][6:11], 2)] - 8192 + i * 4]  # Load memory into cache data

                    Register[int(line[11:16], 2)] = Memory[imm + Register[int(line[6:11], 2)] - 8192]  # Load cache data into register
                    Tag[index] = address[0:16 - 2 - word_offset - set_offset]  # Update tag
                    if (debugMode):
                        print("Cache missed due to tag mismatch")
                        print("Tag = ", Tag[index])
                        print("Cache", Cache)
                        input()

            if (debugMode):
                printInfo(Register, DIC, PC, Memory, Misses, Hits, Cache)

    print("***Finished simulation***")
    print("Dynamic instructions count: " + str(DIC))
    print("Cache misses:" + str(Misses))
    print("Cache hits:" + str(Hits))
    print("Cache Hit Rate:" + str(100 * (float(Hits) / float(Hits + Misses))))
    print("Registers: " + str(Register))
    print("Cache data: " + str(Cache))

# -------------------------------------------------------------------------------------------------------------------- #
# ---- FUNCTION: Prints the registers information when the debug mode is on.
def printInfo(_register, _DIC, _PC,_Mem,_Misses,_Hits,_Cache):
    print('\n************** Instruction Number ' + str(_PC) + '. ' + asmCopy[_PC-1] + ' : **************\n')
    print('Registers $0 - $23: \n', _register)
    print('Memory 8192 - 8242: \n', _Mem[0:49])
    print('\nDinstructions count: ', _DIC)
    print('PC = ', _PC*4)
    print("\n***Cache Info***")
    print("Cache misses:" + str(_Misses))
    print("Cache hits:" + str(_Hits))
    if(_Hits + _Misses == 0):
        print("Cache Hit Rate:" + str(0))
    else:
        print("Cache Hit Rate:" + str(100 * (float(_Hits) / float(_Hits + _Misses))))
    print("Cache data: " + str(_Cache))
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
# FUNCTION: Takes int and return bin
def intToBin(intNum, bits):
    s = bin(intNum & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)

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
        
        if(line[0][0] == 'lw' or line[0][0] == 'sw'):
            line[1][1] = CheckandConvertHexToInt(line[1][1])
        else:
            line[1][2] = str(CheckandConvertHexToInt(line[1][2]))
        Instruction.append(line)

    return Instruction
            
# -------------------------------------------------------------------------------------------------------------------- #
#---- FUNCTION: Main
def main():

    global instructionsList
    global debugMode

    ## Keeps loop until user hits Exit.
    while True:

        print("\nChoose what you’d like to do (1, 2, or 3): ", "1: Processor Simulation of MC ","2: Processor Simulation of AP ","3: Data Cache Simulator ","4: Exit", sep="\n\n")
        
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
