import numpy as np

def convert_pgm_to_ppm_rgb(input_file, output_file):
    # Lecture du fichier PGM
    with open(input_file, 'rb') as f:
        header = f.readline()  # Lit la ligne d'en-tête P5
        dimensions = f.readline()  # Lit la ligne des dimensions
        maxval = f.readline()  # Lit la ligne de la valeur maximale

        width, height = [int(i) for i in dimensions.split()]
        img_data = np.fromfile(f, dtype=np.uint8).reshape((height, width))

    # Conversion en RGB
    rgb_image = np.stack([img_data]*3, axis=-1)  # Duplique les données en niveaux de gris pour les canaux R, G, B

    # Sauvegarde en format PPM
    with open(output_file, 'wb') as f:
        f.write(b'P6\n')
        f.write(f'{width} {height}\n'.encode())
        f.write(b'255\n')
        rgb_image.tofile(f)

# Exemple d'utilisation
convert_pgm_to_ppm_rgb('pgm_images/0.pgm', 'output.ppm')
