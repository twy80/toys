import numpy as np

# Differential equation of an RLC circuit
def rlc_eqn(x, t, *args):
    resistor, inductor, capacitor, input_choice = args

    voltage = 1. if input_choice == "unit step" else np.sin(np.pi*t)
    
    return [
        0*x[0] + (1/capacitor)*x[1],
        (-1/inductor)*x[0] + (-resistor/inductor)*x[1] + (1/inductor)*voltage
    ]


def run_sim():
    import matplotlib.pyplot as plt
    from scipy.integrate import odeint
    import streamlit as st

    st.write("## 🚀 Simulation of an RLC Circuit")

    st.write("")
    st.image(
        "images/RLC_circuit.jpg",
        caption="From http://goo.gl/r7DZBQ"
    )
    st.write("")

    # Input the rank of the compressed image
    input_choice = st.selectbox(
        "$\\hspace{0.25em}\\texttt{Choice of the input voltage? Unit step or Sine?}$",
        ("unit step", "sine")
    )

    resistor = st.slider(
        label="$\\hspace{0.25em}\\texttt{Resistence}$",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
        label_visibility="visible"
    )
    inductor = st.slider(
        label="$\\hspace{0.25em}\\texttt{Inductance}$",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
        label_visibility="visible"
    )
    capacitor = st.slider(
        label="$\\hspace{0.25em}\\texttt{Capacitance}$",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
        label_visibility="visible"
    )

    tspan = np.linspace(0, 10, 101) # 시간 설정 (0, 0.01, …, 10)

    args = resistor, inductor, capacitor, input_choice

    # Solving the differential equation

    x_init = [0, 0]  # 초깃값 설정
        # 입력 전압 V와  R, L, C 값은 모두 1이라 가정

    xs, infodict = odeint(
        rlc_eqn,
        x_init,
        tspan,
        args,
        full_output=True,
    )

    if infodict["message"] != "Integration successful.":
        st.error("Numerical problems arise.", icon="🚨")

    # voltage = len(tspan)*[1.0] if input_choice == "step" else 1.0*np.sin(np.pi*tspan)

    st.write("")
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