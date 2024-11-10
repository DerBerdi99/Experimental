import tkinter as tk
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import customtkinter as ctk
import sqlite3
import random
import bcrypt 
import sys

default_text_entry_name="Username"
default_text_entry_pass="Password"
default_text_birthnumbers="Year of Birth"
global this_user_name
this_user_name=None
custom_font=("Helvetica",15)
root=ctk.CTk()
root.geometry("350x220")
root.resizable(False,False)

def create_main_window(name_value):
    global root_Frame_0
    for widgets in login_Frame_0.winfo_children():
        widgets.destroy()
    login_Frame_0.destroy()
    root.geometry("600x600")
    root_Frame_0 = ctk.CTkFrame(root,fg_color="#000000")
    global name_var
    name_var=tk.StringVar()
    menu_options_0=ctk.CTkOptionMenu(root,values=["Neues Projekt","Ein Projekt abschließen","Projekte löschen"],fg_color=["grey","red"],button_color="#573827",button_hover_color="#EF9912",text_color="white",corner_radius=0,width=200,command=open_Top_1)
    menu_options_0.set("Projekt")
    menu_options_0.grid(row=0,column=0,sticky="N")
    menu_options_1=ctk.CTkOptionMenu(root,values=["Protokoll laden","Daten Analysieren","Protokoll löschen"],fg_color=["grey","red"],button_color="#573827",button_hover_color="#EF9912",text_color="white",corner_radius=0,width=200,command=open_Top_2)
    menu_options_1.set("Daten")
    menu_options_1.grid(row=0,column=2,sticky="N")
    menu_options_2=ctk.CTkOptionMenu(root,values=["Nutzerprofil","Log Out"],fg_color=["grey","red"],button_color="#573827",button_hover_color="#EF9912",text_color="white",corner_radius=0,width=200,command=open_Top_3)
    menu_options_2.set("Nutzer")
    menu_options_2.grid(row=0,column=4,sticky="N")
    lbl_user_0=ctk.CTkLabel(root,text=name_value,fg_color=["grey","red"],bg_color="#573827",text_color="white",corner_radius=0,width=200)
    lbl_user_0.grid(row=1,column=0,sticky="N")
    lbl_user_1=ctk.CTkLabel(root,text=name_value,fg_color=["grey","red"],bg_color="#573827",text_color="white",corner_radius=0,width=200)
    lbl_user_1.grid(row=1,column=2,sticky="N")
    lbl_user_2=ctk.CTkLabel(root,fg_color=["grey","red"],bg_color="#573827",text_color="white",corner_radius=0,width=200)
    lbl_user_2.grid(row=1,column=4,sticky="N")
    root_Frame_0.grid()
    load_saved_buttons()
    root.mainloop()
#the methods of creating staff/ checkinng values
def create_staff(name_value,password,birth_value):
    #Pers_ID
    name_sub_string=name_value[0:1]
    birth_sub_string=birth_value[2:4]
    Random_Number=str(random.randint(1,999))
    #Hashing
    input_password=str(password)
    hashed_password=bcrypt.hashpw(input_password.encode("utf-8"),bcrypt.gensalt())
    user_name=name_value
    value_list=[user_name,hashed_password]
    #database insert
    conn = sqlite3.connect("D:\Programmtests\DB\Staff.db")
    cur=conn.cursor()
    sql=("INSERT INTO Staff VALUES (?,?)")
    cur.execute(sql,value_list)
    conn.commit()
    conn.close()

def check_signup_values(name,password,birth):
    name_value=name
    password_value=password
    birth_value=birth
    if name_value.isalpha():
        if len(birth_value) == 4 and birth_value.isdigit():
            conn = sqlite3.connect("D:\Programmtests\DB\Staff.db")
            cur=conn.cursor()
            sql="SELECT user_name FROM Staff WHERE user_name = ?"
            cur.execute(sql,(name_value,))
            data=cur.fetchall()
            if not data:
                print("adding Staff")
                create_staff(name_value,password_value,birth_value) 
            else:
                print("user Input Error")
                messagebox.showwarning("Warning",f"{name_value} is already taken.")
        else:
            print("user Input Error")
            messagebox.showwarning("Warning","Use this Format: YYYY")
    else:
        print("user Input Error")
        messagebox.showwarning("Warning","Use letters only.")
        #return False

