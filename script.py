import ssl
import OpenSSL
import datetime
import socket

def check_ssl_expiry(url):
    try:
        hostname = url.strip()
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cert_expiry_date = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                days_left = (cert_expiry_date - datetime.datetime.now()).days
                return days_left
    except Exception as e:
        return None

def main():
    input_file = "arquivo.txt"  # Nome do arquivo contendo as URLs, uma em cada linha
    with open(input_file, "r") as file:
        urls = file.readlines()

    if not urls:
        print("O arquivo das URLs está vazio.\nLeia a documentação README.MD")
        return
    
    print("Verificando certificados SSL... Aguarde.")
    for url in urls:
        days_left = check_ssl_expiry(url)
        if days_left is not None:
            if days_left <= 0:
                print(f"- {url.strip()}: Certificado vencido.")
            else:
                print(f"- {url.strip()}: válido por mais {days_left} dias.\n")
        else:
            print(f"Não foi possível verificar o certificado SSL para a URL: {url.strip()}")

if __name__ == "__main__":
    main()

input("\nPressione Enter para sair...")
