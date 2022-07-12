
import tkinter as tk
import tkinter.ttk as ttk
from turtle import window_height, window_width
from PIL import ImageTk, Image
from itertools import zip_longest
import json, random, hashlib
import matplotlib.pyplot as plt
import collections, os
import numpy as np
from datetime import datetime

pos_num = ("1","2","3","4","5","6","7","8","9")
pos_alp = tuple("a b c d e f g h i j k l m n o p q r s t u v w x y z".split())
pos_sym = tuple("/ ( [ ) ] } ? ! - . ; :".split())
pos = pos_num + pos_alp + pos_sym
change = 11

def encode(string, key):
        lst = []
        for x in string:
            if ord(x) + key <= 122 and ord(x) >= 97:    lst.append(chr(ord(x) + key))
            elif ord(x) + key > 122 and ord(x) >= 97:   lst.append(chr(96 + (ord(x) - 122 + key)))
            elif ord(x) + key <= 59 and ord(x) >= 40:    lst.append(chr(ord(x) + key))
            elif ord(x) + key > 59 and ord(x) >= 40:    lst.append(chr(39+ (ord(x) - 59 + key)))
            else:   lst.append(x)
        return "".join(lst)
def decode(string, key):
        lst = []
        for x in string:
            if ord(x) - key >= 97 and ord(x) <= 122 :   lst.append(chr(ord(x) - key))
            elif ord(x) - key < 97 and ord(x) >= 97 and ord(x) <= 122:  lst.append(chr(123 + (ord(x) - 97 - key)))
            elif ord(x) - key >= 40 and ord(x) <= 59:   lst.append(chr(ord(x) - key))
            elif ord(x) - key < 40 and ord(x) <= 59:    lst.append(chr(60 + (ord(x) - 40 - key)))
            else:   lst.append(x)
        return "".join(lst)