def check_login(username,password):
    name_value=username
    input_password=password
    input_password=input_password.encode("utf-8")
    conn = sqlite3.connect("D:\Programmtests\DB\Staff.db")
    cur=conn.cursor()
    try:
        sql=f"SELECT password_hash FROM Staff WHERE user_name = ?"
        cur.execute(sql,(name_value,))
        saved_hash=cur.fetchone()
        if saved_hash is not None:
            saved_hash=saved_hash[0]   #get value from list
            if bcrypt.checkpw(input_password,saved_hash):
                global this_user_name
                this_user_name=name_value
                create_main_window(name_value)      #ZUGANG GEWÄHREN
            else:
                print("Password didn't match")
        else:
            print("Username not found.")
    except sqlite3.Error as e:
        print("SQLite3 Error: e")
    except IndexError:
        print("Index Error occurred")
    finally:
        conn.close()

def create_signup_frame():
    login_Frame_0.destroy()
    global login_Frame_1
    login_Frame_1=ctk.CTkFrame(root)
    ent_username_signup=ctk.CTkEntry(login_Frame_1)
    ent_username_signup.insert(0,default_text_entry_name)
    ent_username_signup.bind("<FocusIn>",clear_default_text)
    ent_username_signup.grid(row=0,column=1,padx=50)
    ent_password_signup=ctk.CTkEntry(login_Frame_1)
    ent_password_signup.insert(0,default_text_entry_pass)
    ent_password_signup.bind("<FocusIn>",clear_default_text)
    ent_password_signup.grid(row=1,column=1,padx=50)
    ent_birthyear_signup=ctk.CTkEntry(login_Frame_1)
    ent_birthyear_signup.insert(0,default_text_birthnumbers)
    ent_birthyear_signup.bind("<FocusIn>",clear_default_text)
    ent_birthyear_signup.grid(row=2,column=1,padx=50)
    btn_submit_signup=ctk.CTkButton(login_Frame_1,text="sign up",command=lambda:check_signup_values(ent_username_signup.get(),ent_password_signup.get(),ent_birthyear_signup.get()))
    btn_submit_signup.grid(row=3,column=1,padx=50,pady=10)
    btn_return_to_login=ctk.CTkButton(login_Frame_1,text="return",command=lambda:return_to_login_from_signup())
    btn_return_to_login.grid(row=4,column=1,padx=50,pady=10)
    login_Frame_1.grid(row=5,column=1,padx=50)

def return_to_login_from_signup():
    for widgets in login_Frame_1.winfo_children():
        widgets.destroy()
    login_Frame_1.destroy()
    create_login_frame()

def log_out():
    try:
        for widget in root_Frame_0.winfo_children():
            widget.destroy()
    except:
        print("No Widgets left in root_Frame_0")
    root_Frame_0.destroy()
    for widget in root.winfo_children():
        widget.destroy()
    root.geometry("350x220")
    create_login_frame()
#clear_entries
def clear_default_text(event):
    entry=event.widget
    entry.delete(0,END)

def create_login_frame():
    global login_Frame_0
    login_Frame_0=ctk.CTkFrame(root)
    ent_username_login=ctk.CTkEntry(login_Frame_0)
    ent_username_login.insert(0,default_text_entry_name)
    ent_username_login.bind("<FocusIn>",clear_default_text)
    ent_username_login.grid(row=0,column=1,padx=50)
    ent_password_login=ctk.CTkEntry(login_Frame_0)
    ent_password_login.insert(0,default_text_entry_pass)
    ent_password_login.bind("<FocusIn>",clear_default_text)
    ent_password_login.grid(row=1,column=1,padx=50)
    btn_submit_login=ctk.CTkButton(login_Frame_0,text="Login",command=lambda:check_login(ent_username_login.get(),ent_password_login.get()))
    btn_submit_login.grid(row=2,column=1,padx=50,pady=10)
    btn_register=ctk.CTkButton(login_Frame_0,text="sign up",command=lambda:create_signup_frame())
    btn_register.grid(row=3,column=1,padx=50)
    login_Frame_0.grid(row=4,column=1,padx=50)

class Segment_Buttons(): 

    def __init__(self,button_text,button_color):
        btn_project= ctk.CTkButton(root_Frame_0, text=button_text,fg_color=button_color,hover_color="#EF9912",height=100,width=100,font=custom_font, command=lambda:[self.onbtnclick(btn_project),open_Top_0()])
        btn_project._text_label.configure(wraplength=110)
        btn_project.grid()
        
    def onbtnclick(self, btn_project):
        global button_text
        button_text=btn_project.cget("text")
        print(button_text)

