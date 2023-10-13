"""
Simulating the Monty Hall Problem (by T.-W. Yoon, Oct. 2023)
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

doors_closed = [
    door_images["closed"], door_images["closed"], door_images["closed"]
]

positive_message = "Congratulations! You won the car!"
negative_message = "Sorry, you didn't win the car."


def choose_door():
    """
    This function randomly places the car behind a door, and
    reveals a goat door that is not chosen by the user.

    The indices of the doors are saved as streamlit session state
    variables as follows:

    st.session_state.car: door with the car
    st.session_state.shown: door opened
    st.session_state.not_shown: door still closed
    st.session_state.selected: door chosen by the user.
    """

    car = random.choice(doors)  # Place the car at a random position

    # Host reveals a goat door
    goat_doors = [
      door for door in doors if door != st.session_state.selected and door != car
    ]
    shown = goat_doors[0] if len(goat_doors) == 1 else random.choice(goat_doors)
    not_shown = list(set(doors) - {st.session_state.selected, shown})[0]

    # Set the door images
    st.session_state.doors[st.session_state.selected] = door_images["selected"]
    st.session_state.doors[shown] = door_images["goat"]
    st.session_state.doors[not_shown] = door_images["closed"]

    # Save three door states to session_state variables
    st.session_state.car = car
    st.session_state.shown = shown
    st.session_state.not_shown = not_shown

    # Set this to False in order not to allow the user to choose another door
    st.session_state.new_game = False


def keep_choice():
    """
    This function handles the user's choice to keep their selection.

    Session state variables for door information are updated, and
    positive or negative messages are set depending on whether
    the user wins the car or not.

    The button_enabled flag is then set to False to allow the user
    to press the 'keep' button just onces.
    """

    if st.session_state.button_enabled:
        if st.session_state.selected == st.session_state.car:
            st.session_state.message = positive_message
            st.session_state.doors[st.session_state.selected] = door_images["car"]
            st.session_state.doors[st.session_state.not_shown] = door_images["goat"]
            st.session_state.wins += 1
        else:
            st.session_state.message = negative_message
            st.session_state.doors[st.session_state.selected] = door_images["goat"]
            st.session_state.doors[st.session_state.not_shown] = door_images["car"]
            st.session_state.losses += 1
        st.session_state.button_enabled = False


def switch_choice():
    """
    This function handles the user's choice to switch their selection.

    Session state variables for door information are updated, and
    positive or negative messages are set depending on whether
    the user wins the car or not.

    The button_enabled flag is then set to False to allow the user
    to press the 'switch' button just onces.
    """

    if st.session_state.button_enabled:
        if st.session_state.not_shown == st.session_state.car:
            st.session_state.message = positive_message
            st.session_state.doors[st.session_state.selected] = door_images["goat"]
            st.session_state.doors[st.session_state.not_shown] = door_images["car"]
            st.session_state.wins += 1
        else:
            st.session_state.message = negative_message
            st.session_state.doors[st.session_state.selected] = door_images["car"]
            st.session_state.doors[st.session_state.not_shown] = door_images["goat"]
            st.session_state.losses += 1
        st.session_state.button_enabled = False


def play_again():
    """
    This function sets the necessary flags to play another game.
    """
    st.session_state.new_game = True
    st.session_state.button_enabled = True


def reset_game():
    """
    This function sets the necessary flags to reset the game
    for initialization.
    """
    st.session_state.doors = doors_closed[:]
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.new_game = True
    st.session_state.button_enabled = True


def auto_game_keep():
    """
    This function plays the game automatically with random choices
    and the 'keep' policy. The number of games to play is stored
    as st.session_state.no_of_games.
    """
    for _ in range(st.session_state.no_of_games):
        st.session_state.selected = random.choice(doors)
        choose_door()
        keep_choice()
        st.session_state.button_enabled = True


def auto_game_switch():
    """
    This function plays the game automatically with random choices
    and the 'switch' policy. The number of games to play is stored
    as st.session_state.no_of_games.
    """
    for _ in range(st.session_state.no_of_games):
        st.session_state.selected = random.choice(doors)
        choose_door()
        switch_choice()
        st.session_state.button_enabled = True


def monty_hall():
    """
    This function implements a simulation of the Monty Hall Problem.
    It provides a user interface for the user to manually or
    automatically play the game. For manual play, the user selects
    a door and has the option to keep or switch their choice.
    For automatic play, the function allows the user to define
    the number of games to play and provides buttons to randomly
    choose a door and keep or switch the choice. The function also
    keeps track of wins and losses and displays the win percentage.
    """

    st.write("## 🚕 Monty Hall Problem")

    st.write("")
    st.write(
        """
        Behind three doors are two goats and a car.
        Let's see if you win the car!

        Choose one door and press the :blue[Choose] button below. We will then
        open another door to reveal a goat. After that, you can decide whether
        to keep your original choice or switch to the remaining door in order
        to have a chance of winning the car. You can continue playing the game
        or play it automatically.
        """
    )

    if "doors" not in st.session_state:
        st.session_state.doors = doors_closed[:]

    if "wins" not in st.session_state:
        st.session_state.wins = 0

    if "losses" not in st.session_state:
        st.session_state.losses = 0

    if "message" not in st.session_state:
        st.session_state.message = ""

    if "new_game" not in st.session_state:
        st.session_state.new_game = True

    if "button_enabled" not in st.session_state:
        st.session_state.button_enabled = True

    st.write("**Play options**")
    play_options = st.radio(
        label="Play Options",
        options=("Manual play", "Automatic play"),
        horizontal=True,
        label_visibility="collapsed"
    )
    st.write("")

    if play_options == "Manual play":
        c1, c2, c3, c4 = st.columns([3, 3, 3, 8])
        if st.session_state.new_game:
            # Show the three closed doors
            st.session_state.selected = image_select(
                label="",
                images=doors_closed,
                use_container_width=False,
                captions=door_captions,
                return_value="index"
            )
            # Allow the user to select one, or reset the game
            c1.button(label="$~\:$Choose$~\:$", on_click=choose_door)
            c2.button(label="$~\:\,\,$Reset$~\:\,\,$", on_click=reset_game)
        else:
            # Show the selected, opened, and closed doors
            image_select(
                label="",
                images=st.session_state.doors,
                use_container_width=False,
                captions=door_captions,
                return_value="index"
            )
            # Allow the user to keep or switch their choicd
            c1.button(label="$~~\:\,$Keep$~~\:\,$", on_click=keep_choice)
            c2.button(label="$~\,\,$Switch$~\,\,$", on_click=switch_choice)
            # Allow the user to play a new game, or reset the game
            c3.button(label="Play again", on_click=play_again)
            c4.button(label="$~\:\,\,$Reset$~\:\,\,$", on_click=reset_game)

            # Let the user know how to play
            st.write(
                "You chose Door", st.session_state.selected + 1,
                "and$\,$ we open Door", st.session_state.shown + 1,
                "to reveal a goat. $\,$Keep your choice, or switch to Door",
                st.session_state.not_shown + 1, "?"
            )
    else:  # Automatic play
        st.session_state.new_game = True
        st.session_state.button_enabled = True
        st.write("Number of games to play")
        st.session_state.no_of_games = st.slider(
            label="Number of games",
            min_value=10, max_value=1000, value=100, step=1,
            label_visibility="collapsed"
        )
        # Provide the user with the option to choose between two strategies,
        # either keeping or switching.
        st.button(label="Randomly choose $\:$&$\;$ keep", on_click=auto_game_keep)
        st.button(label="Randomly choose & switch", on_click=auto_game_switch)
        st.button("$~\:\,\,$Reset$~\:\,\,$", on_click=reset_game)

    if max(st.session_state.wins, st.session_state.losses) > 0:
        no_of_games = st.session_state.wins + st.session_state.losses
        percentage = 100 * st.session_state.wins / no_of_games
        # Show the result for manual play
        if not st.session_state.button_enabled:
            st.write(st.session_state.message)
        # Show the statistics
        st.write(
            "You won the car", st.session_state.wins,
            "time(s) out of", no_of_games,
            f"game(s) $\,\Rightarrow\,$ {percentage:>.1f}%."
        )


if __name__ == "__main__":
    monty_hall()
