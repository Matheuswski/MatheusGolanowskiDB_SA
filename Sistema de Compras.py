# sistema_compras.py
import customtkinter as ctk
from tkinter import ttk
from db_config import conectar
from CTkMessagebox import CTkMessagebox

class SistemaCompras:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Sistema de Compras")
        self.janela.geometry("1000x700")
        
        self.criar_interface()
        self.carregar_produtos()
    
    def carregar_produtos(self):
        conn = conectar()
        if conn is None:
            CTkMessagebox(title="Erro", message="Não foi possível conectar ao banco", icon="cancel")
            return
            
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT p.id, p.nome, p.descricao, p.preco, p.quantidade, f.nome 
                FROM produto p
                LEFT JOIN fornecedor f ON p.id_fornecedor = f.id
                WHERE p.quantidade > 0
                ORDER BY p.nome
            """)
            
            # Limpar treeview
            for item in self.produtos_tree.get_children():
                self.produtos_tree.delete(item)
            
            # Adicionar produtos
            for produto in cursor.fetchall():
                self.produtos_tree.insert("", "end", values=(
                    produto[0],
                    produto[1],
                    produto[2],
                    f"R$ {produto[3]:.2f}",
                    produto[4],
                    produto[5] or "N/D"
                ))
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Falha ao carregar produtos: {str(e)}", icon="cancel")
        finally:
            cursor.close()
            conn.close()
    
    def finalizar_compra(self):
        if not self.carrinho_tree.get_children():
            CTkMessagebox(title="Aviso", message="Carrinho vazio!", icon="warning")
            return
        
        resposta = CTkMessagebox(
            title="Confirmar Compra",
            message="Deseja finalizar a compra?",
            icon="question",
            option_1="Cancelar",
            option_2="Confirmar"
        )
        
        if resposta.get() == "Confirmar":
            conn = conectar()
            if conn is None:
                return
                
            cursor = conn.cursor()
            try:
                # Registrar venda
                cursor.execute("INSERT INTO venda (total) VALUES (%s)", (self.total_compra,))
                venda_id = cursor.lastrowid
                
                # Registrar itens
                for item in self.carrinho_tree.get_children():
                    valores = self.carrinho_tree.item(item, "values")
                    produto_id = valores[0]
                    quantidade = int(valores[2])
                    preco_unitario = float(valores[3].replace("R$ ", ""))
                    
                    cursor.execute("""
                        INSERT INTO item_venda 
                        (id_venda, id_produto, quantidade, preco_unitario) 
                        VALUES (%s, %s, %s, %s)
                    """, (venda_id, produto_id, quantidade, preco_unitario))
                    
                    # Atualizar estoque
                    cursor.execute("""
                        UPDATE produto 
                        SET quantidade = quantidade - %s 
                        WHERE id = %s
                    """, (quantidade, produto_id))
                
                conn.commit()
                CTkMessagebox(title="Sucesso", message="Compra realizada com sucesso!", icon="check")
                self.limpar_carrinho()
                self.carregar_produtos()
            except Exception as e:
                conn.rollback()
                CTkMessagebox(title="Erro", message=f"Falha ao registrar compra: {str(e)}", icon="cancel")
            finally:
                cursor.close()
                conn.close()

def abrir_tela_compra():
    app = SistemaCompras()
    app.janela.mainloop()