#!/usr/bin/python3

import os
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

def getImage(path) :
    response = requests.get(path)
    print(path)
    try:
        img = Image.open(BytesIO(response.content)).convert('RGB')
    except:
        raise IOError
    return img


def saveMeanColor(img, name):
    f, ax = plt.subplots()
    color_means = [0, 0, 0]

    pixel_list = list(img.getdata())
    #print("pixel list:", pixel_list)
    #print("w:", img.width, "h:", img.height)
    #print("pixel nb", img.width * img.height, "pixel list len", len(pixel_list))

    for i in pixel_list:
        color_means[0] += i[0]
        color_means[1] += i[1]
        color_means[2] += i[2]

    color_means[0] /= len(pixel_list) * 255
    color_means[1] /= len(pixel_list) * 255
    color_means[2] /= len(pixel_list) * 255
    print("color_means: ", color_means)

    to_file_str = "{name}: {mean}\n".format(name=name, mean=color_means)

    plt.fill_between([0, 1], [1], [0], color=tuple(color_means))

    #plt.show()
    plt.axis('off')
    plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off', labeltop='off',
                    labelright='off', labelbottom='off')
    if not os.path.exists("flag_means"):
        os.mkdir("flag_means")
    f.savefig("flag_means/"+name, dpi=100, bbox_inches='tight', pad_inches=-0.5)
    plt.close()
    return to_file_str


def get_all_flags():
    to_file_str = "Mean color of all country flags (R, G, B)\n"
    for line in open("country_flags", 'r').readlines():
        line = line.lower().strip("\n")
        url = "https://flagcdn.com/w20/{isocode}.png".format(isocode=line)
        try:
            img = getImage(url)
        except IOError:
            print("{name} not found".format(name=line))
            continue
        to_file_str += saveMeanColor(img, line)
    f = open("flag_means.txt", "w")
    f.write(to_file_str)
    f.close()


if __name__ == '__main__':
    get_all_flags()

