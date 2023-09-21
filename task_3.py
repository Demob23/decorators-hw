import os
from time import strftime, gmtime
import types


def logger(path):

    def __logger(old_function):
        def log(func, *args, **kwargs):
            with open(f'{path}', mode='a', encoding='utf-8') as file:
                execution_time = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
                file.write(f"Exec time UTC: {execution_time};\n"
                           f"Name of function: {old_function.__name__};\n"
                           f"Call arguments: {args}, {kwargs};\n"
                           f"Function call data: {func(*args, **kwargs)};\n")

        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            log(old_function, *args, **kwargs)
            return result

        return new_function

    return __logger


def create_cook_book():
    cook_book = {}
    with open("recipes.txt", "r", encoding="utf-8") as f:
        recipes = f.read().split('\n')
        for line in recipes:
            if "|" not in line and not line.isdigit() and line != '':
                cook_book[line] = []
                current_dish = line
            if "|" in line:
                ingredient_attributes = line.split("|")
                cook_book[current_dish].append({"ingredient_name": f"{ingredient_attributes[0].strip()}",
                                           "quantity": f"{ingredient_attributes[1].strip()}",
                                           "measure": f"{ingredient_attributes[2].strip()}"})
    return cook_book


def get_shop_list_by_dishes(dishes:list, person_count:int):
    cook_book = create_cook_book()
    shop_list = {}
    for dish in dishes:
        if dish not in cook_book:
            print(f"Блюда {dish} нет в книге рецептов.")
            dishes.remove(dish)
    for dish in dishes:
        for ingredient in cook_book[dish]:
            if ingredient["ingredient_name"] in list(shop_list.keys()):
                for_another_dishes = shop_list[ingredient["ingredient_name"]]["quantity"]
                need_to_add = int(ingredient["quantity"]) * person_count
                shop_list[ingredient["ingredient_name"]].update({"quantity": for_another_dishes + need_to_add})
            else:
                shop_list[ingredient["ingredient_name"]] = {"measure": f"{ingredient['measure']}",
                                                            "quantity": int(ingredient["quantity"]) * person_count}
    return shop_list


@logger(path='log_4.log')
def print_shop_list(shop_list):
    print("Список покупок:")
    for ingredient in shop_list:
        print(f"{ingredient} - {shop_list[ingredient]['quantity']} {shop_list[ingredient]['measure']}")



def sort_txt_files_by_length():
    file_length = {}
    for filename in os.listdir("task 3 files"):
        with open(f"task 3 files\\{filename}", 'r', encoding='utf-8') as file:
            file_length[f'{filename}'] = len(file.read().split("\n"))

    sorted_by_length = sorted(file_length.items(), key=lambda item:item[1])
    for file_tuple in sorted_by_length:
        with open(f"task 3 files\\{file_tuple[0]}", 'r', encoding="utf-8") as f:
            print(f"Имя файла: {file_tuple[0]}")
            print(f"Количество строк: {file_tuple[1]}")
            print(f.read())


shop_list = get_shop_list_by_dishes(["Омлет", "Запеканка"], 2)
print_shop_list(shop_list)
sort_txt_files_by_length()
