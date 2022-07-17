import face_recognition




file = face_recognition.load_image_file('bill_gates1.jpg')

file_encoding = face_recognition.face_encodings(file)[0]


print(file_encoding)

