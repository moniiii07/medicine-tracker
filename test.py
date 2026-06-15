from database import init_db, add_medicine, get_all_medicines

init_db()

add_medicine("Paracetamol", "500mg", "Morning, Night", "After food")
add_medicine("Vitamin D3", "60000 IU", "Once a week", "")

medicines = get_all_medicines()
for med in medicines:
    print(med)