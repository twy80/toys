"""
Control of an inverted pendulum on a cart using PID control
by T.-W. Yoon, Aug. 2023
"""

import numpy as np
from scipy.integrate import odeint
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


# Define the dynamics of the pid controlled inverted pendulum
def pendulum_cart_pid(state, time, *args):
    m_c, m_p, length, b, g, kp, ki, kd = args
    x, x_dot, theta, theta_dot, eta = state

    control = -kp * theta - ki * eta - kd * theta_dot

    x_double_dot = (
        m_p * np.sin(theta) * (g * np.cos(theta) - length * theta_dot ** 2)
        + control - b * x_dot
    ) / (m_c + m_p * np.sin(theta) ** 2)

    theta_double_dot = (
        (m_c + m_p) * g * np.sin(theta)
        - m_p * length * theta_dot ** 2 * np.sin(theta) * np.cos(theta)
        + (control - b * x_dot) * np.cos(theta)
    ) / (length * (m_c + m_p * np.sin(theta) ** 2))

    eta_dot = theta

    return [x_dot, x_double_dot, theta_dot, theta_double_dot, eta_dot]


def print_root(value):
    value = value.real if np.allclose(value.imag, 0.0) else value
    value = 0.0 if np.allclose(np.abs(value), 0.0) else value

    return value


