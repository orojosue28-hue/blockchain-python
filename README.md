# Blockchain básica en Python

Blockchain construida desde cero en Python, con prueba de trabajo (Proof of Work), encadenamiento de bloques con SHA-256 y una API REST en Flask para minar bloques, consultar la cadena y validar su integridad.

Proyecto educativo: la cadena vive en memoria y corre en un solo nodo. No incluye transacciones ni red entre nodos.

## Qué demuestra

- **Prueba de trabajo:** para minar un bloque hay que encontrar un número cuyo hash SHA-256 empiece con `0000`. Encontrarlo requiere miles de intentos; comprobarlo requiere uno.
- **Encadenamiento:** cada bloque guarda el hash del bloque anterior. Si alguien modifica un bloque, ese hash deja de coincidir y la cadena se rompe.
- **Validación:** un endpoint recorre toda la cadena y confirma que los hashes y las pruebas de trabajo son correctos.

## Tecnologías

- Python 3
- Flask (API REST)
- `hashlib` (SHA-256) y `json` de la biblioteca estándar

## Cómo ejecutarlo

```bash
git clone https://github.com/orojosue28-hue/blockchain-python.git
cd blockchain-python
pip install -r requirements.txt
python blockchain.py
```

El servidor queda en `http://127.0.0.1:5001`.

## Endpoints

| Método | Ruta          | Qué hace                                        |
|--------|---------------|-------------------------------------------------|
| GET    | `/`           | Lista los endpoints disponibles                 |
| GET    | `/mine_block` | Mina un bloque nuevo y lo agrega a la cadena    |
| GET    | `/get_chain`  | Devuelve la cadena completa y su longitud       |
| GET    | `/is_valid`   | Verifica la integridad de la cadena             |

## Ejemplo

```bash
curl http://127.0.0.1:5001/mine_block
```

```json
{
  "index": 2,
  "message": "Bloque minado",
  "previous_hash": "…hash del bloque génesis…",
  "proof": 1427,
  "timestamp": "2026-11-13 13:40:00.000000"
}
```

## Estructura de un bloque

| Campo           | Contenido                                   |
|-----------------|---------------------------------------------|
| `index`         | Posición del bloque en la cadena            |
| `timestamp`     | Fecha y hora en que se creó                 |
| `proof`         | Número que resuelve la prueba de trabajo    |
| `previous_hash` | Hash SHA-256 del bloque anterior            |

## Limitaciones y siguientes pasos

- La cadena se guarda en memoria: se pierde al apagar el servidor.
- Los bloques no contienen transacciones.
- Funciona en un solo nodo, sin consenso entre varios.

## Autor

Josué García Orozco — estudiante de Inteligencia Financiera y de Negocios, Universidad de Guadalajara.