class Basement(tk.Tk):
 
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(width=0,height=0)
        self.style = ttk.Style(self)
        self.stringvar = tk.StringVar()

        self.title("Robins PW-Manager Gui")
        
        self.change_root_size(150, 400)
        self.look_for_style()
        
        self.login_frame = Login_Frame(self)
        self.login_frame.grid(column=0,
                              row=0,
                              sticky="nsew")
        self.login_function()
        
        self.pwd_frame = ttk.Frame(self)
        self.pwd_frame.grid(column=0,row=0, sticky = "nsew")
        
        self.upper_frame = Upper_Frame(self.pwd_frame)
        self.upper_frame.grid(column= 0,
                              row= 0,
                              columnspan= 3)
        
        self.lower_frame = Lower_Frame(self.pwd_frame)
        self.lower_frame.grid(column=0,
                              row=1)
        
        self.all_pwd_frame = ttk.Frame(self)
        self.all_pwd_frame.grid(column=0, row = 0, sticky = "nsew")
        
        self.login_frame.tkraise()
        
        self.menu = tk.Menu(self)
        self.configure(menu=self.menu)
        self.menu_fuc()
 
    def look_for_style(self):
        try:
            with open("stored_them.txt", "r") as f:
                theme = f.read()
                theme = theme.strip()
                self.style.theme_use(theme)
                self.stringvar.set(value = theme)
        except:
            pass #no theme selected yet
    
    def menu_fuc(self):
        self.menufile = tk.Menu(self.menu)
        self.menufile.add_command(label = "Quit", command = self.quit)
        self.menu.add_cascade(label="Menu", menu = self.menufile)
    
    def style_func(self):
        toplevel = tk.Toplevel(self)
        img = Image.open("style-me-logo-original.png").resize((300,100))
        self.iamg= ImageTk.PhotoImage(img)
        
        window_width = 300
        window_height = 300
        x_cordinate = (2560/2) - (window_width/2)
        y_cordinate = (1440/2) - (window_height/2)
        toplevel.geometry(f"300x250+{int(x_cordinate)}+{int(y_cordinate)}")
        toplevel.title("Styles")
        
        self.style_frame = ttk.Frame(toplevel)
        self.style_frame.grid(column=0,row=0,sticky="nsew")
        
        ttk.Label(self.style_frame,
                  text="",
                  font = ("Arial",25),
                  image=self.iamg,
                  compound="center").grid(column=0,columnspan=2,row=0)
        
        for y,x in enumerate(self.style.theme_names()):
            tk.Radiobutton(self.style_frame,
                           indicatoron = 0,
                           variable=self.stringvar,
                           text= f"Stye: {x}",
                           value = x,
                           command= self.store_theme
                           ).grid(column=0, row=y+1, sticky = "w", padx = 8, pady = 4)
            
    def pwd_security(self):
        #creating a diagramm wich represents the length and quantity such as the quality of the passwords 
        try:
            os.remove("Plt.png")
        except:
            pass #file not made yet...
        root = tk.Toplevel(self)
        window_height = 400
        window_width = 500
        x_cordinate = (2560/2) - (window_width/2)
        y_cordinate = (1440/2) - (window_height/2)
        root.geometry(f"500x400+{int(x_cordinate)}+{int(y_cordinate)}")
        with open("test.json", "r") as f:
            dic = json.load(f)
            
            pwds = [len(x[0]) for x in dic.values()]
            
            coldic = collections.Counter()
            for x in pwds:
                coldic[str(x)] += 1 
            quantitys = []    
            fig,ax = plt.subplots()
            for length,quantity in coldic.items():
                length = int(length)
                if length <= 5: color = "Red"
                elif length <= 10: color = "Orange"
                elif length > 10: color = "Green"
                quantitys.append(quantity)
                
                ax.bar(length,quantity, linewidth=0.9,color = color)
            
            plt.xlabel("Password lengths")
            plt.ylabel("Quantity of passwords")
            ax.yaxis.set_ticks(np.arange(0,max(quantitys)+2, 1))
            plt.savefig("Plt.png", bbox_inches = "tight")
            
        img = Image.open("Plt.png").resize((500,400))
        self.image123 = ImageTk.PhotoImage(img)
        ttk.Label(root, image=self.image123).grid(sticky = "n",column=0,row=0)
    
    def store_theme(self):
        with open("stored_them.txt", "w") as f:
            f.write(self.stringvar.get())
        self.style.theme_use(self.stringvar.get())             
                   
    def see_all_pwds(self):
        self.get_all_pwds()
        pwd_names = [x[0] for x in self.all_pwds]
        pwds = [decode(x[1][0], x[1][3]) for x in self.all_pwds]
        mails = [x[1][1] for x in self.all_pwds]
        time_stamps = [x[1][2] for x in self.all_pwds]
        columns = ("Password_Name", "Password", "Additional_Infos", "Time_Stamp")
        self.pwd_tree = ttk.Treeview(self.all_pwd_frame,columns=columns, show="headings")
        
        self.pwd_tree.heading("Password_Name", text="Password Name")
        self.pwd_tree.heading("Password", text="Password")
        self.pwd_tree.heading("Additional_Infos", text="Additional Infos")
        self.pwd_tree.heading("Time_Stamp", text = "Time stamp")
        
        self.pwd_tree.column("Password_Name",width=123)
        self.pwd_tree.column("Password",width=180)
        self.pwd_tree.column("Additional_Infos", width=200)
        self.pwd_tree.column("Time_Stamp", width = 170)
        
        self.pwd_tree.bind("<Double-1>", lambda event: self.copyit())
        self.pwd_tree.bind("<Triple-1>", lambda event: self.copyit2())
        
        for x in range(len(pwd_names)):
            self.pwd_tree.insert("",index=tk.END, values = [pwd_names[x], pwds[x], mails[x], time_stamps[x]])
        self.pwd_tree.grid(column=0,row=0)
        ttk.Label(self.all_pwd_frame, text="Double click the line to store the Password to Clipboard!", font = ("Arial", 17)).grid(column=0, row= 1)
        ttk.Label(self.all_pwd_frame, text="Triple click the line to store the Additional informaitions to Clipboard!", font = ("Arial", 17)).grid(column=0, row = 2)
        self.all_pwd_frame.tkraise()

    def get_all_pwds(self):
        self.all_pwds = []
        with open("test.json", "r") as pwds:
            json_file = json.load(pwds)
            for name,values in json_file.items():
              self.all_pwds.append((name, values))
              
    def copyit(self):
        item = self.pwd_tree.selection()[0]
        self.pinged_pwd = self.pwd_tree.item(item)["values"][1]
        self.clipboard_clear()
        self.clipboard_append(self.pinged_pwd)
        self.update()
        
    def copyit2(self):
        item = self.pwd_tree.selection()[0]
        item_mail = self.pwd_tree.item(item)["values"][2]
        self.clipboard_clear()
        self.clipboard_append(item_mail)
        self.update()
     
    def login_function(self):
        self.count = 0
        self.imag = Image.open("860x394.png").resize((350,75))
        self.img = ImageTk.PhotoImage(self.imag)
        ttk.Label(self.login_frame,
                  text="Login",
                  foreground="#35BCFF",
                  font= ("Arial", 23),
                  image= self.img,
                  compound="center"
                  ).grid(column=0, row =0, columnspan=3, sticky = "we") 
        
        ttk.Label(self.login_frame,
                  text = "Please enter your password:       "
                  ).grid(column=0, row = 1, sticky = "w", pady = 5)
        
        self.password_var = tk.StringVar(value="Your Password")
        
        self.password_entry = ttk.Entry(self.login_frame,
                                        width= 15,
                                        textvariable = self.password_var)
        self.password_entry.grid(column= 1,
                                 row = 1,
                                 sticky = "we",
                                 pady = 5)
        
        self.show_hide_var = tk.StringVar(value="Show\npwd")
        self.show_hide_button = ttk.Button(self.login_frame,
                                           width=5,
                                           textvariable= self.show_hide_var,
                                           command = self.change_show)
        self.show_hide_button.grid(column= 2,
                                 row = 1,
                                 padx = 5,
                                 pady = 5,
                                 rowspan=2,
                                 sticky = "news")
        
        
        self.send_pwd = ttk.Button(self.login_frame,
                                   text="send_pwd",
                                   command= self.pwd_control )
        self.send_pwd.grid(row = 2,
                           column = 1,
                           sticky = "we")
        
        self.password_entry.bind("<FocusIn>",lambda x: self.little_work())
    
        self.trys = tk.IntVar(value=3)
        self.innerframe = ttk.Frame(self.login_frame)
        self.innerframe.grid(row = 2, column= 0, sticky = "w")
        self.counter = ttk.Entry(self.innerframe,
                                 textvariable=self.trys,
                                 width = 1,
                                 state = "disabled"
                                 ).grid(row = 0, column=1)
        self.label = ttk.Label(self.innerframe,
                               text="Trys until logout:"
                               ).grid(row=0, column=0)
 
    def change_show(self):
        if self.show_hide_var.get() == "Show\npwd":
            self.password_entry.destroy()
            self.password_entry = ttk.Entry(self.login_frame,
                                        width= 15,
                                        textvariable = self.password_var)
            self.password_entry.grid(column= 1,
                                 row = 1,
                                 sticky = "we",
                                 pady = 5)
            self.show_hide_var.set(value="Hide\npwd")
        else:
            self.password_entry["show"] = "*"
            self.show_hide_var.set(value="Show\npwd")
        
    def little_work(self):
        if self.count == 0:
            self.password_var.set("")
            self.count += 1
        self.password_entry.configure(show="*")

    def pwd_control(self):
        if hashlib.md5(bytes(self.password_var.get(), "utf-8")).hexdigest() == "676c917c347c186c1efaaedca2692e58":
            self.pwd_frame.tkraise()
            self.menufile.add_command(label="See all passwords", command = self.see_all_pwds)
            self.menufile.add_command(label = "Home", command = self.change_back)
            self.menufile.add_command(label="Style", command = self.style_func)
            self.menufile.add_command(label= "Pwd_Security", command = self.pwd_security)
            self.geometry("670x450")
        if self.trys.get() == 0:
            self.destroy()
        else: self.trys.set(self.trys.get() - 1)
        
    def change_back(self):
        self.pwd_frame.tkraise()
        
    def change_root_size(self,window_height:int, window_width: int):
        x_cordinate = (2560/2) - (window_width/2)
        y_cordinate = (1440/2) - (window_height/2)
        self.geometry("{}x{}+{}+{}".format(window_width, window_height, int(x_cordinate), int(y_cordinate)))
        
        
