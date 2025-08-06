import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import json
from scipy.integrate import solve_ivp

st.set_page_config(page_title="LLM-Powered Projectile Simulator")

st.title("🎯 LLM-Powered Projectile Simulator")
st.markdown("Describe a projectile scenario, and the app will simulate it.")

user_input = st.text_area("Enter scenario (natural language)", value="Launch a ball at 45 degrees, 50 m/s, from 2m, mass 0.5kg, drag 0.1")

if st.button("Simulate"):

    with st.spinner("🔍 Parsing input using LLM..."):

        prompt = f"""
You are a physics assistant. Extract key parameters from this input:

\"\"\"{user_input}\"\"\"

Respond ONLY with a JSON object:
{{
  "velocity": float (in m/s),
  "angle": float (in degrees),
  "initial_height": float (in meters),
  "mass": float (kg),
  "drag_coefficient": float (0-1, optional, default 0)
}}
"""

        try:
            result = subprocess.run(
                ["ollama", "run", "llama3"],
                input=prompt.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )

            output = result.stdout.decode()
            json_start = output.find('{')
            json_data = json.loads(output[json_start:])

            v0 = json_data.get("velocity", 50)
            angle = np.radians(json_data.get("angle", 45))
            h0 = json_data.get("initial_height", 0)
            mass = json_data.get("mass", 1)
            drag = json_data.get("drag_coefficient", 0)

            st.success("✅ Parameters parsed successfully")
            st.json(json_data)

        except Exception as e:
            st.error(f"LLM failed to parse input: {e}")
            st.stop()

    # Begin physics simulation
    st.subheader("📈 Simulated Trajectory")

    g = 9.81

    def simulate_with_drag(v0, angle, h0, mass, drag):
        vx0 = v0 * np.cos(angle)
        vy0 = v0 * np.sin(angle)

        def dynamics(t, y):
            x, y_pos, vx, vy = y
            v = np.sqrt(vx**2 + vy**2)
            ax = - (drag / mass) * v * vx
            ay = -g - (drag / mass) * v * vy
            return [vx, vy, ax, ay]

        y0_state = [0, h0, vx0, vy0]
        t_span = (0, 20)
        t_eval = np.linspace(0, 20, 1000)

        sol = solve_ivp(dynamics, t_span, y0_state, t_eval=t_eval, events=lambda t, y: y[1])

        return sol.t, sol.y[0], sol.y[1]  # time, x, y

    t_vals, x_vals, y_vals = simulate_with_drag(v0, angle, h0, mass, drag)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Projectile Motion with Air Resistance" if drag > 0 else "Ideal Projectile Motion")
    ax.grid()
    st.pyplot(fig)

    st.markdown(f"**Flight Time:** {t_vals[-1]:.2f} s")
    st.markdown(f"**Horizontal Range:** {x_vals[-1]:.2f} m")
    st.markdown(f"**Max Height:** {np.max(y_vals):.2f} m")
