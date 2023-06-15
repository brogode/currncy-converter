#---------------------------------------------------------------------
#this are all the imports you need
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from  matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import customtkinter

import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
#-------------------------------------------------------------------------

#here is were we difine our univesal fornt size and the style of our graph
LARGE_FONT = ('Verdana', 12)
style.use('ggplot')
#---------------------------------------------------------------

#below is the variable that comtraise all the currency
options = ["AED","AFN","AMD","ANG","AOA","ARS","AUD","AWG","AZN","BAM","BBD","BDT","BGN","BHD","BIF","BMD","BND","BOB",
           "BRL","BTN","BWP","BYN","BZD","2CDF","CHF","CLP","CNY","COP","CRC","CUP","CVE","CZK","DJF","DKK","DOP","DZD",
           "EGP","ERN","ETB","EUR","FJD","FKP","FOK","GBP","GEL","GGP","GHS","GIP","GMD"
           ,"GNF","GTQ","GYD","HKD","HNL","HRK","HTG","HUF","IDR","ILS","IMP","INR","IQD"
           ,"IRR","ISK","JEP","JMD","JOD","JPY","KES","KGS","KHR","KID","KMF","KRW","KWD","KYD","KZT"
           ,"LAK","LBP","LKR","LRD","LSL","LYD","MAD","MDL","MGA","MKD","MMK","MNT","MOP","MRU"
           ,"MUR","MVR","MWK","MXN","MYR","MZN","NAD","NGN","NIO","NOK","NPR","NZD","OMR","PAB","PEN","PGK","PHP",
           "PKR","PLN","PYG","QAR","RON","RSD","RUB","RWF","SAR","SBD","SCR","SDG","SEK","SGD","SHP","SLE","SOS","SRD","SSP","STN","SYP",
           "SZL","THB","TJS","TMT","TND","TOP","TRY","TTD","TVD","TWD","TZS","UAH","UGX","USD","UYU","UZS","VES","VND","VUV","WST",
           "XAF","XCD","XDR","XOF","XPF","ZAR","ZMW","ZWL"]

#----------------------------------------------------

#there we difine the size our graph is going to take and were we are going to plot
f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)
#----------------------------------------------------

#there is the fucntion that plots the graph

def get_yearly_rates(amount, currency, converted_currency, amount_of_days):
    today_date = datetime.datetime.now()
    date_1year = (today_date - datetime.timedelta(days=1 * amount_of_days))

    url = f'https://api.exchangerate.host/timeseries'
    payload = {'base': currency, 'amount': amount, 'start_date': date_1year.date(),
               'end_date': today_date.date()}
    reponse = requests.get(url, params=payload)
    data = reponse.json()

    # CREATING DATE STORAGE
    currency_history = {}
    rate_history_array = []

    for item in data['rates']:
        current_date = item
        currency_rate = data['rates'][item][converted_currency]

        currency_history[current_date] = [currency_rate]
        rate_history_array.append(currency_rate)

    pd_data = pd.DataFrame(currency_history).transpose()
    pd_data.columns = ['rates']
    pd.set_option('display.max_rows', None)
    print(pd_data)


    a.clear()
    a.plot(rate_history_array)

    title = (f'Current rate for {amount} {currency} to {converted_currency} is {rate_history_array[-1]}')
    a.set_title(title)

    # Add the ball to the plot
    ball, = a.plot([], [], 'o', color='r')

    # Define the animation function
    def animate(i):
        # Get the rate for the current animation frame
        rate = rate_history_array[i]

        # Calculate the x and y coordinates for the ball
        x = i
        y = rate

        # Update the position of the ball
        ball.set_data(x, y)

        return ball,

    # Create the animation object
    anim = animation.FuncAnimation(f, animate, interval=500)

    # Create the canvas and add it to the frame
    canvas = FigureCanvasTkAgg(f)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

#--------------------------------------------------------------------------

#here is the master class the will be inherited buy other classis and where they will get all their propatise

