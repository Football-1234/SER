from tkinter import *
from tkinter import messagebox
import ast
import tkinter as tk
from tkinter import font
import tkinter.filedialog as filedialog
import pyaudio
import wave
import soundfile as sf
import numpy as np
from keras.models import load_model
from scipy.signal import resample
from emoji import emojize
import threading

root=Tk()
root.title(" SER LOGIN ")
root.geometry("925x500")
root.configure(bg="#fff")
root.resizable(False,False)

#-----------------------Blink buttons------------------
def blink_button(name):
    def on_enter(event):
        name.config(bg="lightblue")
    def on_leave(event):
        name.config(bg="#57a1f8")
    name.bind("<Enter>", on_enter)
    name.bind("<Leave>", on_leave)

#-------------Sign-in page-------------------------------
def Signin():
    username=user.get()
    password=pwd.get()

    file=open("datasheet.txt","r")
    d=file.read()
    r=ast.literal_eval(d)
    file.close()

    print(r.keys())     # this is both  for checking the username and password into the dictionary.
    print(r.values())
    
    if username =="Username" and password=="Password":
        messagebox.showerror("Opps!","Please Enter the Username and Password.")
    else:    
        if username in r.keys() and password ==r[username]:     # r[user] means that password of given username.
            root.withdraw()     # Hide the Sign-In form
            messagebox.showinfo("Login","Login Successfully! Press Ok to Continue.")
            #-------------------------------
            model = load_model("D:\\BS(AI)-4th-semester\\programming for AI\\New folder\\ser_model.h5")
            
            wd=Toplevel(root)
            wd.title("Speech Emotion Recognition")
            wd.geometry("925x500")
            wd.configure(bg="#fff")
            wd.resizable(False,False)
            def upload_audio():
                file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
                audio_entry.delete(0, tk.END)
                audio_entry.insert(0, file_path)

            def start_recording():
                global is_recording
                is_recording = True

                p = pyaudio.PyAudio()
                stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

                frames = []
                while is_recording:
                    try:
                        data = stream.read(1024)
                        frames.append(data)
                    except Exception as e:
                        print("Error recording:", str(e))

                stream.stop_stream()
                stream.close()
                p.terminate()  
                audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
                sf.write("live_recording.wav", audio_data, 44100)
                audio_entry.delete(0, tk.END)
                audio_entry.insert(0, "live_recording.wav")


            def stop_recording():
                global is_recording
                is_recording = False

            def predict_emotion(): 
                audio_file = audio_entry.get()
                if audio_file:
                    try:
                # Load and preprocess the audio file
                        audio_data, _ = sf.read(audio_file)
                        audio_data = resample(audio_data, 44100, 16000)  # Resample to match model input
                        audio_data = audio_data.reshape(1, -1, 1)
                # Perform emotion prediction
                        emotion_probs = model.predict(audio_data)
                        emotions = ["Happy", "Sad", "Angry", "Neutral"]
                        emotion_results = [f"{emojize(f':{emo}:', use_aliases=True)} {emotion} ({round(prob * 100, 2)}%)" for emo, prob, emotion in zip(range(4), emotion_probs[0], emotions)]

                        result_label.config(text="Emotion Predictions:\n" + "\n".join(emotion_results))
                    except Exception as e:
                        result_label.config(text="Error: " + str(e))
                else:
                    result_label.config(text="No audio file selected.")

            
            img= PhotoImage(file="D:\\BS(AI)-4th-semester\\programming for AI\\source_image\\website-design-2.png")
            Label(wd,image=img, bg="white").place(x=480,y=100)
        
            message_label = tk.Label(wd, text="Please Select Audio file", font=("Arial", 12), fg="white", padx=10, pady=5)
            message_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
            message_label.place(x=90,y=204)
            blink_button(message_label)

            tk.Frame(wd,width=295,height=2,bg="black").place(x=25,y=270)

            audio_entry = tk.Entry(wd,width=50,fg="black",border=0,bg="white")
            audio_entry.place(x=15,y=240)

            upload_button = tk.Button(wd,width=15,pady=3, text="Upload Audio",bg="#57a1f8",fg="white",border=0, command=upload_audio)
            upload_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
            upload_button.place(x=95,y=300)
            blink_button(upload_button)

            record_button = tk.Button(wd, pady=3, text="Start Recording", bg="#57a1f8",fg="white",border=0,command=lambda: threading.Thread(target=start_recording).start())
            record_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
            record_button.place(x=100,y=350)
            blink_button(record_button)
            
            stop_button = tk.Button(wd,pady=3, text="Stop Recording",bg="#57a1f8",fg="white",border=0, command=stop_recording)
            stop_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
            stop_button.place(x=200,y=350)
            blink_button(stop_button)
            
            predict_button = tk.Button(wd,pady=3, text="Predict Emotion",bg="#57a1f8",fg="white",border=0, command=predict_emotion)
            predict_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
            predict_button.place(x=300,y=350)
            blink_button(predict_button)
            
            result_label = tk.Label(wd, text="",bg="white",fg="black",border=0)
            result_label.pack()
            wd.mainloop()
        else:
            messagebox.showerror("Opps!","Invalid Username or Password.")
        
