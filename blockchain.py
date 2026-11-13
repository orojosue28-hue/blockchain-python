"""Blockchain básica en Python con prueba de trabajo y API REST en Flask.

Autor: Josué García Orozco

Cómo ejecutarlo:
    pip install -r requirements.txt
    python blockchain.py

Después abre en el navegador http://127.0.0.1:5001
"""

import datetime
import hashlib
import json

from flask import Flask, jsonify

# Cuántos ceros debe tener al inicio un hash para considerarse válido.
# Más ceros = minar tarda más (mayor dificultad).
PREFIJO_DIFICULTAD = '0000'


class Blockchain:
    """Cadena de bloques guardada en memoria (se reinicia al apagar el servidor)."""

    def __init__(self):
        self.chain = []
        # Bloque génesis: el primero de la cadena, no tiene bloque anterior.
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        """Crea un bloque nuevo y lo agrega al final de la cadena."""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        """Devuelve el último bloque de la cadena."""
        return self.chain[-1]

    @staticmethod
    def hash_proof(proof, previous_proof):
        """Calcula el hash SHA-256 que relaciona una prueba con la anterior.

        Se usa tanto para minar como para validar, por eso vive en una sola
        función: así las dos partes siempre aplican la misma regla.
        """
        operacion = str(proof**3 - previous_proof**3).encode()
        return hashlib.sha256(operacion).hexdigest()

    def proof_of_work(self, previous_proof):
        """Prueba de trabajo: busca por fuerza bruta un número cuyo hash
        empiece con PREFIJO_DIFICULTAD.

        Encontrarlo cuesta muchos intentos, pero comprobarlo cuesta uno solo.
        """
        new_proof = 1
        while not self.hash_proof(new_proof, previous_proof).startswith(PREFIJO_DIFICULTAD):
            new_proof += 1
        return new_proof

    def hash(self, block):
        """Devuelve el hash SHA-256 de un bloque completo.

        sort_keys=True ordena las llaves para que el mismo bloque produzca
        siempre el mismo hash.
        """
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        """Revisa la cadena bloque por bloque. Es válida solo si:

        1. Cada bloque guarda el hash correcto del bloque anterior.
        2. Cada prueba de trabajo cumple la dificultad.
        """
        previous_block = chain[0]
        for block in chain[1:]:
            # 1. Si alguien modificó el bloque anterior, su hash ya no coincide.
            if block['previous_hash'] != self.hash(previous_block):
                return False
            # 2. La prueba debe cumplir la regla de los ceros iniciales.
            hash_operation = self.hash_proof(block['proof'], previous_block['proof'])
            if not hash_operation.startswith(PREFIJO_DIFICULTAD):
                return False
            previous_block = block
        return True


# ── App Flask ──────────────────────────────────────────
app = Flask(__name__)
blockchain = Blockchain()


@app.route('/', methods=['GET'])
def index():
    """Página de inicio: lista los endpoints disponibles."""
    response = {
        'message': 'Blockchain básica en Python',
        'endpoints': {
            '/mine_block': 'Mina un bloque nuevo y lo agrega a la cadena',
            '/get_chain': 'Devuelve la cadena completa y su longitud',
            '/is_valid': 'Verifica la integridad de la cadena',
        },
    }
    return jsonify(response), 200


@app.route('/mine_block', methods=['GET'])
def mine_block():
    """Mina un bloque: resuelve la prueba de trabajo y lo encadena al anterior."""
    previous_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(previous_block['proof'])
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Bloque minado',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    """Devuelve todos los bloques y cuántos hay."""
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    """Indica si la cadena conserva su integridad."""
    if blockchain.is_chain_valid(blockchain.chain):
        response = {'message': 'Blockchain válida ✓'}
    else:
        response = {'message': 'Blockchain inválida ✗'}
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
