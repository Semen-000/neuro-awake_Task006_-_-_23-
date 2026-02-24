import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import csv
import os
from datetime import datetime

class OperatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Нейрободр - Идентификация оператора")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Создание папок и файлов
        self.setup_files()
        
        # Переменные
        self.current_operator_id = None
        self.operator_data = {}
        
        # Показываем стартовое окно
        self.show_start_window()
    
    def setup_files(self):
        """Создание необходимых папок и файлов"""
        if not os.path.exists('operations'):
            os.makedirs('operations')
        
        if not os.path.exists('operation_db.csv'):
            with open('operation_db.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'last_name', 'first_name', 'middle_name', 'age', 
                               'birth_date', 'birth_time', 'software_start_time', 'days_duration'])
    
    def show_start_window(self):
        """Окно №1 - Стартовая форма"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Заголовок
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="НЕЙРОБОДР", font=('Arial', 30, 'bold'), 
                bg='#2c3e50', fg='white').pack(expand=True)
        
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
        
        tk.Label(main_frame, text="Группа для администратора и постоянного пользователя", 
                font=('Arial', 18), bg='#f0f0f0', fg='#34495e').pack(pady=30)
        
        btn_container = tk.Frame(main_frame, bg='#f0f0f0')
        btn_container.pack(expand=True)
        
        tk.Label(btn_container, text="Выберите необходимые действия:", 
                font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#2c3e50').pack(pady=40)
        
        btn_frame = tk.Frame(btn_container, bg='#f0f0f0')
        btn_frame.pack()
        
        tk.Button(btn_frame, text="РЕГИСТРАЦИЯ", command=self.show_registration_form,
                font=('Arial', 18, 'bold'), bg='#27ae60', fg='white', 
                padx=50, pady=25, width=12).pack(side=tk.LEFT, padx=30)
        
        tk.Button(btn_frame, text="АВТОРИЗАЦИЯ", command=self.show_auth_form,
                font=('Arial', 18, 'bold'), bg='#2980b9', fg='white', 
                padx=50, pady=25, width=12).pack(side=tk.LEFT, padx=30)
    
    def show_registration_form(self):
        """Форма регистрации"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        title_frame = tk.Frame(self.root, bg='#27ae60', height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="РЕГИСТРАЦИЯ ОПЕРАТОРА", font=('Arial', 22, 'bold'), 
                bg='#27ae60', fg='white').pack(expand=True)
        
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Блок регистрации
        reg_frame = tk.LabelFrame(main_container, text="Регистрация оператора", 
                                  font=('Arial', 16, 'bold'), bg='white', 
                                  padx=30, pady=20)
        reg_frame.pack(fill=tk.X, pady=10)
        
        fields = [
            ('Фамилия:', 'last_name'),
            ('Имя:', 'first_name'),
            ('Отчество:', 'middle_name'),
            ('Возраст:', 'age')
        ]
        
        self.reg_entries = {}
        for label_text, field_name in fields:
            frame = tk.Frame(reg_frame, bg='white')
            frame.pack(fill=tk.X, pady=8)
            
            tk.Label(frame, text=label_text, width=12, anchor='w', bg='white', 
                    font=('Arial', 14)).pack(side=tk.LEFT)
            
            entry = tk.Entry(frame, width=40, font=('Arial', 14))
            entry.pack(side=tk.LEFT, padx=10)
            self.reg_entries[field_name] = entry
        
        tk.Button(reg_frame, text="ЗАПИСАТЬ", command=self.save_operator,
                bg='#27ae60', fg='white', font=('Arial', 14, 'bold'),
                padx=30, pady=8, width=12).pack(pady=15)
        
        # Блок идентификации
        self.id_frame = tk.LabelFrame(main_container, text="Идентификация", 
                                      font=('Arial', 16, 'bold'), bg='white', 
                                      padx=30, pady=20)
        
        # Блок информации
        self.info_frame = tk.LabelFrame(main_container, text="Информационный блок", 
                                        font=('Arial', 16, 'bold'), bg='white', 
                                        padx=30, pady=20)
        
        tk.Button(self.root, text="← НАЗАД", command=self.show_start_window,
                bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                padx=20, pady=5).pack(pady=10)
    
    def save_operator(self):
        """Сохранение данных оператора"""
        last_name = self.reg_entries['last_name'].get()
        first_name = self.reg_entries['first_name'].get()
        age = self.reg_entries['age'].get()
        
        if not all([last_name, first_name, age]):
            messagebox.showerror("Ошибка", "Заполните фамилию, имя и возраст!")
            return
        
        # Получаем следующий ID
        next_id = 1
        if os.path.exists('operation_db.csv'):
            with open('operation_db.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                if len(rows) > 1:
                    next_id = int(rows[-1][0]) + 1
        
        now = datetime.now()
        
        with open('operation_db.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                next_id,
                last_name,
                first_name,
                self.reg_entries['middle_name'].get(),
                age,
                now.strftime('%d-%m-%Y'),
                now.strftime('%H:%M:%S'),
                now.strftime('%H:%M:%S'),
                '00:00:00'
            ])
        
        self.current_operator_id = next_id
        self.operator_data = {
            'id': next_id,
            'last_name': last_name,
            'first_name': first_name,
            'middle_name': self.reg_entries['middle_name'].get(),
            'age': age
        }
        
        messagebox.showinfo("Успех", f"Оператор зарегистрирован с ID: {next_id}")
        
        self.id_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.show_identification()
    
    def show_identification(self):
        """Блок идентификации"""
        for widget in self.id_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.id_frame, text="ТРЕБОВАНИЕ К ФОТО: 800 x 600 px", 
                font=('Arial', 14, 'bold'), fg='#e67e22', bg='white').pack(pady=10)
        
        tk.Button(self.id_frame, text="ЗАГРУЗИТЬ ФОТО", command=self.upload_photo,
                bg='#3498db', fg='white', font=('Arial', 14, 'bold'),
                padx=30, pady=10, width=15).pack(pady=15)
        
        self.photo_frame = tk.Frame(self.id_frame, bg='#ecf0f1', bd=2, 
                                   width=500, height=400)
        self.photo_frame.pack(pady=15)
        self.photo_frame.pack_propagate(False)
        
        self.photo_label = tk.Label(self.photo_frame, bg='#ecf0f1')
        self.photo_label.pack(expand=True, fill=tk.BOTH)
    
    def upload_photo(self):
        """Загрузка фото"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        
        if file_path:
            try:
                img = Image.open(file_path)
                width, height = img.size
                
                if width == 800 and height == 600:
                    if self.current_operator_id:
                        save_path = f"operations/ID_{self.current_operator_id}.jpg"
                        img.save(save_path)
                        
                        img.thumbnail((480, 380))
                        photo = ImageTk.PhotoImage(img)
                        self.photo_label.config(image=photo)
                        self.photo_label.image = photo
                        
                        self.show_verification_result(True)
                    else:
                        messagebox.showerror("Ошибка", "ID оператора не найден")
                else:
                    messagebox.showerror("Ошибка", 
                                       f"Неверный размер!\nТребуется: 800x600\nПолучено: {width}x{height}")
                    self.show_verification_result(False)
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить фото: {str(e)}")
    
    def show_verification_result(self, success):
        """Результат верификации"""
        for widget in self.info_frame.winfo_children():
            widget.destroy()
        
        if success:
            tk.Label(self.info_frame, text="✅ УСПЕШНАЯ ВЕРИФИКАЦИЯ", 
                    font=('Arial', 16, 'bold'), fg='#27ae60', bg='white').pack(pady=15)
        else:
            tk.Label(self.info_frame, text="❌ НЕУДАЧНАЯ ВЕРИФИКАЦИЯ", 
                    font=('Arial', 16, 'bold'), fg='#e74c3c', bg='white').pack(pady=15)
            
            tk.Label(self.info_frame, text="Оператор не определен.\nПройти идентификацию заново?",
                    font=('Arial', 14), bg='white').pack(pady=15)
            
            btn_frame = tk.Frame(self.info_frame, bg='white')
            btn_frame.pack(pady=15)
            
            tk.Button(btn_frame, text="ДАЛЕЕ", command=self.retry_identification,
                     bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                     padx=25, pady=8, width=10).pack(side=tk.LEFT, padx=10)
            
            tk.Button(btn_frame, text="ОТМЕНА", command=self.show_start_window,
                     bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                     padx=25, pady=8, width=10).pack(side=tk.LEFT, padx=10)
    
    def retry_identification(self):
        self.show_identification()
    
    def show_auth_form(self):
        """Авторизация - ТОЛЬКО ID (без пароля и hashlib)"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        title_frame = tk.Frame(self.root, bg='#2980b9', height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="АВТОРИЗАЦИЯ ОПЕРАТОРА", font=('Arial', 22, 'bold'), 
                bg='#2980b9', fg='white').pack(expand=True)
        
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
        
        auth_frame = tk.Frame(main_frame, bg='white', bd=3)
        auth_frame.pack(expand=True, ipadx=80, ipady=40)
        
        tk.Label(auth_frame, text="ВВЕДИТЕ ID ОПЕРАТОРА:", 
                font=('Arial', 18, 'bold'), bg='white', fg='#2c3e50').pack(pady=30)
        
        self.auth_id_entry = tk.Entry(auth_frame, font=('Arial', 20), width=12, 
                                     justify='center')
        self.auth_id_entry.pack(pady=15)
        
        tk.Label(auth_frame, text="(ID может состоять из одной цифры)", 
                font=('Arial', 12), bg='white', fg='#7f8c8d').pack(pady=10)
        
        # Обычная авторизация БЕЗ hashlib
        tk.Button(auth_frame, text="АВТОРИЗАЦИЯ", command=self.check_auth_simple,
                bg='#2980b9', fg='white', font=('Arial', 16, 'bold'),
                padx=40, pady=12, width=12).pack(pady=30)
        
        tk.Button(self.root, text="← НАЗАД", command=self.show_start_window,
                bg='#e74c3c', fg='white', font=('Arial', 14, 'bold'),
                padx=30, pady=8).pack()
    
    def check_auth_simple(self):
        """Проверка авторизации - ПРОСТАЯ (БЕЗ hashlib)"""
        operator_id = self.auth_id_entry.get().strip()
        
        if not operator_id:
            messagebox.showerror("Ошибка", "Введите ID оператора")
            return
        
        # Просто ищем ID в CSV без всякого хэширования
        if os.path.exists('operation_db.csv'):
            with open('operation_db.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['id'] == operator_id:
                        self.operator_data = {
                            'id': row['id'],
                            'last_name': row['last_name'],
                            'first_name': row['first_name'],
                            'middle_name': row['middle_name'],
                            'age': row['age']
                        }
                        self.current_operator_id = int(operator_id)
                        self.show_operator_info()
                        return
            
            messagebox.showerror("Ошибка", f"Оператор с ID {operator_id} не найден")
    
    def show_operator_info(self):
        """Информация об операторе"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        title_frame = tk.Frame(self.root, bg='#8e44ad', height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="ИНФОРМАЦИЯ ОПЕРАТОРА", font=('Arial', 22, 'bold'), 
                bg='#8e44ad', fg='white').pack(expand=True)
        
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        windows_frame = tk.Frame(main_frame, bg='#f0f0f0')
        windows_frame.pack(expand=True, fill=tk.BOTH)
        
        # Окно №1
        window1 = tk.LabelFrame(windows_frame, text="Окно №1", 
                               font=('Arial', 16, 'bold'), bg='white', 
                               padx=30, pady=20)
        window1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15)
        
        info_data1 = [
            ("Фамилия:", self.operator_data['last_name']),
            ("Имя:", self.operator_data['first_name']),
            ("Отчество:", self.operator_data['middle_name']),
            ("Дата рождения:", "12.04.2000"),
            ("Специальность:", "Физик"),
            ("Телефон:", "+7 (999) 123-45-67")
        ]
        
        for label, value in info_data1:
            frame = tk.Frame(window1, bg='white')
            frame.pack(fill=tk.X, pady=8)
            tk.Label(frame, text=label, width=18, anchor='w', bg='white', 
                    font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
            tk.Label(frame, text=value, anchor='w', bg='white', 
                    font=('Arial', 12)).pack(side=tk.LEFT, padx=8)
        
        # Окно №2
        window2 = tk.LabelFrame(windows_frame, text="Окно №2", 
                               font=('Arial', 16, 'bold'), bg='white', 
                               padx=30, pady=20)
        window2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15)
        
        info_data2 = [
            ("Название Имени Оператора:", "Петров"),
            ("Фамилия:", "Иванова"),
            ("Имя:", "Петров"),
            ("Отчество:", "Иванович"),
            ("Дата рождения:", "12.04.2000"),
            ("Специальность:", "Физик")
        ]
        
        for label, value in info_data2:
            frame = tk.Frame(window2, bg='white')
            frame.pack(fill=tk.X, pady=8)
            tk.Label(frame, text=label, width=26, anchor='w', bg='white', 
                    font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
            tk.Label(frame, text=value, anchor='w', bg='white', 
                    font=('Arial', 12)).pack(side=tk.LEFT, padx=8)
        
        tk.Button(self.root, text="← НАЗАД", command=self.show_start_window,
                bg='#e74c3c', fg='white', font=('Arial', 14, 'bold'),
                padx=30, pady=8).pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = OperatorApp(root)
    root.mainloop()