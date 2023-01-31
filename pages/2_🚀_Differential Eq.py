import numpy as np

# Differential equation of an RLC circuit
def rlc_eqn(x, t, *args):
    resistor, inductor, capacitor, input_choice = args

    voltage = 1. if input_choice == "Unit step" else np.sin(np.pi*t)
    
    return [
        0*x[0] + (1/capacitor)*x[1],
        (-1/inductor)*x[0] + (-resistor/inductor)*x[1] + (1/inductor)*voltage
    ]


def run_sim():
    import matplotlib.pyplot as plt
    from scipy.integrate import odeint
    import streamlit as st

    st.write("## 🚀 Simulation of a Circuit")

    st.write("")
    st.image(
        "images/RLC_circuit.jpg",
        caption="Image from http://goo.gl/r7DZBQ"
    )
    st.write("")

    # Choose the unit step or a sine function for the input voltage
    input_choice = st.selectbox(
        "$\\hspace{0.25em}\\texttt{Choice of the input voltage? Unit step or Sine?}$",
        ("Unit step", "Sine")
    )

    # Setting the R, L & C values
    resistor = st.slider(
        label="$\\hspace{0.25em}\\texttt{Resistence}$",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
        format="%.1f"
    )
    inductor = st.slider(
        label="$\\hspace{0.25em}\\texttt{Inductance}$",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
        format="%.1f"
    )
    capacitor = st.slider(
        label="$\\hspace{0.25em}\\texttt{Capacitance}$",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
        format="%.1f"
    )

    tspan = np.linspace(0, 10, 101)

    args = resistor, inductor, capacitor, input_choice

    # Solving the differential equation

    x_init = [0, 0]  # Initial state

    try:
        xs, infodict = odeint(
            rlc_eqn,
            x_init,
            tspan,
            args,
            full_output=True,
        )
        if infodict["message"] != "Integration successful.":
            st.error("Numerical problems arise.", icon="🚨")

    except Exception as e:
            st.error(f"An error occurred: {e}", icon="🚨")


    # voltage = len(tspan)*[1.0] if input_choice == "Unit step" else 1.0*np.sin(np.pi*tspan)

    st.write("")
    fig, ax = plt.subplots(1, 2)

    ax[0].plot(xs[:, 0], xs[:, 1], "r-")  # path
    ax[0].plot([xs[0, 0]], "s")
    ax[0].set_xlabel("$v_C(t)$")
    ax[0].set_ylabel("$i(t)$")
    ax[0].set_title("Phase portrait")
    ax[0].set_box_aspect(1)

    ax[1].plot(tspan, xs[:, 0], "g", label="$v_C(t)$")
    ax[1].plot(tspan, xs[:, 1], "b", label="$i(t)$")
    ax[1].legend(loc="best")
    ax[1].set_xlabel("Time")
    ax[1].set_title("Time responses")
    ax[1].set_box_aspect(1)

    st.pyplot(fig)


if __name__ == "__main__":
    run_sim()
