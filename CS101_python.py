# Balls to Fit a Plane: A Standardized Solution

# Version 1.0

    # for changelog, see changelog file.

    # if ever this code is improved, it will reflect in the changelog.

# About:

    # A standardized solution for the famous question, "How many balls can fit in a plane?"

    # A standardized solution; meaning, it is up to the user's input to define the plane and the ball's model
    # and dimensions.

    # Application of CS101 topics are applied, such as OOP and linear data structures.


# ------ code begins here ------ #

# easy code content traversal:

    # 5 hyphens (<space>-----<space>) - subject macro-seperator

    # 4 hyphens (<space>----<space>) - subject micro-seperator

import time
import sys

# ----- indexing ----- #

    # - stores 5 of the latest final calculations and their respective plane and ball names.

calculation_history = []

# ----- user input ----- #

def get_user_input_plane():
    input_list_plane = []

    # ---- input: plane name ---- #
    input_1 = str(input("Set Plane name: ") or "User Standard Plane")
    input_list_plane.append(input_1)

    # ---- input: plane length ---- #
    input_2 = float(input("Set Plane length: ") or 1.0)

    # ---- below zero barrier ---- #
    while input_2 <= 0:
        print("Please choose a value above zero.")
        input_2 = float(input("Set Plane length: ") or 1.0)

    input_list_plane.append(input_2)

    # ---- input: plane width ---- #
    input_3 = float(input("Set Plane width: ") or 1.0)

    # ---- below zero barrier ---- #
    while input_3 <= 0:
        print("Please choose a value above zero.")
        input_3 = float(input("Set Plane width: ") or 1.0)

    input_list_plane.append(input_3)

    # ---- input: plane height ---- #
    input_4 = float(input("Set Plane height: ") or 1.0)

    # ---- below zero barrier ---- #
    while input_4 <= 0:
        print("Please choose a value above zero.")
        input_4 = float(input("Set Plane height: ") or 1.0)

    input_list_plane.append(input_4)

    print()

    return input_list_plane

def get_user_input_ball():
    input_list_ball = []

    # ---- input: ball name ---- #
    input_1 = str(input("Set Ball name: ") or "User Standard Ball")
    input_list_ball.append(input_1)
    
    ball_uniformity = str(input("Does the ball have uniform dimensions? Y/N: ") or "N")

    if ball_uniformity.upper() == "Y":
        # ---- input: ball length ---- #
        input_d = float(input("Set Ball diameter: ") or 1.0)

        # ---- below zero barrier ---- #
        while input_d <= 0:
            print("Please choose a value above zero.")
            input_d = float(input("Set Ball diameter: ") or 1.0)

        input_list_ball.append(input_d)
        input_list_ball.append(input_d)
        input_list_ball.append(input_d)

    elif ball_uniformity.upper() != "Y":
        # ---- input: ball length ---- #
        input_2 = float(input("Set Ball length: ") or 1.0)

        # ---- below zero barrier ---- #
        while input_2 <= 0:
            print("Please choose a value above zero.")
            input_2 = float(input("Set Ball length: ") or 1.0)

        input_list_ball.append(input_2)

        # ---- input: ball width ---- #
        input_3 = float(input("Set Ball width: ") or 1.0)

        # ---- below zero barrier ---- #
        while input_3 <= 0:
            print("Please choose a value above zero.")
            input_3 = float(input("Set Ball width: ") or 1.0)

        input_list_ball.append(input_3)

        # ---- input: ball height ---- #
        input_4 = float(input("Set Ball height: ") or 1.0)

        # ---- below zero barrier ---- #
        while input_4 <= 0:
            print("Please choose a value above zero.")
            input_4 = float(input("Set Ball height: ") or 1.0)

        input_list_ball.append(input_4)

    print()

    return input_list_ball

# ----- plane dimensions ----- #

    # - its shape, by default, is defined as a cylinder cut in half along its height.
        # - excludes wings and tail

    # - took into account the plane not having a uniform radius.

def set_and_calculate_plane_dimensions(input_list_plane):
    plane_name = input_list_plane[0]
    plane_length = input_list_plane[1] 
    plane_radius_1 = input_list_plane[2] / 2 # width (diameter) / 2
    plane_radius_2 = input_list_plane[3] # height = radius2

    # ---- calculating for plane volume ---- #
    plane_volume = (3.14 / 2) * plane_radius_1 * plane_radius_2 * plane_length
    # Volume of half cylinder = [(pi)(r1)(r2)(length)] / 2

    # ---- standardized plane description ---- #
    print(\
        f"Plane: {input_list_plane[0]}" + "\n"
        f"Plane Dimensions:" + "\n"
        f"  Length: {input_list_plane[1]}" + "\n"
        f"  Width: {input_list_plane[2]}" + "\n"
        f"  Height: {input_list_plane[3]}" + "\n"
    )

    return plane_name, plane_volume

