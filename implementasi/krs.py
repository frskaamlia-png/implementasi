        finally:
            if cursor:
                cursor.close()
            if db and db.is_connected():
                db.close()

    # MEMILIH DATA PADA TABEL
    def pilih_data(self, event):
        pilihan = self.tabel.selection()

        if not pilihan:
            return

        data = self.tabel.item(
            pilihan[0], "values"
        )

        self.id_terpilih = data[0]

        self.kode_mk.delete(0, tk.END)
        self.kode_mk.insert(0, data[1])

        self.mata_kuliah.delete(0, tk.END)
        self.mata_kuliah.insert(0, data[2])

        self.semester.set(data[3])
        self.sks.set(data[4])

    # EDIT KRS
    def edit(self):
        if self.id_terpilih is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data yang ingin diedit!"
            )
            return

        data = self.ambil_input()

        if data is None:
            return

        kode, matkul, semester, sks = data

        berhasil = self.jalankan_sql(
            "UPDATE krs SET kode_mk=%s, "
            "mata_kuliah=%s, semester=%s, sks=%s "
            "WHERE id_krs=%s AND nim=%s",
            (
                kode, matkul, semester, sks,
                self.id_terpilih, self.nim
            )
        )

        if berhasil:
            messagebox.showinfo(
                "Berhasil", "Data KRS berhasil diedit!"
            )
            self.bersihkan()
            self.tampilkan()

    # HAPUS KRS
    def hapus(self):
        if self.id_terpilih is None:
            messagebox.showwarning(
                "Peringatan",
                "Pilih data yang ingin dihapus!"
            )
            return

        yakin = messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus data ini?"
        )

        if yakin:
            berhasil = self.jalankan_sql(
                "DELETE FROM krs "
                "WHERE id_krs=%s AND nim=%s",
                (self.id_terpilih, self.nim)
            )

            if berhasil:
                messagebox.showinfo(
                    "Berhasil", "Data KRS berhasil dihapus!"
                )
                self.bersihkan()
                self.tampilkan()

    # MEMBERSIHKAN FORM
    def bersihkan(self):
        self.id_terpilih = None
        self.kode_mk.delete(0, tk.END)
        self.mata_kuliah.delete(0, tk.END)
        self.semester.set("")
        self.sks.set("")

        for item in self.tabel.selection():
            self.tabel.selection_remove(item)


# MENJALANKAN PROGRAM
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    DB_PASSWORD = simpledialog.askstring(
        "Koneksi MySQL", "Masukkan password MySQL root:", show="*", parent=root
    )
    if DB_PASSWORD is None:
        root.destroy()
        raise SystemExit

    try:
        buat_database()
        root.deiconify()
        aplikasi = LoginWindow(root)
        root.mainloop()

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Database Error",
            "Pastikan MySQL Laragon sudah aktif!\n\n"
            + str(error)
        )
        root.destroy()
