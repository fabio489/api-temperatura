from flask import Flask, jsonify
import requests

app = Flask(__name__)

# CONFIGURA TUS CREDENCIALES
TOKEN = "nYK3edoz8m2DrtuLfliNdvsZDpaw912x5lwevrjnEo6qKWMBoHaFbQBuTtEg0XdmQYth3xRl1YxbaJ29qZ4_Iw=="
ORG = "Cold Metrica"
URL_INFLUX = "https://us-east-1-1.aws.cloud2.influxdata.com"
BUCKET = "Sensores"

@app.route('/api/temperatura', methods=['GET'])
def obtener_datos():
    query = f'''
    from(bucket: "{BUCKET}")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "temperatura")
      |> sort(columns: ["_time"], desc: true)
      |> limit(n: 1)
    '''
    
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/vnd.flux",
        "Accept": "application/json"
    }

    response = requests.post(
        f"{URL_INFLUX}/api/v2/query?org={ORG}",
        headers=headers,
        data=query
    )

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

