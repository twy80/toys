"""
Doing Something (by T.-W. Yoon, Mar. 2023)
"""

import streamlit as st
from streamlit_image_select import image_select
import random

# Door indices
doors = [0, 1, 2]

# Door images
door_images = {
    "closed": "files/closed_door.png",
    "car": "files/car_door.png",
    "goat": "files/goat_door.png",
    "selected": "files/selected_door.png"
}

door_captions = ["Door 1", "Door 2", "Door 3"]

doors_ready = [
    door_images["closed"], door_images["closed"], door_images["closed"]
]

positive_message = "Congratulations! You won the car!"
negative_message = "Sorry, you didn't win the car."


def choose_door():
    # Place the car at a random position
    car = random.choice(doors)

    # Host reveals a goat door
    goat_doors = [
        door for door in doors if door != st.session_state.selected and door != car
    ]
    shown = goat_doors[0] if len(goat_doors) == 1 else random.choice(goat_doors)
    not_shown = list(set(doors) - {st.session_state.selected, shown})[0]

    st.session_state.doors[st.session_state.selected] = door_images["selected"]
    st.session_state.doors[shown] = door_images["goat"]
    st.session_state.doors[not_shown] = door_images["closed"]

    st.session_state.car = car
    st.session_state.shown = shown
    st.session_state.not_shown = not_shown
    st.session_state.ready = False


def keep_choice():
    if not st.session_state.button_pressed:
        if st.session_state.selected == st.session_state.car:
            # st.write("Congratulations! You won the car!")
            st.session_state.message = positive_message
            st.session_state.doors[st.session_state.selected] = door_images["car"]
            st.session_state.doors[st.session_state.not_shown] = door_images["goat"]
            st.session_state.wins += 1
        else:
            # st.write("Sorry, you didn't win the car.")
            st.session_state.message = negative_message
            st.session_state.doors[st.session_state.selected] = door_images["goat"]
            st.session_state.doors[st.session_state.not_shown] = door_images["car"]
            st.session_state.losses += 1
        st.session_state.button_pressed = True


def switch_choice():
    if not st.session_state.button_pressed:
        if st.session_state.not_shown == st.session_state.car:
            # st.write("Congratulations! You won the car!")
            st.session_state.message = positive_message
            st.session_state.doors[st.session_state.selected] = door_images["goat"]
            st.session_state.doors[st.session_state.not_shown] = door_images["car"]
            st.session_state.wins += 1
        else:
            # st.write("Sorry, you didn't win the car.")
            st.session_state.message = negative_message
            st.session_state.doors[st.session_state.selected] = door_images["car"]
            st.session_state.doors[st.session_state.not_shown] = door_images["goat"]
            st.session_state.losses += 1
        st.session_state.button_pressed = True


def play_again():
    st.session_state.ready = True
    st.session_state.button_pressed = False


def reset_game():
    st.session_state.doors = doors_ready[:]
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.ready = True
    st.session_state.button_pressed = False


def auto_game_keep():
    for _ in range(st.session_state.no_of_games):
        st.session_state.selected = random.choice(doors)
        choose_door()
        keep_choice()
        st.session_state.button_pressed = False


def auto_game_switch():
    for _ in range(st.session_state.no_of_games):
        st.session_state.selected = random.choice(doors)
        choose_door()
        switch_choice()
        st.session_state.button_pressed = False


