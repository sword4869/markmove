import os
import PySimpleGUI as psg
from markmove import move
import configargparse

class MyGUI:
    def __init__(self, args):
        self.init_windows(args)

    def init_windows(self, args):
        layout = [
            [
                psg.Text("IN_ROOT:"),
                psg.Input(key='-IN_ROOT-', default_text=args.in_root),
                psg.Button("IN_ROOT")
            ],
            [
                psg.Text("IN_ARTICLE:"),
                psg.Input(key='-IN_ARTICLE-', default_text=args.in_article),
                psg.Button("IN_ARTICLE")
            ],
            [
                psg.Text("OUT_ROOT:"),
                psg.Input(key='-OUT_ROOT-', default_text=args.out_root),
                psg.Button("OUT_ROOT")
            ],
            [
                psg.Text("OUT_ARTICLE_DIR:"),
                psg.Input(key='-OUT_ARTICLE_DIR-', default_text=args.out_article_dir),
                psg.Button("OUT_ARTICLE_DIR")
            ],
            [
                psg.Text("OUT_ARTICLE_NAME:"),
                psg.Input(key='-OUT_ARTICLE_NAME-', default_text=args.out_article_name),
            ],
            [
                psg.Text("OUT_IMAGESDIR:"),
                psg.Input(key='-OUT_IMAGESDIR-', default_text=args.out_imgsdir),
                psg.Button("OUT_IMAGESDIR")
            ],
            [
                psg.Text("REMOTE_IMG_SUFFIX:"),
                psg.Input(key='-REMOTE_IMG_SUFFIX-', default_text=args.remote_img_suffix),
                psg.Button("NONE", key='-REMOTE_IMG_SUFFIX_None-')
            ],
            [
                psg.Checkbox("download", key="-DOWNLOAD-", default=args.download if args else False),
                psg.Checkbox("delete", key="-DELETE-", default=args.delete if args else False),
                psg.Checkbox("newline", key="-NEWLINE-", default=args.newline if args else False),
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

def parse_args(cmd_args=None):
    parser = configargparse.ArgumentParser()
    parser.add_argument('--in_root', default='', type=str,  help='Input root. ![](/image/b0.png) 所代表的image文件夹的路径')
    parser.add_argument('--in_article', default='', type=str,  help='Input article, relativate path')
    parser.add_argument('--out_root', default='', type=str,  help='Output root')
    
    parser.add_argument('--out_article_dir', default='', type=str)
    parser.add_argument('--out_article_name', default='', type=str)

    parser.add_argument('--out_imgsdir', type=str, default='images', help='Output imgs directory')
    parser.add_argument('--remote_img_suffix', nargs='+', default=['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'], help='Remote img_path suffix')
    parser.add_argument('--download', action='store_true', help='Download input imgs')
    parser.add_argument('--delete', action='store_true', help='Delete input imgs')
    parser.add_argument('--newline', action='store_true', help='Newline')
    return parser.parse_args(cmd_args)

def main():
    args = parse_args()
    gui = MyGUI(args)
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
            OUT_ARTICLE_DIR = psg.popup_get_folder('OUT_ARTICLE_DIR')
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
            print(values)
            print()
            if values['-IN_ROOT-'] == '':
                psg.popup_error('IN_ROOT is None')
                continue
            if values['-IN_ARTICLE-'] == '':
                psg.popup_error('IN_ARTICLE is None')
                continue
            if values['-OUT_ROOT-'] == '':
                psg.popup_error('OUT_ROOT is None')
                continue
            if values['-OUT_IMAGESDIR-'] == '':
                psg.popup_error('OUT_IMAGESDIR is None')
                continue
            if values['-OUT_ARTICLE_NAME-'] == '':
                psg.popup_error('OUT_ARTICLE_NAME is None')
                continue
            if values['-REMOTE_IMG_SUFFIX-'] == 'None':
                remote_img_suffix = 'None'
            else:
                remote_img_suffix = ''
                remote_img_suffix = ' '.join(values['-REMOTE_IMG_SUFFIX-'].split(' '))

            
            debug_info = f'--in_root {values["-IN_ROOT-"]} ' \
                f'--in_article {values["-IN_ARTICLE-"]} ' \
                f'--out_root {values["-OUT_ROOT-"]} ' \
                f'--out_article_dir {values["-OUT_ARTICLE_DIR-"]} ' \
                f'--out_article_name {values["-OUT_ARTICLE_NAME-"]} ' \
                f'--out_imgsdir {values["-OUT_IMAGESDIR-"]} ' \
                f'--remote_img_suffix {remote_img_suffix} '
            
            if values['-DOWNLOAD-']:
                debug_info.append('--download')
            if values['-DELETE-']:
                debug_info.append('--delete')
            if values['-NEWLINE-']:
                debug_info.append('--newline')

            print(debug_info)
            print()
            args = parse_args(debug_info.split(' '))
            print('args: ', args)
            print()
            move.main(args)
            psg.popup_ok('Done!')
    gui.window.close()

if __name__ == "__main__":
    main()