#--------------------------------------------------------

def signup_command():           # here is sign-up form
    root.withdraw()
    window=Toplevel(root)
    window.title("Sign-Up")
    window.geometry("925x500")
    window.configure(bg="#fff")
    window.resizable(False,False)

    def is_username_exists(username, filename):     #  checking if a username exists in the file
        with open(filename, 'r') as file:
            data = ast.literal_eval(file.read())
            if username in data:
                return True
        return False

    def is_password_exists(password, filename):     #  checking if a password exists in the file
        with open(filename, 'r') as file:
            data = ast.literal_eval(file.read())
            for stored_password in data.values():
                if password == stored_password:
                    return True
        return False

    def register_user(username, password, filename):        #  register a new user
        if is_username_exists(username, filename):
            messagebox.showerror("Error", "Username already exists.")

        elif is_password_exists(password, filename):
            messagebox.showerror("Error", "Password already exists.")

        else:
            try:
                file = open(filename, 'r+')
                data = ast.literal_eval(file.read())
                data[username] = password
                file.seek(0)
                file.truncate()
                file.write(str(data))
                file.close()
                messagebox.showinfo("Signup", "Successfully Sign Up")
                window.destroy()

            except:
                file = open(filename, 'w')
                data = {username: password}
                file.write(str(data))
                file.close()
                messagebox.showinfo("Signup", "Successfully Sign Up")
                window.destroy()


    def Signup():               # Function for the signup button click event
        window.deiconify()  # sign up close
        root.withdraw()    # show sign in
        username = user.get()
        password = pwd.get()
        conform_password = cf_pwd.get()

        if password == conform_password:
            register_user(username, password, "datasheet.txt")

        elif username=="Username" and password=="Password" and conform_password=="Conform Password":
            messagebox.showerror("Oops!","Please Enter all fields.")
        else:
            messagebox.showerror("Oops!", "Both passwords should match")
    #------------------------------------------------------------


    def sign():
        window.withdraw()    #  sign up close.
        root.deiconify()     # show sign in

    img=PhotoImage(file="D:\\BS(AI)-4th-semester\\programming for AI\\source_image\\design.png")
    Label(window,image=img,border=0,bg="white").place(x=20,y=90)
    frame=Frame(window,width=350,height=390,bg="#fff")
    frame.place(x=480,y=50)
    heading=Label(frame,text="Sign up",fg="#57a1f8",bg="white",font=("Microsoft Yahei UI Light",23,"bold"))
    heading.place(x=100,y=5)

    #--------------------Username-------------------
    def on_enter(e):
        user.delete(0,"end")

    def on_leave(e):
        if user.get()=="":
            user.insert(0,"Username")
    user=Entry(frame,width=25,fg="black",border=0,bg="white",font=("Microsoft YaHei UI Light",11))
    user.place(x=30,y=80)
    user.insert(0,"Username")
    user.bind("<FocusIn>",on_enter)
    user.bind("<FocusOut>",on_leave)

    Frame(frame,width=295,height=2,bg="black").place(x=25,y=107)

    #--------------------Password-------------------
    def on_enter(e):
        pwd.delete(0,"end")

    def on_leave(e):
        if pwd.get()=="":
            pwd.insert(0,"Password")
    pwd=Entry(frame,width=25,fg="black",border=0,bg="white",font=("Microsoft YaHei UI Light",11))
    pwd.place(x=30,y=150)
    pwd.insert(0,"Password")
    pwd.bind("<FocusIn>",on_enter)
    pwd.bind("<FocusOut>",on_leave)

    Frame(frame,width=295,height=2,bg="black").place(x=25,y=177)

    #--------------------Conform-Password-------------------
    def on_enter(e):
        cf_pwd.delete(0,"end")

    def on_leave(e):
        if cf_pwd.get()=="":
            cf_pwd.insert(0,"Conform Password")
    cf_pwd=Entry(frame,width=25,fg="black",border=0,bg="white",font=("Microsoft YaHei UI Light",11))
    cf_pwd.place(x=30,y=220)
    cf_pwd.insert(0,"Conform Password")
    cf_pwd.bind("<FocusIn>",on_enter)
    cf_pwd.bind("<FocusOut>",on_leave)

    Frame(frame,width=295,height=2,bg="black").place(x=25,y=247)

    #=-----------------------------------------------------
    Button(frame, width=39,pady=7,text="Sign Up",bg="#57a1f8",fg="white",border=0,command=Signup).place(x=35,y=280)
    label=Label(frame,text="I have an account",fg="black",bg="white",font=("Microsoft YaHei UI Light",9))
    label.place(x=90,y=340)
    signin=Button(frame, width=6, text="Sign in", border=0, bg="white",cursor="hand2", fg="#57a1f8",command=sign)
    signin.place(x=200,y=340)
    window.mainloop()