class Segment_Mimes():
    def __init__(self,button_text,button_color):
        
        btn_project_mime= ctk.CTkButton(root_Frame_0, text=button_text,fg_color=button_color,hover_color="#EF9912",height=100,width=100,font=custom_font, command=lambda:[self.confirm_delete(btn_project_mime,button_text)])
        btn_project_mime._text_label.configure(wraplength=110)
        btn_project_mime.grid()
    def confirm_delete(self,btn_project_mime,button_text):
        result=messagebox.askyesno("Confirm","Sure you want to delete?")
        if result:
            btn_project_mime.destroy()
            self.delete_project(button_text)
            add_log_file(button_text)
    def delete_project(self,button_text):
        self.delete_databases_by_name(button_text)
    def delete_databases_by_name(self, button_text):
        conn = sqlite3.connect("D:\Programmtests\DB\Buttons.db")
        cur = conn.cursor()
        try:
            sql=("DELETE FROM BUTTONS WHERE user_name=? AND NAMES=?")
            cur.execute(sql,(this_user_name, button_text))
            print("Single button erased")
        except:
            print("None buttons left")
        conn.commit()
        conn.close()
        conn = sqlite3.connect("D:\Programmtests\DB\Materials.db")
        cur = conn.cursor()
        try:
            sql=("DELETE FROM Materials WHERE user_name=? AND NAMES =?")
            cur.execute(sql,(this_user_name, button_text))
            print("Materials erased")
        except:
            print("No Material left")
        conn.commit()
        conn.close()
        conn = sqlite3.connect("D:\Programmtests\DB\Processes.db")
        cur = conn.cursor()
        try:
            sql=("DELETE FROM Processes WHERE user_name=? AND NAMES =?")
            cur.execute(sql,(this_user_name, button_text))
            print("Process erased")
        except:
            print("No Process left")
        conn.commit()
        conn.close()
     
def add_btn_project(name_value,prio_color):
    Segment_Buttons(name_value,prio_color) 

def add_btn_mime(name_value,prio_color):
    Segment_Mimes(name_value,prio_color)

def add_label_mat_values(name_value,sum_value):
    add_labels_to_Frame_0(name_value,sum_value)

def add_label_process_values(process_value):
    add_labels_to_Frame_1(process_value)

def add_log_file(project_name):
    time=datetime.now()
    timestamp=time.strftime("%Y-%m-%d")
    value_list=[project_name,timestamp]
    conn = sqlite3.connect("D:\Programmtests\DB\Log.db") 
    cur = conn.cursor()
    sql="INSERT INTO Log VALUES (?,?)"
    cur.execute(sql,value_list)
    conn.commit()
    conn.close() 

def read_database_buttons():
    
    conn = sqlite3.connect("D:\Programmtests\DB\Buttons.db")         #1.R DB Abfrage
    cur = conn.cursor()                                            # 
    sql="SELECT NAMES,PRIOS FROM Buttons WHERE user_name=?"                             
    cur.execute(sql,(this_user_name,))                                                 #                                               #
    data = cur.fetchall()
    conn.close()
    if not data:
        return 0
    else:
        return data
    
       
def read_database_materials():
    try:
        conn = sqlite3.connect("D:\Programmtests\DB\Materials.db")         #1.R DB Abfrage
        cur = conn.cursor()                                              
        sql=("SELECT MATS,SUMS FROM Materials WHERE user_name=? AND NAMES=?")                                  
        cur.execute(sql,(this_user_name, button_text))                                                 
        data = cur.fetchall() 
        conn.close()                                          
        return data    
    except:
        return 0
    
def read_database_process():
    try:
        conn = sqlite3.connect("D:\Programmtests\DB\Processes.db")         
        cur = conn.cursor()                                               
        sql=("SELECT PROCESSES FROM Processes WHERE user_name=? AND Names=?")                                  
        cur.execute(sql,(this_user_name, button_text))                                                 
        data = cur.fetchall()
        print(data)
        conn.close()
        return data   
    except:
        return 0

def write_database_buttons(button_value_list):
    conn = sqlite3.connect("D:\Programmtests\DB\Buttons.db")    #W Buttons.db
    cur = conn.cursor()                                         #                                        #füge ohne weiteres name, prios hinzu 
    cur.execute("INSERT INTO Buttons VALUES(?,?,?,?)",button_value_list)
    conn.commit()

