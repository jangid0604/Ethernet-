from flask import Flask, request, jsonify, render_template
import socket

app = Flask(__name__)

# Function to send data through Ethernet
def send_data(data):
    # Example IP and port
    host = '192.168.1.100'
    port = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        sock.sendall(data.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')
    finally:
        sock.close()
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.json.get('data')
    if data:
        response = send_data(data)
        return jsonify({'response': response})
    return jsonify({'error': 'No data received'}), 400

if __name__ == '__main__':
    app.run(debug=True)
