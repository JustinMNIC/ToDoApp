import customtkinter as ctk

class mainframe(ctk.CTk):
    tasks = []

    def __init__(self):
        super().__init__()

        self.title("What you'll do today ;)")
        self.geometry("800x400")

        self.grid_columnconfigure(tuple(range(7)), weight=1, uniform="yes")
        self.grid_rowconfigure(tuple(range(15)), weight=1, uniform="yes")

        var_message = ctk.StringVar(self, value="Work hard\nParty harder!", name="var_message")
        self.message = ctk.CTkLabel(self, text=var_message.get(), text_color="red")
        self.message.grid(row=0, rowspan=2, column=2, columnspan=3)

        self.add_new_task = ctk.CTkEntry(self, placeholder_text="type something..")
        self.add_new_task.grid(row=2, column=0, columnspan=2, sticky="news")
        
        self.button_add_new_task = ctk.CTkButton(self, text="ADD", command=self.new_task)
        self.button_add_new_task.grid(row=2, column=2)

        self.checkbox_frame = ctk.CTkFrame(self)
        self.checkbox_frame.grid(row=4, rowspan=10, column=0, columnspan=7, sticky="news")

    def show_tasks(self, *args):
        for child in self.checkbox_frame.winfo_children():
            child.destroy()
        for i, task in enumerate(self.tasks):
            button_task = ctk.CTkButton(self.checkbox_frame, text=task, command=lambda i=i: self.remove_task(i))
            button_task.pack()

    def new_task(self):
        textt = self.add_new_task.get()
        if textt != "":
            self.tasks.append(textt)
        self.add_new_task.delete(0, 'end')
        self.show_tasks()


    def remove_task(self, index):
        self.tasks.pop(index)
        self.show_tasks()

if __name__ == "__main__":
    program = mainframe()
    program.mainloop()