# Main function
def sim_pendulum_pid():
    """
    This function sets all the parameters for PID control of an inverted
    pendulum on cart, and performs simulations.
    """

    # Cart parameters
    m_c, m_p, length, b, g = 0.5, 0.2, 0.3, 0.1, 9.8

    # Initial desired char. poly.": s^3 + am_1 s^2 + am_2 s + am_3 = 0
    am_10, am_20, am_30 = 33.1, 93.3, 9.0

    # Open_loop transfer function
    b_0 = 1.0 / (m_c * length)
    a_1, a_2, a_3 = b / m_c, -(m_c + m_p) * g * b_0, -b * g * b_0
    # num_open = np.array([b_0, 0.0])
    den_open = np.array([1.0, a_1, a_2, a_3])
    open_loop_poles = np.roots(den_open)

    # Select the PID gains to achieve the desired char. poly.
    kd0 = (am_10 - a_1) / b_0
    kp0 = (am_20 - a_2) / b_0
    ki0 = (am_30 - a_3) / b_0

    # kd = am_1 * m_c * length - b * length
    # kp = am_2 * m_c * length + (m_c + m_p) * g
    # ki = am_3 * m_c * length + b * g

    st.write("")
    st.write(
        f"""
        ##### Simulations
        
        * Cart-pendulum parameters
        
        >> $M = 0.5$, $~m = 0.2$, $~\ell = 0.3$, $~b = 0.1~$
           ($b\,$: Friction coefficient)

        * Open-loop poles:
          $~\\small {print_root(open_loop_poles[0]):>.2f}$,
          $~\\small {print_root(open_loop_poles[1]):>.2f}$,
          $~\\small {print_root(open_loop_poles[2]):>.2f}~$
          (Unstable!)
        """
    )
    st.write(
        """
        * PID gains resulting from $~a_{m1} = 33.1$, $~a_{m2} = 93.3$,
          $~a_{m3} = 9.0$

        >> $K_p = 20.86$, $~K_i = 2.33$, $~K_d = 4.94$ 

        * Further tune the PID gains
        """
    )

    _, left, _, right = st.columns([1, 13, 1, 12])
    kp = left.slider(
        label="$\\texttt{Proportional gain~} K_p$",
        min_value=15.0, max_value=30.0, value=kp0, step=0.01, format="%.2f"
    )
    ki = left.slider(
        label="$\\texttt{Integral gain~} K_i$",
        min_value=1.0, max_value=5.0, value=ki0, step=0.01, format="%.2f"
    )
    kd = left.slider(
        label="$\\texttt{Derivative gain~} K_d$",
        min_value=1.0, max_value=10.0, value=kd0, step=0.01, format="%.2f"
    )

    am_1 = kd * b_0 + a_1
    am_2 = kp * b_0 + a_2
    am_3 = ki * b_0 + a_3

    char_poly = np.array([1.0, am_1, am_2, am_3])
    closed_loop_poles = np.roots(char_poly)

    # Print closed-loop poles
    right.write(
        f"""
        Closed-loop poles:
        $\,\\small {print_root(closed_loop_poles[0]):>.2f}$,
        $\,\\small {print_root(closed_loop_poles[1]):>.2f}$,
        $\,\\small {print_root(closed_loop_poles[2]):>.2f}$
        """
    )
    right.info(
        """
        - One pole at the origin is not shown here; this pole results
          from the motion of the cart, and is canceled out by one
          zero at the origin.

        - The nonlinear closed-loop system can be unstable
          even when the linearized system is stable with all
          the poles located in the left half plane. 
        """
    )

    st.write(
        """
        * Set the initial angular position ($\\times \pi$)
        """
    )
    _, left, _ = st.columns([1, 13, 13])

    theta0 = left.slider(
        label="$\\texttt{Initial angular position~} \\theta(0)$",
        min_value=-1.0, max_value=1.0, value=-0.5, step=0.05, format="%.2f"
    )
    theta0 *= np.pi

    # Parameters of the ODE
    args = m_c, m_p, length, b, g, kp, ki, kd

    # Initial state variables
    x0 = 0.0  # Initial position of the cart
    x_dot0 = 0.0  # Initial velocity of the cart
    # theta0 = -0.5 * np.pi  # Initial angle of the pendulum
    theta_dot0 = 0.0  # Initial angular velocity of the pendulum
    eta0 = 0.0  # Initial integration of the angle

    # Time span
    t_start, t_end, t_step = 0.0, 5.0, 0.025

    no_of_iter = round((t_end - t_start) / t_step)

    char_poly = np.array([1.0, am_1, am_2, am_3])
    closed_loop_poles = np.roots(char_poly)

    state_init = np.array([x0, x_dot0, theta0, theta_dot0, eta0])

    # t_span = t_start, t_end
    times = np.linspace(t_start, t_end, no_of_iter + 1)

    # Solve the ODE
    try:
        states, infodict = odeint(
            pendulum_cart_pid, state_init, times, args, full_output=True
        )
        if infodict["message"] != "Integration successful.":
            st.error("Numerical problems arise.", icon="🚨")
            return
    except Exception as e:
        st.error(f"An error occurred: {e}", icon="🚨")
        return

    positions = states[:, 0]
    angles = states[:, 2]
    # controls = -kp * states[:, 2] - ki * states[:, 4] - kd * states[:, 3]

    plt.rcParams.update({'font.size': 7})

    st.write(
        """
        * Simulations results: trajectories over time
        """
    )

    fig, ax = plt.subplots(2, 1)
    ax[0].plot(times, positions)
    ax[0].set_ylabel('Cart position $\,x(t)$')
    ax[0].set_xlim([0, 5])
    ax[0].set_xticklabels([])

    # Set up the figure and axis for angle plot
    ax[1].plot(times, angles)
    ax[1].set_ylabel('Pendulum angle $\,\\theta(t)$')
    ax[1].set_xlabel('Time (sec)')
    ax[1].set_xlim([0, 5])

    st.pyplot(fig)

    # Animation
    # plt.rcParams.update({'font.size': 8})
    st.write("")
    st.write(
        """
        * Simulations results: animation
        """
    )

    fig, ax = plt.subplots()

    cart_width = 2
    cart_height = 1
    pendulum_length = 7.0

    def update_frame(index):
        ax.clear()

        # Draw the cart
        cart_x = positions[index]
        cart_y = 0.0

        cart_bottom_left = (cart_x - cart_width / 2, cart_y - cart_height / 2)
        cart_bottom_right = (cart_x + cart_width / 2, cart_y - cart_height / 2)
        cart_top_left = (cart_x - cart_width / 2, cart_y + cart_height / 2)
        cart_top_right = (cart_x + cart_width / 2, cart_y + cart_height / 2)
        ax.plot(
            [cart_bottom_left[0], cart_bottom_right[0]],
            [cart_bottom_left[1], cart_bottom_right[1]], 'k'
        )
        ax.plot(
            [cart_bottom_left[0], cart_top_left[0]],
            [cart_bottom_left[1], cart_top_left[1]], 'k'
        )
        ax.plot(
            [cart_bottom_right[0], cart_top_right[0]],
            [cart_bottom_right[1], cart_top_right[1]], 'k'
        )
        ax.plot(
            [cart_top_left[0], cart_top_right[0]],
            [cart_top_left[1], cart_top_right[1]], 'k'
        )

        pendulum_x = cart_x - pendulum_length * np.sin(angles[index])
        pendulum_y = pendulum_length * np.cos(angles[index])
        ax.plot([cart_x, pendulum_x], [cart_y, pendulum_y], 'r')
        ax.plot(pendulum_x, pendulum_y, 'ro', markersize=10)

        k = round(cart_x / 20)
        ax.set_xlim([20*(k-1), 20*(k+1)])
        ax.set_ylim([-10, 10])

        # Set aspect ratio
        ax.set_aspect('equal')
        ax.set_yticks([-10, -5, 0, 5, 10])
        ax.set_yticklabels([])

        # Set title
        ax.set_title('Time: {:.2f}sec'.format(times[index]))

    animation = FuncAnimation(
        fig, update_frame, frames=len(times), interval=1000*t_step
    )
    # st.pyplot(fig)

    with st.spinner("Preparing for animation..."):
        animation.save('files/pendulum.gif', writer=PillowWriter())

    st.image("files/pendulum.gif")


