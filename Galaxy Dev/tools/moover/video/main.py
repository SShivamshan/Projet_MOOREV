import argparse
import sys
import csv
import cv2
from ultralytics import YOLO
from torch import load, save
import numpy as np 

def main(task, video_path, weights_path, conf, output_video_path, output_csv_path):
    model = YOLO(weights_path)
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    if task == "track":
    # Open CSV file for writing
        with open(output_csv_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Frame', 'Class', 'id', 'X1', 'Y1', 'X2', 'Y2', 'Confidence'])

            frame_count = 0

            while cap.isOpened():
                success, frame = cap.read()

                if success:
                        frame_count += 1
                        results = model.track(frame, conf=conf)
                        annotated_frame = results[0].plot()
                        out.write(annotated_frame)

                        for r in results[0] :
                            x1, y1, x2, y2, id_, cnf, class_id = r.boxes.data.tolist()[0]
                            print([frame_count, model.names[class_id], id_, x1, y1, x2, y2, cnf])
                            csv_writer.writerow([frame_count, model.names[class_id], int(id_), x1, y1, x2, y2, cnf])
                else:
                    break
                        
                            
    elif task == "segment":
        frame_count = 0

        while cap.isOpened():

            success, frame = cap.read()
            if success:

                results = model(frame, conf=conf)
                annotated_frame = results[0].plot()
                out.write(annotated_frame)

                for r in results[0] :
                    binary_mask = r.masks.data.numpy()
                    binary_mask = cv2.resize(binary_mask, (width, height))

                    # X = np.reshape(binary_mask, [1,:,:])

            else:
                break

    else:
        frame_count = 0

        while cap.isOpened():
                
            success, frame = cap.read()
            if success:
                results = model(frame, agnostic_nms=True, conf=conf)[0]

                for result in results:
                    for r in result.boxes.data.tolist():
                        x1, y1, x2, y2, score, class_id = r
                        x1 = int(x1)
                        x2 = int(x2)
                        y1 = int(y1)
                        y2 = int(y2)
                        class_id = int(class_id)
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 3)
                        cv2.putText(frame, f"cls: {model.names[class_id]}", (int(x1), int(y1) - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                annotated_frame = frame
                out.write(annotated_frame)


                # Write the annotated frame to the output video
                out.write(annotated_frame)
            else:
                break
            

        cap.release()
        out.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('task', type=str, default="track", help='task')
    parser.add_argument('input_file', type=argparse.FileType('r'), default=sys.stdin, help='input file')
    parser.add_argument('model_path', type=argparse.FileType('r'), default=sys.stdin, help='model_path') 
    parser.add_argument('conf', type=float, default=0.5, help='confidence')
    parser.add_argument('dir', type=str)

    args = parser.parse_args()


    wights_path = args.dir + "/be45st.pt" if args.model_path == sys.stdin else args.model_path.name

    save(load(wights_path), "model.pt")

    main(args.task, args.input_file.name, "model.pt", args.conf/100, "output_video.mp4", "output.csv")