def load_saved_buttons():
    data=read_database_buttons()
    if data == 0:
        pass
    else:
        for names,prios in data:
            add_btn_project(names,prios)     
def load_saved_labels():
    data=read_database_materials()
    if data == 0:
        pass
    else:
        for mats,sums in data:
            add_label_mat_values(mats,sums)                                       #3.C addlbl0
    data=read_database_process()
    if data == 0:
        pass
    else:
        for processes in data:
            processes = processes[0]
            add_label_process_values(processes)

def load_saved_mimes():
    data=read_database_buttons()
    if data == 0:
        pass
    else:
        for btn_project in root_Frame_0.winfo_children():                                 #Löschen Buttons
            btn_project.destroy()
        for names,prios in data:
            add_btn_mime(names,prios)

def remove_button_single():
    load_saved_mimes()

def remove_button_all():
    for btn_project in root_Frame_0.winfo_children():                                 #Löschen Buttons
        btn_project.destroy()
    try:
        Top_0.destroy()
    except:
        print("window has been closed")
    conn = sqlite3.connect("D:\Programmtests\DB\Buttons.db")
    cur = conn.cursor()
    try:
        sql = ("DELETE FROM Buttons WHERE user_name=?")
        cur.execute(sql,(this_user_name,)) 
    except:
        print("No Buttons left")
    conn.commit()
    conn.close()
    conn = sqlite3.connect("D:\Programmtests\DB\Materials.db")
    cur=conn.cursor()
    try:
        sql=("DELETE FROM Materials WHERE user_name=?")
        cur.execute(sql,(this_user_name,)) 
    except:
        print("No Mat left")
    conn.commit()
    conn.close()
    conn = sqlite3.connect("D:\Programmtests\DB\Processes.db")
    cur=conn.cursor()
    try:
        sql=("DELETE FROM Processes WHERE user_name=?")
        cur.execute(sql,(this_user_name,)) 
    except:
        print("No Processes left")
    conn.commit()
    conn.close()

def open_Top_0():
    global Top_0
    global Top_0_Frame_0
    global Top_0_Frame_1
    Top_0=Toplevel()
    Top_0.title(button_text)
    Top_0.geometry("700x700")
    btn_mat=ctk.CTkButton(Top_0,text="Add Material",fg_color="#573827",hover_color="#EF9912",command=lambda:open_Top_00())
    btn_proc=ctk.CTkButton(Top_0,text="Add Process",fg_color="#573827",hover_color="#EF9912",command=lambda:openTop_01())
    btn_calc=ctk.CTkButton(Top_0,text="Calculator",fg_color="#573827",hover_color="#EF9912",command=None)
    btn_desc=ctk.CTkButton(Top_0,text="Description",fg_color="#573827",hover_color="#EF9912",command=lambda:openTop_02())
    Top_0_Frame_0=ctk.CTkFrame(Top_0,fg_color="#EF9912",height=300,border_width=5,border_color="#573827")
    Top_0_Frame_1=ctk.CTkFrame(Top_0,fg_color="#EF9912",height=300,border_width=5,border_color="#573827") 
    btn_mat.grid(row=1,column=0)
    btn_proc.grid(row=1,column=3)
    btn_calc.grid(row=3,column=0)
    btn_desc.grid(row=3,column=3)
    Top_0_Frame_0.grid(row=6,column=0)
    Top_0_Frame_1.grid(row=6,column=3)
    load_saved_labels()
    Top_0.mainloop()

