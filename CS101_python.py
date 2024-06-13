# Balls to Fit an Airplane: A Standardized Solution

# Version 1.1
    # v1.1: polished the code, and added adjustments to the comments and descriptions.

    # FOR FUTURE VERSION(S): better logic barriers (ex. when a string is inputted when a number value is expected),
    #                        more compact, more polished, optimized code

# About:
    # A standardized solution for the famous coding exercise in tech interviews, "How many balls can fit into an airplane?"

    # A standardized solution; meaning, it is up to the user's input to define the plane and the ball's model and dimensions.

    # Application of CS101 topics are applied, such as OOP and linear data structures.


# ------ code begins here ------ #

# easy code content traversal:
    # 5 hyphens (<space>-----<space>) - subject macro-seperator

    # 4 hyphens (<space>----<space>) - subject micro-seperator

import time
import sys

# ----- indexing ----- #
    # stores 5 of the latest final calculations and their respective plane and ball names.

calculation_history = []

# ----- user inputs ----- #

def get_user_input_plane():
    input_list_plane = []

    # ---- input: plane name ---- #
    input_1 = str(input(
      "\nSet an airplane model name, or create your own. The default airplane model is a Boeing 737.\n\
Set Airplane Name: ") or "Boeing 737")
    
    input_list_plane.append(input_1)

    # ---- input: plane cabin length ---- #
    input_2 = float(input(
      "\nSet the airplane cabin length. The default length is 33.93m.\n\
Set Airplane Cabin Length: ") or 33.93)

    # ---- below zero barrier ---- #
    while input_2 <= 0:
        print("\nPlease choose a value above zero.")
        input_2 = float(input("Set Airplane Cabin Length: ") or 33.93)

    input_list_plane.append(input_2)

    # ---- input: plane cabin width ---- #
    input_3 = float(input(
      "\nSet the airplane cabin width. The default width is 3.56m.\n\
Set Airplane Cabin Width: ") or 3.56)

    # ---- below zero barrier ---- #
    while input_3 <= 0:
        print("\nPlease choose a value above zero.")
        input_3 = float(input("Set Airplane Cabin Width: ") or 3.56)

    input_list_plane.append(input_3)

    # ---- input: plane height ---- #
    input_4 = float(input(
      "\nSet the airplane cabin height. The default height is 4.27m.\n\
Set Airplane Cabin Height: ") or 4.27)

    # ---- below zero barrier ---- #
    while input_4 <= 0:
        print("\nPlease choose a value above zero.")
        input_4 = float(input("Set Airplane Cabin Height: ") or 4.27)

    input_list_plane.append(input_4)

    return input_list_plane

def get_user_input_ball():
    input_list_ball = []

    # ---- input: ball name ---- #
    input_1 = str(input(
      "\nSet a ball model name, or create your own. The default ball model is a basketball.\n\
Set Ball Name: ") or "Basketball")
    
    input_list_ball.append(input_1)
    
    ball_uniformity = str(input(
      "\nDoes the ball have uniform dimensions? The default is Y.\n\
Y/N: ") or "Y")

    if ball_uniformity.upper() == "Y":
        # ---- input: ball length ---- #
        input_d = float(input("\nSet Ball Diameter: ") or 0.241)

        # ---- below zero barrier ---- #
        while input_d <= 0:
            print("\nPlease choose a value above zero.")
            input_d = float(input("Set Ball Diameter: ") or 0.241)

        input_list_ball.append(input_d)
        input_list_ball.append(input_d)
        input_list_ball.append(input_d)

    elif ball_uniformity.upper() != "Y":
      
        # ---- input: ball length ---- #
        input_2 = float(input("\nSet Ball Length: ") or 1.0)

        # ---- below zero barrier ---- #
        while input_2 <= 0:
            print("\nPlease choose a value above zero.")
            input_2 = float(input("Set Ball Length: ") or 1.0)

        input_list_ball.append(input_2)

        # ---- input: ball width ---- #
        input_3 = float(input("\nSet Ball Width: ") or 1.0)

        # ---- below zero barrier ---- #
        while input_3 <= 0:
            print("\nPlease choose a value above zero.")
            input_3 = float(input("Set Ball Width: ") or 1.0)

        input_list_ball.append(input_3)

        # ---- input: ball height ---- #
        input_4 = float(input("\nSet Ball Height: ") or 1.0)

        # ---- below zero barrier ---- #
        while input_4 <= 0:
            print("\nPlease choose a value above zero.")
            input_4 = float(input("Set Ball Height: ") or 1.0)

        input_list_ball.append(input_4)

    return input_list_ball