class Upper_Frame(ttk.Frame):
 
    def __init__(self,container, *args,**kwargs):
        super().__init__(container,*args,**kwargs)
        self.columnconfigure(0, weight=1)
        
        self.image_long = Image.open("home_pic.jpeg").resize((600,155))
        self.image = ImageTk.PhotoImage(self.image_long)
        
        ttk.Label(
                    self,
                    text = "Password Manager",
                    font = ("Arial", 23),
                    image = self.image,
                    compound = "center",
                    foreground= "Black",
                ).grid(column=0, row=0, padx = 30, pady = 20)


class Lower_Frame(ttk.Frame):

    def __init__(self,container, *args,**kwargs):
        super().__init__(container,*args,**kwargs)
        self.Frameread = Frame_read(container)
        self.Framewrite = Frame_write(container)
        self.Framesave = Save_pwd_Frame(container)
        
        self.value = tk.StringVar()

        self.radiobutton_get = ttk.Radiobutton(self,
                                               text = "Make a password!",
                                               value="0",
                                               variable=self.value,
                                               command = lambda: self.switch_frame(Frame_write)
                                               ).grid(row=0,column=0,sticky ="w")
        
        self.radiobutton_give = ttk.Radiobutton(self,
                                                text ="Get a password!",
                                                value="1",
                                                variable=self.value,
                                                command = lambda: self.switch_frame(Frame_read)
                                                ).grid(row=1,column=0, sticky="w")
        self.radiobutton_make = ttk.Radiobutton(self,
                                                text ="Save a password!",
                                                value="2",
                                                variable=self.value,
                                                command = lambda: self.switch_frame(Save_pwd_Frame)
                                                ).grid(row=2,column=0, sticky="w")

        self.windows = {Frame_read:self.Frameread, Frame_write: self.Framewrite, Save_pwd_Frame:self.Framesave }
        
    def switch_frame(self, frame):
        self.Frame = self.windows[frame]
        self.Frame.grid(column = 0, row = 2, sticky="NSEW")
        self.Frame.tkraise()

        
