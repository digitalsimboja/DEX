import http.server
import socketserver

def main():
    print("Starting server...")
    with socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler) as httpd:
        print("Server running at http://localhost:8000")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