# ----- ball dimensions ----- #

    # - took into account the ball not having a uniform radius.

def set_and_calculate_ball_dimensions(input_list_ball):
    ball_name = input_list_ball[0]
    ball_radius_1 = input_list_ball[1] / 2 # \
    ball_radius_2 = input_list_ball[2] / 2 #  } = diameters
    ball_radius_3 = input_list_ball[3] / 2 # /

    # ---- calculating for ball volume ---- #
    ball_volume = ((4 / 3) * 3.14) * ball_radius_1 * ball_radius_2 * ball_radius_3 
    # V = (4 / 3)(r1)(r2)(r3)

    # ---- standardized ball description ---- #
    print(\
        f"Ball: {input_list_ball[0]}" + "\n"
        f"Ball Dimensions:" + "\n"
        f"  Length: {input_list_ball[1]}" + "\n"
        f"  Width: {input_list_ball[2]}" + "\n"
        f"  Height: {input_list_ball[3]}" + "\n"
    )

    return ball_name, ball_volume

# ----- plane + ball calculations ----- #

def calculate_final(plane_name, plane_volume, ball_name, ball_volume):

    # ---- fancy loading text + logic ---- #
    sys.stdout.write("Calculating")
    for each_x in range(5):
        time.sleep(1)
        sys.stdout.write(".")
        sys.stdout.flush()

    print()

    # ---- math logic before final calculations ---- #
    if ball_volume > plane_volume:
        print(
            f"The {ball_name} is too big, it can't be stuffed into the {plane_name}!"
        )

    # ---- final calculations ---- #
    else:
        total_ball_count = int(plane_volume/ball_volume)

        # ---- final calculation description ---- #
        if total_ball_count == 1:
            print(\
                f"A maximum of {total_ball_count} {ball_name.lower()} can be stuffed in the {plane_name}!" + "\n"
            )

            # ---- checker for index array not to extend beyond 5: 1 ball case---- #
            if len(calculation_history) == 5:
                calculation_history.pop(0)
                calculation_history.append([plane_name, ball_name, (str(total_ball_count) + " ball")])

            # ---- index to array: 1 ball case ---- #
            else:
                calculation_history.append([plane_name, ball_name, (str(total_ball_count) + " ball")])

        else:
            print(\
                f"A maximum of {total_ball_count} {ball_name.lower()}s can be stuffed in the {plane_name}!" + "\n"
            )
    
            # ---- checker for index array not to extend beyond 5 ---- #
            if len(calculation_history) == 5:
                calculation_history.pop(0)
                calculation_history.append([plane_name, ball_name, (str(total_ball_count) + " balls")])

            # ---- index to array ---- #
            else:
                calculation_history.append([plane_name, ball_name, (str(total_ball_count) + " balls")])

# ------ testing and debugging ------ #

# ----- program intro ----- #

dialogue = input(
    "Balls to Fit a Plane: Standardized Edition" + "\n\n"

    "This code seeks to answer the popular question: \"How many (description)balls can fit into a" + "\n"
    "(description)plane?\"" + "\n\n"

    "This code has been standardized; meaning, it's up to you, the user, to create or to standardize" + "\n"
    "your own measurements for both the plane and the ball." + "\n\n"

    "Press any key to continue." + "\n"
)

# ---- restart start loop ---- #
restart = 0

while restart != "x":

    test_user_input_plane = get_user_input_plane()
    test_user_input_ball = get_user_input_ball()

    # ---- timer start plug for literal runtime ---- #
    start_time = time.time()

    test_plane = set_and_calculate_plane_dimensions(test_user_input_plane)
    test_ball = set_and_calculate_ball_dimensions(test_user_input_ball)

    test_calculate = calculate_final(test_plane[0], test_plane[1], test_ball[0], test_ball[1])

    # ---- timer end plug for literal runtime ---- #
    print(
        "RUNTIME:" + "\n"
        f"--- {time.time() - start_time} seconds ---" + "\n"
    )

    # ---- history array plug ---- #
    print(
        "HISTORY:" + "\n"
        f"{calculation_history}" + "\n"
    )

    # ---- restart end loop ---- #
    restart = input("Press any key to restart, or type \"x\" to exit the program.")