import streamlit as st

# 1. Nastavení stránky a KCD stylů (barvy, fonty)
st.set_page_config(page_title="Jindřichův Deník Úkolů", page_icon="🛡️")

st.markdown("""
<style>
    /* Pozadí a hlavní text */
    .stApp { background-color: #1a1311; color: #d6b560; font-family: 'Garamond', serif; }
    /* Nadpisy */
    h1, h2, h3 { color: #8a241b !important; font-family: 'Garamond', serif; }
    /* Text u zaškrtávacích políček */
    .stCheckbox p { color: #d6b560 !important; font-size: 18px !important; font-family: 'Garamond', serif; }
    /* Vstupní pole a tlačítka */
    .stTextInput input { background-color: #2b201a !important; color: #d6b560 !important; border: 1px solid #756d63; }
    .stButton button { background-color: #2b201a !important; color: #d6b560 !important; border: 1px solid #8a241b !important; }
    .stButton button:hover { border: 1px solid #d6b560 !important; color: #ffffff !important; }
    /* Skrytí defaultního horního menu Streamlitu pro lepší imerzi */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 2. Inicializace databáze (uložení do paměti relace)
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "text": "...", "type": "main", "completed": False},
        {"id": 2, "text": "...", "type": "side", "completed": False},
        {"id": 3, "text": "...", "type": "activity", "completed": False},
    ]
if 'next_id' not in st.session_state:
    st.session_state.next_id = 4

# Funkce pro přidání úkolu
def add_task(task_type, input_key):
    text = st.session_state[input_key].strip()
    if text:
        st.session_state.tasks.append({
            "id": st.session_state.next_id,
            "text": text,
            "type": task_type,
            "completed": False
        })
        st.session_state.next_id += 1
        st.session_state[input_key] = "" # Vyčištění pole

# Funkce pro změnu stavu (hotovo/nehotovo)
def toggle_task(task_id):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break

# 3. Vykreslení UI
st.markdown("<h1 style='text-align: center;'>~ DENÍK ÚKOLŮ ~</h1>", unsafe_allow_html=True)

categories = [
    ("main", "Hlavní úkoly", "🛡️"),
    ("side", "Vedlejší úkoly", "⚔️"),
    ("activity", "Aktivity", "🎯")
]

# Zobrazení aktivních úkolů
for cat_id, cat_name, icon in categories:
    st.markdown(f"### {icon} {cat_name.upper()}")
    
    # Vyfiltrujeme nedokončené úkoly v této kategorii
    cat_tasks = [t for t in st.session_state.tasks if t["type"] == cat_id and not t["completed"]]
    
    for task in cat_tasks:
        st.checkbox(task["text"], key=f"chk_{task['id']}", value=False, on_change=toggle_task, args=(task['id'],))
    
    # Řádek pro přidání nového úkolu
    col1, col2 = st.columns([4, 1])
    input_key = f"new_{cat_id}"
    with col1:
        st.text_input("Nový úkol", key=input_key, label_visibility="collapsed", placeholder="Zapiš do deníku...")
    with col2:
        st.button("Přidat", key=f"btn_{cat_id}", on_click=add_task, args=(cat_id, input_key))
    
    st.write("") # Mezera

# Zobrazení dokončených úkolů
finished_tasks = [t for t in st.session_state.tasks if t["completed"]]
if finished_tasks:
    st.markdown("---")
    st.markdown("<h3 style='color: #756d63 !important;'>📜 DOKONČENÉ (Zapsáno v kronikách)</h3>", unsafe_allow_html=True)
    
    for task in finished_tasks:
        # Checkbox u dokončeného úkolu je zaškrtnutý, po odškrtnutí se vrátí nahoru
        st.checkbox(f"~~{task['text']}~~", key=f"chk_{task['id']}", value=True, on_change=toggle_task, args=(task['id'],))
