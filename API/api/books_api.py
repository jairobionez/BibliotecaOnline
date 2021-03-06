from flask import Flask, jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from connect_db import connectToDb
import psycopg2

books_api = Blueprint('books_api', 'books_api', url_prefix="/api/books")

@books_api.route('/', methods=['GET', 'POST', 'PUT'])
def api_verbs():
    if request.method == 'GET':
        conn = connectToDb()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute('select * from livros')
            result = cur.fetchall()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return jsonify(result)

    elif request.method == 'POST':
        dados = request.json

        conn = connectToDb()
        cur = conn.cursor()

        try:
            cur.execute('''
                        insert into livros (titulo, autor, editora, descricao, datapublicacao)
                        values (%s, %s, %s, %s, %s);
                        ''',
                        (dados['titulo'],
                         dados['autor'],
                         dados['editora'],
                         dados['descricao'],
                         dados['datapublicacao']))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return "Livro inserido com sucesso"

    else:
        dados = request.json

        conn = connectToDb()
        cur = conn.cursor()

        try:
            cur.execute('''
                        update livros
                        set titulo = %s, autor = %s, editora = %s, descricao = %s, datapublicacao = %s
                        where id = %s
                        ''',
                        (dados['titulo'],
                         dados['autor'],
                         dados['editora'],
                         dados['descricao'],
                         dados['datapublicacao'],
                         dados['id']))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return("Livro atualizado com sucesso")


@books_api.route('/<string:id>', methods=['GET'])
def get_books_by_id(id):
    conn = connectToDb()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    print(id)

    try:
        cur.execute('''select * from livros where id = %s''', (id,))
        result = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return jsonify(result)

@books_api.route('/<string:id>', methods=['DELETE'])
def delete(id):
    conn = connectToDb()
    cur = conn.cursor()

    try:
        cur.execute('''delete from livros where id = %s ''', (id,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return "Livro deletado com sucesso"