def open_Top_1(choice):
    if choice == "Neues Projekt":
        load_saved_buttons()     
        
    def get_all_values():
        
        global names
        global prios
        global prio_value
        global name_value
        global prio_color
        prio_state=False
        name_state=False
        prio_value=lbl_info_1.cget("text")  
        name_value=name_var.get()
        text_value=tex_desc.get("0.0",END)                                #text nicht belegt
        if prio_value != ("Priorität wählen"):          
            prio_state = True
        else:
            prio_state=False
        if name_value != (""):
            name_state = True
        else:
            name_state=False
        if ((prio_state == True) and (name_state == True)):
            if prio_value == "hoch":
                prio_color = "red"
            elif prio_value =="normal":
                prio_color = "yellow"
            else:
                prio_color="green"    
            names = name_value
            prios = prio_color
            descr = text_value
            button_value_list = [(this_user_name),(names),(prios),(descr)]
            write_database_buttons(button_value_list)                                                    #Call Addbtn
            add_btn_project(names,prios)
    def red():                                                          #Farbübersetzung, C über jeweiliges Lbl
        lbl_info_1.configure(text="hoch")
    def yellow():
        lbl_info_1.configure(text="normal")
    def green():
        lbl_info_1.configure(text="niedrig")

    
    if choice == "Ein Projekt abschließen":
        print("Ein Projekt abschließen")
        remove_button_single()
        return
    if choice == "Projekte löschen":
        print("Projekte löschen")
        remove_button_all()                                                        #C removebutton löscht alle buttons + db
        return
    Top_1=Toplevel()
    lbl_info_0=ctk.CTkLabel(Top_1,text="Projektname eingeben")
    ent_name=ctk.CTkEntry(Top_1,textvariable=name_var)
    lbl_info=ctk.CTkLabel(Top_1,text="Beschreibung eingeben")
    tex_desc=ctk.CTkTextbox(Top_1,width=200,height=100)
    btn_save=ctk.CTkButton(Top_1,text="Speichern",command=get_all_values)
    btn_red=ctk.CTkButton(Top_1,text="",fg_color="red", width=20, height=40,command=red)
    btn_yellow=ctk.CTkButton(Top_1,text="",fg_color="yellow", width=20, height=40,command= yellow)
    btn_green=ctk.CTkButton(Top_1,text="",fg_color="green", width=20, height=40,command= green)
    lbl_info_1=ctk.CTkLabel(Top_1,text="Priorität wählen")
    lbl_info_0.grid(row=0,column=0)
    ent_name.grid(row=0,column=1)
    lbl_info.grid(row=1,column=0)
    tex_desc.grid(row=1,column=1)
    btn_save.grid(row=2,column=1)
    btn_red.grid(row=0,column=3)
    btn_yellow.grid(row=1,column=3)
    btn_green.grid(row=2,column=3)
    lbl_info_1.grid(row=2,column=0)
    Top_1.mainloop()


def display_data(values):
    Top_2=Toplevel()
    Top_2.columnconfigure(index=1,weight=1)
    Top_2.columnconfigure(index=2,weight=1)
    Top_2_Frame_0=ctk.CTkScrollableFrame(Top_2)
    for data in values:
        lbl=ctk.CTkLabel(Top_2_Frame_0,text=data)
        lbl.grid(column=1)
    Top_2_Frame_0.grid(column=1)   
    Top_2.mainloop()

def open_Top_2(choice):
    if choice == "Protokoll laden":
        open_log_file()     
        return
    if choice == "Protokoll löschen":
        delete_log_file()
        return
    
def open_Top_3(choice):
    if choice == "Log Out":
        log_out()

def open_log_file():
    
    conn = sqlite3.connect("D:\Programmtests\DB\Log.db")
    cur=conn.cursor()
    try:
        sql=("SELECT * FROM Log")
        cur.execute(sql)
        data=cur.fetchall()
        display_data(data)
    except:
        print("Datafetch Error: Log leer")
        messagebox.showinfo("Information","Die Protokolldatei ist leer")
        return
    
def delete_log_file():
    conn = sqlite3.connect("D:\Programmtests\DB\Log.db")
    cur=conn.cursor()   
    try:
        sql=("DROP TABLE Log")
        cur.execute(sql)
        sql=("CREATE TABLE Log(NAMES TEXT,TIMESTAMP TEXT);")
    except:
        print("Delete Error: Log leer")

def add_labels_to_Frame_0(name_value,sum_value):
    global Top_0_Frame_0 
    lbl_name=ctk.CTkLabel(Top_0_Frame_0,text=name_value)
    lbl_sum=ctk.CTkLabel(Top_0_Frame_0,text=sum_value)
    lbl_name.grid()
    lbl_sum.grid()
    
def add_labels_to_Frame_1(process_value):
    global Top_0_Frame_1
    lbl_proc=ctk.CTkLabel(Top_0_Frame_1,text=process_value)
    lbl_space=ctk.CTkLabel(Top_0_Frame_1,text=None)
    lbl_proc.grid()
    lbl_space.grid()

