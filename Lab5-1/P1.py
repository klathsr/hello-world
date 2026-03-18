import tkinter as tk
from PIL import Image, ImageTk

window = tk.Tk()
window.title("Login")
window.geometry("350x500")

tk.Label(window, text = "LOGIN",font = ("Arial",14,"bold")).pack(anchor = tk.W, padx= 30, pady = 30)
tk.Label(window, text = "Email", font = ("Arial", 12)).pack(anchor = tk.W, padx= 30,)
tk.Entry(window,width = 30).pack(anchor = tk.W, padx= 30,)
tk.Label(window, text = "Password", font = ("Arial", 12)).pack(anchor = tk.W, padx= 30,pady =10)
tk.Entry(window,width = 30).pack(anchor = tk.W, padx= 30,)

var1 = tk.IntVar()
tk.Checkbutton(window, text="Remember me?", variable=var1, selectcolor = "pink").pack(anchor=tk.W, padx = 30, pady =10)

login = tk.Button(window, text = "LOGIN",
                  font= "bold", 
                  width = 30, 
                  height = 2,  
                  fg = "white",
                  highlightbackground = "#C00022", 
                  command= window.destroy).pack(anchor = tk.W,padx = 30, pady =10)

tk.Label(window,  text = "Forgot Password?", font = ("Arial", 12 ),fg = "grey").pack(anchor = tk.E,padx= 35)
tk.Label(window,  text = "OR", font = ("Arial", 12 ),fg = "grey").pack(anchor = tk.N,padx= 35,pady = 10)

fb_image = Image.open("Facebook.png")
fb_image = fb_image.resize((50,50))
fb_image= ImageTk.PhotoImage(fb_image)
fb_button = tk.Button(image = fb_image).pack()

link_image = Image.open("linkedin.png")
link_image = link_image.resize((50,50))
link_image= ImageTk.PhotoImage(link_image)
link_button = tk.Button(image = link_image).pack()

g_image = Image.open("gmail.png")
g_image = g_image.resize((50,50))
g_image= ImageTk.PhotoImage(g_image)
g_button = tk.Button(image = g_image).pack()

tk.Label(window,  text = "Need an account? SIGN UP", font = ("Arial", 12 ),fg = "grey").pack(anchor = tk.N,padx= 35)

window.mainloop()