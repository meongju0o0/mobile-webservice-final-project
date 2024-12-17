import warnings
import cv2
import requests
import torch
import time
import io
import numpy as np

warnings.filterwarnings("ignore", category=FutureWarning)

# 사용자 입력 받기
professor_id = input("교수 ID를 입력하세요: ")
lecture_name = input("강의명을 입력하세요: ")
classroom_number = input("강의실 호수를 입력하세요: ")

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

PERSON_CLASS_ID = 0
django_server_url = "https://meongju0o0.pythonanywhere.com/api/update_people_count/"
prev_people_count = -1

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

interval_seconds = 5
last_detection_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다. 종료합니다.")
        break

    cv2.imshow("Webcam Feed", frame)

    current_time = time.time()
    if current_time - last_detection_time >= interval_seconds:
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(img_rgb, size=640)

        people_count = 0
        for det in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = det
            if int(cls) == PERSON_CLASS_ID:
                people_count += 1
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                label = f"Person {conf:.2f}"
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if people_count != prev_people_count:
            _, buffer = cv2.imencode('.jpg', frame)
            file_bytes = io.BytesIO(buffer)

            data = {
                'people_count': people_count,
                'professor_id': professor_id,
                'lecture_name': lecture_name,
                'classroom_number': classroom_number
            }
            files = {'image': ('frame_with_boxes.jpg', file_bytes, 'image/jpeg')}

            try:
                response = requests.post(
                    django_server_url, 
                    data=data, 
                    files=files,
                    verify=False
                )
                if response.status_code == 201:
                    print("사람 수 업데이트 성공:", response.json())
                else:
                    print("사람 수 업데이트 실패:", response.status_code, response.text)
            except Exception as e:
                print("요청 중 오류 발생:", e)

            prev_people_count = people_count

        last_detection_time = current_time

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()