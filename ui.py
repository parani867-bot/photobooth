import tkinter as tk
from camera import capture_photos, capture_single_photo
from processor import create_photo_strip
from PIL import Image, ImageTk
import os

BG = "#0f0f0f"
CARD = "#1c1c1c"
BTN = "#00c853"
TXT = "white"
SUB = "#bbbbbb"

class PhotoBoothUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Booth")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=BG)

        self.mode = tk.StringVar(value="Color")
        self.count = tk.IntVar(value=2)
        self.photos = []
        self.thumbs = []
        self.strip_img = None
        self.strip_path = None

        self.show_home()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def card(self):
        frame = tk.Frame(self.root, bg=CARD, padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        return frame

    # ---------------- HOME ----------------
    def show_home(self):
        self.clear()
        c = self.card()

        tk.Label(
            c, text="PHOTO BOOTH",
            fg=TXT, bg=CARD,
            font=("Segoe UI", 36, "bold")
        ).pack(pady=20)

        tk.Button(
            c, text="START",
            bg=BTN, fg="white",
            font=("Segoe UI", 22, "bold"),
            width=16, height=2,
            relief="flat",
            command=self.show_options
        ).pack(pady=20)

    # ---------------- OPTIONS ----------------
    def show_options(self):
        self.clear()
        c = self.card()

        tk.Label(
            c, text="Select Options",
            fg=TXT, bg=CARD,
            font=("Segoe UI", 28, "bold")
        ).pack(pady=20)

        for m in ["Color", "BW"]:
            tk.Radiobutton(
                c, text=m,
                variable=self.mode, value=m,
                fg=TXT, bg=CARD,
                selectcolor=CARD,
                font=("Segoe UI", 18)
            ).pack(anchor="w")

        for n in [2, 4, 6]:
            tk.Radiobutton(
                c, text=str(n),
                variable=self.count, value=n,
                fg=TXT, bg=CARD,
                selectcolor=CARD,
                font=("Segoe UI", 18)
            ).pack(anchor="w")

        tk.Button(
            c, text="TAKE PHOTO",
            bg=BTN, fg="white",
            font=("Segoe UI", 20, "bold"),
            width=18, height=2,
            relief="flat",
            command=self.start_session
        ).pack(pady=30)

    # ---------------- CAPTURE ----------------
    def start_session(self):
        self.clear()
        self.root.update()

        self.photos = capture_photos(
            self.mode.get(),
            self.count.get()
        )

        self.show_review()

    # ---------------- REVIEW ----------------
    def show_review(self):
        self.clear()
        c = self.card()

        tk.Label(
            c, text="REVIEW PHOTOS",
            fg=TXT, bg=CARD,
            font=("Segoe UI", 28, "bold")
        ).pack(pady=10)

        grid = tk.Frame(c, bg=CARD)
        grid.pack(pady=10)

        self.thumbs.clear()

        for i, path in enumerate(self.photos):
            img = Image.open(path).resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            self.thumbs.append(img_tk)

            tk.Button(
                grid, image=img_tk,
                bg=CARD, relief="flat",
                command=lambda idx=i: self.retake_photo(idx)
            ).grid(row=0, column=i, padx=10)

        tk.Label(
            c, text="Tap photo to retake",
            fg=SUB, bg=CARD,
            font=("Segoe UI", 14)
        ).pack(pady=10)

        tk.Button(
            c, text="CONFIRM",
            bg=BTN, fg="white",
            font=("Segoe UI", 20, "bold"),
            width=14, height=2,
            relief="flat",
            command=self.generate_strip
        ).pack(pady=20)

    def retake_photo(self, index):
        try:
            os.remove(self.photos[index])
        except:
            pass

        new_photo = capture_single_photo(self.mode.get())
        if new_photo:
            self.photos[index] = new_photo

        self.show_review()

    # ---------------- STRIP ----------------
    def generate_strip(self):
        self.clear()
        c = self.card()

        tk.Label(
            c, text="CREATING PHOTO STRIP...",
            fg=TXT, bg=CARD,
            font=("Segoe UI", 28, "bold")
        ).pack(pady=30)

        self.root.update()

        self.strip_path = create_photo_strip(self.photos)
        self.show_strip()

    def show_strip(self):
        self.clear()
        c = self.card()

        img = Image.open(self.strip_path)
        img.thumbnail((400, 1000))
        self.strip_img = ImageTk.PhotoImage(img)

        tk.Label(c, image=self.strip_img, bg=CARD).pack(pady=20)

        tk.Button(
            c, text="PRINT",
            bg=BTN, fg="white",
            font=("Segoe UI", 20, "bold"),
            width=14, height=2,
            relief="flat",
            command=self.finish_session
        ).pack(pady=10)

    # ---------------- FINISH ----------------
    def finish_session(self):
        self.clear()
        c = self.card()

        tk.Label(
            c, text="PRINTING...",
            fg=TXT, bg=CARD,
            font=("Segoe UI", 32, "bold")
        ).pack(pady=30)

        # 🔜 Printer integration goes here

        self.root.after(3000, self.show_home)
