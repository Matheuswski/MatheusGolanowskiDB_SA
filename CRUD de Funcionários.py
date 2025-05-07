# crud_funcionario.py
import customtkinter as ctk
from db_config import conectar
from tkinter import messagebox
import re

class FuncionarioCRUD:
    def __init__(self, master):
        self.master = master
        self.janela = ctk.CTkToplevel(master)
        self.janela.title("CRUD - Funcionário")
        self.janela.geometry("800x600")
        
        self.criar_interface()
        self.listar_funcionarios()
    
    def criar_interface(self):
        # [...] (implementação similar ao código anterior)
        pass
    
    def listar_funcionarios(self):
        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados")
            return
            
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nome, cargo, cpf, salario FROM funcionario ORDER BY nome")
            
            # Limpar treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Preencher com novos dados
            for funcionario in cursor.fetchall():
                self.tree.insert("", "end", values=(
                    funcionario[0],
                    funcionario[1],
                    funcionario[2],
                    self.formatar_cpf(funcionario[3]),
                    f"R$ {funcionario[4]:.2f}"
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar funcionários: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    
    def inserir_funcionario(self):
        if not self.validar_campos():
            return
            
        conn = conectar()
        if conn is None:
            return
            
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO funcionario (nome, cargo, cpf, salario) VALUES (%s, %s, %s, %s)",
                (
                    self.campos["nome"].get(),
                    self.campos["cargo"].get(),
                    re.sub(r'[^0-9]', '', self.campos["cpf"].get()),
                    float(self.campos["salario"].get().replace(",", "."))
                )
            )
            conn.commit()
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
            self.limpar_campos()
            self.listar_funcionarios()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao inserir funcionário: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    
    # [...] (outros métodos permanecem iguais)