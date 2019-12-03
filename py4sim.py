import os
import math

debugMode = False
instructionsList = []

# -------------------------------------------------------------------------------------------------------------------- #
# FUNCTION: Mc Simulation.
def simMC():
    print("\n\nOption 1: Processor Simulation of MC\n\n")


def simAP():
    print("\n\nOption 2: Processor Simulation of AP\n\n")


def cacheSim():
    print("\n\nOption 3: Data Cache Simulator\n\n")


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
#---- FUNCTION: function read in asm file and returns it as a list
def insertMipsFile():

    I_file = open(SelectFile("prog.asm"),"r")

    Instruction = []    # array containing all instructions to execute         
    InstructionHex = []

    for line in I_file:
        if (line == "\n" or line[0] =='#'):              # empty lines,comments ignored
            continue
        line = line.replace('\n','')
        InstructionHex.append(line)
        line = format(int(line,16),"032b")
        Instruction.append(line)
        
    return Instruction
            

def main():

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

        ## Debug mode or normal mode
        print("\nWould you like to run simulator in debug mode ?")
        debugMode =True if  int(input("\n1: debug mode \n\n2: normal execution\n")) == 1 else False

        instructionsList = insertMipsFile()

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
            cacheSim()

        
        ## -------------------------------------------------------------------------------------------------------------------- #
        ##  Exit 
        elif menu == 4:
            break

        else:
            print("\n\nEnter a valid input!!! -_- \n\n")



if __name__ == "__main__":
    main()
