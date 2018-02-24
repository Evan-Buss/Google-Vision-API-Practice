# import io
from PIL import Image, ImageDraw, ImageFont
from google.cloud import vision
from google.cloud.vision import types

input = 'emotions.jpeg'
output = 'highlighted2_' + input


def detect_face(face_file, max_results=4):
    client = vision.ImageAnnotatorClient()
    content = face_file.read()
    image = types.Image(content=content)

    return client.face_detection(image=image).face_annotations


def highlight_faces(image, faces, output_filename):
    im = Image.open(image)
    font = ImageFont.truetype('Hack-Regular.ttf', 28)

    draw = ImageDraw.Draw(im)

    calculate_mood(draw, font, faces)

    im.save(output_filename)


def calculate_mood(draw, font, faces):
    """ Draws each person's mood under their face. """

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.fd_bounding_poly.vertices]

        draw.line(box + [box[0]], width=5, fill='#00ff00')

        emotions = {'Joyous': face.joy_likelihood,
                    'Angery': face.anger_likelihood,
                    'Surprised': face.surprise_likelihood,
                    'Sorrowful': face.sorrow_likelihood}
        emotion = max(emotions, key=emotions.get)

        draw.text(box[3], (emotion + " " + str(emotions.get(emotion))),
                  fill='#F2F2F2', font=font)
        new_pos = (box[3][0], box[3][1]+30)
        print(new_pos)
        draw.text(new_pos, likelihood_name[emotions.get(
            emotion)], fill='#F2F2F2', font=font)


def main(input_filename, output_filename, max_results):
    with open(input_filename, 'rb') as image:

        faces = detect_face(image, max_results)
        print('Found {} face{}'.format(
            len(faces), '' if len(faces) == 1 else 's'))

        print('Writing to file {}'.format(output_filename))

        image.seek(0)
        highlight_faces(image, faces, output_filename)


if __name__ == "__main__":
    main(input, output, 0)
