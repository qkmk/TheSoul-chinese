import http.server
import socketserver
import threading
import webbrowser
import os
import sys
import time

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/shutdown':
            self.send_response(200)
            self.end_headers()
            threading.Thread(target=os._exit, args=(0,)).start()
        else:
            self.send_error(404)

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

def main():
    # 启动服务器线程
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # 打开浏览器
    url = f"http://localhost:{PORT}/index.html"
    webbrowser.open(url)

    try:
        print("按 Ctrl+C 退出，或关闭浏览器标签页后自动退出。")
        while True:
            time.sleep(1)
            # 检查是否还有浏览器窗口打开
            # 这里简单处理：按 Ctrl+C 退出
            # 进阶：通过监听服务器线程是否存活来判断是否收到 JS 的 /shutdown 通知
            if not server_thread.is_alive():
                print("检测到浏览器已关闭，服务器已退出。")
                break
    except KeyboardInterrupt:
        print("正在关闭服务器...")

if __name__ == "__main__":
    main()
