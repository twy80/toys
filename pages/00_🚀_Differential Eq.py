"""
Simulation of an RLC circuit by T.-W. Yoon, Jan. 2023
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import streamlit as st


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


def lorenz(x, t, *args):
    rho, sigma, beta = args
    return [
        sigma * (x[1] - x[0]),
        x[0] * (rho - x[2]) - x[1],
        x[0] * x[1] - beta * x[2]
    ]


def run_rlc():
    st.write("")
    st.write("#### Linear RLC circuit")

    st.image(
        "files/RLC_circuit.jpg",
        caption="Image from http://goo.gl/r7DZBQ"
    )

    st.write(
        """
        This circuit can be described by
        
        >> ${\\displaystyle \\frac{dv_c}{dt} = \\frac{1}{C}\,i}\quad$ and
        >> $\quad{\\displaystyle \\frac{di}{dt} = -\\frac{1}{L}\,v_c -
        >> \\frac{R}{L}\,i + \\frac{1}{L}\,v}$.
        
        The equilirum state is unique and stable as long as the eigenvalues
        of the system, i.e. the roots of
        $\,\lambda^2 + \\frac{R}{L}\lambda + \\frac{1}{LC}=0\,$ have
        negative real parts. This stability is guaranteed by setting $R$, $L$
        and $C$ to be positive. Varying the values will only affect the transient
        behavour.
        """
    )
    st.write("---")

    # Choose the unit step or a sine function for the input voltage
    input_choice = st.radio(
        "$\\texttt{Choice of the input voltage?}$",
        ("Unit step", "Sine wave")
    )

    st.write("")

    left, right = st.columns([2, 1])
    with left:
        # Setting the R, L & C values
        resistor = st.slider(
            label="$\\texttt{Resistence R}$",
            min_value=0.1, max_value=5.0, value=1.0, step=0.1, format="%.1f"
        )
        inductor = st.slider(
            label="$\\texttt{Inductance L}$",
            min_value=0.1, max_value=5.0, value=1.0, step=0.1, format="%.1f"
        )
        capacitor = st.slider(
            label="$\\texttt{Capacitance C}$",
            min_value=0.1, max_value=5.0, value=1.0, step=0.1, format="%.1f"
        )

    t_rlc = np.linspace(0, 20, 501)
    x_rlc_0 = [0, 0]  # Initial state
    args_rlc = resistor, inductor, capacitor, input_choice

    with right:
        eigenvalues, _ = np.linalg.eig(rlc_eqn_jacobian(x_rlc_0, None, *args_rlc))
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
        x_rlc, infodict = odeint(
            rlc_eqn, x_rlc_0, t_rlc, args_rlc,
            Dfun=rlc_eqn_jacobian, full_output=True,
        )
        if infodict["message"] != "Integration successful.":
            st.error("Numerical problems arise.", icon="🚨")

    except Exception as e:
        st.error(f"An error occurred: {e}", icon="🚨")

    st.write("")
    st.write("$\\hspace{0.07em}\\texttt{\small Simulations results}$")
    plot_opt = st.radio(
        "$\\texttt{Simulations results}$",
        ("Time responses & Phase portrait", "Time responses only"),
        label_visibility="collapsed"
    )

    st.write("")

    if plot_opt == "Time responses & Phase portrait":
        fig, ax = plt.subplots(1, 2)
        ax[0].plot(t_rlc, x_rlc[:, 0], "g", label="$v_C(t)$")
        ax[0].plot(t_rlc, x_rlc[:, 1], "b", label="$i(t)$")
        ax[0].legend(loc="best")
        ax[0].set_xlabel("Time")
        ax[0].set_ylabel("State variables")
        ax[0].set_title("Time responses")
        ax[0].set_box_aspect(1)
        ax[1].plot(x_rlc[:, 0], x_rlc[:, 1], "r")  # path
        ax[1].plot(x_rlc[0, 0], x_rlc[0, 1], "o")
        ax[1].set_xlabel("$v_C(t)$")
        ax[1].set_ylabel("$i(t)$")
        ax[1].yaxis.set_label_position("right")
        ax[1].set_title("Phase portrait")
        ax[1].set_box_aspect(1)
    else:
        fig, ax = plt.subplots(2, 1, sharex=True)
        ax[0].set_title("Time Responses")
        ax[0].plot(t_rlc, x_rlc[:, 0], "g")
        ax[0].set_ylabel("$v_C(t)$")
        ax[1].plot(t_rlc, x_rlc[:, 1], "b")
        ax[1].set_ylabel("$i(t)$")
        ax[1].set_xlabel("Time")
    ax[0].set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])

    st.pyplot(fig)


def reset_initial_rho():
    st.session_state.pre_rho = st.session_state.rho


def run_lorenz():
    st.write("")
    st.write(
        """
        #### Nonlinear Lorenz system
        
        >> ${\\displaystyle \\frac{dx}{dt} = \sigma (y - x)}$
        
        >> ${\\displaystyle \\frac{dy}{dt} = x(\\rho - z) - y}$
        
        >> ${\\displaystyle \\frac{dz}{dt} = xy - \\beta z}$
        
        Bifurcations occur in this system, and the responses can be chaotic.
        For the sake of discussions, let us fix $(\\beta, \sigma)$ to
        $(8/3 , 10)$ and vary $\\rho$. If $\,0 < \\rho < 1$, the origin is
        the only equilibrium point. $\\rho = 1$ is where a pitchfork
        bifurcation occurs, leading to two additional equlibria;
        the origin then becomes unstable. Increasing $\\rho$
        further will show interesting behaviour like existence of chaotic
        solutions. To see this for example, set $\\rho$ to 28.
        
        ---
        """
    )

    # Input the value of rho
    rho_min, rho_init, rho_max = 1.0, 10.0, 30.0

    if "pre_rho" not in st.session_state:
        st.session_state.pre_rho = rho_init

    left, _, right = st.columns([5, 1, 5])
    option = left.radio(
        "$\\hspace{0.07em}\\texttt{How to set } \\rho$",
        ("Slider", "Textbox"),
        horizontal=True,
        on_change=reset_initial_rho
    )

    input_method = right.slider if option == "Slider" else right.number_input
    st.session_state.rho = input_method(
        label="$\\texttt{Value of }\\rho$",
        min_value=rho_min, max_value=rho_max, value=st.session_state.pre_rho,
        step=0.1, format="%.2f"
    )

    t_lorenz = np.linspace(0, 25, 10001)
    x_lorenz_0 = [1.0, 1.0, 1.0]

    sigma, beta = 10, 8/3.0
    rho = st.session_state.rho
    args_lorenz = rho, sigma, beta

    # Solving the differential equation
    try:
        x_lorenz, infodict = odeint(
            lorenz, x_lorenz_0, t_lorenz, args_lorenz, full_output=True,
        )
        if infodict["message"] != "Integration successful.":
            st.error("Numerical problems arise.", icon="🚨")

    except Exception as e:
        st.error(f"An error occurred: {e}", icon="🚨")

    st.write("")
    st.write("$\\hspace{0.07em}\\texttt{\small Simulations results}$")

    fig = plt.figure()

    states = "$x(t)$", "$y(t)$", "$z(t)$"
    colors = "k", "b", "g"
    ax1 = 3*[None]

    for k in range(3):
        ax1[k] = plt.subplot2grid((3, 2),  (k, 0), fig=fig)
        ax1[k].plot(t_lorenz, x_lorenz[:,k], color=colors[k], alpha=0.8)
        ax1[k].set_xlabel('Time')
        ax1[k].set_ylabel(states[k])
    ax1[0].set_title("Time responses")

    ax2 = plt.subplot2grid((3, 2), (0, 1), projection="3d", rowspan=3, fig=fig)
    ax2.plot(x_lorenz[0, 0], x_lorenz[0, 1], x_lorenz[0, 2], "o")
    ax2.plot(x_lorenz[:,0], x_lorenz[:,1], x_lorenz[:,2], color="r", alpha=0.5)
    ax2.set_xlabel('$x$')
    ax2.set_ylabel('$y$')
    ax2.set_zlabel('$z$')
    ax2.set_xticks([-20, -10, 0, 10, 20])
    ax2.set_yticks([-20, -10, 0, 10, 20])
    ax2.set_zticks([0, 10, 20, 30, 40])
    ax2.set_title("Phase portrait")

    st.pyplot(fig)


def run_sim():
    st.write("## 🚀 Differential Equations")

    st.write("")
    st.write(
        """
        Differential equations form a mathematical language, which can precisely
        describe objects in the world that are varying over time. Being able to
        deal with differential equations is therefore an essential element for
        science and technology. Two examples are given below: 2nd-order linear
        and 3rd-order nonlinear dynamcal systems.
        """
    )

    plt.rcParams.update({'font.size': 6})

    run_rlc()
    run_lorenz()


if __name__ == "__main__":
    run_sim()
