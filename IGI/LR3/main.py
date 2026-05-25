import sys
import task_1 as t1
import task_2 as t2
import task_3 as t3
import task_4 as t4
import task_5 as t5
import list_initialization as list_init

def run_program():
    while True:
        print("\nSelect:")
        print("1. Task 1")
        print("2. Task 2")
        print("3. Task 3")
        print("4. Task 4")
        print("5. Task 5")
   
        print("0. Exit")
        
        while True:
            try:
                choice = int(input("Enter clause: "))
                if choice < 0 or choice > 5:
                    print("Error: integer from 0 to 5 required")
                    continue
                break
            except ValueError:
                print("Error: integer required")
        print("")

        try:
            match choice:
                case 1:
                    x, eps = t1.get_user_input()
                    t1.calculate_series(x, eps)
                
                case 2:
                    print("Enter numbers. Finish with zero.")
                    nums = t2.get_int_sequence()

                    count = t2.count_in_range(nums)
                    print(f"Count of numbers between 5 and 25: {count}")
                    
                case 3:
                    string = input("Enter the string: ")

                    res = t3.analyze_text_symbols(string)
                    print(f"Spaces: {res[0]}\tApostrophes: {res[1]}")

                case 4:
                    string = "So she was considering in her own mind, " \
                    "as well as she could, for the hot day made her feel very sleepy and stupid," \
                    " whether the pleasure of making a daisy-chain would be worth" \
                    " the trouble of getting up and picking the daisies," \
                    " when suddenly a White Rabbit with pink eyes ran close by her"

                    words = t4.get_clean_words(string)

                    print(f"Words count with len < 6: {t4.count_small_words(words)}")
                    short_w = t4.find_shortest_w_word(words)
                    print(f"The shortest word ending with \"w\": {"No words" if short_w == None else short_w}")
                    print(f"Sorted list of words: {t4.sort_words_by_length(words)}")

                case 5:
                    while True:
                        try:
                            method = int(input("Enter initialization method:\n1. Manual\n2. Generator\n"))
                            if method <= 0 or method > 2:
                                print("Error: integer 1 or 2 required")
                                continue
                            break
                        except ValueError:
                            print("Error: integer required")
                    
                    list = []

                    if method == 1:
                        list = list_init.init_from_user()
                    else:
                        for value in list_init.init_with_generator():
                            list.append(value)

                    print(f"List: {list}")
                    print(f"Product of negatives: {t5.product_of_negatives(list)}")
                    print(f"Sum of positives before absolute maximum: {t5.sum_positives_before_max_abs(list)}")

                case 0:
                    break

                case _:
                    print("Unknown command.")
                
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_program()