class Frame_read(ttk.Frame):
 
    def __init__(self, container):
        super().__init__(container)
        self.root = container
        self.wich_read = ttk.Label(self,
                                   text = "PW Name:",
                                   font=("Arial", 20))
        self.wich_read.grid(column=0,
                            row=0,
                            sticky ="w")
        
        self.inputVar = tk.StringVar()
        self.wich_entry = ttk.Entry(self,
                                    textvariable = self.inputVar
                                    ).grid(column=1, row=0)
        
        self.Button = ttk.Button(self, text="Look for password", command =self.lfpwd)
        self.Button.grid(column = 0, row = 1, sticky = "w", padx = 4)
        
        self.output_pw = ttk.Label(self,
                                text = "Your Password:",
                                font=("Arial", 20))
        self.output_pw.grid(column=0,
                         row=2,
                         sticky ="w")
        self.output_mail = ttk.Label(self,
                                     text = "Your Mail/Username:",
                                     font=("Arial", 20))
        self.output_mail.grid(column=0,row=3)
         
        self.outputvar = tk.StringVar()
        self.outputvar_mail = tk.StringVar()
        self.output_pw_entry = ttk.Entry(self,
                                      textvariable = self.outputvar
                                      ).grid(column=1, row=2)
        self.output_mail_entry = ttk.Entry(self,
                                           textvariable=self.outputvar_mail
                                           ).grid(column=1, row=3)
    
    def lfpwd(self):
        if self.inputVar.get() == "":
            self.top = tk.Toplevel(self.root)
            self.top.geometry("200x100")
            self.top.title("Error")
                    
            ttk.Label(self.top,
                    text  = "Password name is empty,\nplease give a name to it!"
                    ).grid(column = 0, row = 0)
            
            button_ok = ttk.Button(self.top,
                                    text="OK",
                                    command = self.top.destroy
                                    ).grid(column= 0, row =1, padx = 10)
            return
        with open("test.json", "r") as Json:
            json_file = json.load(Json)
            your_pwd = json_file[self.inputVar.get()]
            pwd_decoded = decode(your_pwd[0], your_pwd[3])
            self.outputvar.set(pwd_decoded)
            self.outputvar_mail.set(your_pwd[1])
            

