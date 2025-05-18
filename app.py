import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

#Functions from other classes
from embed import embed_watermark
from verify import verify_watermark
from tamper_check import detect_tampering
from image_utils import crop_image, rotate_image, resize_image, compress_image

class StegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography Tool")
        self.root.geometry("800x600")

        self.cover_img = None
        self.watermark_img = None
        self.watermark_embedded = False
        self.embedded_image_loaded = False

        # UI elements
        self.img_label = tk.Label(self.root)
        self.img_label.pack(pady=10)

        self.create_buttons()

    def create_buttons(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        #Main Functionalities
        tk.Button(btn_frame, text="Load Embedded Image", command=self.load_embedded_image).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Load Cover Image", command=self.load_cover_image).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Load Watermark", command=self.load_watermark).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Embed Watermark", command=self.embed_watermark).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Verify Watermark", command=self.verify_watermark).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Detect Tampering", command=self.detect_tampering).grid(row=0, column=5, padx=5)
        
        #Tampering Functionalities
        tk.Button(btn_frame, text="Crop Image", command=self.crop_current_image).grid(row=1, column=0, pady=(20, 0))
        tk.Button(btn_frame, text="Rotate Image", command=self.rotate_current_image).grid(row=1, column=1, pady=(20, 0))
        tk.Button(btn_frame, text="Resize Image", command=self.resize_current_image).grid(row=1, column=2, pady=(20, 0))
        tk.Button(btn_frame, text="Compress Image", command=self.compress_current_image).grid(row=1, column=3, pady=(20, 0))
        
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
            
    def load_embedded_image(self):
        path = filedialog.askopenfilename(title="Select Embedded Image")
        if path:
            self.cover_img = cv2.imread(path)
            self.display_image(self.cover_img)
            self.watermark_embedded = True #Assume image is already embedded (tampered or not)
            self.embedded_image_loaded = True

    def embed_watermark(self):
        if self.cover_img is None or self.watermark_img is None:
            messagebox.showerror("Error", "Load both cover and watermark images first.")
            return
        
        if self.embedded_image_loaded == True:
            messagebox.showwarning("Warning", "Image is already embedded")
            return
        
        try:
            embedded = embed_watermark(self.cover_img, self.watermark_img)
            
            self.cover_img = embedded
            self.display_image(embedded)
            self.watermark_embedded = True
            self.embedded_image = False
            
            save_path = "assets/embedded_output.png"
            cv2.imwrite(save_path, embedded)
            
            messagebox.showinfo("Success", "Watermark embedding successful!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Embedding failed: {str(e)}")

    def verify_watermark(self):
        if self.cover_img is None or self.watermark_img is None:
            messagebox.showerror("Error", "Load an image (embedded or cover) and watermark first.")
            return
        
        if not self.watermark_embedded:
            messagebox.showwarning("Missing Watermark", "Embed an image or load an embedded image")
            return
            
        is_present, match_pct= verify_watermark(self.cover_img, self.watermark_img)
        
        if is_present:
            messagebox.showinfo("Verification", f"Watermark detected! Match: {match_pct:.2%}")
        else:
            messagebox.showwarning("Verification", f"Watermark NOT detected. Match: {match_pct:.2%}")

    def detect_tampering(self):
        if self.cover_img is None or self.watermark_img is None:
            messagebox.showerror("Error", "Load an image (embedded or cover) and watermark first")
            return
        
        if not self.watermark_embedded:
            messagebox.showwarning("Missing Watermark", "Embed an image or load an embedded image")
            return
        
        tampered, match_pct, cause = detect_tampering(self.cover_img, self.watermark_img)
        
        if tampered:
            messagebox.showinfo("Tampering Detected", f"Watermark mismatch detected. \nMatch: {match_pct:.2%} \nCause: {cause}")
        else:
            messagebox.showinfo("No Tampering", f"Watermark consistent.\nMatch: {match_pct:.2%} \nStatus: {cause}")
        
    
    def display_image(self, image):
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(rgb)
        img_resized = img_pil.resize((400, 400))  # Adjust size to fit window
        tk_img = ImageTk.PhotoImage(img_resized)
        self.img_label.config(image=tk_img)
        self.img_label.image = tk_img
        
    #Tampering Functions
    
    def crop_current_image(self):
        if not self.watermark_embedded:
            messagebox.showwarning("Tampering Not Allowed", "Please embed an image")
            return
        
        self.cover_img = crop_image(self.cover_img)
        self.display_image(self.cover_img)
        messagebox.showinfo("Tampering Applied", "Image Cropped")
        
    def rotate_current_image(self):
        if not self.watermark_embedded:
            messagebox.showwarning("Tampering Not Allowed", "Please embed an image")
            return
        
        self.cover_img = rotate_image(self.cover_img)
        self.display_image(self.cover_img)
        messagebox.showinfo("Tampering Applied", "Image Rotated")
        
    def resize_current_image(self):
        if not self.watermark_embedded:
            messagebox.showwarning("Tampering Not Allowed", "Please embed an image")
            return
        
        self.cover_img = resize_image(self.cover_img)
        self.display_image(self.cover_img)
        messagebox.showinfo("Tampering Applied", "Image Resized")
        
    def compress_current_image(self):
        if not self.watermark_embedded:
            messagebox.showwarning("Tampering Not Allowed", "Please embed an image")
            return
        
        self.cover_img = compress_image(self.cover_img)
        self.display_image(self.cover_img)
        messagebox.showinfo("Tampering Applied", "Image Compressed")
        

def launch_app():
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()