from __future__ import unicode_literals
import PySimpleGUI as sg
import sys, youtube_dl, subprocess

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

formatos = ["mp4", "ogg", "m4a", "webm"]


def baixar(cmd, timeout=None, window=None):
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    output = ""
    for line in p.stdout:
        line = line.decode(
            errors="replace" if (sys.version_info) < (3, 5) else "backslashreplace"
        ).rstrip()
        output += line
        print(line)
        window.Refresh() if window else None  # yes, a 1-line if, so shoot me
    retval = p.wait(timeout)
    return (retval, output)


sg.theme("Reddit")


layout = [
    [
        sg.Stretch(),
        sg.Image(sg.EMOJI_BASE64_HAPPY_IDEA),
        sg.Text("YouTube-DL", font=("Arial", 24)),
        sg.Stretch(),
    ],
    [sg.Stretch(), sg.Text("URL do YouTube", size=(60, 1)), sg.Stretch()],
    [sg.Stretch(), sg.Input("", key="-url-", size=(60, 1)), sg.Stretch()],
    [sg.Stretch(), sg.Text("Escolha o formato de saída", size=(60, 1)), sg.Stretch()],
    [
        sg.Stretch(),
        sg.Combo(formatos, default_value="mp4", size=(60,), key="-formato-"),
        sg.Stretch(),
    ],
    [sg.Stretch(), sg.Button("Fazer Download", size=(50, 2)), sg.Stretch()],
    [sg.Stretch(), sg.Output(size=(60, 25)), sg.Stretch()],
]

window = sg.Window("Youtube Downloader", layout=layout, size=(400, 300), resizable=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break

    elif event in "Fazer Download":

        link = values["-url-"]
        formato = values["-formato-"]
        pasta = sg.popup_get_folder("Pasta/Dir...")

        sg.popup_timed(
            "Atenção!",
            "Preparando para iniciar o Download... \nFique atento: O YouTube pode bloquear alguns downloads...",
        )

        try:
            cmd = f"cd {pasta}; youtube-dl -f {formato} --write-thumbnail {link}"
            baixar(cmd)

        except Exception as e:
            sg.popup_error(f"""{e}""")

        window["-url-"].update("")


window.close()
