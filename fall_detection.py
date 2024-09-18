import cv2
import numpy as np
from StatusQueue import StatusQueue


def Status_judgement(status_queue):
    s0 = status_queue.get_by_index(0)
    s1 = status_queue.get_by_index(1)
    s2 = status_queue.get_by_index(2)
    s3 = status_queue.get_by_index(3)
    s4 = status_queue.get_by_index(4)
    s5 = status_queue.get_by_index(5)
    s6 = status_queue.get_by_index(6)
    s7 = status_queue.get_by_index(7)
    # print(s2, s3)
    if (s0.status == "standing") and (s1.status == "standing") and (s2.status != "lying") and (s3.status != "lying") and (s4.status != "lying") and (s5.status != "lying") and (s6.status == "lying" and s7.status == "lying"):
        print("Fall")
        return True
    else:
        return False
        

def Status_judgement2(status_queue):
    s0 = status_queue.get_by_index(0)
    s1 = status_queue.get_by_index(1)
    s2 = status_queue.get_by_index(2)
    s3 = status_queue.get_by_index(3)
    s4 = status_queue.get_by_index(4)
    s25 = status_queue.get_by_index(25)
    s26 = status_queue.get_by_index(26)
    s27 = status_queue.get_by_index(27)
    s28 = status_queue.get_by_index(28)
    s29 = status_queue.get_by_index(29)
    if (s0.status == "standing") and (s1.status == "standing") and (s2.status == "standing") and (s3.status == "standing") and (s4.status == "standing") and (s25.status == "lying") and (s26.status == "lying") and (s27.status == "lying") and (s28.status == "lying") and (s29.status == "lying"):
        print("Fall")
        return True
    else:
        return False


def Person_Status(status_queue, h, w):
    if h!= 0:
        hw_ratio = h/w
        height_min, height_max = 150, 180
        shoulder_min, shoulder_max = 33, 45
        stand_min, stand_max = height_min/ shoulder_max, height_max/ shoulder_min
        fall_min, fall_max = shoulder_min/ height_max, 1
        if 1.8 < hw_ratio <= 3:
            status_queue.enqueue(hw_ratio, 'standing')
            return status_queue
        elif 0.3 < hw_ratio <= 1:
            status_queue.enqueue(hw_ratio, 'lying')
            return status_queue
        elif 1 <= hw_ratio <=1.3:
            status_queue.enqueue(hw_ratio, 'siting')
            return status_queue
        else:
            status_queue.enqueue(hw_ratio, 'unknown')
            return status_queue
    else:
        status_queue.enqueue(0, 'unknown')
        return status_queue


def union_rectangles(rectangles):
    # 初始化并集矩形的边界，使用极大值和极小值方便计算
    if not rectangles:
        return None  # 如果列表为空，返回None

    # 从第一个矩形开始初始化
    union_x, union_y, w, h = rectangles[0]
    union_x2 = union_x + w
    union_y2 = union_y + h

    # 遍历剩余的矩形，扩展并集矩形的边界
    for (x, y, w, h) in rectangles[1:]:
        union_x = min(union_x, x)
        union_y = min(union_y, y)
        union_x2 = max(union_x2, x + w)
        union_y2 = max(union_y2, y + h)

    # 计算最终并集矩形的宽度和高度
    final_w = union_x2 - union_x
    final_h = union_y2 - union_y

    if final_w * final_h > 640 * 720:
        return None
    else:
        return (union_x, union_y, final_w, final_h)


def img_process(frame2, backSub, kernel):
    alpha = 2.0
    frame2 = cv2.convertScaleAbs(frame2, alpha=alpha)

    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    fgmask = backSub.apply(gray)
    
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel, iterations=2)
    

    #edges = cv2.Canny(fgmask, threshold1=30, threshold2=150)
    # edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)

    # if 30*5<frame_num<30*6:
    #     save_path = f"./img/{frame_num}.jpg"
    #     cv2.imwrite(save_path, frame2)
    return fgmask, frame2
        

def find_people(fgmask, frame2, sq):
    # find contours and filter 
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areas = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        img_max_w, img_max_h = 1280/2, 720/2
        if 30*30 < w*h < img_max_w * img_max_h:
            areas.append((x, y, w, h))
    
    area=union_rectangles(areas)

    
    # draw contours
    if area != None:
        # max_index, max_rectangle = max(enumerate(areas), key=lambda item: item[1][2] * item[1][3])
        # x,y,w,h = areas[max_index][0],areas[max_index][1],areas[max_index][2],areas[max_index][3]
        x, y , w, h = area
        sq = Person_Status(sq, h, w)
        if sq.is_full():
            fall = Status_judgement2(sq)
            
            text_x = x + 5  
            text_y = y - 5  
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.8
            line_type = 4

            current_status = sq.get_by_index(29)

            # print(current_status.status, current_status.hw_ratio)
            if current_status.status == "standing":
                color =  (0, 0, 255)
                cv2.rectangle(frame2, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame2, current_status.status, (text_x, text_y), font, font_scale, color, line_type)
            elif current_status.status == "lying":
                if fall:
                    color =  (0, 255, 0)
                    cv2.rectangle(frame2, (x, y), (x+w, y+h), color, 10)
                    cv2.putText(frame2, "fall", (text_x, text_y), font, font_scale, color, line_type)
                else:
                    color =  (255, 0, 0)
                    cv2.rectangle(frame2, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame2, "lying", (text_x, text_y), font, font_scale, color, line_type)
            elif current_status.status == "siting":
                color =  (0, 0, 0)
                cv2.rectangle(frame2, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame2, current_status.status, (text_x, text_y), font, font_scale, color, line_type)
            else:
                pass
        else:
            pass

    else:
        h, w = 0, 0
        sq = Person_Status(sq, h, w)
        if sq.is_full():
            current_status = sq.get_by_index(29)
            # print(current_status.status, current_status.hw_ratio)
    
    return fgmask, frame2, sq



def Fall_detection(real_time, video_path):
    if not real_time:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print("Video FPS:", fps)

        # knn = cv2.createBackgroundSubtractorKNN(detectShadows=True)
        backSub = cv2.createBackgroundSubtractorMOG2(history=800, varThreshold=10)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

        # get first frame
        ret, frame1 = cap.read()
        if not ret:
            print("Failed to read video")
            exit()

        # frame_num = 0
        sq = StatusQueue(maxlen=30)

        while cap.isOpened():
            ret, frame2 = cap.read()
            if not ret:
                break
            
            # print("Frame: ", frame_num)
            # frame_num += 1
            fgmask, frame2 = img_process(frame2, backSub, kernel)
            fgmask, frame2, sq = find_people(fgmask, frame2, sq)

            # cv2.imshow('Thresh', fgmask)
            cv2.imshow('Frame', frame2)
            
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    else:
        # for raspberry pi5 
        pass