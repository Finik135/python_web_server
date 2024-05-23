import http.server
import socketserver
import urllib.parse

PORT = 8000

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/greet':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            name = post_data.get('name', [''])[0]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            response = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Greet</title>
            </head>
            <body>
                <h1>Привітики, {name}!</h1>
                <a href="/">Назад</a>
            </body>
            </html>
            '''
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_error(404, "File not found")

Handler = SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
