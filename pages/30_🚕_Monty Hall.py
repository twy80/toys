"""
Simulating the Monty Hall Problem (by T.-W. Yoon, Oct. 2023)
"""

import random
import time
import streamlit as st

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


def choose_door(delay=True):
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

    # Save three door states to session_state variables
    st.session_state.car = car
    st.session_state.shown = shown
    st.session_state.not_shown = not_shown

    if delay:
        # Highlight selected door first, and trigger reveal phase with delay
        st.session_state.doors[st.session_state.selected] = door_images["selected"]
        st.session_state.revealing = True
        st.session_state.new_game = False
    else:
        # Set the door images immediately (for automatic play)
        st.session_state.doors[st.session_state.selected] = door_images["selected"]
        st.session_state.doors[shown] = door_images["goat"]
        st.session_state.doors[not_shown] = door_images["closed"]
        st.session_state.new_game = False


def keep_choice():
    """
    This function handles the user's choice to keep their selection.

    Session state variables for door information are updated, and
    positive or negative messages are set depending on whether
    the user wins the car or not.

    The button_enabled flag is then set to False to allow the user
    to press the 'keep' button just once.
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
    to press the 'switch' button just once.
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
    st.session_state.doors = doors_closed[:]
    st.session_state.new_game = True
    st.session_state.revealing = False
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
    st.session_state.revealing = False
    st.session_state.button_enabled = True


def auto_game_keep():
    """
    This function plays the game automatically with random choices
    and the 'keep' policy. The number of games to play is stored
    as st.session_state.no_of_games.
    """
    for _ in range(st.session_state.no_of_games):
        st.session_state.selected = random.choice(doors)
        choose_door(delay=False)
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
        choose_door(delay=False)
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

        Choose one door using the buttons below. We will then open another door
        to reveal a goat. After that, you can decide whether to keep your original
        choice or switch to the remaining door in order to have a chance of winning
        the car. You can continue playing the game or play it automatically.
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

    if "revealing" not in st.session_state:
        st.session_state.revealing = False

    if "button_enabled" not in st.session_state:
        st.session_state.button_enabled = True

    st.write("**Play options**")
    play_option = st.radio(
        label="Play Options",
        options=("Manual play", "Automatic play"),
        horizontal=True,
        label_visibility="collapsed"
    )
    st.write("")

    if play_option == "Manual play":
        if st.session_state.new_game:
            st.session_state.doors = doors_closed[:]

        # Add side margins to reduce door image size and perfectly align buttons with doors
        _, col1, col2, col3, _ = st.columns([0.5, 2, 2, 2, 0.5])
        door_cols = [col1, col2, col3]

        # 1. Show 3 door images
        for idx in range(3):
            with door_cols[idx]:
                st.image(st.session_state.doors[idx], caption=door_captions[idx], width='stretch')

        # 2. Controls by game stage
        if st.session_state.new_game:
            # Stage 1: Choose door
            for idx in range(3):
                with door_cols[idx]:
                    if st.button(f"Choose Door {idx + 1}", key=f"choose_door_btn_{idx}", width='stretch'):
                        st.session_state.selected = idx
                        choose_door()
                        st.rerun()

        elif st.session_state.revealing:
            # Stage 2: Delay & Host revealing goat door
            for idx in range(3):
                with door_cols[idx]:
                    st.button(f"Choose Door {idx + 1}", disabled=True, width='stretch')

            with st.spinner("The host is opening a goat door... 🚕🐐"):
                time.sleep(1.0)  # Delay time in seconds

            # Reveal goat door after delay
            st.session_state.doors[st.session_state.shown] = door_images["goat"]
            st.session_state.doors[st.session_state.not_shown] = door_images["closed"]
            st.session_state.revealing = False
            st.rerun()

        elif st.session_state.button_enabled:
            # Stage 3: Keep or Switch decision (Show Keep & Switch buttons only)
            st.write("")
            c1, c2 = st.columns(2)
            c1.button(label="$~~\:\,$Keep$~~\:\,$", on_click=keep_choice, width='stretch')
            c2.button(label="$~\,\,$Switch$~\,\,$", on_click=switch_choice, width='stretch')

            # Let the user know how to play
            st.write(
                "You chose Door", st.session_state.selected + 1,
                "and$\,$ we open Door", st.session_state.shown + 1,
                "to reveal a goat. $\,$Keep your choice, or switch to Door",
                st.session_state.not_shown + 1, "?"
            )

        else:
            # Stage 4: Result phase (Show Play again & Reset buttons only)
            st.write("")
            c1, c2 = st.columns(2)
            c1.button(label="Play again", on_click=play_again, width='stretch')
            c2.button(label="$~\:\,\,$Reset$~\:\,\,$", on_click=reset_game, width='stretch')

    else:  # Automatic play
        st.session_state.new_game = True
        st.session_state.revealing = False
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
        st.button(label="$~\:\,\,$Reset$~\:\,\,$", on_click=reset_game)

    if max(st.session_state.wins, st.session_state.losses) > 0:
        no_of_games = st.session_state.wins + st.session_state.losses
        percentage = 100 * st.session_state.wins / no_of_games
        # Show the result for manual play with vibrant callout boxes
        if not st.session_state.button_enabled:
            if "Congratulations" in st.session_state.message:
                st.success(f"🎉 **{st.session_state.message}**")
            else:
                st.error(f"😢 **{st.session_state.message}**")

        # Show the statistics
        st.write(
            "You won the car", st.session_state.wins,
            "time(s) out of", no_of_games,
            f"game(s) $\,\Rightarrow\,$ :green[{percentage:>.1f}]%."
        )


if __name__ == "__main__":
    monty_hall()

