from flask import Flask, jsonify, make_response, request
from sqlalchemy import create_engine, text

QUERY_VERIFICA_DUPLICIDADE = text(
    "SELECT 1 FROM receitas WHERE data = :date AND description = :desc")
QUERY_CADASTRO_RECEITA = text(
    "INSERT INTO receitas(description, value, data) VALUES (:desc, :value, :date)")


app = Flask(__name__)


@app.post('/receitas')
def cadastro_de_receitas():
    data = request.get_json()

    try:
        with alchemy_engine.connect() as db_connection:
            if db_connection.execute(QUERY_VERIFICA_DUPLICIDADE, {"date": data["date"], "desc": data["description"]}).scalar():
                return make_response(jsonify({"message": "Transação Duplicada"}), 400)

            db_connection.execute(QUERY_CADASTRO_RECEITA, {
                                  "desc": data["description"], "value": data["value"], "date": data["date"]})
            db_connection.commit()

        return make_response(jsonify({"message": "Receita cadastrada"}), 201)
    except Exception as e:
        return make_response(jsonify({"message": "Erro ao cadastrar receita"}), 500)


if __name__ == '__main__':

    url = 'postgresql+psycopg2://lucas:@localhost/estudo'
    alchemy_engine = create_engine(url)
    app.run(debug=True)