#-------------------------------------------------------
img=PhotoImage(file="D:\\BS(AI)-4th-semester\\programming for AI\\source_image\\website-design-2.png")
Label(root,image=img, bg="white").place(x=50,y=50)
frame=Frame(root,width=350,height=350,bg="white")
frame.place(x=480,y=70)
heading =Label(frame,text="Sign in ", fg="#57a1f8",bg="white",font=("Microsoft Yahei UI Light",23,"bold"))
heading.place(x=100,y=5)

#--------------Username--------------------------
def on_enter(e):
    user.delete(0,"end")
def on_leave(e):
    name=user.get()
    if name=="":
        user.insert(0,"Username")

user=Entry(frame,width=25,fg="black",border=0,bg="white",font=("Microsoft YaHei UI Light",11))
user.place(x=3,y=80)
user.insert(0,"Username")
user.bind("<FocusIn>",on_enter)
user.bind("<FocusOut>",on_leave)
Frame(frame,width=295,height=2,bg="black").place(x=0,y=107)
#---------------Password--------------------------
def on_enter(e):
    pwd.delete(0,"end")
def on_leave(e):
    name=pwd.get()
    if name== "":
        pwd.insert(0,"Password")
pwd=Entry(frame,width=25,fg="black",border=0,bg="white",font=("Microsoft YaHei UI Light",11))
pwd.place(x=3,y=150)
pwd.insert(0,"Password")
pwd.bind("<FocusIn>",on_enter)
pwd.bind("<FocusOut>",on_leave)

Frame(frame,width=295,height=2,bg="black").place(x=0,y=177)
#------------------No Account-----------------------
Button(frame,width=39,pady=7,text="Sign in",bg="#57a1f8",fg="white",border=0,command=Signin).place(x=15,y=204)
label=Label(frame,text="Don't have an account? ",fg="black",bg="white",font=("Microsoft YaHei UI Light",9))
label.place(x=25,y=270)
#---------------Sign-up botton-----------------------
sign_up=Button(frame, width=6,text="Sign-Up", border=0, bg="white",cursor="hand2",fg="#57a1f8",command=signup_command)
sign_up.place(x=215,y=270)
root.mainloop()
