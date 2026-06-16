import streamlit as st
from database import init_db, add_medicine, get_all_medicines


init_db()


st.title("💊 Medicine Tracker")
st.write("Add and manage your medicines.")


st.divider()


st.subheader("Add a Medicine")

name = st.text_input("Medicine Name")
dosage = st.text_input("Dosage (e.g. 500mg)")
timing = st.text_input("Timing (e.g. Morning, Night)")
notes = st.text_input("Notes (e.g. After food)")

if st.button("Add Medicine"):
    if name.strip() == "":
        st.error("Medicine name cannot be empty.")
    else:
        add_medicine(name, dosage, timing, notes)
        st.success(f"{name} added successfully!")

# Divider
st.divider()

# Section 2: View All Medicines
st.subheader("Your Medicines")

medicines = get_all_medicines()

if len(medicines) == 0:
    st.info("No medicines added yet.")
else:
    for med in medicines:
        st.write(f"**{med[1]}** — {med[2]} — {med[3]}")