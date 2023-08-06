from PIL import Image
import torchvision as pytorch
import torchvision.transforms as T
import sys
import numpy as np
import cv2 as cv
import random
import datetime
import argparse

useCuda=False

processingSize = (640, 360)

model=None

class PseudoLabeller:
    cocoLabels = [
        '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
        'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
        'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
        'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
        'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
        'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
        'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
        'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
        'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
        'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
    ]
    maskThreshold = 0.5
    bgSubtractionInterval=1500
    datasetClassIndice = 0
    solidColor=(0,0,0)
    filterClassIndices=[]

    def __init__(this, widthRange, heightRange, roiPoints, threshold, aspectAndDelta, intersectionThreshold,
                 datasetPath, backgroundPath,segmentation):
        this.widthRange = widthRange
        this.heightRange = heightRange
        this.transform = T.Compose([T.ToTensor()])
        this.rois = roiPoints
        this.threshold = threshold
        this.zoneRoiRects = []
        this.croppedZoneMask = []
        this.aspectAndDelta = aspectAndDelta
        this.intersectionThreshold = intersectionThreshold
        this.datasetPath = datasetPath
        this.backgroundHandler = cv.createBackgroundSubtractorMOG2()
        this.totalObjectCaughtSoFar = 0
        this.backgroundPath = backgroundPath
        this.internalFrameOrder = 0
        this.background = []
        this.segmentation=segmentation
        this.__setupZone()
        return

    def __setupZone(this):
        if this.backgroundPath:
            if this.backgroundPath=="solid":
                this.background = np.zeros((processingSize[1], processingSize[0], 3), np.uint8)
                cv.rectangle(this.background, (0,0),(processingSize[0],processingSize[1]), color=PseudoLabeller.solidColor, thickness=-1)
            else:
                this.background = cv.imread(this.backgroundPath)
                this.background = cv.resize(this.background,processingSize)
        if this.rois == []:
            this.rois = np.array(
                [[[0, 0], [processingSize[0], 0], [processingSize[0], processingSize[1]], [0, processingSize[1]]]],
                np.int)
        else:
            this.rois = np.array(this.rois, np.int)
        roiRect = [processingSize[0], processingSize[1], 0, 0]
        for zone in this.rois:
            roiRectOfZone = cv.boundingRect(zone)  # get united rect
            this.zoneRoiRects.append(roiRectOfZone)
            if roiRectOfZone[0] < roiRect[0]:
                roiRect[0] = roiRectOfZone[0]
            if roiRectOfZone[1] < roiRect[1]:
                roiRect[1] = roiRectOfZone[1]
            if roiRectOfZone[0] + roiRectOfZone[2] > roiRect[0] + roiRect[2]:
                roiRect[2] = roiRectOfZone[0] + roiRectOfZone[2] - roiRect[0]
            if roiRectOfZone[1] + roiRectOfZone[3] > roiRect[1] + roiRect[3]:
                roiRect[3] = roiRectOfZone[1] + roiRectOfZone[3] - roiRect[1]
            this.unitedZoneRoiRectSlice = np.s_[roiRect[1]:roiRect[1] + roiRect[3], roiRect[0]:roiRect[0] + roiRect[2]]
            this.croppedZoneMask = np.zeros((roiRect[3], roiRect[2], 3), np.uint8)
            this.zoneMask = np.zeros((processingSize[1], processingSize[0], 3), np.uint8)
            for zone in this.rois:
                cv.drawContours(this.zoneMask, [zone], 0, (255, 255, 255), -1)
                for point in zone:
                    point[0] -= roiRect[0]
                    point[1] -= roiRect[1]
                cv.drawContours(this.croppedZoneMask, [zone], 0, (255, 255, 255), -1)
            this.singleChannelZoneMask = cv.cvtColor(this.zoneMask, cv.COLOR_BGR2GRAY)
        return

    def __getZoneSight(this, frame):
        return cv.bitwise_and(frame[this.unitedZoneRoiRectSlice], this.croppedZoneMask)

    def __forward(this, img, threshold):
        img = Image.fromarray(img)
        img = this.transform(img)  # .cuda()
        # torch.cuda.empty_cache()
        prediction = model([img])[0]
        scores = list(prediction['scores'].detach().numpy())
        winners = [scores.index(x) for x in scores if x > threshold]
        if not winners:
            return [], [], []
        winners = winners[-1]
        masks = (prediction['masks'] > this.maskThreshold).squeeze().detach().cpu().numpy()
        classes = list(prediction['labels'].numpy())
        boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(prediction['boxes'].detach().numpy())]
        masks = masks[:winners + 1]
        boxes = boxes[:winners + 1]
        classes = classes[:winners + 1]
        # TODO: return Rect namedtuple or dict
        return masks, boxes, classes

    @staticmethod
    def __random_colour_masks(matrix):
        colours = [[0, 255, 0], [0, 0, 255], [255, 0, 0], [0, 255, 255], [255, 255, 0], [255, 0, 255], [80, 70, 180],
                   [250, 80, 190], [245, 145, 50], [70, 150, 250], [50, 190, 190]]
        r = np.zeros_like(matrix).astype(np.uint8)
        g = np.zeros_like(matrix).astype(np.uint8)
        b = np.zeros_like(matrix).astype(np.uint8)
        r[matrix == 1], g[matrix == 1], b[matrix == 1] = [255,255,255]#colours[random.randrange(0, 10)]
        coloured_mask = np.stack([r, g, b], axis=2)
        return coloured_mask

    def __testSizeCriterion(this, size):
        if this.widthRange[0] > -1:
            if size[0] < this.widthRange[0]:
                return False
        if this.widthRange[1] > -1:
            if size[0] > this.widthRange[1]:
                return False
        if this.heightRange[0] > -1:
            if size[1] < this.heightRange[0]:
                return False
        if this.heightRange[1] > -1:
            if size[1] > this.heightRange[1]:
                return False
        return True

    def __calculateIntersection(this, rect1, rect2):
        l1 = rect1[0][0]
        l2 = rect2[0][0]
        r1 = rect1[1][0]
        r2 = rect2[1][0]
        t1 = rect1[0][1]
        t2 = rect2[0][1]
        b1 = rect1[1][1]
        b2 = rect2[1][1]
        hIntersection = 0
        vIntersection = 0

        if l1 >= l2 and r1 <= r2:  # Contained
            hIntersection = r1 - l1
        elif l1 < l2 and r1 > r2:  # Contains
            hIntersection = r2 - l2
        elif l1 < l2 and r1 > l2:  # Intersects right
            hIntersection = r1 - l2
        elif r1 > r2 and l1 < r2:  # Intersects left
            hIntersection = r2 - l1
        else:  # No intersection (either side)
            hIntersection = 0

        if not hIntersection:
            return 0

        if t1 >= t2 and b1 <= b2:  # Contained
            vIntersection = b1 - t1
        elif t1 < t2 and b1 > b2:  # Contains
            vIntersection = b2 - t2
        elif t1 < t2 and b1 > t2:  # Intersects right
            vIntersection = b1 - t2
        elif b1 > b2 and t1 < b2:  # Intersects left
            vIntersection = b2 - t1
        else:  # No intersection (either side)
            vIntersection = 0

        return hIntersection * vIntersection

    def __testAspectRatio(this, box):
        if this.aspectAndDelta[0] == -1:
            return True
        x1 = box[0][0]
        x2 = box[1][0]
        y1 = box[0][1]
        y2 = box[1][1]
        aspect = (x2 - x1) / float(y2 - y1)
        return aspect < (this.aspectAndDelta[0] + this.aspectAndDelta[1]) and (
                aspect > this.aspectAndDelta[0] - this.aspectAndDelta[1])

    def __handleIntersection(this, boxes,masks):
        badBoxes = []
        badMasks = []
        goodMasks = []
        for i in range(len(boxes)):
            outerBox=boxes[i]
            if outerBox in badBoxes:
                continue
            outerY = outerBox[0][1]
            outerWidth = outerBox[1][0] - outerBox[0][0]
            outerHeight = outerBox[1][1] - outerBox[0][1]
            outerBoxArea = float(outerHeight * outerWidth)

            for j in range(len(boxes)):
                innerBox = boxes[j]
                if i == j:
                    continue
                if innerBox in badBoxes:
                    continue
                innerY = innerBox[0][1]
                innerWidth = innerBox[1][0] - innerBox[0][0]
                innerHeight = innerBox[1][1] - innerBox[0][1]
                innerBoxArea = float(innerWidth * innerHeight)

                intersectionArea = this.__calculateIntersection(innerBox, outerBox)
                if not intersectionArea:
                    continue
                if (intersectionArea / outerBoxArea) > this.intersectionThreshold or (
                        intersectionArea / innerBoxArea) > this.intersectionThreshold:
                    far = outerBox if outerY < innerY else innerBox
                    badBoxes.append(far)
                    badMasks.append(i if far==outerBox else j)
        goodBoxes = [x for x in boxes if x not in badBoxes]
        for index in range(len(masks)):
            if  not index in badMasks:
                goodMasks.append(masks[index])
        return goodBoxes,goodMasks

    def __testZoneCriterion(this, box):
        x1 = box[0][0]
        x2 = box[1][0]
        y1 = box[0][1]
        y2 = box[1][1]
        for zone in this.zoneRoiRects:
            if zone[0] > x1:
                continue
            if zone[1] > y1:
                continue
            if zone[0] + zone[2] < x2:
                continue
            if zone[1] + zone[3] < y2:
                continue
            return True
        return False

    def __getBoxSlice(this,box):
        boxInt = np.array(box, np.int)
        boxSlice = np.s_[boxInt[0][1]:boxInt[1][1], boxInt[0][0]:boxInt[1][0]]
        return boxSlice

    def __getBackground(this):
        if not this.backgroundPath=="":
            return this.background.copy()
        return this.backgroundHandler.getBackgroundImage().copy()

    def __testZoneMaskCriterion(this, box, owningZoneRatio=0.90):
        nonZero = cv.countNonZero(this.singleChannelZoneMask[this.__getBoxSlice(box)])
        area = ((box[1][1] - box[0][1]) * (box[1][0] - box[0][0]))
        ratio = (nonZero / float(area))
        return ratio > owningZoneRatio

    def __handleObjectMaskCriterion(this, image, mask,boxSlice):
        segmentMask=PseudoLabeller.__random_colour_masks(mask)[boxSlice]
        segmentMask = cv.cvtColor(segmentMask, cv.COLOR_RGB2GRAY)
        nonZero=cv.countNonZero(segmentMask)
        area=float(image[boxSlice].shape[0]*image[boxSlice].shape[1])
        if (nonZero/area)>0.1:
            background=this.__getBackground()[boxSlice]
            cv.copyTo(image[boxSlice],segmentMask,background)
            image[boxSlice]=background
        return

    def __deliverResult(this, img, boxes, masks,frameOrder):
        if not len(boxes):
            print("Nothing detected in frame: " + str(frameOrder))
            print("Caught " + str(this.totalObjectCaughtSoFar) + " objects so far.")
            return this.__getBackground()

        goodBoxes,goodMasks = this.__handleIntersection(boxes,masks)
        baseOverlay = np.zeros((processingSize[1], processingSize[0], 3), np.uint8)

        cv.copyTo(this.__getBackground(), None, baseOverlay)

        annotationTxt = open(this.datasetPath + str(frameOrder) + ".txt", "a+")
        trainTxt = open(this.datasetPath + "_train" + ".txt", "a+")
        trainTxt.write("%s\n" % (this.datasetPath + str(frameOrder) + ".jpg"))
        trainTxt.close()

        print("Committed " + str(len(goodBoxes)) + " object(s) in frame: " + str(frameOrder))
        this.totalObjectCaughtSoFar += len(goodBoxes)
        print("Caught " + str(this.totalObjectCaughtSoFar) + " objects so far.")

        for i in range(len(goodBoxes)):
            box=goodBoxes[i]
            boxSlice = np.s_[int(box[0][1]):int(box[1][1]), int(box[0][0]):int(box[1][0])]
            if this.segmentation:
                this.__handleObjectMaskCriterion(img,goodMasks[i],boxSlice)
            cv.copyTo(img[boxSlice], None, baseOverlay[boxSlice])
            yoloX = float(box[0][0] + ((box[1][0] - box[0][0]) / 2)) / img.shape[1]
            yoloY = float(box[0][1] + ((box[1][1] - box[0][1]) / 2)) / img.shape[0]
            yoloWidth = float(box[1][0] - box[0][0]) / img.shape[1]
            yoloHeight = float(box[1][1] - box[0][1]) / img.shape[0]
            annotationTxt.write("%d %f %f %f %f\n" % (PseudoLabeller.datasetClassIndice, yoloX, yoloY, yoloWidth, yoloHeight))
        annotationTxt.close()

        cv.imwrite(this.datasetPath + str(frameOrder) + ".jpg", baseOverlay)
        for box in goodBoxes:
            cv.rectangle(img, box[0], box[1], color=(0, 255, 0), thickness=1)
        return baseOverlay

    def segment(this, img, frameOrder):
        if not this.backgroundPath:
            this.internalFrameOrder+=1
            this.backgroundHandler.apply(img)
            if this.internalFrameOrder < PseudoLabeller.bgSubtractionInterval:
                progress = int(this.internalFrameOrder / float(PseudoLabeller.bgSubtractionInterval) * 100)
                print("Having background: %" + str(progress))
                return this.__getBackground(),False
        masks, boxes, classIndices = this.__forward(img, this.threshold)
        goodBoxes = []
        goodMasks=[]
        for i in range(len(boxes)):
            if not PseudoLabeller.filterClassIndices==[]:
                if classIndices[i] not in PseudoLabeller.filterClassIndices:
                    continue
            box=boxes[i]
            if not this.__testZoneMaskCriterion(box):
                continue
            boxWidth = box[1][0] - box[0][0]
            boxHeight = box[1][1] - box[0][1]
            if not this.__testSizeCriterion((boxWidth, boxHeight)):  # x1,y1,x2,y2
                continue
            goodBoxes.append(box)
            goodMasks.append(masks[i])
        return this.__deliverResult(img, goodBoxes,goodMasks, frameOrder),True


