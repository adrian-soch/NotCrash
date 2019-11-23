import tkinter as tk

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.amp = 0
        self.master.title("NotCrash")
        self.master.configure(background='blue')
        self.frame = tk.Frame(self.master, variable = amp)

        self.volume = tk.Scale(self.parent)
        self.volume.set(5)
        self.volume.grid(row=3,column=2,columnspan =1,padx = 200, pady = 20)


if __name__ == "__main__":
    root = tk.Tk()
    
    root.mainloop()