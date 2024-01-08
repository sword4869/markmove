import PySimpleGUI as psg
from markmove import move

class MyGUI:
    def __init__(self):
        self.init_windows()

    def init_windows(self):
        layout = [
            [
                psg.Text("IN_ROOT:"),
                psg.Input(key='-IN_ROOT-'),
                psg.Button("IN_ROOT")
            ],
            [
                psg.Text("IN_ARTICLE:"),
                psg.Input(key='-IN_ARTICLE-'),
                psg.Button("IN_ARTICLE")
            ],
            [
                psg.Text("OUT_ROOT:"),
                psg.Input(key='-OUT_ROOT-'),
                psg.Button("OUT_ROOT")
            ],
            [
                psg.Text("OUT_ARTICLE_DIR:"),
                psg.Input(key='-OUT_ARTICLE_DIR-'),
                psg.Button("OUT_ARTICLE_DIR"),
                psg.Input(key='-OUT_ARTICLE_NAME-')
            ],
            [
                psg.Text("OUT_IMAGESDIR:"),
                psg.Input(key='-OUT_IMAGESDIR-'),
                psg.Button("OUT_IMAGESDIR")
            ],
            [
                psg.Text("REMOTE_IMG_SUFFIX:"),
                psg.Input('.png .jpg .jpeg .gif .bmp .webp', key='-REMOTE_IMG_SUFFIX-'),
                psg.Button("NONE", key='-REMOTE_IMG_SUFFIX_None-')
            ],
            [
                psg.Checkbox("download", key="-DOWNLOAD-"),
                psg.Checkbox("delete", key="-DELETE-"),
                psg.Checkbox("newline", key="-NEWLINE-"),
            ],
            [
                psg.Button("START")
            ]
        ]
        self.window = psg.Window(
            "markmove",
            layout,
            size=(800, 400),
            grab_anywhere=True,  # Window can be moved
            resizable=True,  # Resize
        )

def main():
    gui = MyGUI()
    while True:
        event, values = gui.window.read()

        if event in (None, "Exit"):
            break

        if event == 'IN_ROOT':
            in_root = psg.popup_get_folder('IN_ROOT')
            gui.window['-IN_ROOT-'].update(in_root)
        if event == 'IN_ARTICLE':
            in_article = psg.popup_get_file('IN_ARTICLE')
            if in_article is None:
                continue
            if not in_article.startswith(values['-IN_ROOT-']):
                psg.popup_error('IN_ARTICLE must be in IN_ROOT')
                continue
            in_article = in_article[len(values['-IN_ROOT-']) + 1:]
            gui.window['-IN_ARTICLE-'].update(in_article)
        if event == 'OUT_ROOT':
            gui.window['-OUT_ROOT-'].update(psg.popup_get_folder('OUT_ROOT'))
        if event == 'OUT_ARTICLE_DIR':
            OUT_ARTICLE_DIR = psg.popup_get_file('OUT_ARTICLE_DIR')
            if OUT_ARTICLE_DIR is None:
                continue
            if OUT_ARTICLE_DIR is None:
                continue
            if not OUT_ARTICLE_DIR.startswith(values['-OUT_ROOT-']):
                psg.popup_error('OUT_ARTICLE_DIR must be in OUT_ROOT')
                continue
            OUT_ARTICLE_DIR = OUT_ARTICLE_DIR[len(values['-OUT_ROOT-']) + 1:]
            gui.window['-OUT_ARTICLE_DIR-'].update(OUT_ARTICLE_DIR)
        if event == 'OUT_IMAGESDIR':
            out_imgsdir = psg.popup_get_folder('OUT_IMAGESDIR')
            if out_imgsdir is None:
                continue
            if not out_imgsdir.startswith(values['-OUT_ROOT-']):
                psg.popup_error('OUT_IMAGESDIR must be in OUT_ROOT')
                continue
            out_imgsdir = out_imgsdir[len(values['-OUT_ROOT-']) + 1:]
            gui.window['-OUT_IMAGESDIR-'].update(out_imgsdir)
        if event == '-REMOTE_IMG_SUFFIX_None-':
            gui.window['-REMOTE_IMG_SUFFIX-'].update('None')
        if event == 'START':
            if values['-IN_ROOT-'] == 'None':
                psg.popup_error('IN_ROOT is None')
                continue
            if values['-IN_ARTICLE-'] == 'None':
                psg.popup_error('IN_ARTICLE is None')
                continue
            if values['-OUT_ROOT-'] == 'None':
                psg.popup_error('OUT_ROOT is None')
                continue
            
            if values['-REMOTE_IMG_SUFFIX-'] == 'None':
                remote_img_suffix = 'None'
            else:
                remote_img_suffix = ''
                remote_img_suffix = ' '.join(values['-REMOTE_IMG_SUFFIX-'].split(' '))
            OUT_ARTICLE = values['-OUT_ARTICLE_DIR-'] + '/' + values['-OUT_ARTICLE_NAME-']
            cmd = f'--in_root {values["-IN_ROOT-"]} --in_article {values["-IN_ARTICLE-"]} --out_root {values["-OUT_ROOT-"]} --OUT_ARTICLE_DIR {OUT_ARTICLE} --out_imgsdir {values["-OUT_IMAGESDIR-"]} --remote_img_suffix {remote_img_suffix}'
            if values['-DOWNLOAD-']:
                cmd += ' --download'
            if values['-DELETE-']:
                cmd += ' --delete'
            if values['-NEWLINE-']:
                cmd += ' --newline'
            print(cmd)
            move.main(cmd.split(' '))
    gui.window.close()

if __name__ == "__main__":
    main()