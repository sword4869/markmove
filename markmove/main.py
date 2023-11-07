import configargparse
import os
import re
import shutil
import cv2
import numpy as np


def main():

    parser = configargparse.ArgumentParser()
    parser.add_argument('--in_root', type=str, required=True, help='Input root')
    parser.add_argument('--in_article', type=str, required=True, help='Input article, relativate path')
    parser.add_argument('--out_root', type=str, required=True, help='Output root')
    parser.add_argument('--out_article', type=str, required=True, help='Output article, relativate path')
    parser.add_argument('--out_imgsdir', type=str, default='images', help='Output imgs directory')
    parser.add_argument('--delete', action='store_true', help='Delete input imgs')
    args = parser.parse_args()

    print(args)

    in_article_file = os.path.join(args.in_root, args.in_article)
    out_article_file = os.path.join(args.out_root, args.out_article)
    print('in_article_file:', in_article_file)
    print('out_article_file:', out_article_file)

    os.makedirs(os.path.abspath(os.path.join(args.out_root, args.out_imgsdir)), exist_ok=True)
    os.makedirs(os.path.abspath(os.path.join(args.out_root, args.out_article, '..')), exist_ok=True)

    new_img_content_prefix = '../' * len(args.out_article.split(os.sep)[:-1]) + args.out_imgsdir + '/'
    print('new_img_content_prefix:', new_img_content_prefix)

    print('-' * 80)

    new_lines = []
    with open(in_article_file, 'r', encoding='utf-8') as f:
        for line_id, line in enumerate(f):
            line_id += 1    # start from 1
            regex = '!\[.*\]\(.*\)'
            img_contents = re.findall(regex, line)
            new_img_contents = []

            # 如果一行有多个图片，先复制图片，再设定新的图片路径
            for img_content in img_contents:
                # 括号内部和去掉括号
                img_content = re.findall('\(.*\)', img_content)[0]
                img_content = img_content[1:-1]
                # http/https的图片不复制
                if img_content[0] == 'h':
                    print(line_id, 'http/https', img_content)
                # `![](/image/b0.png)`的格式需要特殊处理
                if img_content[0] == '/':
                    img = os.path.abspath(os.path.join(args.in_root, img_content[1:]))
                else:
                    img = os.path.abspath(os.path.join(in_article_file, '..', img_content))
                assert os.path.exists(img), 'not exists: ' + img

                basename = os.path.basename(img)
                new_img = os.path.join(args.out_root, args.out_imgsdir, basename)
                if os.path.exists(new_img):
                    print(line_id, 'exists: ' + new_img)
                    show_img = cv2.imread(img)
                    show_new_img = cv2.imread(new_img)
                    paste_img = np.zeros((max(show_img.shape[0], show_new_img.shape[0]), show_img.shape[1] + show_new_img.shape[1], show_img.shape[2]), dtype=np.uint8)
                    paste_img[:show_img.shape[0], :show_img.shape[1], :] = show_img
                    paste_img[:show_new_img.shape[0], show_img.shape[1]:, :] = show_new_img
                    cv2.imshow('same? [y/n]', paste_img)
                    if cv2.waitKey(0) == ord('y'):
                        print('skip')
                    elif cv2.waitKey(0) == ord('n'):
                        basename = os.path.basename(img).split('.')[0] + '_new.' + os.path.basename(img).split('.')[1]
                        new_img = os.path.join(args.out_root, args.out_imgsdir, basename)
                        print('new name', new_img)
                        shutil.copy(img, new_img)
                    else:
                        print('exit')
                        exit()
                else:
                    shutil.copy(img, new_img)
                if args.delete:
                    os.remove(img)

                new_img_content = f'![]({new_img_content_prefix + basename})'
                new_img_contents.append(new_img_content)

            new_line = ''
            if len(new_img_contents) > 0:
                others = re.split(regex, line)
                for id, other in enumerate(others):
                    if id > 0:
                        new_line += new_img_contents[id - 1]
                    new_line += other

            else:
                new_line += line
            new_lines.append(new_line)

    with open(out_article_file, 'w', encoding='utf-8') as f:
        for line in new_lines:
            f.write(line)

if __name__ == '__main__':
    main()