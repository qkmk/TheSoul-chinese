import http.server
import socketserver
import threading
import webbrowser
import sys
import os

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # 只有收到POST请求到/__shutdown__时才会关闭服务器
        if self.path == '/__shutdown__':
            def shutdown_server():
                print("收到关闭请求，服务器即将关闭。")
                threading.Thread(target=httpd.shutdown).start()
            self.send_response(200)
            self.end_headers()
            shutdown_server()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        # 刷新页面时浏览器只会发送GET请求，不会触发关闭逻辑
        return super().do_GET()

def open_browser():
    url = f'http://localhost:{PORT}/index.html'
    webbrowser.open(url)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    handler = CustomHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    threading.Timer(1.0, open_browser).start()
    print(f"服务器已启动: http://localhost:{PORT}/index.html")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("服务器已关闭。")