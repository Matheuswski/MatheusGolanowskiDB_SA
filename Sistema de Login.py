# login.py
import customtkinter as ctk
from tkinter import messagebox
from db_config import conectar

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Login")
        self.geometry("400x350")
        self.resizable(False, False)
        
        self.criar_interface()
    
    def criar_interface(self):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=50, padx=20, fill="both", expand=True)
        
        label_titulo = ctk.CTkLabel(frame, text="Login", font=("Arial", 24))
        label_titulo.pack(pady=20)
        
        # Campo de usuário
        ctk.CTkLabel(frame, text="Usuário").pack()
        self.entry_usuario = ctk.CTkEntry(frame, width=200)
        self.entry_usuario.pack(pady=5)
        
        # Campo de senha
        ctk.CTkLabel(frame, text="Senha").pack()
        self.entry_senha = ctk.CTkEntry(frame, width=200, show="*")
        self.entry_senha.pack(pady=5)
        
        # Botão de login
        ctk.CTkButton(frame, text="Entrar", command=self.verificar_login).pack(pady=20)
        
        # Botão para cadastro
        ctk.CTkButton(frame, text="Criar Conta", command=self.abrir_cadastro,
                     fg_color="transparent", border_width=1).pack(pady=5)
    
    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados")
            return
            
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT tipo FROM usuario WHERE nome = %s AND senha = %s", 
                (usuario, senha)
            )
            resultado = cursor.fetchone()
            
            if resultado:
                tipo = resultado[0]
                self.destroy()  # Fecha a janela de login
                
                if tipo == "administrador":
                    from admin_menu import abrir_menu_admin
                    abrir_menu_admin()
                else:
                    from sistema_compras import abrir_tela_compra
                    abrir_tela_compra()
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao verificar login: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    
    def abrir_cadastro(self):
        from cadastro_usuario import CadastroUsuario
        cadastro = CadastroUsuario(self)
        cadastro.grab_set()  # Torna a janela modal

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()