# ----- setting and calculating plane cabin dimensions ----- #

    # - its shape, by default, is defined as a cylinder cut in half along its height.
        # - excludes wings and tail

    # - took into account the plane not having a uniform radius.

def set_and_calculate_plane_dimensions(input_list_plane):
    plane_name = input_list_plane[0]
    plane_length = input_list_plane[1] 
    plane_r1 = input_list_plane[2] / 2 # width
    plane_r2 = input_list_plane[3] / 2 # height

    # ---- calculating for plane volume ---- #
    plane_volume = (3.14 / 2) * plane_length * (plane_r1) * (plane_r2)
      # Volume of half cylinder = [(pi)(r1)(r2)(h)] / 2
      # - r1 = w/2, and r2 = h/2

    # ---- standardized plane description ---- #
    print(
        f"\nPlane: {input_list_plane[0]}" + "\n"
        f"Plane Cabin Dimensions:" + "\n"
        f"  Cabin Length: {input_list_plane[1]}" + "\n"
        f"  Cabin Width: {input_list_plane[2]}" + "\n"
        f"  Cabin Height: {input_list_plane[3]}"
    )

    return plane_name, plane_volume

# ----- ball dimensions ----- #

    # - took into account the ball not having a uniform radius.

def set_and_calculate_ball_dimensions(input_list_ball):
    ball_name = input_list_ball[0]
    ball_radius_1 = input_list_ball[1] / 2 # \
    ball_radius_2 = input_list_ball[2] / 2 #  } radii = diameters / 2
    ball_radius_3 = input_list_ball[3] / 2 # /

    # ---- calculating for ball volume ---- #
    ball_volume = (4 / 3) * (3.14) * ball_radius_1 * ball_radius_2 * ball_radius_3 
    # V = (4 / 3)(r1)(r2)(r3)

    # ---- standardized ball description ---- #
    print(
        f"\nBall: {input_list_ball[0]}" + "\n"
        f"Ball Dimensions:" + "\n"
        f"  Length: {input_list_ball[1]}" + "\n"
        f"  Width: {input_list_ball[2]}" + "\n"
        f"  Height: {input_list_ball[3]}"
    )

    return ball_name, ball_volume

# ----- plane + ball calculations ----- #

def calculate_final(plane_name, plane_volume, ball_name, ball_volume):

    # ---- fancy loading text + logic ---- #
    sys.stdout.write("\nCalculating")
    for each_x in range(5):
        time.sleep(1)
        sys.stdout.write(".")
        sys.stdout.flush()

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
            print(
                f"\nOnly one {ball_name.lower()} can be stuffed in the {plane_name}!" + "\n"
            )

            # ---- checker for index array not to extend beyond 5: 1 ball case---- #
            if len(calculation_history) == 5:
                calculation_history.pop(0)
                calculation_history.append([plane_name, ball_name, (str(total_ball_count) + " " + ball_name.lower())])

            # ---- index to array: 1 ball case ---- #
            else:
                calculation_history.append([plane_name, ball_name, (str(total_ball_count) + " " + ball_name.lower())])

        else:
            print(
                f"\nA maximum of {total_ball_count} {ball_name.lower()}s can be stuffed in the {plane_name}!" + "\n"
            )
    
            # ---- checker for index array not to extend beyond 5 ---- #
            if len(calculation_history) == 5:
                calculation_history.pop(0)
                calculation_history.append([plane_name, ball_name, (str(total_ball_count) + " " + ball_name.lower() + "s")])

            # ---- index to array ---- #
            else:
                calculation_history.append([plane_name, ball_name, (str(total_ball_count) + " " + ball_name.lower() + "s")])

# ------ testing and debugging ------ #

# ----- program intro ----- #

dialogue = input(
    "Balls to Fit an Airplane: Standardized Edition" + "\n\n"

    "This code seeks to answer the popular coding exercise in tech interviews: \"How many balls can fit into an airplane?\"" + "\n\n"

    "This code has been standardized; meaning, it's up to you, the user, to create or to standardize your own" + "\n"
    "measurements for both the plane and the ball." + "\n\n"

    "Press any key to continue."
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