class Frame_write(ttk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        self.root = container
        self.change = 11
        self.pwd_len_label = ttk.Label(self,
                                       text = "Enter Password length:",
                                       font=("'Helvetica 15 underline')", 20),
                                       foreground="purple"
                                       ).grid(row = 0, column = 0, padx = 13)
         
        self.pwd_name = tk.StringVar()
        
        self.pwd_len_var = tk.IntVar(value=10)
        self.pwd_len_entry = ttk.Entry(self,
                                       textvariable=self.pwd_len_var,
                                       font=("Arial",13),
                                       width=4
                                       ).grid(row = 0, column = 1, sticky = "w", padx = 35)
        
        self.save_input_len_button = ttk.Button(self,
                                           text = "Save your input",
                                           command = self.pwd_gen
                                           ).grid(row = 3, column = 0, sticky="we", padx=8, pady = 12)
        
        self.label_npwd_name = ttk.Label(self,
                                         text="PWD Name:"
                                         ).grid(row=1,column=0)
        
        self.entry_npwd_name = ttk.Entry(self,
                                         textvariable = self.pwd_name
                                         ).grid(row=1, column=1)
        self.mail_label = ttk.Label(self, text = "Your mail adress/Username: ").grid(row = 2, column = 0)
        self.mail_var = tk.StringVar()
        self.mail_entry = ttk.Entry(self, textvariable = self.mail_var).grid(row= 2 , column = 1)
        
        self.new_pwd_label = ttk.Label(self,
                                       text=  "Your new Password:",
                                       font= ("Arial", 17)
                                       ).grid(row=4, column= 0)
        
        self.pwd_scroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.pwd_scroll.grid(row = 5, column=1, sticky="ew")
        self.pwd_var = tk.StringVar()
        self.new_pwd_entry = ttk.Entry(self,
                                       textvariable = self.pwd_var,
                                       font=("Arial", 13),
                                       xscrollcommand= self.pwd_scroll.set
                                       )
        self.new_pwd_entry.grid(column = 1, row = 4, padx = 15, sticky = "we")
        self.pwd_scroll.config(command = self.new_pwd_entry.xview)
    
    def pwd_gen(self):
        self.pwd_var.set("")
        if self.mail_var.get() == "" or self.pwd_name.get() == "":
            self.top = tk.Toplevel(self.root)
            self.top.geometry("300x100")
            self.top.title("Error")
                    
            ttk.Label(self.top,
                    text  = "Username or pwd name is empty,\nplease write a name inside of it"
                    ).grid(column = 0, row = 0)
            
            button_ok = ttk.Button(self.top,
                                    text="OK",
                                    command = self.top.destroy
                                    ).grid(column= 0, row =1, padx = 10)
            return
            
        self.gen()
        
    def gen(self) -> None:
            k = random.randint(1,24)
            self.pwd = (encode("".join(random.choices(pos, k= self.pwd_len_var.get())),k), self.mail_var.get(),datetime.now().strftime("%H:%M (%d-%b-%Y)"),k)
            return self.file_append()
        
    def file_append(self):
            with open("test.json", "r") as file_r:
                json_file = json.load(file_r)
                if self.pwd_name.get() not in json_file or self.change == 12:
                    json_file[self.pwd_name.get()] = self.pwd

                    with open("test.json","w") as file_w:
                        json.dump(json_file, file_w, indent=4)
                        self.pwd_var.set(decode(self.pwd[0],self.pwd[3]))
                        self.change = 11
                        root = tk.Toplevel()
                        root.geometry("200x50+1000+1000")
                        root.title("Success")
                        ttk.Label(root, text = "Password is stored").pack()
                        root.after(1500,lambda: root.destroy())
                else:
                    self.top = tk.Toplevel(self.root)
                    self.top.geometry("300x100")
                    self.top.title("password already in system")
                    
                    ttk.Label(self.top,
                              text  = "password already in system!"
                              ).grid(column = 0, row = 0)
                    
                    button_yes = ttk.Button(self.top,
                                            text="I want to change the password!",
                                            command = self.still_change
                                            ).grid(column= 0, row =1)
                    button_no = ttk.Button(self.top,
                                           text="Oops, missclicked!",
                                           command = self.top.destroy
                                           ).grid(column= 1, row =1, padx = 10)

    def still_change(self):
        self.change = 12
        self.top.destroy()
        return self.file_append()


class Login_Frame(ttk.Frame):
 
    def __init__(self, container):
        super().__init__(container)
        self.root = container


class Save_pwd_Frame(ttk.Frame):
  
    def __init__(self, container) -> None:
        super().__init__(container)
        self.label_name = ttk.Label(self,
                               text = "Password Name:",
                               font = ("Arial", 20)
                               ).grid(row = 0, column=0, sticky = "w")
        self.label_mail = ttk.Label(self,
                                    font = ("Arial", 20),
                                    text = "You mail adress/Username:"
                                    ).grid(row = 1, column = 0, sticky = "w")
        self.label_pwd =  ttk.Label(self,
                                    text = "Enter your password:",
                                    font = ("Arial", 20)
                                    ).grid(row = 2, column = 0, sticky = "w")
        self.repeat_pwd = ttk.Label(self, 
                                    text = "Please repeat your password:",
                                    font = ("Arial",20)
                                    ).grid(row = 3, column = 0, sticky = "w")
        
        self.name_var = tk.StringVar(value = "Enter your Name!")
        self.mail_var = tk.StringVar(value="Enter your Mail adress!")
        self.pwd1_var = tk.StringVar()
        self.pwd2_var = tk.StringVar()
        
        self.entry_name =ttk.Entry(self,
                                  width=20,
                                  textvariable=self.name_var)
        self.entry_name.grid(row = 0, column=1,sticky = "e")
        self.entry_name.bind("<FocusIn>", lambda e: self.name_var.set(value=""))
        
        self.entry_mail = ttk.Entry(self,
                                    width = 20,
                                    textvariable= self.mail_var)
        self.entry_mail.grid(column=1, row = 1, sticky = "e")
        self.entry_mail.bind("<FocusIn>", lambda e: self.mail_var.set(value=""))
        
        self.create_pwd_entrys()

        self.button = ttk.Button(self,
                                 text = "Save informaitions",
                                 command = self.append_infos
                                 )
        self.button1 = ttk.Button(self,
                                 text = "Show plain passwords",
                                 command = self.show
                                 )
        self.button.grid(row = 4, column=0, sticky = "ew")
        self.button1.grid(row = 4, column=1, sticky = "ew")
 
    def show(self):
        self.entry_pwd1.destroy()
        self.entry_pwd2.destroy()
        self.entry_pwd2 = ttk.Entry(self,
                                    width = 20,
                                    textvariable= self.pwd2_var)
        self.entry_pwd2.grid(column=1, row = 3, sticky = "e")
        self.entry_pwd1 = ttk.Entry(self,
                                    width = 20,
                                    textvariable= self.pwd1_var)
        self.entry_pwd1.grid(column=1, row = 2, sticky = "e")
        self.button1["text"] = "Hide passwords"
        self.button1["command"] = self.hide
        
    def hide(self):
        self.entry_pwd1.destroy()
        self.entry_pwd2.destroy()
        self.create_pwd_entrys()
        self.button1["text"] = "Show plain passwords"
        self.button1["command"] = self.show
   
    def create_pwd_entrys(self):
        self.entry_pwd1 = ttk.Entry(self,
                                    width = 20,
                                    textvariable= self.pwd1_var,
                                    show = "*")
        
        self.entry_pwd1.grid(column=1, row = 2, sticky = "e")
        self.entry_pwd2 = ttk.Entry(self,
                                    width = 20,
                                    textvariable= self.pwd2_var,
                                    show = "*")
        self.entry_pwd2.grid(column=1, row = 3, sticky = "e")
    
    
    def append_infos(self):
        if self.pwd1_var.get() == self.pwd2_var.get():
            with open("test.json", "r") as f:
                file = json.load(f)
                k = random.randint(0,24)
                
                file[self.name_var.get()] = (encode(self.pwd1_var.get(), k), self.mail_var.get(), datetime.now().strftime("%H:%M (%d-%b-%Y)"), k)
                with open("test.json", "w") as w:
                    json.dump(file,w, indent=4)
                    self.pwd1_var.set(value="")
                    self.pwd2_var.set(value="")
                    self.name_var.set(value = "Enter your Name!")
                    self.mail_var.set(value="Enter your Mail adress!")
                    
                    root = tk.Toplevel()
                    root.geometry("200x50+1000+1000")
                    root.title("Success")
                    ttk.Label(root, text = "Password is stored").pack()
                    root.after(1500,lambda: root.destroy())
                    
        else:
            root = tk.Toplevel()
            root.title("Error, passwords do not match!")
            root.geometry("300x50+1200+500")
            ttk.Label(root, text = "Passwords do not match, please try again!").pack()


root = Basement()
root.mainloop()