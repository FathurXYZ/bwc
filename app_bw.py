import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def pilih_gambar():
    # Membuka jendela dialog untuk memilih file gambar
    filename = filedialog.askopenfilenames(
        title="Pilih Gambar",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )
    
    if filename:
        # Menyimpan daftar file ke variabel global agar bisa diproses
        global file_terpilih
        file_terpilih = filename
        label_info.config(text=f"{len(filename)} gambar dipilih.")
        btn_convert.config(state="normal", bg="#4CAF50") # Aktifkan tombol convert
    else:
        label_info.config(text="Belum ada gambar yang dipilih.")

def proses_konversi():
    if not file_terpilih:
        return

    jumlah_sukses = 0
    
    for path_file in file_terpilih:
        try:
            # 1. Buka Gambar
            img = Image.open(path_file)
            
            # 2. Buat folder output di lokasi gambar asli
            folder_asal = os.path.dirname(path_file)
            folder_output = os.path.join(folder_asal, "Hasil_BW")
            
            if not os.path.exists(folder_output):
                os.makedirs(folder_output)
            
            # 3. Konversi ke Hitam Putih
            img_bw = img.convert("L")
            
            # 4. Simpan dengan nama baru
            nama_asli = os.path.basename(path_file)
            path_simpan = os.path.join(folder_output, f"bw_{nama_asli}")
            
            img_bw.save(path_simpan)
            jumlah_sukses += 1
            
            # Update status di label (efek loading sederhana)
            label_status.config(text=f"Memproses: {nama_asli}...")
            window.update() # Refresh UI agar tidak macet/freeze
            
        except Exception as e:
            print(f"Gagal: {e}")

    # Reset UI setelah selesai
    label_status.config(text="Selesai!")
    messagebox.showinfo("Berhasil", f"Selesai! {jumlah_sukses} gambar telah disimpan di folder 'Hasil_BW'.")
    file_terpilih_reset()

def file_terpilih_reset():
    global file_terpilih
    file_terpilih = []
    label_info.config(text="Silakan pilih gambar lagi.")
    btn_convert.config(state="disabled", bg="#cccccc")

# --- MEMBUAT TAMPILAN (GUI) ---
window = tk.Tk()
window.title("Aplikasi Foto Hitam Putih")
window.geometry("400x300")
window.config(bg="#f0f0f0")

file_terpilih = []

# Judul
label_judul = tk.Label(window, text="Konverter Hitam Putih", font=("Arial", 16, "bold"), bg="#f0f0f0")
label_judul.pack(pady=20)

# Tombol Pilih
btn_pilih = tk.Button(window, text="📂 Pilih Gambar", command=pilih_gambar, font=("Arial", 12), width=20)
btn_pilih.pack(pady=5)

# Label Info Jumlah File
label_info = tk.Label(window, text="Belum ada gambar dipilih", bg="#f0f0f0")
label_info.pack(pady=5)

# Tombol Convert (Awalnya dimatikan/abu-abu)
btn_convert = tk.Button(window, text="🚀 Ubah Jadi Hitam Putih", command=proses_konversi, state="disabled", bg="#cccccc", fg="white", font=("Arial", 12, "bold"), width=25, height=2)
btn_convert.pack(pady=20)

# Label Status Proses
label_status = tk.Label(window, text="", bg="#f0f0f0", fg="blue")
label_status.pack(pady=5)

# Menjalankan Aplikasi
window.mainloop()