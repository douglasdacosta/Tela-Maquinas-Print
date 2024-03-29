import json
import subprocess
import configparser
import pyautogui
import datetime

def read_cnc_ini(file_path):
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                # Dividir a linha em duas partes no primeiro '=' encontrado
                parts = line.strip().split('=', 1)
                # Se houver duas partes após a divisão, assumir que é uma chave e um valor
                if len(parts) == 2:
                    key, value = parts
                    data[key.strip()] = value.strip()
                # Caso contrário, tratar como uma linha inválida
                else:
                    print(f"A linha '{line.strip()}' não possui um formato válido e será ignorada.")
    return data

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def log_error(message):
    with open('error.log', 'a') as file:
        file.write(message + '\n')

def main():
    
     # Ler o arquivo de configuração
    config = read_config('config.conf')
    
    # Obter o valor do endpoint da seção 'API'
    file_path = config['CONFIG']['file_path']

    json_data = read_cnc_ini(file_path)
    
    NUMERO_CNC = config['CONFIG']['NUMERO_CNC']
    TOKEN = config['API']['TOKEN']
    LOGIN = config['API']['LOGIN']
    SENHA = config['API']['SENHA']
    # Convertendo os dados para JSON
    json_string = json.dumps(json_data)

    json_data = json.loads(json_string)

    # Modifique o valor da chave "NUMERO_CNC"
    json_data["NUMERO_CNC"] = NUMERO_CNC
    json_data["TOKEN"] = TOKEN
    json_data["LOGIN"] = LOGIN
    json_data["SENHA"] = SENHA

    # Converta o objeto Python de volta para uma string JSON
    json_string = json.dumps(json_data)

    # Escrevendo o JSON em um arquivo temporário
    temp_file_path = "temp_data.json"
    
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(json_string)

    
    # Enviando o JSON para a API usando curl via subprocess
    #url = 'http://sistema.eplax.com.br/salvadadosmaquina'
    endpoint = config['API']['endpoint']
    
    curl_command = [
        'curl',
        '-X', 'POST',
        '-H', 'Content-Type: application/json',
        '-d', '@' + temp_file_path,
        endpoint
    ]
    
    try:
        # Executando o comando curl
        subprocess.run(curl_command, check=True)
        print("JSON enviado com sucesso para a API.")
        log_error("JSON enviado com sucesso para a API.")
    except subprocess.CalledProcessError as e:
        log_error(f"Erro ao enviar JSON para a API: {e}")
        print(f"Erro ao enviar JSON para a API: {e}")

if __name__ == "__main__":
    main()
