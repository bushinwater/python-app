import tkinter as tk
from tkinter import font, filedialog, ttk
import pandas as pd
import sys

def pronadji_proizvod():
    update_cena.config(text="Izmeni cenu")
    barcode = entery1.get()

    # Pravljenje datafile
    df = pd.read_excel(file_path, header=None, dtype=str)

    # Izbacuje vrste sa NaN vrednostima u barkode i naziv kolonama
    df = df.dropna(subset=[barcode_column, name_column])

    if barcode in df[barcode_column].astype(str).values:
        product_name = df.loc[df[barcode_column].astype(str) == barcode, name_column].values[0]
        old_price = df.loc[df[barcode_column].astype(str) == barcode, price_column].values[0]

        output_label.config(text=f"Stara cena {product_name} (Barcode {barcode}): {old_price}")

    else:
        output_label.config(text=f"Proizvod nije pronadjen")

def updateCena():
    barkod = entery1.get()
    new_price = nova_cena.get()

    df = pd.read_excel(file_path, header=None, dtype=str)

    # Ažuriraj cenu samo ako je nova cena uneta
    if new_price:
        # Ažuriraj DataFrame, ne briši redove sa NaN vrednostima
        mask = df[barcode_column].notna() & df[name_column].notna()
        mask &= df[barcode_column].astype(str) == barkod
        df.loc[mask, price_column] = float(new_price)
        df.to_excel(file_path, index=False, header=False)

        # Obriši podatke u entry boxevima nakon izvršenja ažuriranja cene
        entery1.delete(0, tk.END)
        nova_cena.delete(0, tk.END)
        entery2.delete(0, tk.END)

        # Vrati fokus na prvi entry point
        root.after(10, lambda: entery1.focus_set())
        update_cena.config(text="Cena uspešno promenjena")
    else:
        entery1.delete(0, tk.END)
        entery2.delete(0, tk.END)
        nova_cena.delete(0, tk.END)
        update_cena.config(text="Nova cena nije uneta")
        # Ako nova cena nije uneta, vrati fokus na prvi entry point
        root.after(10, lambda: entery1.focus_set())
    output_label.config(text="")
    predlozena_cena.config(text="")

#pitaj za lokaciju fajla
def ask_for_file_location():
    #popup
    popup = tk.Tk()
    custom_font = font.Font(family="Helvetica", size=12)
    popup.title("Select File")
    popup.geometry("200x80")
    popup.minsize(200, 80)

    #inacijalizacija max velicine prozora
    max_width = 200
    max_height = 80
    popup.maxsize(max_width, max_height)

    def enforce_max_size(event):
        if popup.winfo_width() > max_width or popup.winfo_height() > max_height:
            popup.geometry(f"{min(popup.winfo_width(), max_width)}x{min(popup.winfo_height(), max_height)}")

    popup.bind("<Configure>", enforce_max_size)

    #tekst i dugme
    label = tk.Label(popup, text="Please select the file path", font=custom_font)
    label.pack()

    def ok_button_clicked():
        popup.destroy()

    ok_button = tk.Button(popup, text="OK", command=ok_button_clicked, font=custom_font)
    ok_button.pack()

    popup.mainloop()

    #otvori fajl dijalog nakon sto je popup zatvoren
    file_path = filedialog.askopenfilename(title="Select File")
    return file_path

############# komande za fokusiranje sledecih widgeta ###############
def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

def activate_button(event=None):
    pronadji_proizvod()
    event.widget.tk_focusNext().focus()
    return "break"

def activate_button2(event=None):
    updateCena()
    event.widget.tk_focusNext().focus()
############################
    
def calculate_and_display_price():
    pdv_price_entry = entery2.get()

    nova_cena.focus_set()

    if pdv_price_entry:
        try:
            pdv_price = float(pdv_price_entry)
            suggested_price = pdv_price * 1.3
            predlozena_cena.config(text=f"Predlozena cena: {suggested_price}")
            nova_cena.focus_set()  # Set focus to the "Uneti novu cenu" entry
        except ValueError:
            predlozena_cena.config(text="Unesite validnu cenu sa PDV-om")
    else:
        predlozena_cena.config(text="Cena sa PDV-om nije uneta")

