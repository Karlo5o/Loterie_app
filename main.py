import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.font import Font





# Definice textu





X = np.arange(10)
X2 = np.arange(15)
Y1 = X / 2
Y2 = X2 * 2



class Root(tk.Tk):

    def __init__(self):
        super().__init__()

        self.geometry("1500x800")
        self.title("Loterie Aplikace")
        self.my_font = Font(size=15)
        self.iconbitmap('D:\\Python\\Projects\\fun_with_data\\cash_icon.ico')

        self.make_labels()
        self.make_buttons()
        self.make_entries()

        self.bind('<Return>', lambda a: self.yes_click())
    def make_labels(self):

        act_date = datetime.date.today().isocalendar()[1]
        date_text = "Současný týden: " + str(act_date)

        self.label_date = tk.Label(self, text=date_text, font=self.my_font)
        self.label_date.grid(row=0, column=3)

        self.label_tyden = tk.Label(self, text="Týden", font=self.my_font)
        self.label_tyden.grid(row=0, column=1, columnspan=2)

        self.label_error = tk.Label(self, text="", font=self.my_font)
        self.label_error.grid(row=8, column=1, columnspan=2)


    def make_buttons(self):
        # definice vsech tlacitek v rozhrani
        self.button_yes = tk.Button(self, text="OK", command=self.yes_click, font=self.my_font)
        self.button_yes.grid(row=1, column=3, sticky='NW', padx=5)

        self.button_next = tk.Button(self, text='==>', command=self.next_click, font=self.my_font)
        self.button_next.grid(row=2, column=2)

        self.button_previous = tk.Button(self, text='<==', command=self.previous_click, state='disabled', font=self.my_font)
        self.button_previous.grid(row=2, column=1)

    def make_entries(self):
        # definice vsech entry v rozhrani
        self.entry_tyden = tk.Entry(self, font=self.my_font, width=10)
        self.entry_tyden.grid(row=1, column=1, columnspan=2, padx=5)
        self.entry_tyden.insert(0, '1')

    def next_click(self):
        # funkce tlacitka zvysujici hodnotu tydne

        # zmena hodnoty v entry
        next_week = int(self.entry_tyden.get()) + 1
        self.entry_tyden.delete(0, tk.END)
        self.entry_tyden.insert(0, str(next_week))

        # pripadne vypnuti a zapnuti tlacitek
        self.button_previous['state'] = 'active'
        if next_week == datetime.date.today().isocalendar()[1]:
            self.button_next['state'] = 'disabled'
            
    def previous_click(self):
        # funkce tlacitka snizujici hodnotu tydne

        # zmena hodnoty v entry
        previous_week = int(self.entry_tyden.get()) - 1
        self.entry_tyden.delete(0, tk.END)
        self.entry_tyden.insert(0, str(previous_week))

        # pripadne vypnuti a zapnuti tlacitek
        self.button_next['state'] = 'active'
        if previous_week == 1:
            self.button_previous['state'] = 'disabled'

    def yes_click(self):
        # funkce pro zobrazeni grafu na zaklade precteni entry

        # nacteni linku
        try:
            used_url = "http://www.sazka.cz/system/vyherka?year=2020&week={}&game=kasicka".format(self.entry_tyden.get())
            raw_data = pd.read_html(used_url)

            # vybrani potrebnych sloupcu a procisteni od NA
            data = raw_data[3][[1, 2, 3, 4, 5, 6]].dropna()

            # vytvoreni value_counts pro cely dataframe
            v_count = pd.Series([], dtype=np.int8)
            for c in data.columns:
                v_count = v_count.add(data[c].value_counts(), fill_value=0)

            # vytvoreni figure
            fig = plt.Figure(figsize=(10, 8), dpi=100)
            fig.suptitle("Čísla tažená v {}. týdnu".format(self.entry_tyden.get()))

            # vizualizace grafu
            ax = fig.add_subplot(1, 1, 1)
            data = v_count.sort_values()
            ax.bar(list(map(str, data.index.astype(int))), data.values)
            ax.tick_params(axis='x', rotation=50)
            canvas = FigureCanvasTkAgg(fig, self)
            canvas.get_tk_widget().grid(row=0, column=4, rowspan=100)
            self.print_error("")
        except IndexError:
            self.print_error("TÝDEN NEEXISTUJE!")
        except Exception:
            self.print_error("TÝDEN ZADÁN VE ŠPATNÉM FORMÁTU!")


    def print_error(self, message):
        self.label_error.configure(text=message)

if __name__ == '__main__':
    main_win = Root()

    main_win.mainloop()


    ### toto je nove
    print('babababa')
