import tkinter as tk
from tkinter import ttk, filedialog, Scale, HORIZONTAL
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps
import os
import numpy as np
from pathlib import Path
import cv2
from tkinterdnd2 import DND_FILES, TkinterDnD

class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Filtering App")
        self.root.geometry("1200x800")

        #variables
        self.original_image = None
        self.displayed_image = None
        self.current_image = None
        self.filename = None
        self.export_format = tk.StringVar(value='png')
        self.export_quality = tk.IntVar(value=90)
        self.export_filename = tk.StringVar(value='filtered_image')

        #track transformation states
        self.rotation_angle = 0
        self.flip_horizontal = False
        self.flip_vertical = False
        self.zoom_factor = 1.0

        #Create UI
        self.create_ui()

        #setup drag & drop
        self.setup_drag_drop()

    def create_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        left_panel = ttk.LabelFrame(main_frame, text="Filters & Tools")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)


        upload_frame = ttk.Frame(left_panel)
        upload_frame.pack(fill=tk.X, padx=5, pady=5)


        upload_btn = ttk.Button(upload_frame, text="Upload Image", command=self.upload_image)
        upload_btn.pack(fill=tk.X, padx=5, pady=5)


        reset_btn = ttk.Button(upload_frame, text="Reset To Original", command=self.upload_image)
        reset_btn.pack(fill=tk.X, padx=5, pady=5)


        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=5)


        filter_notebook = ttk.Notebook(left_panel)
        filter_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


        basic_filters_frame = ttk.Frame(filter_notebook)
        filter_notebook.add(basic_filters_frame, text="Basic Filters")

        basic_filters = [
            ("Grayscale", self.apply_grayscale),
            ("Sepia", self.apply_sepia),
            ("Negative", self.apply_negative),
            ("Black $ White", self.apply_bw_threshold)
        ]

        for filter_name, filter_function in basic_filters:
            btn = ttk.Button(basic_filters_frame, text=filter_name, command=filter_function)
            btn.pack(fill=tk.X, padx=5, pady=3)


        adjustments_frame = ttk.Frame(filter_notebook)
        filter_notebook.add(adjustments_frame, text="Adjustments")

        #Brigthness
        ttk.Label(adjustments_frame, text="Brightness:").pack(anchor=tk.W, padx=5, pady=2)
        brightness_scale = Scale(adjustments_frame, from_=0, to=200, orient=HORIZONTAL,
                                 resolution=1, command=self.adjust_brightness)
        brightness_scale.set(100)
        brightness_scale.pack(fill=tk.X, padx=5, pady=2)

        #Contrast
        ttk.Label(adjustments_frame, text="Contrast:").pack(anchor=tk.W, padx=5, pady=2)
        contrast_scale = Scale(adjustments_frame, from_=0, to=200, orient=HORIZONTAL,
                               resolution=1, command=self.adjust_contrast)
        contrast_scale.set(100)
        contrast_scale.pack(fill=tk.X, padx=5, pady=2)

        #Saturation
        ttk.Label(adjustments_frame, text='Saturation:').pack(anchor=tk.W, padx=5, pady=2)
        saturation_scale = Scale(adjustments_frame, from_=0, to=200, orient=HORIZONTAL,
                               resolution=1, command=self.adjust_contrast)
        saturation_scale.set(100)
        saturation_scale.pack(fill=tk.X, padx=5, pady=2)

        #Blur
        ttk.Label(adjustments_frame, text="Blur:").pack(anchor=tk.W, padx=5, pady=2)
        blur_scale = Scale(adjustments_frame, from_=0, to=200, orient=HORIZONTAL,
                           resolution=1, command=self.adjust_blur)
        blur_scale.set(0)
        blur_scale.pack(fill=tk.X, padx=5, pady=2)

        #Sharpen
        ttk.Label(adjustments_frame, text="Sharpen:").pack(anchor=tk.W, padx=5, pady=2)
        sharpen_scale = Scale(adjustments_frame, from_=0, to=10, orient=HORIZONTAL,
                              resolution=0.1, command=self.adjust_sharpen)
        sharpen_scale.set(0)
        sharpen_scale.pack(fill=tk.X, padx=5, pady=2)


        edit_frame = ttk.Frame(filter_notebook)
        filter_notebook.add(edit_frame, text="Edit")


        rotate_from = ttk.Frame(edit_frame)
        rotate_from.pack(fill=tk.X, padx=5, pady=5)


        ttk.Button(rotate_from, text="Rotate 90°", command=lambda: self.rotate_image(90)).pack(side=tk.LEFT, padx=2)
        ttk.Button(rotate_from, text="Rotate 180°", command=lambda: self.rotate_image(180)).pack(side=tk.LEFT, padx=2)
        ttk.Button(rotate_from, text="Rotate 270°", command=lambda: self.rotate_image(270)).pack(side=tk.LEFT, padx=2)
        

        flip_frame = ttk.Frame(edit_frame)
        flip_frame.pack(fill=tk.X, padx=5, pady=5)


        ttk.Button(flip_frame, text="Flip Horizontal", command=self.flip_horizontal_image).pack(side=tk.LEFT, padx=2)
        ttk.Button(flip_frame, text="Flip Vertical", command=self.flip_vertical_image).pack(side=tk.LEFT, padx=2)


        zoom_frame = ttk.Frame(edit_frame)
        zoom_frame.pack(fill=tk.X, padx=5, pady=5)


        ttk.Button(zoom_frame, text="Zoom in", command=self.zoom_in).pack(side=tk.LEFT, padx=2)
        ttk.Button(zoom_frame, text="Zoom Out", command=self.zoom_out).pack(side=tk.LEFT, padx=2)
        ttk.Button(zoom_frame, text="Reset Zoom", command=self.reset_zoom).pack(side=tk.LEFT, padx=2)


        ttk.Button(edit_frame, text="Crop (Select Region)", command=self.start_crop).pack(fill=tk.X, padx=5, pady=5)


        effects_frame = ttk.Frame(filter_notebook)
        filter_notebook.add(effects_frame, text="Effects")

        effects = [
            ("Edge Detection", self.apply_edge_detection),
            ("Vignette", self.apply_vignette),
            ("Vintage", self.apply_vintage),
            ("Color Inversion", self.apply_color_inversion)
        ]

        for effect_name, effect_function in effects:
            btn = ttk.Button(effects_frame, text=effect_name, command=effect_function)
            btn.pack(fill=tk.X, padx=5, pady=3)


        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=10)


        export_frame = ttk.LabelFrame(left_panel, text="Export Options")
        export_frame.pack(fill=tk.X, padx=5, pady=5)


        ttk.Label(export_frame, text="Filename:").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Entry(export_frame, textvariable=self.export_filename).pack(fill=tk.X, padx=5, pady=2)


        format_frame = ttk.Frame(export_frame)
        format_frame.pack(fill=tk.X, padx=5, pady=2)


        ttk.Label(format_frame, text="Format:").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="PNG", variable=self.export_format, value="png").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="JPEG", variable=self.export_format, value="jpeg").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="WebP", variable=self.export_format, value="webp").pack(side=tk.LEFT, padx=5)


        ttk.Label(export_frame, text="Quality:").pack(anchor=tk.W, padx=5, pady=2)
        quality_scale = Scale(export_frame, from_=1, to=100, orient=HORIZONTAL,
                              variable=self.export_quality)
        quality_scale.pack(fill=tk.X, padx=5, pady=2)


        ttk.Button(export_frame, text="Save Image", command=self.save_image).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(export_frame, text="Save Before/After", command=self.save_before_after).pack(fill=tk.X, padx=5, pady=5)


        right_panel = ttk.LabelFrame(main_frame, text="Image Preview")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)


        self.canvas = tk.Canvas(right_panel, bg="lightgray")
        self.canvas.pack(fill=tk.BOTH, expand=True)


        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Upload an image to begin")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_drag_drop(self):
        self.canvas.drop_target_register("DND_Files")
        self.canvas.dnd_bind('<<Drop>>', self.drop)

    def drop(self, event):
        file_path = event.data.strip('{}')
        if os.path.isfile(file_path):
            self.load_image(file_path)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path):
        try:
            self.filename = file_path
            self.original_image = Image.open(file_path)
            self.current_image = self.original_image.copy()
            self.display_image()


            base_name = os.path.splitext(base_name)[0]
            name_without_ext = os.path.splitext(base_name)[0]
            self.export_filename.set(f"{name_without_ext}_filtered")


            self.status_var.set(f"Loaded image: {base_name}")
        except Exception as e:
            self.status_var.set(f"Error laoding image: {str(e)}")

    def display_image(self):
        if self.current_image:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            img_width, img_height = self.current_image.size


            display_width = int(img_width * self.zoom_factor)
            display_height = int(img_height * self.zoom_factor)

            if display_width > canvas_width or display_height > canvas_height:
                width_ratio = canvas_width / display_width
                height_ratio = canvas_height / display_height
                ratio = min(width_ratio, height_ratio)

                display_width = int(display_width * ratio)
                display_height = int(display_height * ratio)
            
            display_img = self.current_image.copy()
            display_img = display_img.resize((display_width, display_height),  Image.LANCZOS)

            self.displayed_image = ImageTk.PhotoImage(display_img)

            self.canvas.delete('all')
            self.canvas.create_image(
                canvas_width // 2, canvas_height // 2,
                image=self.displayed_image,
                anchor=tk.CENTER
            )

    def reset_to_original(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.rotation_angle = 0
            self.flip_horizontal = False
            self.flip_vertical = False
            self.zoom_factor = 1.0
            self.display_image()
            self.status_var.set("Reset to original image")
    
    def apply_grayscale(self):
        if self.current_image:
            self.current_image = ImageOps.grayscale(self.current_image).convert('RGB')
            self.display_image()
            self.status_var.set('Applied: Grayscale')

    def apply_sepia(self):
        if self.current_image:
            gray_img = ImageOps.grayscale(self.current_image)

            sepia_data = np.array(gray_img)
            sepia_data = cv2.cvtColor(sepia_data, cv2.COLOR_GRAY2RGB)

            sepia_data = sepia_data.astype(np.float64)
            sepia_data[:, :, 0] = sepia_data[:, :, 0] * 0.393 + sepia_data[:, :, 1] * 0.769 + sepia_data[:, :, 2] * 0.189
            sepia_data[:, :, 1] = sepia_data[:, :, 0] * 0.349 + sepia_data[:, :, 1] * 0.686 + sepia_data[:, :, 2] * 0.168
            sepia_data[:, :, 2] = sepia_data[:, :, 0] * 0.272 + sepia_data[:, :, 1] * 0.534 + sepia_data[:, :, 2] * 0.131

            sepia_data = np.clip(sepia_data, 0, 255).astype(np.uint8)

            self.current_image = Image.fromarray(sepia_data)
            self.display_image()
            self.status_var.set("Applied: Sepia")


    def apply_negative(self):
        if self.current_image:
            self.current_image = ImageOps.invert(self.current_image)
            self.display_image()
            self.status_var.set("Applied: Negative")

    def apply_bw_threshold(self):
        if self.current_image:
          gray_img = ImageOps.grayscale(self.current_image)

          threshold = 127
          self.current_image = gray_img.point(lambda p: 255 if p > threshold else 0).convert('RGB')
          self.display_image()
          self.status_var.set('Applied: Black & White Threshold')

    def adjust_brightness(self, value):
        if self.original_image:
            temp_img = self.original_image.copy()

            if self.rotation_angle != 0:
                temp_img = temp_img.rotate(self.rotation_angle, expand=True)
            if self.flip_horizontal:
                temp_img = ImageOps.mirror(temp_img)
            if self.flip_vertical:
                temp_img = ImageOps.flip(temp_img)

            factor = float(value) / 100
            enhancer = ImageEnhance.Brightness(temp_img)
            self.current_image = enhancer.enhance(factor)
            self.display_image()
            self.status_var.set(f"Brightness: {value}%")

    def adjust_contrast(self, value):
        if self.original_image:
            temp_img = self.original_image.copy()

            if self.rotation_angle != 0:
                temp_img = temp_img.rotate(self.rotation_angle, expand=True)
            if self.flip_horizontal:
                temp_img = ImageOps.mirror(temp_img)
            if self.flip_vertical:
                temp_img = ImageOps.flip(temp_img)

            factor = float(value) / 100
            enhancer = ImageEnhance.Contrast(temp_img)
            self.current_image = enhancer.enhance(factor)
            self.display_image()
            self.status_var.set(f"Contrast: {value}%")

    def adjust_saturation(self, value):
        if self.original_image:
            temp_img = self.original_image.copy()

            if self.rotation_angle != 0:
                temp_img = temp_img.rotate(self.rotation_angle, expand=True)
            if self.flip_horizontal:
                temp_img = ImageOps.mirror(temp_img)
            if self.flip_vertical:
                temp_img = ImageOps.flip(temp_img)

            factor = float(value) / 100
            enhancer = ImageEnhance.Color(temp_img)
            self.current_image = enhancer.enhance(factor)
            self.display_image()
            self.status_var.set(f"Saturation: {value}%")

    def adjust_blur(self, value):
        if self.original_image:
            # Create a copy of the original image for adjustments
            temp_img = self.original_image.copy()
            
            # Apply previous transformations
            if self.rotation_angle != 0:
                temp_img = temp_img.rotate(self.rotation_angle, expand=True)
            if self.flip_horizontal:
                temp_img = ImageOps.mirror(temp_img)
            if self.flip_vertical:
                temp_img = ImageOps.flip(temp_img)

            radius = float(value)
            if radius > 0:
                self.current_image = temp_img.filter(ImageFilter.GaussianBlur(radius=radius))
            else:
                self.current_image = temp_img
            self.display_image()
            self.status_var.set(f"Blur: {value}")

    def adjust_sharpen(self, value):
        if self.original_image:
            # Create a copy of the original image for adjustments
            temp_img = self.original_image.copy()
            
            # Apply previous transformations
            if self.rotation_angle != 0:
                temp_img = temp_img.rotate(self.rotation_angle, expand=True)
            if self.flip_horizontal:
                temp_img = ImageOps.mirror(temp_img)
            if self.flip_vertical:
                temp_img = ImageOps.flip(temp_img)

            factor = float(value)
            if factor > 0:
                self.current_image = temp_img.filter(ImageFilter.UnsharpMask(radius=2, percent=factor * 50, threshold=3))
            else:
                self.current_image = temp_img
            self.display_image()
            self.status_var.set(f"Sharpen: {value}")

    def rotate_image(self, degrees):
        if self.current_image:
            self.rotation_angle = (self.rotation_angle + degrees) % 360
            self.current_image = self.current_image.rotate(degrees, expand=True)
            self.display_image()
            self.status_var.set(f"Rotated image {degrees}")

    def flip_horizontal_image(self):
        if self.current_image:
            self.flip_horizontal = not self.flip_horizontal
            self.current_image = ImageOps.mirror(self.current_image)
            self.display_image()
            self.status_var.set("Flipped image horizontally")

    def flip_vertical_image(self):
        if self.current_image:
            self.flip_vertical = not self.flip_vertical
            self.current_image = ImageOps.flip(self.current_image)
            self.display_image()
            self.status_var.set("Flipped image vertically")

    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.display_image()
        self.status_var.set(f"Zoom: {self.zoom_factor:.2f}x")

    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.display_image()
        self.status_var.set("Zoom reset to 1.0x")

    def reset_zoom(self):
        pass

    def start_crop(self):
        pass

    def on_crop_start(self, event):
        pass

    def on_crop_drag(self, event):
        pass

    def on_crop_release(self, event):
        pass

    def apply_edge_detection(self):
        pass

    def apply_vignette(self):
        pass

    def apply_vintage(self):
        pass

    def apply_color_inversion(self):
        pass

    def save_image(self):
        pass

    def save_before_after(self):
        pass

    def on_resize(self, event):
        pass

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageFilterApp(root)


    root.bind("<Configure>", app.on_resize)


    style = ttk.Style()
    if 'clam' in style.theme_names():
        style.theme_use('clam')
    

    root.minsize(900, 600)

    root.mainloop()