import cv2
import subprocess
from tkinter import messagebox

face_cascade_path = 'haarcascades/haarcascade_frontalface_default.xml'
eye_cascade_path = 'haarcascades/haarcascade_eye.xml'
smile_cascade_path = 'haarcascades/haarcascade_smile.xml'

face_cascade = cv2.CascadeClassifier(face_cascade_path)
eye_cascade = cv2.CascadeClassifier(smile_cascade_path)

cap = cv2.VideoCapture(0)


def device_detection():
    process = subprocess.Popen('python label_image.py --graph retrained_graph.pb --labels retrained_labels.txt --input_layer Placeholder --output_layer final_result --image face.jpg', stdout=subprocess.PIPE, shell=True)
    messagebox.showinfo('結果', process.stdout.decode('utf-8'))

def main():
    while True:
        ret,frame = cap.read()
        frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(frame_gray, scaleFactor=1.11)
        for x, y, w, h in faces:
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # face = frame[y: y + h, x: x + w]
            face_gray = frame_gray[y: y + h, x: x + w]
            eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.8, minNeighbors=20)
            for (ex, ey, ew, eh) in eyes:
                # cv2.imwrite('eye' + str(cnt) + '.jpg', face[ey:ey + eh, ex:ex + ew])
                # cv2.rectangle(face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                # eye = face[ey: ey+eh,ex:ex+ew]
                cv2.imwrite('face.jpg', frame)
                device_detection()
                exit(0)
        cv2.imshow('detection', frame)
        k = cv2.waitKey(1)
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()