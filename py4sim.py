
import math



def simMC():
    print("\n\nOption 1: Processor Simulation of MC\n\n")


def simAP():
    print("\n\nOption 2: Processor Simulation of AP\n\n")


def cacheSim():
    print("\n\nOption 3: Data Cache Simulator\n\n")



def main():

    ## Keeps loop until user hits Exit.
    while True:

        print("Choose what you’d like to do (1, 2, or 3): ", "1: Processor Simulation of MC ","2: Processor Simulation of AP ","3: Data Cache Simulator ","4: Exit", sep="\n\n")
        
        while True:
            Input = input()
            ## Input validater 
            if Input != '1' and Input != '2' and Input != '3' and Input != '4' :
                print("\n\nPlease Enter a valid input!!!\n\n")
            else:
                break


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
            print("\n\nPlease Enter a valid input!!!\n\n")



if __name__ == "__main__":
    main()
