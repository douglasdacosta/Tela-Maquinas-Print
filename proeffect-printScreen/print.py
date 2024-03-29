import pyautogui
import datetime

def main():
    hora_atual = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    minha_imagem = pyautogui.screenshot()
    minha_imagem.save('imagens/print_'+hora_atual+'.png')

if __name__ == "__main__":
    main()
