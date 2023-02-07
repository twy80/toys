"""
Simulation of an RLC circuit by T.-W. Yoon, Jan. 2023
"""

import numpy as np


# Differential equation of an RLC circuit
def rlc_eqn(x, t, *args):
    resistor, inductor, capacitor, input_choice = args

    voltage = 1. if input_choice == "Unit step" else np.sin(np.pi*t)
    
    return [
        0*x[0] + (1/capacitor)*x[1],
        (-1/inductor)*x[0] + (-resistor/inductor)*x[1] + (1/inductor)*voltage
    ]


def rlc_eqn_jacobian(x, t, *args):
    resistor, inductor, capacitor, _ = args

    return [
        [0, 1/capacitor],
        [-1/inductor, -resistor/inductor]
    ]


def run_sim():
    import matplotlib.pyplot as plt
    from scipy.integrate import odeint
    import streamlit as st

    st.write("## 🚀 Differential Equations")

    st.write("")
    st.write(
        """
        Differential equations form a mathematical language, which can precisely
        describe objects in the world that are varying over time. Being able to
        deal with differential equations is therefore an essential element for
        science and technology. Here is a simple example of simulating an RLC
        electric circuit expressed as a 2nd order differential equation.
        """
    )
    st.write("")
    st.write("##### RLC circuit")

    st.image(
        "files/RLC_circuit.jpg",
        caption="Image from http://goo.gl/r7DZBQ"
    )
    st.write("")

    # Choose the unit step or a sine function for the input voltage
    input_choice = st.selectbox(
        "$\\hspace{0.25em}\\texttt{Choice of the input voltage? Unit step or Sine?}$",
        ("Unit step", "Sine")
    )

    tspan = np.linspace(0, 10, 101)
    x_init = [0, 0]  # Initial state

    st.write("")

    left, right = st.columns([2, 1])
    with left:
        # Setting the R, L & C values
        resistor = st.slider(
            label="$\\hspace{0.25em}\\texttt{Resistence R}$",
            min_value=0.1,
            max_value=5.0,
            value=1.0,
            step=0.1,
            format="%.1f"
        )
        inductor = st.slider(
            label="$\\hspace{0.25em}\\texttt{Inductance L}$",
            min_value=0.1,
            max_value=5.0,
            value=1.0,
            step=0.1,
            format="%.1f"
        )
        capacitor = st.slider(
            label="$\\hspace{0.25em}\\texttt{Capacitance C}$",
            min_value=0.1,
            max_value=5.0,
            value=1.0,
            step=0.1,
            format="%.1f"
        )
        args = resistor, inductor, capacitor, input_choice

    with right:
        eigenvalues, _ = np.linalg.eig(rlc_eqn_jacobian(x_init, None, *args))
        st.write(
            f"""
            > **Eigenvalues of the system**
            >
            > ${eigenvalues[0]:>.2f}$
            >
            > ${eigenvalues[1]:>.2f}$
            """
        )

    # Solving the differential equation
    try:
        xs, infodict = odeint(
            rlc_eqn,
            x_init,
            tspan,
            args,
            Dfun=rlc_eqn_jacobian,
            full_output=True,
        )
        if infodict["message"] != "Integration successful.":
            st.error("Numerical problems arise.", icon="🚨")

    except Exception as e:
            st.error(f"An error occurred: {e}", icon="🚨")

    # voltage = len(tspan)*[1.0] if input_choice == "Unit step" else 1.0*np.sin(np.pi*tspan)

    st.write("")
    plot_opt = st.selectbox(
        "$\\hspace{0.25em}\\texttt{Simulations results}$",
        ("Phase portrait & Time responses", "Time responses only")
    )

    st.write("")
    plt.rcParams.update({'font.size': 6})

    if plot_opt == "Phase portrait & Time responses":
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
    else:
        fig, ax = plt.subplots(2, 1, sharex=True)
        ax[0].set_title("Time Responses")
        ax[0].plot(tspan, xs[:, 0], "g")
        ax[0].set_ylabel("$v_C(t)$")
        ax[1].plot(tspan, xs[:, 1], "b")
        ax[1].set_ylabel("$i(t)$")
        ax[1].set_xlabel("Time")

    st.pyplot(fig)


if __name__ == "__main__":
    run_sim()
