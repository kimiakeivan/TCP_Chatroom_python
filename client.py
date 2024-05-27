import socket
import threading
import customtkinter
import ast

HOST = "127.0.0.1"
PORT = 15000
FORMAT = "utf-8"
OUTPUT = []
username = None
private_state = False
membersList = []
checkboxes = {}



def receive():
    while True:
        message = client_socket.recv(1024).decode(FORMAT)
        if message.endswith("]\n"):
            message = message.split("\n")
            message.pop(-1)
            global membersList
            membersList = ast.literal_eval(message[-1])
            member_list(membersList)
            message.remove(message[-1])
            for msg in message:
                textlabel = customtkinter.CTkLabel(master=chatArea, text=msg, font=("Roboto", 13))
                textlabel.pack()

        else:
            if not (message.startswith(username)):
                textlabel = customtkinter.CTkLabel(master=chatArea, text=message, fg_color="lavender", font=("Roboto", 16), corner_radius=16, text_color="black")
                textlabel.pack(ipady=3, pady=5, padx=3, anchor="w")


def send():
    global private_state
    message = messageEntry.get()
    messageEntry.delete("0", "end")

    if message == "bye":
        stop()

    elif message == "light" or  message == "dark":
        customtkinter.set_appearance_mode(message)

    else:
        textlabel = customtkinter.CTkLabel(master=chatArea, text=message, fg_color="royalblue", text_color="white", corner_radius=16, font=("Roboto", 16))
        textlabel.pack(ipady=3, pady=5, padx=3, anchor="e")
        message = f"{username}: {message}"
        privateFrame.destroy()
        submitButton.configure(text="Submit")
        submitButton.pack_forget()
        textFrame.pack()
        privateButton.pack(pady=8, padx=8, side="bottom")
        privateButton.configure(state="normal")

        if private_state and ((len(OUTPUT))!=0) and ((len(OUTPUT))<(len(membersList)-1)):
            client_socket.send(f"{OUTPUT}\n{message}".encode(FORMAT))
            memstr = ", ".join(OUTPUT)
            textlabel = customtkinter.CTkLabel(master=chatArea, text=f"you sent a private message to {memstr}", font=("Roboto", 13))
            textlabel.pack()
            private_state = False

        else:
            client_socket.send(message.encode(FORMAT))




def login_button_clicked():
    global username
    username = loginEntry.get()
    login.destroy()
    client_socket.send(username.encode(FORMAT))



def stop():
    root.destroy()
    message = f"{username}: bye"
    client_socket.send(message.encode(FORMAT))
    client_socket.close()



def member_list(members):

    for widget in textFrame.winfo_children():
        widget.destroy()

    for member in members:
        namelabel = customtkinter.CTkLabel(master=textFrame,text='   '+member, anchor="w", width=110, font=("Roboto", 17))
        namelabel.pack(pady=5)

    if len(members) == 1:
        privateButton.configure(state='disabled')
    else:
        privateButton.configure(state='normal')

def private_list():
    checkboxes.clear()
    global username
    global private_state
    global privateFrame
    private_state = True
    textFrame.pack_forget()
    privateButton.pack_forget()
    submitButton.pack(pady=8, padx=8, side="bottom")
    privateFrame = customtkinter.CTkFrame(leftFrame, width=110)
    privateFrame.pack()

    for member in membersList:
        if member != username:
            current_var = customtkinter.IntVar()
            current_box = customtkinter.CTkCheckBox(
                master=privateFrame, text=member, variable=current_var, border_color="royalblue", hover_color="cornflowerblue", fg_color="royalblue", corner_radius=20,font=("Roboto", 16)
            )
            current_box.var = current_var
            current_box.pack(pady=10, side="bottom")
            checkboxes[current_box] = member




def selected_members():
    OUTPUT.clear()
    print(len(OUTPUT))
    for box in checkboxes:
        if box.var.get() == 1:
            OUTPUT.append(checkboxes[box])

    if ((len(OUTPUT))!=0) and ((len(OUTPUT))<(len(membersList)-1)):
        submitButton.configure(text="Submitted")


# connecting
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


# making login page
login = customtkinter.CTk()
login.geometry("600x800")
login.title("Chatroom")

