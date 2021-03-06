import pika
import requests
from flask import Flask, request, abort

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>REST API </p>"

@app.route("/task", methods=['POST'])
def requestTask():
    if request.method =='POST':
        data = request.get_json()
        res = requests.post("https://reqres.in/api/register", json=data)
        print(data['task'])
        if res.json().get('token',0) == 0:
            abort(401)
        else:
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='RegisterQueue')
            channel.basic_publish(exchange='',
                                routing_key='hello',
                                body=data['task'])
            print('[x] Sent',data['task'])
            connection.close()
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
