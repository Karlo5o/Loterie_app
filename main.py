import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.font import Font
from bs4 import BeautifulSoup
import requests





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
        self.my_font_smaller = Font(size=11)
        self.iconbitmap('D:\\Python\\Projects\\fun_with_data\\cash_icon.ico')
        self.radio_var = tk.StringVar()
        self.radio_var.set('Kasička')

        # vykresleni rozhrani
        self.make_frames()
        self.make_labels()
        self.make_buttons()
        self.make_entries()
        self.make_radiobuttons()


        self.bind('<Return>', lambda a: self.yes_click())


    def make_frames(self):
        # definice vsech framu v rozhrani

        self.frame_main = tk.LabelFrame(padx=5, pady=5)
        self.frame_main.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=tk.E + tk.W + tk.N)

        self.frame_error = tk.LabelFrame(padx=5, pady=5, text='Chybové hlášení')
        self.frame_error.grid(row=2, column=0, rowspan=1, columnspan=3, padx=10, pady=10, sticky = tk.W + tk.E + tk.S)

        self.frame_graph = tk.LabelFrame(padx=1, pady=1, text='Sloupcový graf')
        self.frame_graph.grid(row=0, column=3, rowspan=3, padx=10, pady=10)

        self.frame_draws = tk.LabelFrame(padx=10, pady=10, text="Výsledky v daných kolech")
        self.frame_draws.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky = tk.W + tk.E)

        self.frame_radio = tk.LabelFrame(padx=5, pady=5, text='Výběr loterie')
        self.frame_radio.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky=tk.E + tk.W + tk.N)



    def make_labels(self):
        # definice vsech labelu v rozhrani
        act_date = datetime.date.today().isocalendar()[1]
        date_text = "Současný týden: " + str(act_date)


        self.label_date = tk.Label(self.frame_main, text=date_text, bd=5, font=self.my_font)
        self.label_date.grid(row=0, column=3, sticky=tk.N)

        self.label_tyden = tk.Label(self.frame_main, text="Týden", bd=1, font=self.my_font)
        self.label_tyden.grid(row=0, column=1, columnspan=2, sticky=tk.N)

        self.label_error = tk.Label(self.frame_error, text="", font=self.my_font, fg="Red")
        self.label_error.grid(row=3, column=1, columnspan=3, rowspan=4, sticky=tk.N)


    def make_buttons(self):
        # definice vsech tlacitek v rozhrani
        self.button_yes = tk.Button(self.frame_main, text="OK", command=self.yes_click, font=self.my_font)
        self.button_yes.grid(row=1, column=3, sticky=tk.N, padx=5)

        self.button_next = tk.Button(self.frame_main, text='==>', command=self.next_click, font=self.my_font)
        self.button_next.grid(row=2, column=2, sticky=tk.N)

        self.button_previous = tk.Button(self.frame_main, text='<==', command=self.previous_click, state='disabled', font=self.my_font)
        self.button_previous.grid(row=2, column=1, sticky=tk.N)

    def make_entries(self):
        # definice vsech entry v rozhrani
        self.entry_tyden = tk.Entry(self.frame_main, font=self.my_font, width=10)
        self.entry_tyden.grid(row=1, column=1, columnspan=2, padx=5)
        self.entry_tyden.insert(0, '1')

    def make_radiobuttons(self):
        possibilities = ["Kasička", "Sportka", "EuroMiliony"]
        for p in possibilities:
            tk.Radiobutton(self.frame_radio, variable=self.radio_var, text=p, value=p, font=self.my_font).pack(side=tk.LEFT)



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

    def kasicka(self):


        used_url = "http://www.sazka.cz/system/vyherka?year=2020&week={}&game=kasicka".format(
            self.entry_tyden.get())
        raw_data = pd.read_html(used_url)

        # vybrani potrebnych sloupcu a procisteni od NA
        data = raw_data[3][[0, 1, 2, 3, 4, 5, 6]].dropna()

        # vytvoreni value_counts pro cely dataframe
        v_count = pd.Series([], dtype=np.int8)

        for c in data.columns[1:]:
            v_count = v_count.add(data[c].value_counts(), fill_value=0)

        self.draws = []
        draw = []  # vytvoreni promenne, ktera nese datum a pote dve losovani z toho data
        for d in data.values:
            if not draw:
                draw.append(d[0][:-5])  # pridani data

            time = d[0][-5:]
            values = d[1:].astype(int).astype(str)
            values = ", ".join(values)
            draw.append(time + ': ' + values)
            if len(draw) == 3:
                self.draws.append(draw)
                draw = []
        if len(draw) == 2:
            draw.append("")
            self.draws.append(draw)
        self.print_draws()

        # vytvoreni figure
        fig = plt.Figure(figsize=(10, 6), dpi=100)
        fig.suptitle("Čísla tažená v {}. týdnu".format(self.entry_tyden.get()))

        # vizualizace grafu
        ax = fig.add_subplot(1, 1, 1)
        data_graph = v_count.sort_values()
        ax.bar(list(map(str, data_graph.index.astype(int))), data_graph.values)
        ax.tick_params(axis='x', rotation=50)
        canvas = FigureCanvasTkAgg(fig, self.frame_graph)
        canvas.get_tk_widget().grid(row=0, column=4, rowspan=8)
        self.print_error("")


    def sportka(self):


        url = "https://www.sazka.cz/system/vyherka?year=2020&week={}&game=sportka".format(self.entry_tyden.get())
        raw_data = pd.read_html(url)


        # nalezeni potrebnych useku v html
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.findAll("tr", {"class": "loscisla sans"})
        date = soup.findAll("span", {"class": "spn s18b"})


        # vymazani framu, aby v nich nebyly nechane data z minula


        # iterovani skrze tabulky, pokud je len(table) == 3, pak je jen jedno slosovani v tydnu, pokud == 6, pak jsou dve
        for i in range(len(table)//3):
            draw1 = table[3*i].text.strip().split()[2:]
            draw2 = table[3*i+1].text.strip().split()[2:]
            chance = table[3*i+2].text.strip().split()
            single_draw_frame = tk.LabelFrame(self.frame_draws, padx=5, pady=5, text=date[2 * i].text)

            single_draw_frame.pack(side=tk.LEFT)

            l1 = tk.Label(single_draw_frame, text="1.tah: " + ", ".join(draw1[:-1]) + ' |' + draw1[-1], font=self.my_font_smaller)
            l2 = tk.Label(single_draw_frame, text="2.tah: " + ", ".join(draw2[:-1]) + ' |' + draw2[-1], font=self.my_font_smaller)
            l3 = tk.Label(single_draw_frame, text="Šance: " + "".join(chance), font=self.my_font_smaller)

            l1.grid(row=0, column=0, sticky=tk.W)
            l2.grid(row=1, column=0, sticky=tk.W)
            l3.grid(row=2, column=0, sticky=tk.W)



    def euromiliony(self):

        url = "https://www.sazka.cz/system/vyherka?year=2020&week={}&game=euromiliony".format(self.entry_tyden.get())
        data = pd.read_html(url)

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        table = soup.findAll("tr", {"class": "loscisla sans"})
        date = soup.findAll("span", {"class": "spn s18b"})

        for i in range(len(table) // 2):
            draw = table[2 * i].text.strip().split()
            chance = table[2 * i + 1].text.strip().split()

            single_draw_frame = tk.LabelFrame(self.frame_draws, padx=5, pady=5, text=date[i].text)

            single_draw_frame.pack(side=tk.LEFT)

            l1 = tk.Label(single_draw_frame, text="1. osudí: " + ", ".join(draw[:-1]),
                          font=self.my_font_smaller)
            l2 = tk.Label(single_draw_frame, text= '2. osudí: ' + draw[-1],
                          font=self.my_font_smaller)
            l3 = tk.Label(single_draw_frame, text="Eurošance: " + "".join(chance), font=self.my_font_smaller)

            l1.grid(row=0, column=0, sticky=tk.W)
            l2.grid(row=1, column=0, sticky=tk.W)
            l3.grid(row=2, column=0, sticky=tk.W)

        print()


    def yes_click(self):
        # funkce pro zobrazeni grafu na zaklade precteni entry

        try:

            # vymazani predchozich widgetu
            for w in self.frame_draws.winfo_children():
                w.destroy()

            for w in self.frame_graph.winfo_children():
                w.destroy()

            # nacteni linku
            if self.radio_var.get() == 'Kasička':
                self.kasicka()
            elif self.radio_var.get() == 'Sportka':
                self.sportka()
            else:
                self.euromiliony()



        except IndexError:
            self.print_error("TÝDEN NEEXISTUJE!")
        except ValueError:
            self.print_error("TÝDEN ZADÁN VE ŠPATNÉM FORMÁTU!")
        except ImportError:
            self.print_error("ŠPATNÝ FORMÁT TÝDNE!")
        except OSError:
            self.print_error("NEJSTE PŘIPOJEN K INTERNETU!")



    def print_draws(self):


        for date, draw1, draw2 in self.draws:

            f = tk.LabelFrame(self.frame_draws, padx=5, pady=5, text=date, )
            f.pack(side=tk.LEFT)

            l1 = tk.Label(f, text=draw1, font=self.my_font_smaller)
            l2 = tk.Label(f, text=draw2, font=self.my_font_smaller)

            l1.grid(row=0, column=0, sticky=tk.W)
            l2.grid(row=1, column=0, sticky=tk.W)


    def print_error(self, message):
        self.label_error.configure(text=message)

if __name__ == '__main__':
    main_win = Root()

    main_win.mainloop()


    ### toto je nove
    print('babababa')
