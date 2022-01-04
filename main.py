import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def getImage(path):
    response = requests.get(path)
    return Image.open(BytesIO(response.content)).convert('RGB')


def saveMeanColor(img, name):
    f, ax = plt.subplots()
    color_means = [0, 0, 0]

    print("IMG", img.getdata())
    pixel_list = list(img.getdata())
    print("pixel list:", pixel_list)
    print("w:", img.width, "h:", img.height)
    print("pixel nb", img.width * img.height, "pixel list len", len(pixel_list))

    for i in pixel_list:
        color_means[0] += i[0]
        color_means[1] += i[1]
        color_means[2] += i[2]

    color_means[0] /= len(pixel_list) * 255
    color_means[1] /= len(pixel_list) * 255
    color_means[2] /= len(pixel_list) * 255
    print("color_means: ", color_means)

    plt.fill_between([0, 1], [1], [0], color=tuple(color_means))
    plt.show()
    f.savefig(name)


def get_all_flags():
    for line in open("country_flags", 'r').readlines():
        line = line.lower().strip("\n")
        url = "https://flagcdn.com/w20/{isocode}.png".format(isocode=line)
        img = getImage(url)
        saveMeanColor(img, line)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    saveMeanColor(getImage("https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Flag_of_Algeria.svg/langfr-225px-Flag_of_Algeria.svg.png"), "drapeau norvégien")
    #get_all_flags()

