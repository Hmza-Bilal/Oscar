from flask import Flask, request
from multiprocessing import Process, Manager
import psutil
import time

app = Flask(__name__)
manager = Manager()
primes = manager.list()
is_generating = False


def generate_primes(from_num, to_num):
    global primes
    global is_generating
    is_generating = True
    for num in range(from_num, to_num + 1):
        if is_prime(num):
            primes.append(num)
    is_generating = False


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


@app.route('/generate', methods=['GET'])
def generate():
    global is_generating
    if is_generating:
        return 'Generation in progress', 400

    from_num = request.args.get('from', type=int)
    to_num = request.args.get('to', type=int)

    if not from_num or not to_num:
        return 'Invalid input', 400

    primes[:] = []
    process = Process(target=generate_primes, args=(from_num, to_num))
    process.start()
    return 'Generation started', 200


@app.route('/monitor', methods=['GET'])
def monitor():
    k = request.args.get('k', type=int)
    if not k:
        return 'Invalid input', 400

    cpu_percent = psutil.cpu_percent(interval=k * 60)
    mem_percent = psutil.virtual_memory().percent
    return f'CPU: {cpu_percent}% | Memory: {mem_percent}%', 200



@app.route('/get', methods=['GET'])
def get():
    global primes
    return str(primes), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
