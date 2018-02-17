import io
from PIL import Image, ImageDraw, ImageFont
from google.cloud import vision
from google.cloud.vision import types

input = 'jake.jpg'
output = 'highlighted_' + input


def detect_face(face_file, max_results=4):
    client = vision.ImageAnnotatorClient()
    content = face_file.read()
    image = types.Image(content=content)

    return client.face_detection(image=image).face_annotations


def highlight_faces(image, faces, output_filename):
    im = Image.open(image)
    font = ImageFont.truetype('Hack-Regular.ttf', 28)

    draw = ImageDraw.Draw(im)

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')

    draw.text((30, 30), "Joy Levels", font=font)

    for face in faces:
        box = [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]
        
        draw.line(box + [box[0]], width=5, fill="#00ff00")
        draw.text(box[3] + (0,1000), likelihood_name[face.joy_likelihood],fill='#00ff00', font=font)

    im.save(output_filename)


def main(input_filename, output_filename, max_results):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image, max_results)
        print ('Found {} face{}'.format(
            len(faces), '' if len(faces) == 1 else 's'))

        print('Writing to file {}'.format(output_filename))

        image.seek(0)
        highlight_faces(image, faces, output_filename)


if __name__ == "__main__":
    main(input, output, 0)

#TODO: Calculate all moods and find the highest average

