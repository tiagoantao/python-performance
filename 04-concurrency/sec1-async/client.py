import marshal
import pickle
import socket
from time import sleep


def my_funs():
    def mapper(v):
        return 1

    def reducer(v, obs):
        return sum(obs)
    return mapper, reducer



def do_request(my_funs, data):
    conn = socket.create_connection(('127.0.0.1', 1936))
    conn.send(b'\x00')
    my_code = marshal.dumps(my_funs.__code__)
    conn.send(len(my_code).to_bytes(4, 'little', signed=True))
    conn.send(my_code)
    my_data = pickle.dumps(data)
    conn.send(len(my_data).to_bytes(4, 'little', signed=True))
    conn.send(my_data)
    job_id = int.from_bytes(conn.recv(4), 'little', signed=True)
    conn.close()

    print(f'Getting data from job_id {job_id}')
    result = None
    while result is None:
        conn = socket.create_connection(('127.0.0.1', 1936))
        conn.send(b'\x01')
        conn.send(job_id.to_bytes(4, 'little'))
        result = pickle.loads(conn.recv(4096))  # assume the answer is smaller than 4096
        conn.close()
        sleep(1)
    print(f'Result is {result}')

if __name__ == '__main__':
    do_request(my_funs, 'Python rocks. Python is great')
