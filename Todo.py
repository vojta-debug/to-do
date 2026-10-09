import tkinter as tk
from tkinter import font

class KCDQuestLog:
    def __init__(self, root):
        self.root = root
        self.root.title("Jindřichův Deník Úkolů")
        self.root.geometry("600x800")
        self.root.configure(bg="#1a1311") # Tmavě hnědá/černá (pozadí deníku)

        # Barvy a fonty ve stylu KCD
        self.BG = "#1a1311"
        self.FG_GOLD = "#d6b560"     # Zlatavá barva textu
        self.FG_RED = "#8a241b"      # Tmavě červená pro hlavní nadpisy
        self.FG_GRAY = "#756d63"     # Šedá pro splněné questy
        self.BTN_BG = "#2b201a"
        
        # Pokus o načtení dobového fontu (pokud není, použije se fallback)
        self.FONT_TITLE = ("Garamond", 22, "bold")
        self.FONT_CAT = ("Garamond", 16, "bold")
        self.FONT_QUEST = ("Garamond", 14)
        
        # Ikony pro kategorie
        self.ICONS = {
            "main": "🛡️",  # Štít pro hlavní úkoly
            "side": "⚔️",  # Meče pro vedlejší úkoly
            "activity": "🎯" # Terč pro aktivity
        }

        # Databáze úkolů (obsahuje výchozí prázdné body podle zadání)
        self.tasks = [
            {"id": 1, "text": "...", "type": "main", "completed": False},
            {"id": 2, "text": "...", "type": "side", "completed": False},
            {"id": 3, "text": "...", "type": "activity", "completed": False},
        ]
        self.next_id = 4

        # Hlavní kontejner
        self.main_frame = tk.Frame(self.root, bg=self.BG)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Nadpis
        title_label = tk.Label(
            self.main_frame, 
            text="~ DENÍK ÚKOLŮ ~", 
            font=self.FONT_TITLE, 
            bg=self.BG, 
            fg=self.FG_RED
        )
        title_label.pack(pady=(0, 20))

        # Rámec pro dynamický výpis úkolů
        self.quests_frame = tk.Frame(self.main_frame, bg=self.BG)
        self.quests_frame.pack(fill=tk.BOTH, expand=True)

        self.render_ui()

    def add_task(self, task_type, entry_widget):
        text = entry_widget.get().strip()
        if text:
            self.tasks.append({
                "id": self.next_id,
                "text": text,
                "type": task_type,
                "completed": False
            })
            self.next_id += 1
            self.render_ui()

    def toggle_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                break
        self.render_ui()

    def render_ui(self):
        # Vyčištění aktuálního zobrazení
        for widget in self.quests_frame.winfo_children():
            widget.destroy()

        categories = [
            ("main", "Hlavní úkoly"),
            ("side", "Vedlejší úkoly"),
            ("activity", "Aktivity")
        ]

        # VYKRESLENÍ AKTIVNÍCH ÚKOLŮ
        for cat_id, cat_name in categories:
            # Hlavička kategorie
            cat_label = tk.Label(
                self.quests_frame, 
                text=f"{self.ICONS[cat_id]} {cat_name.upper()}", 
                font=self.FONT_CAT, 
                bg=self.BG, 
                fg=self.FG_GOLD
            )
            cat_label.pack(anchor="w", pady=(15, 5))

            # Úkoly v dané kategorii
            cat_tasks = [t for t in self.tasks if t["type"] == cat_id and not t["completed"]]
            
            for task in cat_tasks:
                self.create_task_row(task, self.FG_GOLD)

            # Přidávací řádek
            add_frame = tk.Frame(self.quests_frame, bg=self.BG)
            add_frame.pack(anchor="w", padx=30, pady=5)
            
            entry = tk.Entry(add_frame, bg=self.BTN_BG, fg=self.FG_GOLD, font=self.FONT_QUEST, insertbackground=self.FG_GOLD, width=30)
            entry.pack(side=tk.LEFT, padx=(0, 10))
            
            add_btn = tk.Button(
                add_frame, 
                text="Přidat", 
                bg=self.BTN_BG, 
                fg=self.FG_GOLD, 
                activebackground=self.FG_RED,
                activeforeground=self.FG_GOLD,
                font=("Garamond", 10, "bold"),
                relief=tk.FLAT,
                command=lambda t=cat_id, e=entry: self.add_task(t, e)
            )
            add_btn.pack(side=tk.LEFT)

        # VYKRESLENÍ DOKONČENÝCH ÚKOLŮ
        finished_tasks = [t for t in self.tasks if t["completed"]]
        if finished_tasks:
            # Oddělovač
            tk.Frame(self.quests_frame, height=2, bg=self.FG_RED).pack(fill=tk.X, pady=(20, 10))
            
            finished_label = tk.Label(
                self.quests_frame, 
                text="📜 DOKONČENÉ (Zapsáno v kronikách)", 
                font=self.FONT_CAT, 
                bg=self.BG, 
                fg=self.FG_GRAY
            )
            finished_label.pack(anchor="w", pady=(5, 5))

            for task in finished_tasks:
                self.create_task_row(task, self.FG_GRAY, is_finished=True)

    def create_task_row(self, task, color, is_finished=False):
        row_frame = tk.Frame(self.quests_frame, bg=self.BG)
        row_frame.pack(anchor="w", padx=30, pady=2)

        # Checkbox simulovaný pomocí tlačítka/labelu pro lepší vzhled
        box_text = "☒" if is_finished else "☐"
        
        check_btn = tk.Button(
            row_frame, 
            text=box_text, 
            font=self.FONT_QUEST, 
            bg=self.BG, 
            fg=color, 
            activebackground=self.BG,
            activeforeground=self.FG_RED,
            relief=tk.FLAT,
            bd=0,
            command=lambda id=task["id"]: self.toggle_task(id)
        )
        check_btn.pack(side=tk.LEFT)

        # Pokud je úkol hotový, přidáme přeškrtnutí
        task_text = task["text"]
        
        task_label = tk.Label(
            row_frame, 
            text=task_text, 
            font=self.FONT_QUEST, 
            bg=self.BG, 
            fg=color
        )
        task_label.pack(side=tk.LEFT, padx=(5, 0))

        if is_finished:
            # Přeškrtnutí fontu (Tkinter overstrike)
            f = font.Font(task_label, task_label.cget("font"))
            f.configure(overstrike=True)
            task_label.configure(font=f)

if __name__ == "__main__":
    root = tk.Tk()
    app = KCDQuestLog(root)
    
    # Klávesová zkratka pro zavření okna přes Escape (jako ve hře)
    root.bind('<Escape>', lambda e: root.quit())
    
    root.mainloop()
