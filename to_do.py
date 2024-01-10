import customtkinter as ctk
import json


class mainframe(ctk.CTk):
    json_file = "./tasks.json"

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

        self.load_json_data()
        self.show_tasks()

    def new_task(self):
        text = self.add_new_task.get()
        if text != "":
            new_task = {
                f"task_id_{len(data.keys()) + 1}": {
                    "task": text,
                    "completed": False
                }
            }
            data.update(new_task)
            with open(self.json_file, "w") as file:
                json.dump(data, file, indent=2)
        self.add_new_task.delete(0, 'end')
        self.show_tasks()

    def load_json_data(self):
        global data
        try:
            with open(self.json_file, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}
            with open(self.json_file, "w") as file:
                json.dump(data, file, indent=2)

    def show_tasks(self, *args):
        for child in self.checkbox_frame.winfo_children():
            child.destroy()
        self.load_json_data()
        for key, val in data.items():
            if not val["completed"]:
                var_checkbox = ctk.IntVar(value=val["completed"])
                checkbox_task = ctk.CTkCheckBox(self.checkbox_frame, text=val["task"], variable=var_checkbox)
                checkbox_task.bind("<Button-1>", lambda event, key=key, var_checkbox=var_checkbox: self.toggle_task(key, var_checkbox.get()))
                checkbox_task.pack()
                
    def toggle_task(self, index, state):
        data[index]["completed"] = state
        print
        with open(self.json_file, "w") as file:
            json.dump(data, file, indent=2)
        self.load_json_data()
        self.show_tasks()

if __name__ == "__main__":
    program = mainframe()
    program.mainloop()