# Create and pack the frame
frame = customtkinter.CTkFrame(master=login, corner_radius=20)
frame.pack(pady=280, padx=130, fill="both")

# Create and pack the login entry
loginEntry = customtkinter.CTkEntry(
    master=frame,
    placeholder_text="Enter your name",
    justify="center",
    width=250,
    height=50,
    border_width=0,
    font=("Roboto", 17),
    corner_radius=20,
    placeholder_text_color="gray",
)
loginEntry.pack(pady=30, expand=True)


# entering the username and closes the page
loginButton = customtkinter.CTkButton(
    master=frame,
    text="Login",
    font=("Roboto", 17),
    width=100,
    fg_color="royalblue",
    text_color="white",
    height=42,
    hover_color="cornflowerblue",
    corner_radius=30,
    command=login_button_clicked,
)
loginButton.pack(pady=20, padx=10)

# Start the main loop
login.mainloop()


root = customtkinter.CTk()
root.title("Chatroom")
root.geometry("600x800")


leftFrame = customtkinter.CTkFrame(
    master=root,
    height=400,
    width=100,
    corner_radius=20)
leftFrame.pack(pady=8, padx=8, fill="both", side="left")


# creating a label for members
label = customtkinter.CTkLabel(
    master=leftFrame,
    text="Members",
    font=("Roboto", 18),
    width=120,
    height=35,
    corner_radius=20,
    text_color="white",
    fg_color="royalblue",
)
label.pack(pady=10, padx=5)


# membersFrame = customtkinter.CTkFrame(master=leftFrame, height=650, width=110)
# membersFrame.pack()


textFrame = customtkinter.CTkFrame(master=leftFrame, height=650, width=110, corner_radius=0)
textFrame.pack()


privateFrame = customtkinter.CTkFrame(leftFrame, width=120)
privateFrame.pack_forget()
privateButton = customtkinter.CTkButton(
    master=leftFrame,
    text="Private",
    font=("Roboto", 16),
    width=120,
    fg_color="royalblue",
    text_color="white",
    height=37,
    hover_color="cornflowerblue",
    corner_radius=20,
    command=private_list,
)
privateButton.pack(pady=8, padx=8, side="bottom")



submitButton = customtkinter.CTkButton(
    master=leftFrame,
    text="Submit",
    font=("Roboto", 16),
    width=120,
    fg_color="royalblue",
    text_color="white",
    height=37,
    hover_color="cornflowerblue",
    corner_radius=20,
    command=selected_members,
)


rightFrame = customtkinter.CTkFrame(master=root,
        height=400,
        width=450,
        corner_radius=20)
rightFrame.pack(pady=8, padx=8, fill="both", expand=True, side="right")



chatArea = customtkinter.CTkScrollableFrame(
    master=rightFrame,
    height=650,
    width=450,
    corner_radius=20
)
chatArea.pack(pady=8, padx=10, fill="both", expand=True, side="top")



# messageArea = customtkinter.CTkFrame(
#     master=rightFrame,
#     height=50,
#     width=450,
#     corner_radius=20)
# messageArea.pack(fill="both", side="bottom")



entryFrame = customtkinter.CTkFrame(
    master=rightFrame,
    height=50,
    width=350,
    corner_radius=20
)
entryFrame.pack(fill="both", expand=True, side="left")



sendFrame = customtkinter.CTkFrame(
    master=rightFrame,
    height=50,
    width=50,
    corner_radius=20
)
sendFrame.pack(fill="both", side="right")



messageEntry = customtkinter.CTkEntry(
    master=entryFrame,
    placeholder_text="Message",
    width=330,
    height=37,
    corner_radius=20,
    border_width=0,
)
messageEntry.pack(pady=5, padx=5, expand=True, fill="both")



sendButton = customtkinter.CTkButton(
    master=sendFrame,
    text="Send",
    font=("Roboto", 14),
    width=20,
    corner_radius=18,
    fg_color="royalblue",
    text_color="white",
    height=37,
    hover_color="cornflowerblue",
    command=send,
)
sendButton.pack(pady=5, padx=5)


receive_thread = threading.Thread(target=receive)
receive_thread.start()

root.protocol("WM_DELETE_WINDOW", stop)

root.mainloop()