def monty_hall():
    st.write("## 🚕 Monty Hall Problem")

    if "ready" not in st.session_state:
        st.session_state.ready = True

    if "wins" not in st.session_state:
        st.session_state.wins = 0

    if "losses" not in st.session_state:
        st.session_state.losses = 0

    if "doors" not in st.session_state:
        st.session_state.doors = doors_ready[:]

    if "message" not in st.session_state:
        st.session_state.message = ""

    if "button_pressed" not in st.session_state:
        st.session_state.button_pressed = False

    st.write(
        """
        Welcome to the Monty Hall problem!

        Behind one of these doors is a car, and behind the other two are goats.
        Let's see if you win the car!

        Choose one door and press the :blue[Choose] button below. We will then
        open another door to reveal a goat. After that, you can decide whether
        to keep your original choice or switch to the remaining door
        in order to have a chance of winning the car. If you want to learn
        about the probability of winning the car, you can continue playing
        the game or automatically play it. You can also reset the game.
        """
    )

    st.write("##### Play options")
    play_option = st.radio(
        label="Play Options",
        options=("Manual Play", "Automatic Play"),
        horizontal=True,
        label_visibility="collapsed"
    )
    st.write("")

    if play_option == "Manual Play":
        c1, c2, c3, c4 = st.columns([3, 4, 4, 8])
        if st.session_state.ready:
            st.session_state.selected = image_select(
                label="",
                images=doors_ready,
                use_container_width=False,
                captions=door_captions,
                return_value="index"
            )
            c1.button(label="Choose", on_click=choose_door)
            c2.button(label="$\;$Reset$\;$", on_click=reset_game)
        else:
            image_select(
                label="",
                images=st.session_state.doors,
                use_container_width=False,
                captions=door_captions,
                return_value="index"
            )
            c1.button(label="Keep", on_click=keep_choice)
            c2.button(label="Switch", on_click=switch_choice)
            c3.button(label="Play again", on_click=play_again)
            c4.button(label="$\;$Reset$\;$", on_click=reset_game)

            st.write(
                "You chose Door", st.session_state.selected + 1,
                "and$\,$ we open Door", st.session_state.shown + 1,
                "to reveal a goat. $\,$Keep your choice, or switch to Door",
                st.session_state.not_shown + 1, "?"
            )

        if max(st.session_state.wins, st.session_state.losses) > 0:
            no_of_games = st.session_state.wins + st.session_state.losses
            percentage = 100 * st.session_state.wins / no_of_games
            if st.session_state.button_pressed:
                st.write(st.session_state.message)
            st.write(
                "You won the car", st.session_state.wins,
                "time(s) out of", no_of_games,
                f"game(s) $\,\Rightarrow\,$ {percentage:>.1f}%."
            )
    else:
        st.write("Number of games to play")
        st.session_state.no_of_games = st.slider(
            label="Number of games",
            min_value=10, max_value=1000, value=100, step=1,
            label_visibility="collapsed"
        )
        st.button(label="Randomly choose $\:$&$\;$ keep", on_click=auto_game_keep)
        st.button(label="Randomly choose & switch", on_click=auto_game_switch)
        st.button("$\;$Reset$\;$", on_click=reset_game)

        if max(st.session_state.wins, st.session_state.losses) > 0:
            no_of_games = st.session_state.wins + st.session_state.losses
            percentage = 100 * st.session_state.wins / no_of_games
            st.write(
                "You won the car", st.session_state.wins,
                "time(s) out of", no_of_games,
                f"game(s) $\,\Rightarrow\,$ {percentage:>.1f}%."
            )

        st.session_state.ready = True

if __name__ == "__main__":
    monty_hall()


# import streamlit as st
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.animation import FuncAnimation


# def increase_status():
#     st.session_state.status += 1


# def decrease_status():
#     st.session_state.status -= 1


# # Main function
# def main():
#     st.write("## 🛠️ Doing Something")

#     st.write("")
#     st.write(
#         """
#         Let us do something fantastic!
#         """
#     )

#     plt.rcParams.update({'font.size': 8})

#     if 'status' not in st.session_state:
#         st.session_state.status = 10

#     st.write(f"Upper value: {st.session_state.status}")

#     # if st.button('increase'):
#     #     st.session_state.status += 1
#     # if st.button('decrease'):
#     #     st.session_state.status -= 1

#     st.button('increase', on_click=increase_status)
#     st.button('decrease', on_click=decrease_status)

#     st.write(f"Lower value: {st.session_state.status}")


# if __name__ == '__main__':
#     main()
