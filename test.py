

             
def print_something(Name, Surname, Color_index, Int1, Int2, Bool):
    try:

        print("hello, " + Name + ' ' + Surname)

        result = Int1 + Int2
        print(str(Int1)+ ' + ' + str(Int2) + ' = ' + str(result)) 

        available_colors = ["blue", "green", "yellow", "black"]
        print("You have chosen the color " + available_colors[Color_index])

        if Bool: print("boolean variable is selected")
        else: print("boolean variable is unselected")

    except Exception as e: 
        print("Some errors occurred!")
        print(e)



