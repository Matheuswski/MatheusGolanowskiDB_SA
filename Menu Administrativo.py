# admin_menu.py
import customtkinter as ctk
from tkinter import messagebox
from db_config import conectar

class AdminMenu:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Painel Administrativo")
        self.janela.geometry("500x450")
        self.janela.resizable(False, False)
        
        self.criar_interface()
    
    def criar_interface(self):
        self.main_frame = ctk.CTkFrame(self.janela)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(
            self.main_frame, 
            text="Menu Administrativo", 
            font=("Arial", 20, "bold")
        ).pack(pady=(10, 20))
        
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20)
        
        botoes = [
            ("👥 Usuários", self.abrir_crud_usuario),
            ("🏢 Fornecedores", self.abrir_crud_fornecedor),
            ("📦 Produtos", self.abrir_crud_produto),
            ("👨‍💼 Funcionários", self.abrir_crud_funcionario)
        ]
        
        for texto, comando in botoes:
            btn = ctk.CTkButton(
                btn_frame,
                text=texto,
                command=comando,
                height=40,
                font=("Arial", 14),
                corner_radius=8
            )
            btn.pack(pady=8, fill="x")
        
        ctk.CTkButton(
            self.main_frame,
            text="🚪 Sair",
            command=self.janela.destroy,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "#DCE4EE"),
            height=40,
            font=("Arial", 14),
            corner_radius=8
        ).pack(pady=(20, 10), padx=20, fill="x")
    
    def abrir_crud_usuario(self):
        from crud_usuario import UsuarioCRUD
        self.janela.withdraw()
        usuario_crud = UsuarioCRUD(self.janela)
        self.janela.wait_window(usuario_crud.janela)
        self.janela.deiconify()
    
    def abrir_crud_fornecedor(self):
        from crud_fornecedor import FornecedorCRUD
        self.janela.withdraw()
        fornecedor_crud = FornecedorCRUD(self.janela)
        self.janela.wait_window(fornecedor_crud.janela)
        self.janela.deiconify()
    
    def abrir_crud_produto(self):
        from crud_produto import ProdutoCRUD
        self.janela.withdraw()
        produto_crud = ProdutoCRUD(self.janela)
        self.janela.wait_window(produto_crud.janela)
        self.janela.deiconify()
    
    def abrir_crud_funcionario(self):
        from crud_funcionario import FuncionarioCRUD
        self.janela.withdraw()
        funcionario_crud = FuncionarioCRUD(self.janela)
        self.janela.wait_window(funcionario_crud.janela)
        self.janela.deiconify()

def abrir_menu_admin():
    app = AdminMenu()
    app.janela.mainloop()

if __name__ == "__main__":
    abrir_menu_admin()