class Currency_Converter(tk.Tk):
    def __init__(self, *args, **kwargs ):
        tk.Tk.__init__(self, *args, **kwargs)

        #-----------------------------
         #there we define the frame

        #tk.Tk.iconbitmap(self, default='currency.png')
        tk.Tk.wm_title(self, 'Currency Converter')


        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0 , weight=1)
        container.grid_columnconfigure(0, weight=1)

       #this will help us move from the sart page to the main page
        self.frames = {}

        for k in (PageOne,StartPage):
            frame = k(container, self)

            self.frames[k] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.label = ttk.Label(self, text='Start upp', font=LARGE_FONT)
        self.label.pack(pady=10,padx=10)

        self.button1 = ttk.Button(self, text='Visite page 1', command=lambda :controller.show_frame(PageOne) )
        self.button1.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        #------------------------------------
        #below is the top frame
        frame = tk.Frame(self, height=120, width=180, bg='#ff9912', bd=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.pack(fill='both', expand=True)

        #--------------------------------

        self.label = ttk.Label(frame, text='Page One', font=LARGE_FONT)
        self.label.pack(pady=10, padx=10)

        self.button1 = customtkinter.CTkButton(frame, text='Visite start up page',
                                          command=lambda: controller.show_frame(StartPage))
        self.button1.pack()

        self.button2 = tk.Button(frame)
        self.button2.pack(padx=400, pady=80)

        self.from_lable = customtkinter.CTkLabel(frame, text='From', font=('Arial', 15, 'bold'), bg_color='#ff9912')
        self.from_lable.place(relx=0.3, rely=0.1)
        self.from_list = ttk.Combobox(frame, values=options,  font=('Arial', 12, 'bold'),width=4)
        self.from_list.place(relx=0.3,rely=0.2)
        self.convert_bnt = customtkinter.CTkButton(frame, text='Cornvert', font=LARGE_FONT, command=lambda :convert())
        self.convert_bnt.place(relx=0.3, rely=0.7)

        self.entry = ttk.Entry(frame, font=('arial',20,'bold'),width=15)
        self.entry.place(relx=0.35,rely=0.4)

        self.lable2 = customtkinter.CTkLabel(frame, text='To', font=('Arial', 15, 'bold'), bg_color='#ff9912')
        self.lable2.place(relx=0.6, rely=0.1)
        self.To_list = ttk.Combobox(frame,values=options,font=('Arial', 12, 'bold'), width=4)
        self.To_list.place(relx=0.6, rely=0.2)
        self.button3 = customtkinter.CTkButton(frame, text='Reset', font=('Arial', 12, 'bold'), command=lambda :reset(),)
        self.button3.place(relx=0.6, rely=0.7)

        #-----------------------------------------------
        #the spliting frame
        split_frame =tk.Frame(self,bg='#CD2626' , height=30)
        split_frame.pack(side=tk.TOP, expand=True, fill='both')

        #----------------------------------------------------------
        #the side Frame

        side_frame = tk.Frame(self, bg='#710193', bd=1, width=50, height=850)
        side_frame.pack(side=tk.LEFT ,fill='both')

        self.side_from = ttk.Combobox(side_frame, width=10,values=options)
        self.side_from.pack(side=tk.LEFT, padx=3)

        self.side_to = ttk.Combobox(side_frame, width=10, values=options)
        self.side_to.pack(side=tk.LEFT, padx=80)

        self.graph_lable= ttk.Label(side_frame, text='Put the curencs on the graph', font=('arial', 12))
        self.graph_lable.place(relx=0.01,rely=0.4)

        self.update_graph = customtkinter.CTkButton(side_frame, text='Update Graph', command=lambda :graph_update())
        self.update_graph.place(rely=0.6,relx=0.13)


        #function to reset the text box
        def reset():
            self.entry.delete(0 ,'end')


        #function for the conversion button
        def convert():

            try:
                currency_history = {}
                from_currency = self.from_list.get()
                to_currency = self.To_list.get()
                amount = self.entry.get()

                today_date = datetime.datetime.now()
                date_1year = (today_date - datetime.timedelta(days=1))

                url = f'https://api.exchangerate.host/timeseries'
                payload = {'base': from_currency, 'amount': amount, 'start_date': today_date.date(),
                           'end_date': today_date.date()}
                reponse = requests.get(url, params=payload)
                data = reponse.json()

                currency_history = {}
                rate_history_array = []

                for item in data['rates']:
                    current_date = item
                    currency_rate = data['rates'][item][to_currency]

                    currency_history[current_date] = [currency_rate]
                    rate_history_array = currency_rate
                txt=str(rate_history_array)
                self.convertedvalue = ttk.Label(frame, text=txt, font=('Arial', 15, 'bold'))
                self.convertedvalue.place(relx=0.48, rely=0.85)
            except:
                self.error ='Please enter the currency or you wish to Convert'
                messagebox.showerror(title='ERROR', message='Please enter the currency or you wish to Convert')



        #fuction for the update graph button
        def graph_update():
            try:
                amount = 1
                currency = self.side_from.get()
                converted_currency = self.side_to.get()
                amount_of_days = 30
                anim = animation.FuncAnimation(f, get_yearly_rates(amount, currency, converted_currency, amount_of_days), interval=5000)

                canvas.draw()
            except:
                messagebox.showerror(title='ERROR', message='Please enter the currecys you want the graph to show')

        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        anim = animation.FuncAnimation(f, get_yearly_rates(1, 'EUR', 'GBP', 30), interval=5000)






app = Currency_Converter()
app.geometry('800x720')
app.mainloop()

