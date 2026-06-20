# webcam_yolo.py
import cv2
from ultralytics import YOLO

model = YOLO("runs/classify/train-2/weights/best.pt")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: could not open webcam")
    exit()

print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)   # mirror the feed

    results = model.predict(frame, verbose=False)
    result  = results[0]

    top1_idx  = result.probs.top1
    top1_conf = result.probs.top1conf.item()
    label     = result.names[top1_idx]

    text = f"{label}: {top1_conf*100:.1f}%"
    cv2.putText(
        frame, text, (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
    )

    cv2.imshow("YOLOv8 CBDSL Live Inference", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()