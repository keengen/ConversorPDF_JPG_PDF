import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
from tkinter.ttk import Notebook


class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Imagens")
        self.root.geometry("700x600")
        
        # Notebook (abas)
        self.notebook = Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Abas
        self.create_jpg_to_pdf_tab()
        self.create_pdf_to_jpg_tab()
        
    def create_jpg_to_pdf_tab(self):
        """Cria a aba de conversão JPG para PDF"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="JPG para PDF")
        
        # Variáveis
        self.jpg_input = tk.StringVar()
        self.pdf_output = tk.StringVar()
        self.combine_var = tk.BooleanVar(value=False)
        self.single_file_mode = tk.BooleanVar(value=False)
        
        # Widgets
        ttk.Label(tab, text="Conversor JPG para PDF", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Frame de seleção de modo
        mode_frame = ttk.Frame(tab)
        mode_frame.pack(pady=5)
        ttk.Radiobutton(mode_frame, text="Pasta com vários JPGs", variable=self.single_file_mode, 
                        value=False, command=self.update_jpg_ui).grid(row=0, column=0, padx=10)
        ttk.Radiobutton(mode_frame, text="Arquivo JPG único", variable=self.single_file_mode, 
                        value=True, command=self.update_jpg_ui).grid(row=0, column=1, padx=10)
        
        # Frame de entrada
        input_frame = ttk.Frame(tab)
        input_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(input_frame, text="Origem:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.jpg_input, width=50).grid(row=1, column=0, padx=5)
        ttk.Button(input_frame, text="Selecionar", command=self.select_jpg_input).grid(row=1, column=1)
        
        # Frame de saída
        output_frame = ttk.Frame(tab)
        output_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(output_frame, text="Destino:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(output_frame, textvariable=self.pdf_output, width=50).grid(row=1, column=0, padx=5)
        ttk.Button(output_frame, text="Selecionar", command=self.select_pdf_output).grid(row=1, column=1)
        
        # Opções
        options_frame = ttk.Frame(tab)
        options_frame.pack(pady=10)
        ttk.Checkbutton(options_frame, text="Combinar todos JPGs em um único PDF", 
                        variable=self.combine_var, state='disabled').grid(row=0, column=0, sticky=tk.W)
        
        # Lista de arquivos
        self.jpg_list = scrolledtext.ScrolledText(tab, width=80, height=10, state='disabled')
        self.jpg_list.pack(pady=10)
        
        # Progresso
        self.jpg_progress = ttk.Progressbar(tab, orient=tk.HORIZONTAL, length=500, mode='determinate')
        self.jpg_progress.pack(pady=5)
        
        # Botão de conversão
        ttk.Button(tab, text="Converter para PDF", command=self.convert_to_pdf).pack(pady=10)
        
        # Status
        self.jpg_status = ttk.Label(tab, text="Selecione os arquivos de origem e destino", foreground="gray")
        self.jpg_status.pack()
        
        self.update_jpg_ui()
    
    def create_pdf_to_jpg_tab(self):
        """Cria a aba de conversão PDF para JPG"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="PDF para JPG")
        
        # Variáveis
        self.pdf_input = tk.StringVar()
        self.jpg_output = tk.StringVar()
        self.single_pdf_mode = tk.BooleanVar(value=False)
        
        # Widgets
        ttk.Label(tab, text="Conversor PDF para JPG", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Frame de seleção de modo
        mode_frame = ttk.Frame(tab)
        mode_frame.pack(pady=5)
        ttk.Radiobutton(mode_frame, text="Pasta com vários PDFs", variable=self.single_pdf_mode, 
                        value=False, command=self.update_pdf_ui).grid(row=0, column=0, padx=10)
        ttk.Radiobutton(mode_frame, text="Arquivo PDF único", variable=self.single_pdf_mode, 
                        value=True, command=self.update_pdf_ui).grid(row=0, column=1, padx=10)
        
        # Frame de entrada
        input_frame = ttk.Frame(tab)
        input_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(input_frame, text="Origem:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.pdf_input, width=50).grid(row=1, column=0, padx=5)
        ttk.Button(input_frame, text="Selecionar", command=self.select_pdf_input).grid(row=1, column=1)
        
        # Frame de saída
        output_frame = ttk.Frame(tab)
        output_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(output_frame, text="Destino:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(output_frame, textvariable=self.jpg_output, width=50).grid(row=1, column=0, padx=5)
        ttk.Button(output_frame, text="Selecionar", command=self.select_jpg_output).grid(row=1, column=1)
        
        # Lista de arquivos
        self.pdf_list = scrolledtext.ScrolledText(tab, width=80, height=10, state='disabled')
        self.pdf_list.pack(pady=10)
        
        # Progresso
        self.pdf_progress = ttk.Progressbar(tab, orient=tk.HORIZONTAL, length=500, mode='determinate')
        self.pdf_progress.pack(pady=5)
        
        # Botão de conversão
        ttk.Button(tab, text="Converter para JPG", command=self.convert_to_jpg).pack(pady=10)
        
        # Status
        self.pdf_status = ttk.Label(tab, text="Selecione os arquivos de origem e destino", foreground="gray")
        self.pdf_status.pack()
        
        self.update_pdf_ui()
    
    def update_jpg_ui(self):
        """Atualiza a UI da aba JPG para PDF"""
        if self.single_file_mode.get():
            self.combine_var.set(False)
            self.combine_var.set(False)
            for widget in self.notebook.winfo_children():
                if isinstance(widget, ttk.Frame):
                    for child in widget.winfo_children():
                        if "Combinar" in str(child):
                            child.configure(state='disabled')
            self.update_jpg_list()
        else:
            for widget in self.notebook.winfo_children():
                if isinstance(widget, ttk.Frame):
                    for child in widget.winfo_children():
                        if "Combinar" in str(child):
                            child.configure(state='normal')
            self.update_jpg_list()
    
    def update_pdf_ui(self):
        """Atualiza a UI da aba PDF para JPG"""
        self.update_pdf_list()
    
    def select_jpg_input(self):
        """Seleciona a entrada (arquivo ou pasta) JPG"""
        if self.single_file_mode.get():
            file = filedialog.askopenfilename(
                title="Selecione o arquivo JPG",
                filetypes=(("Arquivos JPG", "*.jpg"), ("Todos os arquivos", "*.*"))
            )
            if file:
                self.jpg_input.set(file)
        else:
            folder = filedialog.askdirectory(title="Selecione a pasta com os arquivos JPG")
            if folder:
                self.jpg_input.set(folder)
        self.update_jpg_list()
    
    def select_pdf_output(self):
        """Seleciona a pasta de saída PDF"""
        folder = filedialog.askdirectory(title="Selecione a pasta para salvar os PDFs")
        if folder:
            self.pdf_output.set(folder)
    
    def select_pdf_input(self):
        """Seleciona a entrada (arquivo ou pasta) PDF"""
        if self.single_pdf_mode.get():
            file = filedialog.askopenfilename(
                title="Selecione o arquivo PDF",
                filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*"))
            )
            if file:
                self.pdf_input.set(file)
        else:
            folder = filedialog.askdirectory(title="Selecione a pasta com os arquivos PDF")
            if folder:
                self.pdf_input.set(folder)
        self.update_pdf_list()
    
    def select_jpg_output(self):
        """Seleciona a pasta de saída JPG"""
        folder = filedialog.askdirectory(title="Selecione a pasta para salvar os JPGs")
        if folder:
            self.jpg_output.set(folder)
    
    def update_jpg_list(self):
        """Atualiza a lista de arquivos JPG"""
        self.jpg_list.config(state='normal')
        self.jpg_list.delete(1.0, tk.END)
        
        input_path = self.jpg_input.get()
        if not input_path:
            self.jpg_list.insert(tk.END, "Nenhum arquivo ou pasta selecionado")
            self.jpg_status.config(text="Selecione os arquivos de origem e destino", foreground="gray")
            self.jpg_list.config(state='disabled')
            return
        
        if self.single_file_mode.get():
            # Modo arquivo único
            if os.path.isfile(input_path):
                self.jpg_list.insert(tk.END, f"Arquivo selecionado:\n\n{os.path.basename(input_path)}")
                self.jpg_status.config(text="1 arquivo JPG selecionado", foreground="black")
            else:
                self.jpg_list.insert(tk.END, "Nenhum arquivo JPG válido selecionado")
                self.jpg_status.config(text="Selecione um arquivo JPG válido", foreground="red")
        else:
            # Modo pasta
            if os.path.isdir(input_path):
                jpg_files = [f for f in os.listdir(input_path) if f.lower().endswith('.jpg')]
                if not jpg_files:
                    self.jpg_list.insert(tk.END, "Nenhum arquivo JPG encontrado na pasta selecionada")
                    self.jpg_status.config(text="Nenhum JPG encontrado", foreground="red")
                else:
                    self.jpg_list.insert(tk.END, f"{len(jpg_files)} arquivo(s) JPG encontrado(s):\n\n")
                    for file in jpg_files:
                        self.jpg_list.insert(tk.END, f"• {file}\n")
                    self.jpg_status.config(text=f"{len(jpg_files)} arquivo(s) JPG encontrado(s)", foreground="black")
            else:
                self.jpg_list.insert(tk.END, "Pasta inválida selecionada")
                self.jpg_status.config(text="Selecione uma pasta válida", foreground="red")
        
        self.jpg_list.config(state='disabled')
    
    def update_pdf_list(self):
        """Atualiza a lista de arquivos PDF"""
        self.pdf_list.config(state='normal')
        self.pdf_list.delete(1.0, tk.END)
        
        input_path = self.pdf_input.get()
        if not input_path:
            self.pdf_list.insert(tk.END, "Nenhum arquivo ou pasta selecionado")
            self.pdf_status.config(text="Selecione os arquivos de origem e destino", foreground="gray")
            self.pdf_list.config(state='disabled')
            return
        
        if self.single_pdf_mode.get():
            # Modo arquivo único
            if os.path.isfile(input_path) and input_path.lower().endswith('.pdf'):
                self.pdf_list.insert(tk.END, f"Arquivo selecionado:\n\n{os.path.basename(input_path)}")
                self.pdf_status.config(text="1 arquivo PDF selecionado", foreground="black")
            else:
                self.pdf_list.insert(tk.END, "Nenhum arquivo PDF válido selecionado")
                self.pdf_status.config(text="Selecione um arquivo PDF válido", foreground="red")
        else:
            # Modo pasta
            if os.path.isdir(input_path):
                pdf_files = [f for f in os.listdir(input_path) if f.lower().endswith('.pdf')]
                if not pdf_files:
                    self.pdf_list.insert(tk.END, "Nenhum arquivo PDF encontrado na pasta selecionada")
                    self.pdf_status.config(text="Nenhum PDF encontrado", foreground="red")
                else:
                    self.pdf_list.insert(tk.END, f"{len(pdf_files)} arquivo(s) PDF encontrado(s):\n\n")
                    for file in pdf_files:
                        self.pdf_list.insert(tk.END, f"• {file}\n")
                    self.pdf_status.config(text=f"{len(pdf_files)} arquivo(s) PDF encontrado(s)", foreground="black")
            else:
                self.pdf_list.insert(tk.END, "Pasta inválida selecionada")
                self.pdf_status.config(text="Selecione uma pasta válida", foreground="red")
        
        self.pdf_list.config(state='disabled')
    
    def convert_to_pdf(self):
        """Converte JPG para PDF"""
        input_path = self.jpg_input.get()
        output_path = self.pdf_output.get()
        
        if not input_path or not output_path:
            messagebox.showerror("Erro", "Selecione os caminhos de entrada e saída!")
            return
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        try:
            if self.single_file_mode.get():
                # Conversão de arquivo único
                if not os.path.isfile(input_path):
                    messagebox.showerror("Erro", "Arquivo JPG de entrada inválido!")
                    return
                
                self.jpg_progress['maximum'] = 1
                self.jpg_progress['value'] = 0
                self.root.update_idletasks()
                
                output_file = os.path.join(output_path, os.path.splitext(os.path.basename(input_path))[0] + '.pdf')
                
                try:
                    img = Image.open(input_path)
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    img.save(output_file, "PDF", resolution=100.0)
                    self.jpg_progress['value'] = 1
                    self.jpg_status.config(text=f"Conversão concluída: {os.path.basename(output_file)}", foreground="green")
                    messagebox.showinfo("Sucesso", f"Arquivo convertido com sucesso:\n{output_file}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao converter arquivo:\n{e}")
                    self.jpg_status.config(text="Erro na conversão", foreground="red")
            else:
                # Conversão de pasta
                jpg_files = [f for f in os.listdir(input_path) if f.lower().endswith('.jpg')]
                
                if not jpg_files:
                    messagebox.showwarning("Aviso", "Nenhum arquivo JPG encontrado na pasta selecionada!")
                    return
                
                self.jpg_progress['maximum'] = len(jpg_files)
                self.jpg_progress['value'] = 0
                self.root.update_idletasks()
                
                if self.combine_var.get():
                    # Combina todos em um PDF
                    output_file = os.path.join(output_path, "combinado.pdf")
                    images = []
                    
                    for i, jpg_file in enumerate(jpg_files, 1):
                        try:
                            img = Image.open(os.path.join(input_path, jpg_file))
                            if img.mode == 'RGBA':
                                img = img.convert('RGB')
                            images.append(img)
                            self.jpg_status.config(text=f"Processando {i}/{len(jpg_files)}: {jpg_file}")
                            self.jpg_progress['value'] = i
                            self.root.update_idletasks()
                        except Exception as e:
                            messagebox.showwarning("Aviso", f"Erro ao processar {jpg_file}: {e}")
                    
                    if images:
                        images[0].save(
                            output_file, "PDF", 
                            resolution=100.0, 
                            save_all=True, 
                            append_images=images[1:]
                        )
                        self.jpg_status.config(text=f"PDF combinado criado: {output_file}", foreground="green")
                        messagebox.showinfo("Sucesso", f"PDF combinado criado com sucesso:\n{output_file}")
                else:
                    # Converte cada JPG para PDF individual
                    for i, jpg_file in enumerate(jpg_files, 1):
                        try:
                            img = Image.open(os.path.join(input_path, jpg_file))
                            if img.mode == 'RGBA':
                                img = img.convert('RGB')
                            
                            output_file = os.path.join(output_path, os.path.splitext(jpg_file)[0] + '.pdf')
                            img.save(output_file, "PDF", resolution=100.0)
                            
                            self.jpg_status.config(text=f"Convertendo {i}/{len(jpg_files)}: {jpg_file}")
                            self.jpg_progress['value'] = i
                            self.root.update_idletasks()
                        except Exception as e:
                            messagebox.showwarning("Aviso", f"Erro ao converter {jpg_file}: {e}")
                    
                    self.jpg_status.config(text=f"Conversão concluída! {len(jpg_files)} arquivo(s) processado(s).", foreground="green")
                    messagebox.showinfo("Sucesso", f"Conversão concluída!\n{len(jpg_files)} arquivo(s) processado(s).")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a conversão:\n{e}")
            self.jpg_status.config(text="Erro na conversão", foreground="red")
        finally:
            self.jpg_progress['value'] = 0
    
    def convert_to_jpg(self):
        """Converte PDF para JPG"""
        input_path = self.pdf_input.get()
        output_path = self.jpg_output.get()
        
        if not input_path or not output_path:
            messagebox.showerror("Erro", "Selecione os caminhos de entrada e saída!")
            return
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        try:
            if self.single_pdf_mode.get():
                # Conversão de arquivo único
                if not os.path.isfile(input_path) or not input_path.lower().endswith('.pdf'):
                    messagebox.showerror("Erro", "Arquivo PDF de entrada inválido!")
                    return
                
                self.pdf_progress['maximum'] = 1
                self.pdf_progress['value'] = 0
                self.root.update_idletasks()
                
                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_file = os.path.join(output_path, f"{base_name}.jpg")
                
                try:
                    images = self._pdf_to_images(input_path)
                    if images:
                        images[0].save(output_file, "JPEG", quality=95)
                        self.pdf_progress['value'] = 1
                        self.pdf_status.config(text=f"Conversão concluída: {os.path.basename(output_file)}", foreground="green")
                        messagebox.showinfo("Sucesso", f"Arquivo convertido com sucesso:\n{output_file}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao converter arquivo:\n{e}")
                    self.pdf_status.config(text="Erro na conversão", foreground="red")
            else:
                # Conversão de pasta
                pdf_files = [f for f in os.listdir(input_path) if f.lower().endswith('.pdf')]
                
                if not pdf_files:
                    messagebox.showwarning("Aviso", "Nenhum arquivo PDF encontrado na pasta selecionada!")
                    return
                
                self.pdf_progress['maximum'] = len(pdf_files)
                self.pdf_progress['value'] = 0
                self.root.update_idletasks()
                
                success_count = 0
                
                for i, pdf_file in enumerate(pdf_files, 1):
                    try:
                        pdf_path = os.path.join(input_path, pdf_file)
                        base_name = os.path.splitext(pdf_file)[0]
                        output_file = os.path.join(output_path, f"{base_name}.jpg")
                        
                        images = self._pdf_to_images(pdf_path)
                        if images:
                            images[0].save(output_file, "JPEG", quality=95)
                            success_count += 1
                        
                        self.pdf_status.config(text=f"Convertendo {i}/{len(pdf_files)}: {pdf_file}")
                        self.pdf_progress['value'] = i
                        self.root.update_idletasks()
                    except Exception as e:
                        messagebox.showwarning("Aviso", f"Erro ao converter {pdf_file}: {e}")
                
                self.pdf_status.config(
                    text=f"Conversão concluída! {success_count}/{len(pdf_files)} arquivo(s) processado(s).", 
                    foreground="green"
                )
                messagebox.showinfo(
                    "Sucesso", 
                    f"Conversão concluída!\n{success_count} de {len(pdf_files)} arquivo(s) processado(s)."
                )
        
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a conversão:\n{e}")
            self.pdf_status.config(text="Erro na conversão", foreground="red")
        finally:
            self.pdf_progress['value'] = 0
    
    def _pdf_to_images(self, pdf_path):
        """Converte um PDF em uma lista de imagens (uma por página)"""
        try:
            images = []
            with Image.open(pdf_path) as img:
                img.load()  # Carrega todas as páginas
                
                # Se o PDF tem múltiplas páginas, iteramos por elas
                for page in range(img.n_frames):
                    img.seek(page)
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    images.append(img.copy())
            
            return images
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar PDF:\n{e}")
            return None


def main():
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