def run_pendulum_pid():
    st.write("## ⛳ Feedback Control Systems")

    st.write("")
    st.write(
        """
        Control is the act of automatically determining the inputs
        to an object so that it is in a desired state. In constructing
        a control system, it is essential to measure or estimate
        the output or state variables of the target. This feedback is a must,
        as uncertainties such as modeling errors and the presence of
        disturbances are inevitable. Therefore, automatic control and
        feedback are inseparable. Feedback control is also referred to
        as closed-loop control since the closed-loop is formed by feedback.
        As an example, an inverted pendulum on a cart is considered here;
        the control objective is to keep the pendulum in an upright position
        by applying force to the cart.
        """
    )

    st.write("")
    st.write("##### Inverted pendulum on a cart")

    st.image(
        "files/cart-pendulum.png",
        caption="Image from https://upload.wikimedia.org/wikipedia/commons/b/b6/Cart-pendulum.png",
        width=450
    )

    st.write("")
    st.write(
        """
        ##### Mathematical model for simulation

        > ${\\displaystyle \\ddot{x} = \\frac{1}{M + m \sin^2\\theta}
        \left(F - b\dot{x} - m\ell\dot{\\theta}^2\sin\\theta + mg\sin\\theta\cos\\theta\\right)}$
        
        > ${\\displaystyle \\ddot{\\theta} = \\frac{1}{(M + m \sin^2\\theta)\ell}
        \left((F - b\dot{x})\cos\\theta - m\ell\dot{\\theta}^2\sin\\theta\cos\\theta + (M+m)g\sin\\theta\\right)}$
        """
    )

    st.write("")
    st.write(
        """
        ##### PID (Proportional Integral Derivative) control
        
        > ${\\displaystyle F = K_p e + K_i \int_0^t e(\\tau)d\\tau + K_d \dot{e}}~~~$
        where $~~e = \\theta_{ref} - \\theta =  0 - \\theta$

        > ${\\displaystyle \hat{F}(s) = -\\frac{K_d s^2 + K_p s + K_i}{s}\,\hat{\\theta}(s)}$
        """
    )

    st.write("")
    st.write(
        """
        ##### Linearized model for tuning the PID controller
        
        > ${\\displaystyle ~~~\:\,\,\\ddot{x} \\approx -\\frac{b}{M}\dot{x} + \\frac{m}{M}g\\theta + \\frac{1}{M}F}$
        
        > ${\\displaystyle ~~~\:\,\,\\ddot{\\theta} \\approx -\\frac{b}{M\ell}\dot{x} + \\frac{M+m}{M\ell}g\\theta + \\frac{1}{M\ell}F}$

        > ${\\displaystyle \hat{\\theta}(s) \\approx \\frac{\\frac{1}{M\ell}s}
        {s^3 + \\frac{b}{M}s^2 - \\frac{(M+m)g}{M\ell}s - \\frac{bg}{M\ell}}\hat{F}(s) = -\\frac{\\frac{1}{m\ell}(K_ds^2 + K_ps + K_i)}
        {s^3 + \\frac{b}{M}s^2 - \\frac{(M+m)g}{M\ell}s - \\frac{bg}{M\ell}}\hat{\\theta}(s)}$
    
        > $\,\,\left(s^3 + (\\frac{K_d}{M\ell}+\\frac{b}{M})s^2 + (\\frac{K_p}{M\ell}-\\frac{(M+m)g}{M\ell})s + (\\frac{K_i}{M\ell}-\\frac{bg}{M\ell})\\right)\hat{\\theta}(s) \\approx 0$
        """
    )
    st.write("")
    st.write(
        """
        ##### PID controller tuning (via pole placement)

        > $K_p =  a_{m2}M\ell + (M+m)g$,
        > $~\,K_i = a_{m3}M\ell + bg$,
        > $~\,K_d = a_{m1}M\ell - b\ell$
        
        > where $\,s^3 + a_{m1}s^2 + a_{m2}s + a_{m3}\,$ is the desired characteristic polynomial
        """
    )

    sim_pendulum_pid()


if __name__ == '__main__':
    run_pendulum_pid()
