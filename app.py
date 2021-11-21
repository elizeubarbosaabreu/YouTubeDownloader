import PySimpleGUI as sg
from pytube import YouTube
import os

#         __   __         _____      _          
#         \ \ / /__  _   |_   _|   _| |__   ___ 
#          \ V / _ \| | | || || | | | '_ \ / _ \
#           | | (_) | |_| || || |_| | |_) |  __/
#           |_|\___/ \__,_||_| \__,_|_.__/ \___|
#                                               
#          ____                      _                 _           
#         |  _ \  _____      ___ __ | | ___   __ _  __| | ___ _ __ 
#         | | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
#         | |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
#         |____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
#                                                                  
# Desenvolvido por Elizeu Barbosa Abreu

img = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAA5klEQVRYhe2WzRHCIBCFH5mUkSKcoQNbsADvFuQ9BaQFO2DGIuxjvYiD/AkskNHh3ZLN7Pt4gWyAoaGhnSUiNerhNwPAWT0IAFa5OA8Q8TmECK9zMi80SA9prylU6GH+BrCjbwlh93YSSNUmJTYpWeYfAKtchG8TtgDxAnCVA2EuthqAhshNwwEofRU2SEh276oJlKgJwEkp731fsnMP45iqJVBiDlRIoNRY6+s4rjwNHb//PAU/BbD7L1nuJzcVKrlv9jG83A7R+vV4z+pXMnTIB2IYZ/XkTD3SEC9z1gQthgBzsz4BSn5JX8AHHEQAAAAASUVORK5CYII='

sg.theme('DarkRed2')

layout = [
    [sg.Stretch(), sg.Image(img), sg.Text('Youtube Downloader'), sg.Stretch()],
    [sg.Stretch(), sg.Text('URL do YouTube', size=(20,1)),
     sg.Input('', key='-url-', size=(60,1)),sg.Stretch()],
    [sg.Stretch(), sg.Text('Pasta/Diretório', size=(20,1)),
     sg.Input('', key='-folder-'), sg.FolderBrowse('Pasta/Dir...'), sg.Stretch()],
    [sg.Stretch(), sg.Button('Info do Vídeo', size=(20,2)),
     sg.Button('Fazer Download', size=(20,2)), sg.Stretch()],
    [sg.Multiline('', key='-saida-', size=(1024, 25))]
    ]

window = sg.Window('Youtube Downloader', layout, size=(600, 250), resizable=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    if event == 'Info do Vídeo':
        link = values['-url-']
        try:
            yt = YouTube(link) 
            window['-saida-'].update(f'''
    Título: {yt.title}
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    Views: {yt.views}
    Duração: {(yt.length/60):.2f} min
    Avaliação: {(yt.rating):.1f}
    ''')
            
        except:
            window['-saida-'].update(f'''
    ERRO DE DOWNLOAD...
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    Informações sobre op vídeo indisponíveis...
    Alguma coisa está errada...
    Verifique o link ou a conexão com a internet...
    ''')
    
    if event == 'Fazer Download':
        
        sg.popup_timed('Atenção!', 'Preparando para iniciar o Download...')
        
        try:
            yt = YouTube(link)
            link = values['-url-']
            path = values['-folder-']
            img = str(yt.thumbnail_url)
            
            ys = yt.streams.get_highest_resolution()            
            ys.download(path)
            try:
                os.system(f'wget {img}')
            except:
                sg.popup_timed('Erro!', 'Foi impossível baixar a imagem ou você não possui o wget instalado em sua máquina!')
                              
            window['-saida-'].update(f'Vídeo {yt.title} e imagem de capa, salvos com sucesso no Diretório {path}')
            
        except:
            window['-saida-'].update(f'''
    ERRO DE DOWNLOAD...
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    Informações sobre op vídeo indisponíveis...
    Alguma coisa está errada...
    Verifique o link ou a conexão com a internet...
    ''')           
    
window.close()