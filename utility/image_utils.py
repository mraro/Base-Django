import os

from PIL import Image   # https://www.youtube.com/watch?v=jGh-Ffz3FHQ pillow


def resize_img(image, width_desire, height_desire):
    """ IMAGE DJANGO, WIDTH DESIRE, OPTIONAL=HEIGHT_DESIRE """
    try:
        # retornar o path total com o nome do arquivo:  # noqa
        full_path_img = os.path.join(image)
        # abrir a imagem # noqa
        img_pillow = Image.open(full_path_img)
        # desempacotar o tamanho original # noqa
        original_width, original_height = img_pillow.size
        # uma regrinha de 3 para manter a proporção: # noqa
        auto_height = round((width_desire * original_height) / original_width)
        # se quiser pré definir uma autura: # noqa
        if not height_desire:
            final_height = auto_height
        else:
            final_height = height_desire

        output_img = img_pillow.resize((width_desire, final_height), Image.LANCZOS)
        output_img.save(full_path_img,
                        otimize=True,
                        quality=70,
                        )
        print("resoluções: ", width_desire, final_height)
    except FileNotFoundError as e:
        print(e)


def delete_cover_file(instance):
    """ this is a function to delete an image """
    if instance.cover != "static/images/default.jpg":
        try:
            print(f'apagado: {instance.cover.path}')  # LOG
            os.remove(instance.cover.path)
        except (ValueError, FileNotFoundError) as e:  # LOG
            print(f'Erro ao apagar: {e}')

