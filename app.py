import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os

# Optional: Import your logic modules here
# from embedder.embed import embed_watermark
# from verifier.verify import verify_watermark
# from detector.tamper_check import detect_tampering

class StegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography Tool")
        self.root.geometry("800x600")

        self.cover_img = None
        self.watermark_img = None

        # UI elements
        self.img_label = tk.Label(self.root)
        self.img_label.pack(pady=10)

        self.create_buttons()

    def create_buttons(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Load Cover Image", command=self.load_cover_image).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Load Watermark", command=self.load_watermark).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Embed Watermark", command=self.embed_watermark).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Verify Watermark", command=self.verify_watermark).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Detect Tampering", command=self.detect_tampering).grid(row=0, column=4, padx=5)

    def load_cover_image(self):
        path = filedialog.askopenfilename(title="Select Cover Image")
        if path:
            self.cover_img = cv2.imread(path)
            self.display_image(self.cover_img)

    def load_watermark(self):
        path = filedialog.askopenfilename(title="Select Watermark Image")
        if path:
            self.watermark_img = cv2.imread(path)
            messagebox.showinfo("Watermark", "Watermark image loaded successfully!")

    def embed_watermark(self):
        if self.cover_img is None or self.watermark_img is None:
            messagebox.showerror("Error", "Load both cover and watermark images first.")
            return
        # embedded = embed_watermark(self.cover_img, self.watermark_img)
        # self.display_image(embedded)
        messagebox.showinfo("Embed", "Watermark embedding not yet implemented.")

    def verify_watermark(self):
        if self.cover_img is None:
            messagebox.showerror("Error", "Load an image first.")
            return
        # result = verify_watermark(self.cover_img, self.watermark_img)
        # messagebox.showinfo("Verification Result", f"Watermark present: {result}")
        messagebox.showinfo("Verify", "Watermark verification not yet implemented.")

    def detect_tampering(self):
        if self.cover_img is None:
            messagebox.showerror("Error", "Load an image first.")
            return
        # result = detect_tampering(self.cover_img, self.watermark_img)
        # messagebox.showinfo("Tampering Result", f"Tampering Detected: {result}")
        messagebox.showinfo("Detect", "Tampering detection not yet implemented.")

    def display_image(self, image):
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(rgb)
        img_resized = img_pil.resize((400, 400))  # Adjust size to fit window
        tk_img = ImageTk.PhotoImage(img_resized)
        self.img_label.config(image=tk_img)
        self.img_label.image = tk_img

def launch_app():
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()