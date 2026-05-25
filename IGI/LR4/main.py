import sys
import Task1 as t1
import Task2 as t2
import Task3 as t3
import Task4 as t4
import Task5 as t5
import Task6 as t6

def run_program():
    while True:
        print("\nSelect:")
        print("1. Task 1")
        print("2. Task 2")
        print("3. Task 3")
        print("4. Task 4")
        print("5. Task 5")
        print("6. Task 6")
   
        print("0. Exit")
        
        while True:
            try:
                choice = int(input("Enter clause: "))
                if choice < 0 or choice > 6:
                    print("Error: integer from 0 to 5 required")
                    continue
                break
            except ValueError:
                print("Error: integer required")
        print("")

        try:
            match choice:
                case 1:
                    t1.task_1()
                
                case 2:
                    t2.task_2("T2\\init.txt","T2\\res.txt","T2\\archive.zip")
                    
                case 3:
                    t3.task_3(0.17, 6, "T3\\graph.png")

                case 4:
                    t4.task_4("T4\\trapezoid.png")

                case 5:
                    t5.task_5(4,6)

                case 6:
                    t6.task_6()

                case 0:
                    break

                case _:
                    print("Unknown command.")
                
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_program()
