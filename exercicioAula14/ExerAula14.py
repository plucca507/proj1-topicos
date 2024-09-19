import sqlite3

class LivrariaDB:
    def __init__(self, db_name='livraria.db'):
        self.db_name = db_name
        self._criar_tabela()

    def _conectar(self):
        return sqlite3.connect(self.db_name)

    def _criar_tabela(self):
        with self._conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    ano_publicacao INTEGER NOT NULL,
                    preco REAL NOT NULL
                )
            ''')
            conexao.commit()

    def adicionar_livro(self, titulo, autor, ano_publicacao, preco):
        with self._conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                INSERT INTO livros (titulo, autor, ano_publicacao, preco)
                VALUES (?, ?, ?, ?)
            ''', (titulo, autor, ano_publicacao, preco))
            conexao.commit()

    def exibir_livros(self):
        with self._conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('SELECT * FROM livros')
            livros = cursor.fetchall()
            return livros

    def atualizar_preco(self, titulo, novo_preco):
        with self._conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                UPDATE livros SET preco = ? WHERE titulo = ?
            ''', (novo_preco, titulo))
            conexao.commit()

    def remover_livro(self, titulo):
        with self._conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                DELETE FROM livros WHERE titulo = ?
            ''', (titulo,))
            conexao.commit()

class LivrariaApp:
    def __init__(self):
        self.db = LivrariaDB()

    def menu(self):
        while True:
            print("\n1. Adicionar novo livro")
            print("2. Exibir todos os livros")
            print("3. Atualizar preço de um livro")
            print("4. Remover um livro")
            print("5. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                self.adicionar_livro()
            elif opcao == '2':
                self.exibir_livros()
            elif opcao == '3':
                self.atualizar_preco()
            elif opcao == '4':
                self.remover_livro()
            elif opcao == '5':
                break
            else:
                print("Opção inválida!")

    def adicionar_livro(self):
        titulo = input("Título: ")
        autor = input("Autor: ")
        ano_publicacao = int(input("Ano de publicação: "))
        preco = float(input("Preço: "))
        self.db.adicionar_livro(titulo, autor, ano_publicacao, preco)

    def exibir_livros(self):
        livros = self.db.exibir_livros()
        if livros:
            for livro in livros:
                print(f"ID: {livro[0]}, Título: {livro[1]}, Autor: {livro[2]}, Ano: {livro[3]}, Preço: {livro[4]}")
        else:
            print("Nenhum livro encontrado.")

    def atualizar_preco(self):
        titulo = input("Título do livro para atualizar o preço: ")
        novo_preco = float(input("Novo preço: "))
        self.db.atualizar_preco(titulo, novo_preco)

    def remover_livro(self):
        titulo = input("Título do livro para remover: ")
        self.db.remover_livro(titulo)

# Executar o aplicativo
if __name__ == '__main__':
    app = LivrariaApp()
    app.menu()