def open_Top_00():
    Top_00=Toplevel()
    Top_00.title("Add Material")
    Top_00.geometry("440x130")
    def plus():
            p=ent_count.get()
            pInt=int(p)
            pInt+=1
            ent_count.delete(0,"end")
            ent_count.insert(0,pInt)
    def minus():
            m=ent_count.get()
            mInt=int(m)
            mInt-=1
            ent_count.delete(0,"end")
            ent_count.insert(0,mInt)
    def get_both_mat_values():
        material_names=ent_material.get()
        material_sum=(int(ent_price.get())*int(ent_count.get()))
        add_label_mat_values(material_names,material_sum)                                  #c addlbl0                           
        mat_list = [(this_user_name),(button_text),(material_names),(material_sum)]                        
        conn = sqlite3.connect("D:\Programmtests\DB\Materials.db")    #W Materials.db
        cur = conn.cursor()                                                                                                 #wenn noch keine Table da add Table
        sql="INSERT INTO Materials (user_name,NAMES,MATS,SUMS) VALUES(?,?,?,?)"           #und füge Names,Sum hinzu
        cur.execute(sql,mat_list)
        conn.commit()
        conn.close()
    
    Top_00.columnconfigure(0,weight=1)
    Top_00.columnconfigure(1,weight=1)
    Top_00.columnconfigure(2,weight=1)
    Top_00.columnconfigure(3,weight=1)
    Top_00.columnconfigure(4,weight=1)
    lbl_info_0=ctk.CTkLabel(Top_00,text= "Material")
    lbl_info_1=ctk.CTkLabel(Top_00,text= "Preis")
    lbl_info_2=ctk.CTkLabel(Top_00,text= "Menge")
    ent_material= ctk.CTkEntry(Top_00,width=100)
    ent_price= ctk.CTkEntry(Top_00,width=50)
    ent_count= ctk.CTkEntry(Top_00,width=25)
    btn_plus= ctk.CTkButton(Top_00,text="+",width=50,command=lambda:plus())
    btn_minus= ctk.CTkButton(Top_00,text="-",width=20,command=lambda:minus())
    btn_add= ctk.CTkButton(Top_00,text="Hinzufügen",fg_color="#573827",hover_color="#EF9912",width=100,command=lambda:get_both_mat_values())
    lbl_info_0.grid(row=0,column=0)
    lbl_info_1.grid(row=0,column=1)
    lbl_info_2.grid(row=0,column=2)
    ent_material.grid(row=1,column=0)
    ent_price.grid(row=1,column=1)
    ent_count.grid(row=1,column=3)
    btn_plus.grid(row=1,column=2)
    btn_minus.grid(row=1,column=4)
    btn_add.grid(row=3,column=1)
    ent_count.insert(0,"0")
    Top_00.mainloop()
    
def openTop_01():
    def get_process_value():
        process_names=tex_proc.get("1.0",END)
        add_label_process_values(process_names)
        process_list = [(this_user_name),(button_text),(process_names)]                        
        conn = sqlite3.connect("D:\Programmtests\DB\Processes.db")    #W Processes.db
        cur = conn.cursor()                                         
        sql="INSERT INTO Processes VALUES(?,?,?)"           
        cur.execute(sql,process_list)
        conn.commit()
        conn.close()

    Top_01=Toplevel()
    Top_01.title("Prozeßablauf")
    Top_01.geometry("440x440")
    lbl_info=ctk.CTkLabel(Top_01,text= "Geben Sie hier Ihren Prozeßablauf ein")
    tex_proc=ctk.CTkTextbox(Top_01)
    btn_submit=ctk.CTkButton(Top_01,text="speichern",command=lambda:get_process_value())
    lbl_info.grid()
    tex_proc.grid()
    btn_submit.grid()
    Top_01.mainloop()

def openTop_02():
    global button_text
    Top_02=Toplevel()
    Top_02.title("Beschreibung")
    Top_02.geometry("400x550")
    conn = sqlite3.connect("D:\Programmtests\DB\Buttons.db")
    cur=conn.cursor()
    sql=f"SELECT DESCR FROM Buttons WHERE NAMES='{button_text}'"
    cur.execute(sql)
    description=cur.fetchall()
    description=str(description[0][0])
    print(description)
    tex_proc_show=ctk.CTkTextbox(Top_02,width=250,height=300)
    tex_proc_show.insert(END,description)
    tex_proc_show.grid()
    Top_02.mainloop()

create_login_frame()

root.mainloop()