class ZoneDrawer:
    windowName = "Zone Setup"
    done = False
    currentlyDrawingSegment = (0, 0)
    roiPoints = []
    zoneIter = 0

    @staticmethod
    def mouseCallback(event, x, y, flags, param):
        if ZoneDrawer.done:
            return
        if event == cv.EVENT_MOUSEMOVE:
            ZoneDrawer.currentlyDrawingSegment = (x, y)
        elif event == cv.EVENT_LBUTTONDOWN:
            print("Adding point #%d with position(%d,%d)" % (len(ZoneDrawer.roiPoints[ZoneDrawer.zoneIter]), x, y))
            ZoneDrawer.roiPoints[ZoneDrawer.zoneIter].append((x, y))
        elif event == cv.EVENT_RBUTTONDOWN:
            print("Completing polygon with %d points." % len(ZoneDrawer.roiPoints[ZoneDrawer.zoneIter]))
            ZoneDrawer.done = True

    @staticmethod
    def getRoiPoints(cap):
        if ZoneDrawer.done:
            return ZoneDrawer.roiPoints

        ZoneDrawer.roiPoints.append([])

        ret, img = cap.read()
        while not ret:
            print("Retrying frame grabbing")
            ret, img = cap.read()
        img = cv.resize(img, processingSize)
        cv.putText(img,
                   'click points to draw. press d after your job done, r for reset, red segment is zone. n for next zone, p for previous zone.',
                   (20, 20), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1, cv.LINE_AA)
        cv.putText(img,
                   'You may need to press key several times to be able to catch keypress event so be careful and watch terminal output while iterating between zones.',
                   (20, 40), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1, cv.LINE_AA)
        clean = img.copy()
        cv.namedWindow(ZoneDrawer.windowName)
        cv.imshow(ZoneDrawer.windowName, np.zeros(processingSize, np.uint8))
        cv.waitKey(50)
        cv.setMouseCallback(ZoneDrawer.windowName, ZoneDrawer.mouseCallback)

        while (1):
            if (len(ZoneDrawer.roiPoints) > 0):
                cv.polylines(img, np.array([ZoneDrawer.roiPoints[ZoneDrawer.zoneIter]]), False, (0, 0, 255), 2)
            #    if len(ZoneDrawer.roiPoints[ZoneDrawer.zoneIter]):
            #        cv.line(img, ZoneDrawer.roiPoints[ZoneDrawer.zoneIter][-1], ZoneDrawer.currentlyDrawingSegment,
            #                (0, 255, 0), 1)
            cv.imshow(ZoneDrawer.windowName, img)
            if cv.waitKey(50) & 0xFF == ord('d'):
                ZoneDrawer.done = True
                break
            if cv.waitKey(50) & 0xFF == ord('n'):
                if not len(ZoneDrawer.roiPoints) > ZoneDrawer.zoneIter + 1:
                    ZoneDrawer.roiPoints.append([])
                ZoneDrawer.zoneIter += 1
                print("Drawing zone:" + str(ZoneDrawer.zoneIter))
            if cv.waitKey(50) & 0xFF == ord('p'):
                if ZoneDrawer.zoneIter > 0:
                    ZoneDrawer.zoneIter -= 1
                print("Drawing zone:" + str(ZoneDrawer.zoneIter))
            if cv.waitKey(50) & 0xFF == ord('r'):
                print("Resetting zone:" + str(ZoneDrawer.zoneIter))
                ZoneDrawer.roiPoints[ZoneDrawer.zoneIter] = []
                img = clean.copy()
        cv.destroyWindow(ZoneDrawer.windowName)
        return ZoneDrawer.roiPoints

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-in", "--input", required=True, help="Path to the input video or stream")
    ap.add_argument("-hl", "--headless", required=False, action='store_true', help="Headless mode")
    ap.add_argument("-cu", "--cuda", required=False, action='store_true', help="Usa cuda")
    ap.add_argument("-ps", "--processing-size", required=False, nargs='+', default=[1280,720], help="Processing Resolution, int space int")
    ap.add_argument("-zo", "--zones", required=False, nargs='+', type=list,
                    help="You can pass zone points manually like 0,0 1280,0 1280,720 0,720 and you can use | to split zones")
    ap.add_argument("-bp", "--background-path", required=False, help="Static background path")
    ap.add_argument("-sb", "--solid-background", required=False, help="Use solid background. Convention is 1,2,3 in BGR order")
    ap.add_argument("-dp", "--dataset-path", required=True, help="Path for artifacts")
    ap.add_argument("-bi", "--bg-interval", required=False, type=int, default=1500,
                    help="Background collection interval, int")
    ap.add_argument("-di", "--dataset-class-indice", required=False, type=int, default=0,
                    help="Class indice to be used, int")
    ap.add_argument("-if", "--indice-filter", required=False, nargs='+', type=int,
                    help="MaskRCNN classes to be accepted, int int int int int ...")
    ap.add_argument("-fd", "--process-every-n", required=False, type=int, default=30,
                    help="Process every nth frames, int")
    ap.add_argument("-dt", "--detection-threshold", required=False, type=float, default=0.6, help="Detection Threshold, float")
    ap.add_argument("-it", "--intersection-threshold", required=False, type=float,default=0, help="intersection Threshold, more than x will be discarded, float")
    ap.add_argument("-wr", "--width-range", required=False, nargs='+', type=int,default=[-1,-1], help="Width Range: min, max, int")
    ap.add_argument("-hr", "--height-range", required=False, nargs='+', type=int,default=[-1,-1], help="Height Range: min, max, int")
    ap.add_argument("-ar", "--aspect-range", required=False, nargs='+',type=int, default=[-1,0], help="Aspect Range: aspect, deviation, Aspect is width/height, int , int")
    ap.add_argument("-se", "--segmentation", required=False, action='store_true', help="Segment object inside box")
    args = vars(ap.parse_args())

    global useCuda
    global model
    useCuda=args["cuda"]
    if useCuda:
        import pycuda.driver as cuda
        cuda.init()
        #print(pytorch.cuda.get_device_name(0))
        model = pytorch.models.detection.maskrcnn_resnet50_fpn(pretrained=True).cuda()
    else:
        model = pytorch.models.detection.maskrcnn_resnet50_fpn(pretrained=True)

    model.eval()

    widthRange = (-1, -1)
    heightRange = (-1, -1)
    aspectAndDelta = (
        -1,
        0)
    intersectionThreshold = 0.0
    backgroundPath = ""
    datasetPath = ""
    threshold = 0.6
    frameDropInterval = 30

    if not args["processing_size"] is None:
        if len(args["processing_size"])==2:
            global processingSize
            processingSize= (int(args["processing_size"][0]), int(args["processing_size"][1]))

    if not args["width_range"] is None:
        if len(args["width_range"])==2:
            widthRange= (int(args["width_range"][0]), int(args["width_range"][1]))

    if not args["height_range"] is None:
        if len(args["height_range"])==2:
            heightRange= (int(args["height_range"][0]), int(args["height_range"][1]))

    if not args["aspect_range"] is None:
        if len(args["aspect_range"])==2:
            aspectAndDelta= (int(args["aspect_range"][0]), int(args["aspect_range"][1]))

    if not args["intersection_threshold"] is None:
        intersectionThreshold= float(args["intersection_threshold"])

    if not args["detection_threshold"] is None:
        threshold= float(args["detection_threshold"])

    if not args["process_every_n"] is None:
        frameDropInterval= float(args["process_every_n"])

    if not args["bg_interval"] is None:
        PseudoLabeller.bgSubtractionInterval= float(args["bg_interval"])

    if not args["dataset_class_indice"] is None:
        PseudoLabeller.datasetClassIndice= int(args["dataset_class_indice"])

    if not args["indice_filter"] is None:
        PseudoLabeller.filterClassIndices= args["indice_filter"]

    if not args["background_path"] is None:
        backgroundPath= str(args["background_path"])

    if not args["solid_background"] is None:
        channelList = args["solid_background"].split(",")
        if len(channelList)==3:
            backgroundPath="solid"
            PseudoLabeller.solidColor=(int(channelList[0]),int(channelList[1]),int(channelList[2]))

    if not args["dataset_path"] is None:
        datasetPath= str(args["dataset_path"])

    segmentation = args["segmentation"]

    cap = cv.VideoCapture(str(args["input"]))
    headless = args["headless"]
    frameOrder = 0

    roiPoints = []
    if args["zones"] is None:
        roiPointsTuple = ZoneDrawer.getRoiPoints(cap)
        for zoneTuple in roiPointsTuple:
            zoneArray=[]
            for point in zoneTuple:
                zoneArray.append([point[0],point[1]])
            roiPoints.append(zoneArray)
    else:
        print(args["zones"])
        currentZoneList = []
        currentPointPairs = []
        currentCoordinate=""
        args["zones"].append("|")
        for pairs in args["zones"]:
            for i in range(len(pairs)):
                digit=pairs[i]
                if digit == "|":
                    roiPoints.append(currentZoneList)
                    currentZoneList = []
                    currentPointPairs = []
                    currentCoordinate=""
                    continue
                elif digit == ",":
                    currentPointPairs.append(int(currentCoordinate))
                    currentCoordinate=""
                else:
                    currentCoordinate+=(digit)
                if i==len(pairs)-1:
                    currentPointPairs.append(int(currentCoordinate))
                    currentZoneList.append(currentPointPairs)
                    currentPointPairs = []
                    currentCoordinate=""


    labeller = PseudoLabeller(widthRange, heightRange, roiPoints, threshold, aspectAndDelta, intersectionThreshold,
                              datasetPath, backgroundPath,segmentation)


    if cap.isOpened():
        ret, frame = cap.read()
        shouldWeRunFrameDropping = True
        while True:
            if ret:
                frame = cv.resize(frame, processingSize)
                frameOrder += 1
                if (frameOrder > frameDropInterval and (frameOrder % frameDropInterval)==0) or not shouldWeRunFrameDropping:
                    before=datetime.datetime.now()
                    result,shouldWeRunFrameDropping = labeller.segment(frame, frameOrder)
                    after=datetime.datetime.now()
                    print(str((after-before).microseconds/1e6)+" seconds spent in frame: "+str(frameOrder))
                    if not headless:
                        cv.imshow('actual camera', frame)
                        cv.imshow('process output', result)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                cap.release()
                cap = cv.VideoCapture(str(sys.argv[1]))
            ret, frame = cap.read()
    cv.waitKey(0)
    cap.release()
    cv.destroyAllWindows()


main()