#excel konstante
file_path = ask_for_file_location()
barcode_column = 6
name_column = 0
price_column = 1

if file_path:
    #incijaliazcija prozora
    root = tk.Tk()
    #font
    custom_font = font.Font(family="Helvetica")

    #konfiguracija stila za okruglaste okvire i boje za labels i buttons
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TRoundedLabel.TLabel", borderwidth=5, relief="solid", padding=(10, 5))
    style.configure("TRoundedLabel.TLabel",
                    borderwidth=5,
                    relief="solid",
                    padding=(10, 5),
                    bordercolor="#00241B")
    
    style.configure("TColoredButton.TButton",
                    padding=(10, 5),
                    borderwidth=3,
                    relief="solid",
                    background="#65B891",  # Set button background color
                    foreground="black",
                    bordercolor="#00241B",
                    font=custom_font)

    root.title("Kalkulator cena")
    root.geometry("650x400")
    #minimalna velicina programa
    root.minsize(650, 400)
    #stavi prozor ispred svih pri pokretanju
    root.attributes('-topmost', True)
    #boja pozadine
    root.configure(bg="#4E878C")

    #mesta za unos cena i barkoda
    entery1 = tk.Entry(root, font=custom_font)
    nova_cena = tk.Entry(root, font=custom_font)
    
    entery1.focus_set()

    #tekst
    label_barkod = ttk.Label(root, text="Uneti barcode: ", font=custom_font, style="TRoundedLabel.TLabel", background="#93E5AB")
    label_cena = ttk.Label(root, text="Uneti cenu sa PDV-om: ", font=custom_font, style="TRoundedLabel.TLabel", background="#93E5AB")
    label_nova_cena = ttk.Label(root, text="Uneti novu cenu: ", font=custom_font, style="TRoundedLabel.TLabel", background="#93E5AB")

    #gemetrija entry pointsa i label-a
    label_barkod.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
    entery1.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
    #button za trazenje proizvoda
    dugme = ttk.Button(root, text="Pronadji artikl", style="TColoredButton.TButton", command=lambda: pronadji_proizvod())
    dugme.grid(row=1, column=0, columnspan=2, pady=10)

    entery1.bind("<Return>", lambda event: (pronadji_proizvod(), root.after(10, lambda: entery2.focus_set())))


    entery2 = tk.Entry(root, font=custom_font)
    label_cena.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
    entery2.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

    entery2.bind("<Return>", lambda event: calculate_and_display_price())


    #frames za prikaz proizvoda koji je pronadjen
    output_frame1 = tk.Frame(root)
    output_frame1.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    output_label = ttk.Label(output_frame1, text="", font=custom_font, wraplength=400, style="TRoundedLabel.TLabel", background="#93E5AB")
    output_label.pack()

    output_frame2 = tk.Frame(root)
    output_frame2.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    #tekst za predlozenu cenu koji se updatuje iz funkcije
    predlozena_cena = ttk.Label(output_frame2, text="", font=custom_font, wraplength=420, style="TRoundedLabel.TLabel", background="#93E5AB")
    predlozena_cena.pack()

    #grid za novu cenu
    label_nova_cena.grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
    nova_cena.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

    #dugme za update cene
    update_cena = ttk.Button(root, text="Izmeni cenu", style="TColoredButton.TButton", command=lambda: updateCena())
    update_cena.grid(row=6, column=0, columnspan=2, pady=10)

    nova_cena.bind("<Return>", activate_button2)
    #centriranje teksta u kolonama grida
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    for i in range(7):
        root.rowconfigure(i, weight=1)

    # Run the main loop
    root.mainloop()

else:
    sys.exit()
