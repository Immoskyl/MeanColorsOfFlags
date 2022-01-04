import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def getImage(path):
    response = requests.get(path)
    return Image.open(BytesIO(response.content))


def saveMeanColor(img, name):
    f, ax = plt.subplots()
    color_means = [0, 0, 0]

    print("IMG", img.getdata())
    pixel_list = list(img.getdata())
    #print("pixel list:", pixel_list)

    for r, g, b in chunker(pixel_list, 3):
        color_means[0] += r
        color_means[1] += g
        color_means[2] += b

    color_means[0] /= len(pixel_list)/3 * 255
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
    #saveMeanColor(getImage("https://www.google.com/url?sa=i&url=https%3A%2F%2Ffr.geneawiki.com%2Findex.php%3Ftitle%3DFichier%3ADrapeau_Norvege.png&psig=AOvVaw1gdi9W_srDup4JO0Dbyzm1&ust=1641341277646000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCKiE2e_mlvUCFQAAAAAdAAAAABAD"), "drapeau norvégien")
    get_all_flags()

