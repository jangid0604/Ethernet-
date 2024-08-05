from flask import Flask, request, jsonify, render_template
import socket

app = Flask(__name__)

# Function to send data through Ethernet
def send_file(file_data):
    host = '192.168.1.100'  # Change this to your target IP
    port = 12345            # Change this to your target port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        sock.sendall(file_data)
        response = sock.recv(1024).decode('utf-8')
    except Exception as e:
        response = str(e)
    finally:
        sock.close()
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    file_data = file.read()
    response = send_file(file_data)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
