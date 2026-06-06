import customtkinter as ctk
from PIL import Image
from tkinter import filedialog
import os
import json
import shutil
import threading
from answer_querries import main
import webbrowser


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PredictX AI")
        self.geometry("1100x700")
        self.configure(fg_color="#FFFFFF")

        self.is_the_data_in_order = True

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.create_navbar()


        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, sticky="nsew")


        self.show_home()

    def create_navbar(self):
        self.navbar = ctk.CTkFrame(self, fg_color="transparent", height=80)
        self.navbar.grid(row=0, column=0, sticky="ew", padx=60, pady=10)
        self.navbar.grid_propagate(False)

        self.logo_label = ctk.CTkLabel(self.navbar, text="PredictX AI",
                                       font=("Arial Bold", 22), text_color="#1a1a1a")
        self.logo_label.pack(side="left")

        self.cta_button = ctk.CTkButton(self.navbar, text="ESTIMATE NOW",
                                        fg_color="#1a1a1a", corner_radius=10,
                                        width=120, height=40, font=("Arial Bold", 12))
        self.cta_button.pack(side="right")
        self.cta_button.configure(command=self.show_estimate)
        self.menu_frame = ctk.CTkFrame(self.navbar, fg_color="transparent")
        self.menu_frame.pack(side="right", padx=50)

        menu_items = [
            ("Home", self.show_home),
            ("About", self.draw_about),
            ("Analyze", self.draw_examples),
        ]

        for text, command in menu_items:
            btn = ctk.CTkButton(self.menu_frame, text=text, fg_color="transparent",
                                text_color="#444444", hover_color="#F0F0F0",
                                width=60, font=("Arial", 14), command=command)
            btn.pack(side="left", padx=10)

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_container()
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=60, pady=120)

        title = ctk.CTkLabel(left_frame, text="Now accurately\npredict price of\napartments.",
                             font=("Arial Bold", 48), text_color="#1a1a1a",
                             justify="left", anchor="w")
        title.pack(fill="x", pady=(20, 10))

        desc = ctk.CTkLabel(left_frame, text="Based on the Rome page data and AI analysis.",
                            font=("Arial", 18), text_color="#666666",
                            justify="left", anchor="w")
        desc.pack(fill="x", pady=(0, 30))

        btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        btn_frame.pack(fill="x")

        ctk.CTkButton(btn_frame, text="The Best Price", fg_color="#1a1a1a", command=self.show_estimate,
                      height=45, corner_radius=12).pack(side="left", padx=(0, 15))

        ctk.CTkButton(btn_frame, text="Search", fg_color="white", border_width=1,
                      border_color="#1a1a1a", text_color="#1a1a1a", command=self.open_website_nine_nine_nine,
                      height=45, corner_radius=12).pack(side="left")

        try:
            img_raw = Image.open("images/night.png")
            self.home_img = ctk.CTkImage(light_image=img_raw, dark_image=img_raw, size=(450, 550))
            img_label = ctk.CTkLabel(self.main_container, image=self.home_img, text="")
            img_label.grid(row=0, column=1, padx=20, pady=20)
        except Exception as e:
            placeholder = ctk.CTkFrame(self.main_container, width=400, height=500, corner_radius=20)
            placeholder.grid(row=0, column=1, padx=20, pady=20)

    def open_website_nine_nine_nine(self):
        webbrowser.open('https://999.md')

    def draw_about(self):
        self.clear_container()


        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=2)
        self.main_container.grid_rowconfigure(0, weight=1)


        left = ctk.CTkFrame(self.main_container, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(60, 20))

        title = ctk.CTkLabel(
            left,
            text="Fast, fintech-style pricing",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="black"
        )
        title.place(relx=0, rely=0.45, anchor="w")
        desc = ctk.CTkLabel(
            left,
            text="Clean input flow, transparent insights, and a confidence score to help you decide.",
            wraplength=350,
            justify="left",
            text_color="gray20",
            font=("Arial", 14)
        )
        desc.place(relx=0, rely=0.55, anchor="w")

        # RIGHT CARDS
        right = ctk.CTkFrame(self.main_container, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew", padx=(20, 60), pady=40)

        for i in range(3):
            right.grid_rowconfigure(i, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self.create_card(
            right, 0,
            "1) Fill details",
            "Choose location, size, rooms, and condition in a structured form.",
            "icons/2.png"
        )

        self.create_card(
            right, 1,
            "2) Upload photos",
            "AI checks interior/exterior condition, light, finishing, and layout signals.",
            "icons/1.png"
        )

        self.create_card(
            right, 2,
            "3) Get estimate",
            "Receive predicted price with a simple chart and key factors.",
            "icons/3.png"
        )

    # ================= CARD FUNCTION =================

    def create_card(self, parent, row, title, text, image_path=None):
        card = ctk.CTkFrame(
            parent,
            height=110,
            corner_radius=15,
            fg_color="#F0F0F0"
        )
        card.grid(row=row, column=0, sticky="ew", pady=10)
        card.grid_propagate(False)
        card.grid_columnconfigure(1, weight=1)


        if image_path and os.path.exists(image_path):
            try:

                img_data = Image.open(image_path)

                my_image = ctk.CTkImage(light_image=img_data, size=(60, 60))

                icon_display = ctk.CTkLabel(card, image=my_image, text="")
                icon_display.grid(row=0, column=0, rowspan=2, padx=20, pady=20)


                icon_display.image = my_image
            except Exception as e:
                print(f"Ошибка загрузки фото: {e}")
                image_path = None
        if not image_path:

            icon_container = ctk.CTkFrame(card, width=60, height=60, fg_color="#D0D0D0", corner_radius=10)
            icon_container.grid(row=0, column=0, rowspan=2, padx=20, pady=20)

        # TITLE
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="black"
        )
        title_label.grid(row=0, column=1, sticky="w", pady=(20, 0))

        # TEXT
        text_label = ctk.CTkLabel(
            card,
            text=text,
            wraplength=400,
            justify="left",
            text_color="gray20",
            font=("Arial", 12)
        )
        text_label.grid(row=1, column=1, sticky="w", pady=(0, 20))

    def show_placeholder(self, title_text):
        self.clear_container()
        lbl = ctk.CTkLabel(self.main_container, text=title_text, font=("Arial Bold", 32), text_color="#1a1a1a")
        lbl.pack(expand=True)

        # ================= EXAMPLES SCREEN =================

    def draw_examples(self):
        self.clear_container()

        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=2)
        self.main_container.grid_rowconfigure(0, weight=1)

        # LEFT PANEL
        left_panel = ctk.CTkFrame(self.main_container, fg_color="transparent")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(60, 20))

        title = ctk.CTkLabel(
            left_panel,
            text="What we analyze",
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color="#1a1a1a",
            justify="left"
        )
        title.place(relx=0, rely=0.4, anchor="w")

        subtitle = ctk.CTkLabel(
            left_panel,
            text="A quick checklist before you submit.",
            font=ctk.CTkFont(size=16),
            text_color="#666666"
        )
        subtitle.place(relx=0, rely=0.5, anchor="w")

        # RIGHT PANEL
        right_panel = ctk.CTkFrame(self.main_container, fg_color="transparent")


        right_panel.grid(row=0, column=1, sticky="nsew", padx=(20, 60), pady=20)

        for i in range(3): right_panel.grid_rowconfigure(i, weight=1)
        for i in range(2): right_panel.grid_columnconfigure(i, weight=1)

        analysis_data = [
            ("Location", "district / neighborhood", "Local comps", 0, 0, "icons_examples/1.png"),
            ("Size", "m² area", "Price per m²", 0, 1, "icons_examples/2.png"),
            ("Rooms", "layout signals", "Demand fit", 1, 0, "icons_examples/3.png"),
            ("Condition", "renovation level", "Finish adjustments", 1, 1, "icons_examples/4.png"),
            ("Photos", "visual quality", "Condition scoring", 2, 0, "icons_examples/5.png"),
            ("AI model", "prediction engine", "Confidence score", 2, 1, "icons_examples/6.png")
        ]

        for item in analysis_data:
            self.create_analysis_item(right_panel, *item)

    def create_analysis_item(self, parent, title, sub, bold_text, row, col, image_path=None):

        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.grid(row=row, column=col, pady=5)

        # Round icon background
        icon_circle = ctk.CTkFrame(
            item_frame, width=70, height=70,
            corner_radius=35,
            fg_color="#F2F2F2"
        )
        icon_circle.pack(pady=(0, 10))
        icon_circle.pack_propagate(False)

        if image_path and os.path.exists(image_path):
            try:
                img_data = Image.open(image_path)

                img_icon = ctk.CTkImage(light_image=img_data, size=(40, 40))

                icon_label = ctk.CTkLabel(icon_circle, image=img_icon, text="")
                icon_label.place(relx=0.5, rely=0.5, anchor="center")

                # Save the link to the image
                icon_label.image = img_icon
            except Exception as e:
                print(f"Failed to load icon {image_path}: {e}")

        # Текстовые блоки
        ctk.CTkLabel(
            item_frame, text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#1a1a1a"
        ).pack()

        ctk.CTkLabel(
            item_frame, text=sub,
            font=ctk.CTkFont(size=11),
            text_color="#999999"
        ).pack()

        ctk.CTkLabel(
            item_frame, text=bold_text,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1a1a1a"
        ).pack(pady=(5, 10))


    def show_estimate(self):
        self.clear_container()

        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)


        left_side = ctk.CTkFrame(self.main_container, fg_color="transparent")
        left_side.grid(row=0, column=0, sticky="nsew", padx=(80, 100), pady=60)


        center_content = ctk.CTkFrame(left_side, fg_color="transparent")
        center_content.pack(expand=True)


        try:
            raw_img = Image.open("icons/4.png")
            self.upload_icon_image = ctk.CTkImage(light_image=raw_img, dark_image=raw_img, size=(160, 160))
            ctk.CTkLabel(center_content, image=self.upload_icon_image, text="").pack(anchor="center", pady=(0, 25))
        except:
            ctk.CTkFrame(center_content, width=160, height=160, corner_radius=20, fg_color="#f2f2f2").pack(
                anchor="center", pady=(0, 25))


        ctk.CTkLabel(center_content, text="Upload Photos", font=("Arial Bold", 42), text_color="#1a1a1a").pack(
            anchor="center", pady=(0, 10))


        ctk.CTkLabel(center_content,
                     text="To get a precise AI estimation, please upload at least 3-5 high-quality photos of your apartment.",
                     font=("Arial", 17), text_color="#555555", wraplength=420, justify="center").pack(anchor="center")


        right_side = ctk.CTkFrame(self.main_container, fg_color="transparent")
        right_side.grid(row=0, column=1, sticky="nsew", padx=(40, 80), pady=100)

        # Зона drop_zone
        drop_zone = ctk.CTkFrame(right_side, fg_color="#fcfcfc", border_width=1, border_color="#e5e5e5",
                                 corner_radius=30)
        drop_zone.pack(fill="both", expand=True, pady=(0, 30))

        ctk.CTkLabel(drop_zone, text="Drag & Drop files here\nor click to browse",
                     font=("Arial", 15), text_color="#b0b0b0").place(relx=0.5, rely=0.42, anchor="center")
        n = ctk.CTkLabel(right_side, text="Selected: 0 files", font=("Arial", 17), text_color="#555555", wraplength=420, justify="center")
        ctk.CTkButton(drop_zone, text="Select Files",
                      fg_color="#1a1a1a", hover_color="#333333",
                      width=150, height=44, corner_radius=12,
                      font=("Arial Bold", 13),
                      command= lambda : self.browse_files(n)).place(relx=0.5, rely=0.58, anchor="center")

        n.pack(pady=(0, 30), anchor="s")
        self.next_step_btn = ctk.CTkButton(
            right_side,
            text="Next Step →",
            fg_color="#1a1a1a",
            hover_color="#333333",
            width=180,
            height=52,
            corner_radius=15,
            font=("Arial Bold", 15),
            command=self.show_details_input
        )
        self.next_step_btn.pack(side="right")

    def browse_files(self, n):
        files = filedialog.askopenfilenames(
            title="Select photos of the apartment",
            filetypes=[("Images", "*.png *.jpg *.jpeg")]
        )
        if files:
            self.selected_photo_paths = list(files)
            print(f"Selected files: {len(self.selected_photo_paths)}")
            n.configure(text=f"Selected: {len(self.selected_photo_paths)} files")


    def show_details_input(self):
        self.clear_container()
        self.is_the_data_in_order = True

        self.inputs = {}
        self.checkboxes = {}

        scroll_container = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll_container.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(scroll_container, text="Apartment Specifications",
                     font=("Arial Bold", 28), text_color="#1a1a1a").pack(pady=(10, 20))

        form_frame = ctk.CTkFrame(scroll_container, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20)
        form_frame.grid_columnconfigure((0, 1), weight=1)


        left_col = ctk.CTkFrame(form_frame, fg_color="#F9F9F9", corner_radius=20, border_width=1,
                                border_color="#EEEEEE")
        left_col.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(left_col, text="Main Parameters", font=("Arial Bold", 18)).pack(pady=15)


        num_fields = [
            ("Autorul anunțului", "OptionMenu", ['Persoană fizică', 'Agenție', 'Dezvoltator imobiliar', 'Bancă']),
            ("Număr de camere", "OptionMenu", ['O cameră', 'Apartament cu 2 camere', 'Apartament cu 3 camere']),
            ("Suprafață totală", "Entry", "72 m²"),
            ("Fond locativ", "OptionMenu", ['Secundar', 'Construcţii noi']),
            ("Etaj", "Entry", "7"),
            ("Număr de etaje", "Entry", "14"),
            ("Tip clădire", "OptionMenu", ['Cotileț', 'Cărămidă', 'Monolit', 'Combinat']),
            ("Starea apartamentului", "OptionMenu", ['Euroreparație', 'Variantă albă', 'Fără reparație']),
            ("Grup sanitar", "Entry", "1"),
            ("Balcon/ lojie", "Entry", "1"),
            ("Loc de parcare", "OptionMenu", ['Subterană', 'Deschis', 'Garaj']),
            ("Copii", "OptionMenu", ['Fără copii', 'Cu acordul stăpânului']),
            ("lat", "Entry", "47.026478"),
            ("long", "Entry", "28.821596"),
            ("description", "Entry", "Amplasat in centrul orasului...")
        ]

        for key, type, val in num_fields:
            ctk.CTkLabel(left_col, text=key, font=("Arial", 12), text_color="#666666").pack(anchor="w", padx=25)
            if type == "Entry":
                widget = ctk.CTkEntry(left_col, placeholder_text=val, height=35, fg_color="white")
                widget.pack(fill="x", padx=25, pady=(0, 10))
                self.inputs[key] = widget
            else:
                widget = ctk.CTkOptionMenu(left_col, values=val, fg_color="white", text_color="#1a1a1a",
                                           button_color="#F0F0F0", button_hover_color="#E0E0E0")
                widget.pack(fill="x", padx=25, pady=(0, 10))
                self.inputs[key] = widget


        right_col = ctk.CTkFrame(form_frame, fg_color="#F9F9F9", corner_radius=20, border_width=1,
                                 border_color="#EEEEEE")
        right_col.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(right_col, text="Amenities", font=("Arial Bold", 18)).pack(pady=15)

        amenities_list = [
            "Gata de mutat", "Mobilat", "Cu tehnică electrocasnică", "Încălzire autonomă",
            "Aparat de aer condiționat", "Încălzire prin pardoseală", "Geamuri termopan",
            "Parchet", "Ușă blindată", "Linie telefonică", "Internet", "Ascensor"
        ]

        for item in amenities_list:
            cb = ctk.CTkCheckBox(right_col, text=item, font=("Arial", 12),
                                 fg_color="#1a1a1a", hover_color="#333333")
            cb.pack(anchor="w", padx=30, pady=5)
            self.checkboxes[item] = cb

        # Кнопка расчета, которая вызывает сохранение
        calculate_btn = ctk.CTkButton(scroll_container, text="GET FINAL ESTIMATION",
                                      fg_color="#1a1a1a", height=55, corner_radius=15, command=self.start_ai_process,
                                      font=("Arial Bold", 16),
                                      )
        calculate_btn.pack(pady=40, padx=100, fill="x")



    def save_to_json(self):

        self.clear_querry_folder()
        folder_name = "querry"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        data = {}

        for key, widget in self.inputs.items():
            value = widget.get().strip()


            if value == "" or "Amplasat in" in value or "m²" in value:
                continue
            if (value == ""):
                if (key=="description"):
                    value = ""
                else:
                    value=0
            data[key] = value

        for key, widget in self.checkboxes.items():
            data[key] = 1 if widget.get() else 0


        json_path = os.path.join(folder_name, "data.json")
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"JSON is saved in {json_path}")
        except Exception as e:
            print(f"JSON write error: {e}")


        if hasattr(self, 'selected_photo_paths'):
            for i, file_path in enumerate(self.selected_photo_paths):
                try:

                    ext = os.path.splitext(file_path)[1]
                    # New name of file into fold (for example, photo_1.jpg)
                    new_name = f"photo_{i + 1}{ext}"
                    destination = os.path.join(folder_name, new_name)

                    shutil.copy2(file_path, destination)
                    print(f"Copied: {new_name}")
                except Exception as e:
                    print(f"Copy error {file_path}: {e}")
        else:
            print("No photos have been selected!")
            with open("empty_data.json", "r", encoding="utf-8") as empty_data:
                empty_data_json = json.load(empty_data)
                print(empty_data_json)
                print(data)
                if (empty_data_json == data):
                    self.is_the_data_in_order = False
                    self.show_error_screen("You have not entered or selected anything!")

        print("--- All data is collected in the 'querry' folder ---")

    def show_results_screen(self, price, confidence):
        self.clear_container()
        scroll_container = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll_container.pack(fill="both", expand=True)
        # HEADER
        header_frame = ctk.CTkFrame(scroll_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=60, pady=(40, 20))

        ctk.CTkLabel(header_frame, text="Prediction summary", font=("Arial Bold", 34), text_color="black").pack(
            anchor="center")
        ctk.CTkLabel(header_frame, text="Key numbers the model used to produce the estimate.", font=("Arial", 16),
                     text_color="gray").pack(anchor="center")

        # Container for cards
        cards_frame = ctk.CTkFrame(scroll_container, fg_color="transparent")
        cards_frame.pack(fill="x", padx=60)


        # Card 1: Predicted Price
        self.create_result_card(cards_frame, "Predicted price", f"€ {price:.2f}", "Most likely", 0)

        # Card 2: Confidence
        self.create_result_card(cards_frame, "Confidence", f"{confidence:.2f}", "High", 1)

        # Card 3: Price Range
        low = price * 0.9
        high = price * 1.1
        self.create_result_card(cards_frame, "Price range", f"€ {low / 1000:.1f}k–{high / 1000:.1f}k", "± 10%", 2)

        disclaimer_text = (
            "DISCLAIMER: These estimates are for informational purposes only and "
            "do not constitute financial advice. Real estate values are subject to "
            "market volatility and data inaccuracies."
        )


        try:
            img_raw = Image.open("correlation_heatmap.png")
            self.home_img2 = ctk.CTkImage(light_image=img_raw, dark_image=img_raw, size=(1100, 700))
            img_label = ctk.CTkLabel(scroll_container, image=self.home_img2, text="")
            img_label.pack(pady = 40)
        except Exception as e:
            placeholder = ctk.CTkFrame(scroll_container, width=400, height=500, corner_radius=20)
            placeholder.grid(row=0, column=0, padx=20, pady=20)

    def create_result_card(self, parent, title, value, subtext, col):
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", border_width=1, border_color="#E0E0E0", corner_radius=15,
                            height=180)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        ctk.CTkLabel(card, text=title, font=("Arial", 14), text_color="gray").pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(card, text=value, font=("Arial Bold", 28), text_color="black").pack(anchor="w", padx=20)
        ctk.CTkLabel(card, text=subtext, font=("Arial", 13), text_color="gray").pack(anchor="w", padx=20, pady=(5, 20))

    def show_processing_screen(self):
        self.clear_container()
        self.loading_lbl = ctk.CTkLabel(self.main_container,
                                        text="Your request is being processed...\nPlease wait.",
                                        font=("Arial Bold", 24), text_color="#1a1a1a")
        self.loading_lbl.place(relx=0.5, rely=0.5, anchor="center")

    def clear_querry_folder(self):
        folder = "querry"
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        else:
            os.makedirs(folder)
    def start_ai_process(self):
        self.save_to_json()
        if (self.is_the_data_in_order):
            self.show_processing_screen()
            threading.Thread(target=self.run_ai_thread, daemon=True).start()

    def run_ai_thread(self):
        # Call function from ai_engine.py
        main()
        with open("results.json", "r", encoding="utf-8") as f:
            list_res = json.load(f)
            result_price = list_res["price"]

        with open("model_score.json", "r", encoding="utf-8") as file:
            list_conf = json.load(file)
            confidence = list_conf[0]["R2"]
            print("CONF: ", confidence)

        # Return result in main threat by after()
        self.after(0, lambda: self.show_results_screen(result_price, confidence))

    def show_error_screen(self, message):

        self.clear_container()

        error_label = ctk.CTkLabel(
            self.main_container,
            text=message,
            font=("Arial Bold", 32),
            text_color="#E74C3C"
        )
        error_label.place(relx=0.5, rely=0.4, anchor="center")


        back_btn = ctk.CTkButton(
            self.main_container,
            text="Return to input",
            command=self.show_details_input,  # Return to input screen
            fg_color="#1a1a1a"
        )
        back_btn.place(relx=0.5, rely=0.55, anchor="center")



if __name__ == "__main__":
    app = App()
    app.mainloop()
