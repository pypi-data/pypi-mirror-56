import sys
import os

from PySide2 import QtCore, QtGui,QtWidgets
from PySide2.QtCore import Qt, Slot, Signal, QObject, QDir, QRectF, QPointF,QPoint
from PySide2.QtWidgets import*
from PySide2.QtGui import*
from PySide2.QtGui import QColor
from PySide2.QtWidgets import (QGraphicsView,QGraphicsScene, QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,QVBoxLayout, QWidget)
from PySide2.QtCharts import QtCharts
import cv2
from arabaci01.EditWindow import *
from arabaci01.GraphicsView import *
from arabaci01.Scene import *
from PIL import Image
import torchvision as pytorch
import torchvision.transforms as T
import numpy as np
import cv2 as cv
import random
import datetime
import qdarkstyle

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
        print("rois")
        print(this.rois)
        for zone in this.rois:
            print (zone)
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
        print ("img")
        print (model)
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
                                                            #    Mainwindow elements

class RectItem(QGraphicsRectItem):
    def __init__(self,rectThickness,counter,x,y,w,h):
        QGraphicsRectItem.__init__(self)
        self.whichRect=counter
        self.rectF1= QRectF(x,y,w,h)
        self.setRect(self.rectF1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setBrush(QBrush(QtCore.Qt.transparent, style = QtCore.Qt.BDiagPattern))
        self.rectThickness=rectThickness
        self.setPen(QtGui.QPen(QtCore.Qt.red, self.rectThickness))
        self.setOpacity(0.3)

class SelectTemplateRangeWindow(QDialog):
    tempRangeSignal=Signal(int,int)
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Select Template Range")
        self.okButton=QPushButton("OK")
        self.cancelButton=QPushButton("Cancel")
        self.numberRangeBegins = QComboBox()
        self.numberRangeBegins.setEditable(True)
        self.numberRangeEnds = QComboBox()
        self.numberRangeEnds.setEditable(True)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.okButton)
        self.layout.addWidget(self.cancelButton)
        self.layout.addWidget(self.numberRangeBegins)
        self.layout.addWidget(self.numberRangeEnds)
        self.setLayout(self.layout)
        self.okButton.clicked.connect(self.okButtonClicked)
        self.numberRangeBegins.currentIndexChanged.connect(self.changeOfNumberRangeBegins)
        self.numberRangeEnds.currentIndexChanged.connect(self.changeOfNumberRangeEnds)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)
        self.setTabOrder(self.okButton, self.cancelButton)

    @Slot()
    def numberOfPictures(self, currentNumberOfImages, maxNumberOfImages):
        for x in range(maxNumberOfImages):
            self.numberRangeBegins.addItem(str(x))
            self.numberRangeEnds.addItem(str(x))
        self.numberRangeBegins.setCurrentIndex(currentNumberOfImages)
        self.numberRangeEnds.setCurrentIndex(currentNumberOfImages)

    @Slot()
    def changeOfNumberRangeBegins(self,index):
        self.numberRangeBegins.setCurrentText(self.numberRangeBegins.itemText(index))

    @Slot()
    def changeOfNumberRangeEnds(self,index):
        self.numberRangeEnds.setCurrentText(self.numberRangeEnds.itemText(index))

    @Slot()
    def okButtonClicked(self,clicked):
        self.tempRangeSignal.emit(int(self.numberRangeBegins.currentText()),int(self.numberRangeEnds.currentText()))
        self.close()

    @Slot()
    def cancelButtonClicked(self,clicked):
        self.close()

class SelectPainterSizeWindow(QDialog):
    painterSizeSignal=Signal(int,float,float,float,float)
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Select Painter Size")
        self.okButton=QPushButton("OK")
        self.cancelButton=QPushButton("Cancel")
        self.size = QLineEdit()
        self.comboBox = QComboBox()
        self.comboBox.setEditable(True)
        self.paintingColor = QColorDialog()
        self.paintingColor.setWindowFlags(Qt.Widget)
        self.paintingColor.setOptions(QColorDialog.DontUseNativeDialog)
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.paintingColor)
        self.setLayout(self.layout)
        self.okButton.clicked.connect(self.okButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)
        self.comboBox.currentIndexChanged.connect(self.selectionchanged)
        self.paintingColor.colorSelected.connect(self.colorSelected)
        self.setTabOrder(self.okButton, self.cancelButton)
        for x in range(101):
            self.comboBox.addItem(str(x))
        self.comboBox.setCurrentIndex(20)

    @Slot()
    def colorSelected(self):
        self.selectedColor=self.paintingColor.currentColor()
        red=self.selectedColor.redF()
        green=self.selectedColor.greenF()
        blue=self.selectedColor.blueF()
        alpha=self.selectedColor.alphaF()
        self.painterSizeSignal.emit(int(self.comboBox.currentText()), red,green,blue,alpha)
        self.close()

    @Slot()
    def selectionchanged(self,index):
        self.comboBox.setCurrentText(self.comboBox.itemText(index))

    @Slot()
    def okButtonClicked(self,clicked):
        red=self.selectedColor.redF()
        green=self.selectedColor.greenF()
        blue=self.selectedColor.blueF()
        alpha=self.selectedColor.alphaF()
        self.painterSizeSignal.emit(int(self.comboBox.currentText()), red,green,blue,alpha)
        self.close()

    @Slot()
    def cancelButtonClicked(self,clicked):
        self.close()

class EditClassesTxtWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Edit classes.txt File")
        self.saveButton=QPushButton("Save")
        self.editButton=QPushButton("Edit")
        self.textEdit=QTextEdit()
        self.textEdit.setReadOnly(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.saveButton)
        self.layout.addWidget(self.editButton)
        self.layout.addWidget(self.textEdit)
        self.setLayout(self.layout)
        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.editButton.clicked.connect(self.editButtonClicked)
        self.setTabOrder(self.saveButton, self.editButton)

    def pathOfClassesTxt(self,path):
        self.path=path
        if (os.path.isfile(self.path)):
            f=open(self.path, "r")
            self.content=f.readlines()
            f.close()
            self.textEdit.clear()
            for x in self.content:
                if (x[-1]=="\n"):
                    self.textEdit.append(x[:-1])
                else:
                    self.textEdit.append(x)

        else:
            f=open(self.path, "w+")
            self.content=f.readlines()
            f.close()
            for x in self.content:
                self.textEdit.append(x[:-1])


    @Slot()
    def saveButtonClicked(self,clicked):
        f= open(self.path,"w")

        f.writelines(self.textEdit.toPlainText())
        f.close()
        self.textEdit.setReadOnly(True)
        self.textEdit.setTextBackgroundColor(QtCore.Qt.lightGray)

    @Slot()
    def editButtonClicked(self,clicked):
        self.textEdit.setTextBackgroundColor(QtCore.Qt.white)
        self.textEdit.setReadOnly(False)

class LeftToolBar(QToolBar):                    # left tool bar for Marker
    def __init__(self):
        QToolBar.__init__(self)
        self.leftToolBarWidth = 70
        self.setFixedWidth(self.leftToolBarWidth)
        self.setWindowTitle("TOOLS")
        self.setOrientation(QtCore.Qt.Vertical)
        self.setMovable(False)
        self.addSeparator()
        self.osPath= os.getcwd()

        # Open QAction
        openButton = QToolButton()
        openButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        openButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.openAction = QAction(QIcon(self.osPath+"/icons/open.png"),"__Open__", self)
        self.openAction.setToolTip("open single image")
        font = self.openAction.font()
        font.setPointSize(10)
        self.openAction.setFont(font)
        self.openAction.triggered.emit()
        openButton.setDefaultAction(self.openAction)
        self.addWidget(openButton)

        # Open Dir QAction
        openDirButton = QToolButton()
        openDirButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        openDirButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.openDirAction = QAction(QIcon(self.osPath+"/icons/open.png"),"Open Dir", self)
        self.openDirAction.setToolTip("open dataset directory")
        self.openDirAction.setFont(font)
        self.openDirAction.triggered.emit()
        openDirButton.setDefaultAction(self.openDirAction)
        self.addWidget(openDirButton)

        # Delete Img QAction
        deleteImgButton = QToolButton()
        deleteImgButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        deleteImgButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.deleteImgAction = QAction(QIcon(self.osPath+"/icons/delete.png"),"_Delete_\nImg", self)
        self.deleteImgAction.setToolTip("delete image")
        self.deleteImgAction.setFont(font)
        self.deleteImgAction.setEnabled(False)
        self.deleteImgAction.triggered.emit()
        deleteImgButton.setDefaultAction(self.deleteImgAction)
        self.addWidget(deleteImgButton)

        # Next QAction
        nextButton=QToolButton()
        nextButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        nextButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.nextAction = QAction(QIcon(self.osPath+"/icons/next.png"),"__Next__", self)
        self.nextAction.setToolTip("open the next image\nPress to D for shortcut")
        self.nextAction.setFont(font)
        self.nextAction.setShortcut("D")
        self.nextAction.setEnabled(False)
        self.nextAction.triggered.emit()
        nextButton.setDefaultAction(self.nextAction)
        self.addWidget(nextButton)

        # Previous QAction
        previousButton=QToolButton()
        previousButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        previousButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.previousAction = QAction(QIcon(self.osPath+"/icons/prev.png"),"Previous", self)
        self.previousAction.setToolTip("open the previous image\nPress to A for shortcut")
        self.previousAction.setFont(font)
        self.previousAction.setShortcut("A")
        self.previousAction.setEnabled(False)
        self.previousAction.triggered.emit()
        previousButton.setDefaultAction(self.previousAction)
        self.addWidget(previousButton)

        # Create Rect QAction
        createButton= QToolButton()
        createButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.createAction = QAction(QIcon(self.osPath+"/icons/objects.png"),"Cre Rect", self)
        self.createAction.setToolTip("draw a box\nPress to R for shortcut")
        self.createAction.setFont(font)
        self.createAction.setShortcut("R")
        self.createAction.setEnabled(False)
        self.createAction.triggered.emit()
        createButton.setDefaultAction(self.createAction)
        self.addWidget(createButton)

        # Edit Rect QAction
        editButton= QToolButton()
        editButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.editAction = QAction(QIcon(self.osPath+"/icons/labels.png"),"Edit Rect", self)
        self.createAction.setToolTip("edit label of box\nPress to E for shortcut")
        self.editAction.setFont(font)
        self.editAction.setShortcut("E")
        self.editAction.setEnabled(False)
        self.editAction.triggered.emit()
        editButton.setDefaultAction(self.editAction)
        self.addWidget(editButton)

        # Delete Rect QAction
        deleteButton= QToolButton()
        deleteButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.deleteAction = QAction(QIcon(self.osPath+"/icons/delete.png"),"Del. Rect", self)
        self.deleteAction.setToolTip("delete a box\nPress to DEL for shortcut")
        self.deleteAction.setFont(font)
        self.deleteAction.setShortcut("Del")
        self.deleteAction.setEnabled(False)
        self.deleteAction.triggered.emit()
        deleteButton.setDefaultAction(self.deleteAction)
        self.addWidget(deleteButton)

        # Duplicate Rect QAction
        duplicateButton= QToolButton()
        duplicateButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.duplicateAction = QAction(QIcon(self.osPath+"/icons/copy.png"),"Dupl. Rect", self)
        self.duplicateAction.setToolTip("duplicate a box\nPress to F for shortcut")
        self.duplicateAction.setFont(font)
        self.duplicateAction.setShortcut("F")
        self.duplicateAction.setEnabled(True)
        self.duplicateAction.triggered.emit()
        duplicateButton.setDefaultAction(self.duplicateAction)
        self.addWidget(duplicateButton)

        # Show Statistics QAction
        showStatisticsButton= QToolButton()
        showStatisticsButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.showStatisticsAction = QAction(QIcon(self.osPath+"/icons/eye.png"),"Show\nStatistics", self)
        self.showStatisticsAction.setFont(font)
        self.showStatisticsAction.setEnabled(False)
        self.showStatisticsAction.triggered.emit()
        showStatisticsButton.setDefaultAction(self.showStatisticsAction)
        self.addWidget(showStatisticsButton)

        self.label = QLabel("Img No")
        self.label.setFont(font)
        self.addWidget(self.label)
        self.labelImgNo = QLabel("")
        self.labelImgNo.setFont(font)
        self.addWidget(self.labelImgNo)
        self.addSeparator()

class RightToolBar(QToolBar):                   # right tool bar for Marker
    def __init__(self):
        QToolBar.__init__(self)
        self.rightToolBarWidth = 200
        self.setFixedWidth(self.rightToolBarWidth)
        self.setWindowTitle("LISTS")
        self.setOrientation(QtCore.Qt.Vertical)
        self.setMovable(False)
        self.addSeparator()
        self.osPath = os.getcwd()

        # Paint QAction
        self.paintAction = QPushButton()
        self.paintAction.setText("Start Paint")
        self.paintAction.setIcon(QtGui.QIcon(self.osPath+"/icons/color.png"))
        self.paintAction.setEnabled(False)
        self.paintAction.clicked.emit()
        self.addWidget(self.paintAction)

        # Apply Paint QAction
        self.applyPaintAction = QPushButton()
        self.applyPaintAction.setText("Apply")
        self.applyPaintAction.setIcon(QtGui.QIcon(self.osPath + "/icons/done.png"))
        self.applyPaintAction.setEnabled(False)
        self.applyPaintAction.clicked.emit()

        # Cancel Paint QAction
        self.cancelPaintAction = QPushButton()
        self.cancelPaintAction.setText("Cancel")
        self.cancelPaintAction.setIcon(QtGui.QIcon(self.osPath + "/icons/cancel.png"))
        self.cancelPaintAction.setEnabled(False)
        self.cancelPaintAction.clicked.emit()

        self.hBoxLayoutWidget = QWidget()
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayoutWidget.setLayout(self.hBoxLayout)
        self.hBoxLayout.addWidget(self.applyPaintAction)
        self.hBoxLayout.addWidget(self.cancelPaintAction)
        self.addWidget(self.hBoxLayoutWidget)

        # Seperator
        self.spacerWidget = QWidget()
        self.spacerWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.spacerWidget.setVisible(True)
        self.addWidget(self.spacerWidget)
        self.addSeparator()

        # Create Template QAction
        self.createTemplateAction = QPushButton()
        self.createTemplateAction.setText("Create Template")
        self.createTemplateAction.setIcon(QtGui.QIcon(self.osPath + "/icons/color.png"))
        self.createTemplateAction.setEnabled(False)
        self.createTemplateAction.clicked.emit()
        self.addWidget(self.createTemplateAction)

        # Apply Template QAction
        self.applyTemplateAction = QPushButton()
        self.applyTemplateAction.setText("Apply")
        self.applyTemplateAction.setIcon(QtGui.QIcon(self.osPath + "/icons/done.png"))
        self.applyTemplateAction.setEnabled(False)
        self.applyTemplateAction.clicked.emit()

        # Cancel Template QAction
        self.cancelTemplateAction = QPushButton()
        self.cancelTemplateAction.setText("Cancel")
        self.cancelTemplateAction.setIcon(QtGui.QIcon(self.osPath + "/icons/cancel.png"))
        self.cancelTemplateAction.setEnabled(False)
        self.cancelTemplateAction.clicked.emit()

        self.hBoxLayoutWidget2 = QWidget()
        self.hBoxLayout2 = QHBoxLayout()
        self.hBoxLayoutWidget2.setLayout(self.hBoxLayout2)
        self.hBoxLayout2.addWidget(self.applyTemplateAction)
        self.hBoxLayout2.addWidget(self.cancelTemplateAction)
        self.addWidget(self.hBoxLayoutWidget2)

        # Label
        self.label = QLabel("Box List")
        self.addWidget(self.label)

        # CheckListWidget
        self.checkListWidget = QListWidget()
        self.addWidget(self.checkListWidget)
        self.checkListWidget.currentRowChanged.emit(int)
        self.addSeparator()

        # Label2
        self.label2 = QLabel("File List")
        self.addWidget(self.label2)

        # ListWidget
        self.fileListWidget = QListWidget()
        self.fileListWidget.sortItems(Qt.AscendingOrder)
        self.fileListWidget.currentRowChanged.emit(int)
        self.addWidget(self.fileListWidget)

                                                                    #PseudoLabeller elements
class PSLLeftToolBar(QToolBar):
    def __init__(self):
        QToolBar.__init__(self)
        self.pslLeftToolBarWidth = 200
        self.setFixedWidth(self.pslLeftToolBarWidth)
        self.setOrientation(QtCore.Qt.Vertical)
        self.setMovable(False)

        # Input path
        self.inputButton = QPushButton()
        self.inputButton.setText("Input")
        self.inputButton.clicked.emit()
        self.inputTextBox=QLineEdit()
        #self.inputTextBox.setText("/home/ahmet/Videos/new2.mp4")
        self.inputButton.setToolTip("Select input video path")
        self.inputButton.setToolTip("Select input video path")

        # Headless Label
        self.headlessCheckBox=QCheckBox("Headless", self)
        self.headlessCheckBox.setToolTip("Check to hide processing windows ")

        #Cuda
        self.cudaCheckBox = QCheckBox("Cuda", self)
        self.cudaCheckBox.setToolTip("Check to use cuda")

        # Processing size
        self.processingSizeLabel=QLabel("Pro. Size:")
        self.processingSizeLabel.setToolTip("Select Processing Resolution")
        self.hSize=QLineEdit()
        self.hSize.setText("1280")
        self.hSize.setToolTip("Select Processing Height Resolution")
        self.xLabel=QLabel("x")
        self.wSize=QLineEdit()
        self.wSize.setText("720")
        self.wSize.setToolTip("Select Processing Width Resolution")

        #Zone
        self.zoneLabel=QLabel("Zone:")
        self.zoneInputTextBox = QLineEdit()

        #Background path
        self.bgInputButton=QPushButton()
        self.bgInputButton.setText("Bg. Path:")
        self.bgInputButton.clicked.emit()
        self.bgInputTextBox = QLineEdit()
        self.bgInputTextBox.setText("solid")
        self.bgInputButton.setToolTip("Select Background Path")
        self.bgInputTextBox.setToolTip("Select Background Path")

        #solid Background
        self.solidBgCheckBox = QCheckBox("Solid Background", self)
        self.solidBgCheckBox.setToolTip("Check to use solid background")

        #dataset path
        self.datasetInputButton = QPushButton()
        self.datasetInputButton.setText("Datas. Path:")
        self.datasetInputButton.clicked.emit()
        self.datasetInputTextBox = QLineEdit()
        self.datasetInputButton.setToolTip("Select Dataset Path")
        self.datasetInputTextBox.setToolTip("Select Dataset Path")
        #self.datasetInputTextBox.setText("/home/ahmet/PycharmProjects/Marker/dataset")

        #prefix
        self.prefixlabel = QLabel("Prfx:")
        self.prefixTextBox = QLineEdit()
        self.prefixTextBox.setText("prefix-")
        self.prefixTextBox.setToolTip("Prefix for image and txt names")
        self.prefixlabel.setToolTip("Prefix for image and txt names")

        #Background interval
        self.bgIntervalLabel=QLabel("Bg. Interval:")
        self.bgIntervalTextBox = QLineEdit()
        self.bgIntervalTextBox.setText("1500")
        self.bgIntervalLabel.setToolTip("Select background collection interval")
        self.bgIntervalTextBox.setToolTip("Select background collection interval")

        #dataset class indice
        self.classIndiceLabel=QLabel("Class Indice")
        self.classIndiceTextBox=QLineEdit()
        self.classIndiceTextBox.setText("0")
        self.classIndiceLabel.setToolTip("Select default class indice")
        self.classIndiceTextBox.setToolTip("Select default class indice")

        #dataset indice filter
        self.indiceFilterLabel=QLabel("Indice Filter")
        self.indiceFilterTextBox=QLineEdit()
        self.indiceFilterTextBox.setText("0,1,2,3,4,5,6,7,8,9,10,11")
        self.indiceFilterLabel.setToolTip("Select MaskRCNN indices to be labelled. Ex:0,1,2,3,4,5,6...")
        self.indiceFilterTextBox.setToolTip("Select MaskRCNN indices to be labelled. Ex:0,1,2,3,4,5,6...")

        #process every n'th frames
        self.processEveryNthFramesLabel=QLabel("Frame Drop Int.:")
        self.processEveryNthFramesTextBox=QLineEdit()
        self.processEveryNthFramesTextBox.setText("30")
        self.processEveryNthFramesLabel.setToolTip("Select frame process interval")
        self.processEveryNthFramesTextBox.setToolTip("Select frame process interval")

        #detection threshold
        self.detectionThresholdLabel=QLabel("Detection Thresh.:")
        self.detectionThresholdTextBox=QLineEdit()
        self.detectionThresholdTextBox.setText("0.6")
        self.detectionThresholdLabel.setToolTip("Select detection threshold")
        self.detectionThresholdTextBox.setToolTip("Select detection threshold")

        #intersection threshold
        self.intersectionThresholdLabel=QLabel("Intersect. Thresh.:")
        self.intersectionThresholdTextBox=QLineEdit()
        self.intersectionThresholdTextBox.setText("0")
        self.intersectionThresholdLabel.setToolTip("Select intersection threshold")
        self.intersectionThresholdTextBox.setToolTip("Select intersection threshold")

        # width range
        self.widthRangeLabel=QLabel("Width Range")
        self.wMinLabel=QLabel("Min:")
        self.wMinTextBox=QLineEdit()
        self.wMinTextBox.setText("-1")
        self.wMaxLabel=QLabel("Max:")
        self.wMaxTextBox=QLineEdit()
        self.wMaxTextBox.setText("-1")
        self.widthRangeLabel.setToolTip("Select width range of labelled box in pixels")
        self.wMinLabel.setToolTip("Select minimum width range of labelled box in pixels")
        self.wMinTextBox.setToolTip("Select minimum width range of labelled box in pixels")
        self.wMaxLabel.setToolTip("Select maximum width range of labelled box in pixels")
        self.wMaxTextBox.setToolTip("Select maximum width range of labelled box in pixels")

        # height range
        self.heightRangeLabel = QLabel("Height Range")
        self.hMinLabel = QLabel("Min:")
        self.hMinTextBox = QLineEdit()
        self.hMinTextBox.setText("-1")
        self.hMaxLabel = QLabel("Max:")
        self.hMaxTextBox = QLineEdit()
        self.hMaxTextBox.setText("-1")
        self.heightRangeLabel.setToolTip("Select height range of labelled box in pixels")
        self.hMinLabel.setToolTip("Select minimum height range of labelled box in pixels")
        self.hMinTextBox.setToolTip("Select minimum height range of labelled box in pixels")
        self.hMaxLabel.setToolTip("Select maximum height range of labelled box in pixels")
        self.hMaxTextBox.setToolTip("Select maximum height range of labelled box in pixels")

        # aspect range
        self.aspectRangeLabel = QLabel("Aspect Range")
        self.aspectLabel = QLabel("Asp.:")
        self.aspectTextBox = QLineEdit()
        self.aspectTextBox.setText("-1")
        self.deviationLabel = QLabel("Dev.:")
        self.deviationTextBox = QLineEdit()
        self.deviationTextBox.setText("0")
        self.aspectRangeLabel.setToolTip("Select aspect range of labelled box")
        self.aspectTextBox.setToolTip("Select aspect range of labelled box")
        self.deviationLabel.setToolTip("Select deviation of aspect range")
        self.deviationTextBox.setToolTip("Select deviation of aspect range")

        # segmentation
        self.segmantaionCheckBox = QCheckBox("Segmentation", self)
        self.segmantaionCheckBox.setToolTip("Check to use segmentation")

        self.toolbarWidget = QWidget()
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.inputButton,0,0,1,1)
        self.gridLayout.addWidget(self.inputTextBox, 0, 1, 1, 3)
        self.gridLayout.addWidget(self.headlessCheckBox,1,0,1,2)
        self.gridLayout.addWidget(self.cudaCheckBox, 1, 2, 1, 2)
        self.gridLayout.addWidget(self.solidBgCheckBox, 3, 0, 1, 4)
        self.gridLayout.addWidget(self.segmantaionCheckBox, 4, 0, 1, 4)
        self.gridLayout.addWidget(self.processingSizeLabel,5,0,1,2)
        self.gridLayout.addWidget(self.hSize,5,2,1,1)
        self.gridLayout.addWidget(self.wSize,5,3,1,1)
        #self.gridLayout.addWidget(self.zoneLabel,6,0,1,1)
        #self.gridLayout.addWidget(self.zoneInputTextBox,6,1,1,3)
        self.gridLayout.addWidget(self.bgInputButton,8,0,1,2)
        self.gridLayout.addWidget(self.bgInputTextBox,8,2,1,2)
        self.gridLayout.addWidget(self.datasetInputButton,9,0,1,2)
        self.gridLayout.addWidget(self.datasetInputTextBox,9,2,1,2)
        self.gridLayout.addWidget(self.prefixlabel,10,0,1,1)
        self.gridLayout.addWidget(self.prefixTextBox,10,1,1,3)
        self.gridLayout.addWidget(self.bgIntervalLabel,11,0,1,2)
        self.gridLayout.addWidget(self.bgIntervalTextBox,11,2,1,2)
        self.gridLayout.addWidget(self.classIndiceLabel,12,0,1,2)
        self.gridLayout.addWidget(self.classIndiceTextBox,12,2,1,2)
        self.gridLayout.addWidget(self.indiceFilterLabel,13,0,1,2)
        self.gridLayout.addWidget(self.indiceFilterTextBox,13,2,1,2)
        self.gridLayout.addWidget(self.processEveryNthFramesLabel,14,0,1,3)
        self.gridLayout.addWidget(self.processEveryNthFramesTextBox,14,3,1,1)
        self.gridLayout.addWidget(self.detectionThresholdLabel,15,0,1,3)
        self.gridLayout.addWidget(self.detectionThresholdTextBox,15,3,1,1)
        self.gridLayout.addWidget(self.intersectionThresholdLabel,16,0,1,3)
        self.gridLayout.addWidget(self.intersectionThresholdTextBox,16,3,1,1)
        self.gridLayout.addWidget(self.widthRangeLabel,17,0,1,4,Qt.AlignCenter)
        self.gridLayout.addWidget(self.wMinLabel,18,0,1,1)
        self.gridLayout.addWidget(self.wMinTextBox,18,1,1,1)
        self.gridLayout.addWidget(self.wMaxLabel,18,2,1,1)
        self.gridLayout.addWidget(self.wMaxTextBox,18,3,1,1)
        self.gridLayout.addWidget(self.heightRangeLabel,19,0,1,4,Qt.AlignCenter)
        self.gridLayout.addWidget(self.hMinLabel,20,0,1,1)
        self.gridLayout.addWidget(self.hMinTextBox,20,1,1,1)
        self.gridLayout.addWidget(self.hMaxLabel,20,2,1,1)
        self.gridLayout.addWidget(self.hMaxTextBox,20,3,1,1)
        self.gridLayout.addWidget(self.aspectRangeLabel,21,0,1,4,Qt.AlignCenter)
        self.gridLayout.addWidget(self.aspectLabel,22,0,1,1)
        self.gridLayout.addWidget(self.aspectTextBox,22,1,1,1)
        self.gridLayout.addWidget(self.deviationLabel,22,2,1,1)
        self.gridLayout.addWidget(self.deviationTextBox,22,3,1,1)
        self.toolbarWidget.setLayout(self.gridLayout)
        self.addWidget(self.toolbarWidget)

class PSLBottomToolBar(QToolBar):
    def __init__(self):
        QToolBar.__init__(self)
        self.setOrientation(QtCore.Qt.Vertical)
        self.setMovable(False)
        self.addSeparator()

        self.drawZonesButton=QPushButton()
        self.drawZonesButton.setText("Draw Zones")
        self.drawZonesButton.clicked.emit()

        self.nextPolyButton = QPushButton()
        self.nextPolyButton.setText("Next Zone")
        self.nextPolyButton.clicked.emit()

        self.prePolyButton = QPushButton()
        self.prePolyButton.setText("Previous Zone")
        self.prePolyButton.clicked.emit()

        self.deleteZonesButton=QPushButton()
        self.deleteZonesButton.setText("Delete Zones")
        self.deleteZonesButton.clicked.emit()

        self.startProcessButton = QPushButton()
        self.startProcessButton.setText("Start PseudoLabelling")
        self.startProcessButton.clicked.emit()

        self.stopProcessButton=QPushButton()
        self.stopProcessButton.setText("Stop PseudoLabelling")
        self.stopProcessButton.clicked.emit()

        self.addWidget(self.drawZonesButton)
        self.addWidget(self.nextPolyButton)
        self.addWidget(self.prePolyButton)
        self.addWidget(self.deleteZonesButton)
        self.addWidget(self.startProcessButton)
        self.addWidget(self.stopProcessButton)

class MainWindow(QMainWindow):
    def __init__(self,view):
        QMainWindow.__init__(self)
        self.setWindowTitle("YoloMarkerApp")
        self.applyTemplateEnabled=False
        self.createTemplateEnabled=False
        self.lastChoosenIdExist=False
        self.lastChoosenPathExists=False
        self.advancedMode=False
        self.markerMode=True

        #Error Message
        self.errorMessage=QErrorMessage()

        #Getting the screenSize of the Computer
        sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.screenWidth=sizeObject.width()
        self.screenHeight=sizeObject.height()

        #QGraphicsScene
        self.scene = Scene()
        self.setMouseTracking(True)

        #QGraphicsView
        self.view=view
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        #Signals
        self.view.createdRectPositionSignal.connect(self.createdRectPositionSlot)
        self.view.movedRectPositionSignal.connect(self.movedRectPositionSlot)
        self.view.resizedRectPositionalSignal.connect(self.resizedRectPositionalSlot)
        self.view.enableIdInputOfCreatedRectSignal.connect(self.enableIdInputOfCreatedRectSlot)
        self.view.jumpToCreateRectAppSinal.connect(self.createAction)
        self.view.itemSelectionChangedSignal.connect(self.itemSelectionChangedSlot)
        self.view.mousePressedOnNoItemSignal.connect(self.mousePressedOnNoItemSlot)
        self.view.setUpWindowSignal.connect(self.setUpWindow)

        # Menu
        self.menu = QMenuBar()  #qdarkstyle does no support QmenuBar
        self.menuHeight=24
        self.menu.setFixedHeight(self.menuHeight)
        self.fileMenu = self.menu.addMenu("File")
        self.editMenu = self.menu.addMenu("Edit")
        self.viewMenu = self.menu.addMenu("View")
        self.modeMenu = self.menu.addMenu("Mode")
        #self.setMenuBar(self.menu)

        # upper tool bar Menu Bar
        self.upperToolBar=QToolBar()
        self.upperToolBar.setMovable(False)
        self.upperToolBar.setOrientation(QtCore.Qt.Horizontal)
        self.fileMenu = QMenu(self)
        self.editMenu = QMenu(self)
        self.viewMenu = QMenu(self)
        self.markerModeMenu = QMenu(self)
        self.pslModeMenu = QMenu(self)
        self.upperToolBar.addWidget(self.fileMenu)
        self.upperToolBar.addSeparator()
        self.upperToolBar.addWidget(self.editMenu)
        self.upperToolBar.addSeparator()
        self.upperToolBar.addWidget(self.viewMenu)
        self.upperToolBar.addSeparator()
        self.upperToolBar.addWidget(self.markerModeMenu)
        self.upperToolBar.addSeparator()
        self.upperToolBar.addWidget(self.pslModeMenu)
        self.addToolBar(Qt.TopToolBarArea, self.upperToolBar)

        # Exit QAction
        self.exitAction = QAction("Exit", self)
       # self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.triggered.connect(self.exitActionFunc)
        self.fileMenu.addAction(self.exitAction)

        #Edit Classes.txt QAction
        self.editClassesTxtAction=QAction("Edit classes.txt", self)
        self.editClassesTxtAction.triggered.connect(self.editClassesTxtActionFunc)
        self.editMenu.addAction(self.editClassesTxtAction)

        # Advanced Mode QAction
        self.advancedModeAction = QAction("Advanced Mode", self)
        self.advancedModeAction.setCheckable(True)
      #  self.advancedModeAction.setShortcut("Ctrl+A")
        self.advancedModeAction.triggered.connect(self.advancedModeActionFunc)
        self.viewMenu.addAction(self.advancedModeAction)

        # Select Marker/PseudoLabeller Mode QAction
        self.markerModeAction = QAction("Marker Mode", self)
        self.markerModeAction.setEnabled(False)
        self.markerModeAction.triggered.connect(self.markerModeActionFunc)
        self.markerModeMenu.addAction(self.markerModeAction)

        self.pseudoLabellerModeAction = QAction("PseudoLabeller Mode", self)
        self.pseudoLabellerModeAction.triggered.connect(self.pseudoLabellerModeActionFunc)
        self.pslModeMenu.addAction(self.pseudoLabellerModeAction)

        #LeftToolBar
        self.leftToolBar=LeftToolBar()
        self.addToolBar(Qt.LeftToolBarArea, self.leftToolBar)

        # RightToolBar
        self.rightToolBar = RightToolBar()
        self.addToolBar(Qt.RightToolBarArea, self.rightToolBar)
        self.rightToolBar.checkListWidget.itemDoubleClicked.connect(self.editAction)

        #dockWİdget
        self.qdock = QDockWidget()
        self.qdock.setWindowFlags(Qt.FramelessWindowHint)
        self.qdock.hide()

        # Signals
        self.leftToolBar.openAction.triggered.connect(self.openAction)
        self.leftToolBar.openDirAction.triggered.connect(self.openDirAction)
        self.leftToolBar.deleteImgAction.triggered.connect(self.deleteImgAction)
        self.leftToolBar.nextAction.triggered.connect(self.nextAction)
        self.leftToolBar.previousAction.triggered.connect(self.previousAction)
        self.leftToolBar.createAction.triggered.connect(self.createAction)
        self.leftToolBar.editAction.triggered.connect(self.editAction)
        self.leftToolBar.deleteAction.triggered.connect(self.deleteAction)
        self.leftToolBar.duplicateAction.triggered.connect(self.duplicateAction)
        self.leftToolBar.showStatisticsAction.triggered.connect(self.showStatisticsAction)
        self.rightToolBar.paintAction.clicked.connect(self.paintAction)
        self.rightToolBar.applyPaintAction.clicked.connect(self.applyPaintAction)
        self.rightToolBar.cancelPaintAction.clicked.connect(self.cancelPaintAction)
        self.rightToolBar.createTemplateAction.clicked.connect(self.createTemplateAction)
        self.rightToolBar.applyTemplateAction.clicked.connect(self.applyTemplateAction)
        self.rightToolBar.cancelTemplateAction.clicked.connect(self.cancelTemplateAction)
        self.rightToolBar.checkListWidget.currentRowChanged.connect(self.checkListWidgetRowChanged)
        self.rightToolBar.fileListWidget.currentRowChanged.connect(self.fileListWidgetRowChaged)

    def markerModeActionFunc(self):
        if self.markerMode==False:
            self.pslLeftToolBar.hide()
            self.pslBottomToolBar.hide()
            self.advancedModeAction.setEnabled(True)
            self.editClassesTxtAction.setEnabled(True)
            self.markerModeAction.setEnabled(False)
            self.pseudoLabellerModeAction.setEnabled(True)
            self.qdock.hide()
            self.rightToolBar.show()
            self.leftToolBar.show()
            self.view.show()
            self.setCentralWidget(self.view)
            self.addToolBar(Qt.LeftToolBarArea, self.pslLeftToolBar)
            self.markerMode=True

                                                  #Psl Functions
    def pseudoLabellerModeActionFunc(self):
        if self.markerMode==True:
            self.processEnabled = True
            self.rightToolBar.hide()
            self.leftToolBar.hide()
            self.advancedModeAction.setEnabled(False)
            self.editClassesTxtAction.setEnabled(False)
            self.markerModeAction.setEnabled(True)
            self.pseudoLabellerModeAction.setEnabled(False)
            self.view.hide()
            self.pslLeftToolBar = PSLLeftToolBar()
            self.addToolBar(Qt.LeftToolBarArea, self.pslLeftToolBar)
            self.pslBottomToolBar = PSLBottomToolBar()
            self.addToolBar(Qt.BottomToolBarArea, self.pslBottomToolBar)
            self.pslScene = QGraphicsScene()
            self.pslView = PSLGraphicsView(self.pslScene)
            self.qdock.setWidget(self.pslView)
            self.qdock.show()
            self.addDockWidget(Qt.TopDockWidgetArea, self.qdock)
            self.pslLeftToolBar.inputButton.clicked.connect(self.inputButtonClicked)
            self.pslLeftToolBar.datasetInputButton.clicked.connect(self.datasetInputButtonClicked)
            self.pslLeftToolBar.bgInputButton.clicked.connect(self.bgInputButtonClicked)
            self.pslBottomToolBar.drawZonesButton.clicked.connect(self.drawZonesButtonClicked)
            self.pslView.polygonPointsSignal.connect(self.polygonPointsSlot)
            self.pslBottomToolBar.nextPolyButton.clicked.connect(self.nextPolyButtonClicked)
            self.pslBottomToolBar.prePolyButton.clicked.connect(self.previousPolyButtonClicked)
            self.pslBottomToolBar.deleteZonesButton.clicked.connect(self.deleteZonesButtonClicked)
            self.pslBottomToolBar.startProcessButton.clicked.connect(self.startProcessButtonClicked)
            self.pslBottomToolBar.stopProcessButton.clicked.connect(self.stopProcessButtonClicked)
            self.roiPoints = []
            self.markerMode = False

    def inputButtonClicked(self):
        self.entrancePath = "/home/"
        self.input = QFileDialog.getOpenFileName(self, "Input Video", self.entrancePath, "*.mp4")
        self.pslLeftToolBar.inputTextBox.setText(self.input[0])

    def bgInputButtonClicked(self):
        self.entrancePath = "/home"
        self.bgPath = QFileDialog.getOpenFileName(self, "Input Background", self.entrancePath, "*.jpg *.png *.xpm")
        self.pslLeftToolBar.bgInputTextBox.setText(self.bgPath[0])

    def datasetInputButtonClicked(self):
        self.entrancePath = "/home/"
        self.dirName = QFileDialog.getExistingDirectory(self, "Dataset Directory", self.entrancePath,
                                                        QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        print(self.dirName)
        self.pslLeftToolBar.datasetInputTextBox.setText(self.dirName)

    def startProcessButtonClicked(self):
        if self.pslLeftToolBar.datasetInputTextBox.text():
            self.processEnabled = True
            self.pslView.drawingPolygonEnabled = False
            self.PseudoLabellerProcess()
        else:
            self.errorMessage.showMessage("Select dataset path")

    def stopProcessButtonClicked(self):
        self.processEnabled = False

    def drawZonesButtonClicked(self):
        self.processingSize = (1280, 720)
        if self.pslLeftToolBar.inputTextBox.text():
            self.cap = cv2.VideoCapture(self.pslLeftToolBar.inputTextBox.text())
            if not self.pslLeftToolBar.zoneInputTextBox.text():
                ret, frame = self.cap.read()
                while not ret:
                    print("Retrying frame grabbing")
                    ret, frame = self.cap.read()
                frame = cv2.resize(frame, self.processingSize)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                                 QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(convertToQtFormat)
                self.pslScene.addPixmap(pixmap)
                self.pslView.drawingPolygonEnabled = True
                self.zoneIndex=0
            else:
                roiPoints = []
                currentZoneList = []
                currentPointPairs = []
                currentCoordinate = ""
                zones = self.pslLeftToolBar.zoneInputTextBox.text().split(" ")
                zones.append("|")
                for pairs in zones:
                    for i in range(len(pairs)):
                        digit = pairs[i]
                        if digit == "|":
                            self.roiPoints.append(currentZoneList)
                            currentZoneList = []
                            currentPointPairs = []
                            currentCoordinate = ""
                            continue
                        elif digit == ",":
                            currentPointPairs.append(int(currentCoordinate))
                            currentCoordinate = ""
                        else:
                            currentCoordinate += (digit)
                        if i == len(pairs) - 1:
                            currentPointPairs.append(int(currentCoordinate))
                            currentZoneList.append(currentPointPairs)
                            currentPointPairs = []
                            currentCoordinate = ""
                self.PseudoLabellerProcess()
        else:
            self.errorMessage.showMessage("Select input video path")
        self.zonePoints=[]
        self.roiPoints.append(self.zonePoints)
        print (self.roiPoints)

    def polygonPointsSlot(self,x,y):
        self.point=[]
        self.point.append(x)
        self.point.append(y)
        self.zonePoints=self.roiPoints[self.zoneIndex]
        self.zonePoints.append(self.point)
        self.roiPoints[self.zoneIndex] = self.zonePoints

    def nextPolyButtonClicked(self):
        del self.zonePoints[:]
        self.roiPoints.append(self.zonePoints)
        del self.pslView.polygon[:]
        self.pslView.polygonArray.append(self.pslView.polygon)
        print (self.pslView.polygonArray)
        self.zoneIndex +=1
        self.pslView.polygonIndex +=1

    def previousPolyButtonClicked(self):
        if self.zoneIndex>0:
            self.zoneIndex -= 1
        if self.pslView.polygonIndex>0:
            self.pslView.polygonIndex -=1

    def deleteZonesButtonClicked(self):
        self.zonePoints = []
        self.roiPoints = []
        self.pslView.deletePolygons()

    def PseudoLabellerProcess(self):

        global useCuda
        global model
        global processingSize
        useCuda = self.pslLeftToolBar.cudaCheckBox.isChecked()
        if useCuda:
            import pycuda.driver as cuda
            cuda.init()
            # print(pytorch.cuda.get_device_name(0))
            model = pytorch.models.detection.maskrcnn_resnet50_fpn(pretrained=True).cuda()
        else:
            model = pytorch.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
        model.eval()

        self.widthRange = (int(self.pslLeftToolBar.wMinTextBox.text()),int(self.pslLeftToolBar.wMaxTextBox.text()))
        self.heightRange = (int(self.pslLeftToolBar.hMinTextBox.text()),int(self.pslLeftToolBar.hMaxTextBox.text()))
        self.aspectAndDelta = (int(self.pslLeftToolBar.aspectTextBox.text()),int(self.pslLeftToolBar.deviationTextBox.text()))
        self.intersectionThreshold = float(self.pslLeftToolBar.intersectionThresholdTextBox.text())
        if self.pslLeftToolBar.solidBgCheckBox.isChecked():
            self.backgroundPath = "solid"
        else:
            self.backgroundPath=self.pslLeftToolBar.bgInputTextBox.text()
        if self.pslLeftToolBar.prefixTextBox.text():
            self.datasetPath = self.pslLeftToolBar.datasetInputTextBox.text()+"/"+self.pslLeftToolBar.prefixTextBox.text()
        else:
            self.datasetPath = self.pslLeftToolBar.datasetInputText.text()+"/""prefix-"
        self.threshold = float(self.pslLeftToolBar.detectionThresholdTextBox.text())
        self.frameDropInterval = int(self.pslLeftToolBar.processEveryNthFramesTextBox.text())
        self.segmentation=self.pslLeftToolBar.segmantaionCheckBox.isChecked()
        self.headless=self.pslLeftToolBar.headlessCheckBox.isChecked()
        PseudoLabeller.bgSubtractionInterval=int(self.pslLeftToolBar.bgIntervalTextBox.text())
        PseudoLabeller.datasetClassIndice=int(self.pslLeftToolBar.classIndiceTextBox.text())
        processingSize=(int(self.pslLeftToolBar.hSize.text()), int(self.pslLeftToolBar.wSize.text()))
        PseudoLabeller.filterClassIndices=[]
        if self.pslLeftToolBar.indiceFilterTextBox.text():
            PseudoLabeller.filterClassIndices = [int(x) for x in
                                                 self.pslLeftToolBar.indiceFilterTextBox.text().split(",")]

        labeller = PseudoLabeller(self.widthRange, self.heightRange, self.roiPoints, self.threshold, self.aspectAndDelta, self.intersectionThreshold,self.datasetPath, self.backgroundPath, self.segmentation)
        frameOrder = 0
        frameDropInterval =int(self.pslLeftToolBar.processEveryNthFramesTextBox.text())

        if self.cap.isOpened():
            ret, frame = self.cap.read()
            shouldWeRunFrameDropping = True
            while self.processEnabled==True:
                if ret:
                    frame = cv.resize(frame, processingSize)
                    frameOrder += 1
                    if (frameOrder > frameDropInterval and (
                            frameOrder % frameDropInterval) == 0) or not shouldWeRunFrameDropping:
                        before = datetime.datetime.now()
                        result, shouldWeRunFrameDropping = labeller.segment(frame, frameOrder)
                        after = datetime.datetime.now()
                        print(str((after - before).microseconds / 1e6) + " seconds spent in frame: " + str(frameOrder))
                        if not self.headless:
                            cv.imshow('actual camera', frame)
                            cv.imshow('process output', result)
                    if cv.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    self.cap.release()
                    self.cap = cv2.VideoCapture(self.pslLeftToolBar.inputTextBox.text())
                ret, frame = self.cap.read()
        cv.waitKey(0)
        self.cap.release()
        cv.destroyAllWindows()

                                                        #LeftToolBar Actions Definitions
    def openAction(self, checked):
        print("openAction")
        self.files = []
        self.rightToolBar.fileListWidget.clear()
        self.currentFileListIndex = 0
        self.currentCheckListIndex = 0
        # /home/ahmet/QT_projeler/frameWork/test
        if (self.lastChoosenPathExists == True):
            self.entrancePath = self.lastChoosenPath
        else:
            self.entrancePath = "/home/"
        file = QFileDialog.getOpenFileName(self, "Open Image", self.entrancePath, "*.jpg")  # (returns tuple)
        self.files.append(file[0])
        self.dirName = self.files[0].split("/")
        del self.dirName[-1]
        self.dirName = "/".join(self.dirName)
        self.classes = self.readClassesTxt()
        self.rightToolBar.fileListWidget.clear()
        self.rightToolBar.fileListWidget.addItem(self.files[0])
      #  self.rightToolBar.fileListWidget.sortItems(Qt.AscendingOrder)
        self.rightToolBar.fileListWidget.setCurrentRow(self.currentFileListIndex)
        self.setUpWindow()
        self.leftToolBar.editAction.setEnabled(False)
        self.leftToolBar.deleteAction.setEnabled(False)
        self.leftToolBar.duplicateAction.setEnabled(False)
        self.leftToolBar.nextAction.setEnabled(True)
        self.leftToolBar.previousAction.setEnabled(True)
        self.leftToolBar.createAction.setEnabled(True)
        self.leftToolBar.deleteImgAction.setEnabled(True)
        self.leftToolBar.showStatisticsAction.setEnabled(True)
        self.rightToolBar.paintAction.setEnabled(True)
        self.rightToolBar.createTemplateAction.setEnabled(True)
        if ((self.advancedMode == True) & (self.view.drawRect == True)):
            self.leftToolBar.createAction(True)

    def openDirAction(self, checked):
        print("opendir app")
        # /home/ahmet/QT_projeler/frameWork/test
        if (self.lastChoosenPathExists == True):
            self.entrancePath = self.lastChoosenPath
        else:
            self.entrancePath = "/home/"
        self.dirName = QFileDialog.getExistingDirectory(self, "Open Directory", self.entrancePath,
                                                        QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.classes = self.readClassesTxt()
        self.lastChoosenPath = self.dirName
        self.lastChoosenPathExists = True
        self.path = self.dirName
        self.files = []
        self.file_name = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(self.path):
            for file in f:
                if '.jpg' in file:
                    self.files.append(os.path.join(r, file))
                    self.file_name.append(file)
        self.rightToolBar.fileListWidget.clear()
        for x in self.files:
            self.rightToolBar.fileListWidget.addItem(x)
        self.rightToolBar.fileListWidget.sortItems(Qt.AscendingOrder)
        self.createTraintTxt()
        self.currentFileListIndex = 0
        self.currentCheckListIndex = 0
        self.rightToolBar.fileListWidget.setCurrentRow(self.currentFileListIndex)
        if self.files:
            self.view.netZoomFactor = 1
            self.setUpWindow()
            self.leftToolBar.editAction.setEnabled(False)
            self.leftToolBar.deleteAction.setEnabled(False)
            self.leftToolBar.duplicateAction.setEnabled(False)
            self.leftToolBar.nextAction.setEnabled(True)
            self.leftToolBar.previousAction.setEnabled(True)
            self.leftToolBar.createAction.setEnabled(True)
            self.leftToolBar.deleteImgAction.setEnabled(True)
            self.leftToolBar.showStatisticsAction.setEnabled(True)
            self.rightToolBar.paintAction.setEnabled(True)
            self.rightToolBar.createTemplateAction.setEnabled(True)
            if ((self.advancedMode == True) & (self.view.drawRect == True)):
                self.leftToolBar.createAction(True)

    def deleteImgAction(self, checked):
        print("deleteImgAction")
        msgBox = QMessageBox()
        msgBox.setInformativeText("Do you want to delete this image?")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.Yes)
        ret = msgBox.exec_()
        if (ret == QMessageBox.Yes):
            print(self.currentFileListIndex)
            deleteImgPath = self.rightToolBar.fileListWidget.item(self.currentFileListIndex).text()
            tempIndex=self.currentFileListIndex
            deleteTxtPath = deleteImgPath[:-3] + "txt"
            if os.path.exists(deleteImgPath):
                os.remove(deleteImgPath)
            if os.path.exists(deleteTxtPath):
                os.remove(deleteTxtPath)
            self.rightToolBar.fileListWidget.clear()
            self.path = self.dirName
            self.files = []
            self.file_name = []
            # r=root, d=directories, f = files
            for r, d, f in os.walk(self.path):
                for file in f:
                    if '.jpg' in file:
                        self.files.append(os.path.join(r, file))
                        self.file_name.append(file)
            for x in self.files:
                self.rightToolBar.fileListWidget.addItem(x)
            self.rightToolBar.fileListWidget.sortItems(Qt.AscendingOrder)
            self.createTraintTxt()
            self.currentCheckListIndex = 0
            print (self.currentFileListIndex)
            self.rightToolBar.fileListWidget.setCurrentRow(tempIndex)
            if self.files:
                self.view.netZoomFactor = 1
                self.setUpWindow()
                self.leftToolBar.editAction.setEnabled(False)
                self.leftToolBar.deleteAction.setEnabled(False)
                self.leftToolBar.duplicateAction.setEnabled(False)
                self.leftToolBar.nextAction.setEnabled(True)
                self.leftToolBar.previousAction.setEnabled(True)
                self.leftToolBar.createAction.setEnabled(True)
                self.leftToolBar.deleteImgAction.setEnabled(True)
                self.rightToolBar.paintAction.setEnabled(True)
                self.rightToolBar.createTemplateAction.setEnabled(True)

    @Slot()
    def nextAction(self, checked):
        print("next app")
        if self.currentFileListIndex < len(self.files) - 1:
            self.currentFileListIndex = self.currentFileListIndex + 1
            self.rightToolBar.fileListWidget.setCurrentRow(self.currentFileListIndex)
            if self.files:
                self.currentCheckListIndex = 0
                self.view.netZoomFactor = 1
                self.setUpWindow()
                self.leftToolBar.editAction.setEnabled(False)
                self.leftToolBar.deleteAction.setEnabled(False)
                self.leftToolBar.duplicateAction.setEnabled(False)
                self.leftToolBar.createAction.setEnabled(True)
                self.leftToolBar.deleteImgAction.setEnabled(True)
                if self.view.drawRect == True:
                    self.file_txt = open(self.txt_path, "r")
                    print ("next used path")
                    print (self.txt_path)
                    self.txtContentForDrawing = self.file_txt.readlines()
                    self.txtContentForDrawing.append(" ")
                    self.rowIndexOfTxt = len(self.txtContentForDrawing)
                    self.file_txt.close()
                    if (self.advancedMode == True):
                        self.leftToolBar.createAction(True)


    @Slot()
    def previousAction(self, checked):
        print("pre app")
        if self.currentFileListIndex > 0:
            self.currentFileListIndex = self.currentFileListIndex - 1
            self.rightToolBar.fileListWidget.setCurrentRow(self.currentFileListIndex)
            if self.files:
                self.currentCheckListIndex = 0
                self.view.netZoomFactor = 1
                self.setUpWindow()
                self.leftToolBar.editAction.setEnabled(False)
                self.leftToolBar.deleteAction.setEnabled(False)
                self.leftToolBar.duplicateAction.setEnabled(False)
                self.leftToolBar.createAction.setEnabled(True)
                self.leftToolBar.deleteImgAction.setEnabled(True)
                if self.view.drawRect == True:
                    self.file_txt = open(self.txt_path, "r")
                    self.txtContentForDrawing = self.file_txt.readlines()
                    self.txtContentForDrawing.append(" ")
                    self.rowIndexOfTxt = len(self.txtContentForDrawing)
                    self.file_txt.close()
                    if (self.advancedMode == True):
                        self.leftToolBar.createAction(True)


    @Slot()
    def editAction(self, checked):
        print("editAction")
        self.editWindow = EditWindow()
        self.editWindow.readClassesTxt(self.dirName)
        if (self.lastChoosenIdExist == True):
            self.editWindow.setLastChoosenId(self.lastChoosenId)
        self.editWindow.updateIdSignal.connect(self.updateIdSlot)
        self.editWindow.exec_()
        self.leftToolBar.editAction.setEnabled(True)
        self.leftToolBar.deleteAction.setEnabled(True)
        self.leftToolBar.duplicateAction.setEnabled(True)
        self.leftToolBar.createAction.setEnabled(False)
        self.leftToolBar.deleteImgAction.setEnabled(False)

    @Slot()
    def deleteAction(self, checked):
        print("deleteAction")
        content = []
        self.file_txt = open(self.txt_path, "r")
        content = self.file_txt.readlines()
        self.file_txt.close()
        del content[self.currentCheckListIndex]
        self.file_txt = open(self.txt_path, "w")
        self.file_txt.writelines(content)
        self.file_txt.close()
        self.setUpWindow()
        self.view.scale(self.view.netZoomFactor, self.view.netZoomFactor)
        self.view.viewSettingsChanged()
        self.leftToolBar.editAction.setEnabled(True)
        self.leftToolBar.deleteAction.setEnabled(True)
        self.leftToolBar.duplicateAction.setEnabled(True)
        self.leftToolBar.createAction.setEnabled(False)
        self.leftToolBar.deleteImgAction.setEnabled(False)

    @Slot()
    def createAction(self, checked):
        print("createAction")

        lineItem1 = QGraphicsLineItem()
        lineItem2 = QGraphicsLineItem()
        self.scene.addItem(lineItem1)
        self.scene.addItem(lineItem2)

        tempItem = QGraphicsRectItem()
        tempItem.setBrush(QBrush(QtCore.Qt.transparent, style=QtCore.Qt.BDiagPattern))
        tempItem.setPen(QtGui.QPen(QtCore.Qt.red, self.rectThickness))
        tempItem.setOpacity(0.3)

        self.scene.addItem(tempItem)
        print (self.txt_path)
        self.file_txt = open(self.txt_path, "r")
        self.txtContentForDrawing = self.file_txt.readlines()
        self.txtContentForDrawing.append(" ")
        self.rowIndexOfTxt = len(self.txtContentForDrawing)
        self.file_txt.close()
        self.view.viewSettingsChanged()
        self.view.drawRect = True
        self.currentCheckListIndex = self.rectCounter
        item = QtWidgets.QListWidgetItem()
        item.setText("")
        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Checked)
        self.rightToolBar.checkListWidget.addItem(item)
        self.rightToolBar.checkListWidget.setCurrentRow(self.currentCheckListIndex)
        self.leftToolBar.editAction.setEnabled(False)
        self.leftToolBar.deleteAction.setEnabled(False)
        self.leftToolBar.createAction.setEnabled(False)
        self.leftToolBar.deleteImgAction.setEnabled(False)
        self.leftToolBar.duplicateAction.setEnabled(False)

    @Slot()
    def duplicateAction(self, checked):
        print("duplicateAction")
        content = []
        self.file_txt = open(self.txt_path, "r")
        content = self.file_txt.readlines()
        self.file_txt.close()
        duplicatedRect = content[self.currentCheckListIndex]
        list = duplicatedRect.split(" ")
        if ((float(list[1]) - float(list[3]) / 2) > 0.02):  # shift duplicatedRect
            list[1] = str(float(list[1]) - 0.01)
        else:
            list[1] = str(float(list[1]) + 0.01)
        if ((float(list[2]) - float(list[4]) / 2) > 0.02):  # shift duplicatedRect
            list[2] = str(float(list[2]) - 0.01)
        else:
            list[2] = str(float(list[2]) + 0.01)
        duplicatedRect = " ".join(list)
        content.append(duplicatedRect)
        self.file_txt = open(self.txt_path, "w")
        self.file_txt.writelines(content)
        self.file_txt.close()
        self.setUpWindow()
        self.view.scale(self.view.netZoomFactor, self.view.netZoomFactor)
        self.view.viewSettingsChanged()
        self.leftToolBar.editAction.setEnabled(True)
        self.leftToolBar.deleteAction.setEnabled(True)
        self.leftToolBar.duplicateAction.setEnabled(True)
        self.leftToolBar.createAction.setEnabled(False)
        self.leftToolBar.deleteImgAction.setEnabled(False)

    @Slot()
    def showStatisticsAction(self, checked):
        print("showStatisticsAction")
        classesList = self.readClassesTxt()
        numberOfClassesList = [0] * len(classesList)
        totalNumberOfClasses = 0
        for index in range(self.rightToolBar.fileListWidget.count()):
            txtPath = self.rightToolBar.fileListWidget.item(index).text()[:-4] + ".txt"
            txtFile = open(txtPath, 'r')
            content = txtFile.readlines()
            for x in content:
                classValue = int(x.split()[0])
                for index in range(len(classesList)):
                    if (classValue == index):
                        numberOfClassesList[index] = numberOfClassesList[index] + 1
                        totalNumberOfClasses = totalNumberOfClasses + 1
        messageBoxContent = ""
        for index in range(len(classesList)):
            messageBoxContent = messageBoxContent + classesList[index][:-1] + "=" + str(
                numberOfClassesList[index]) + "\n"
        messageBoxContent = messageBoxContent + "Total=" + str(totalNumberOfClasses)
        self.messageBox = QMessageBox()
        self.messageBox.setText(messageBoxContent)
        self.messageBox.exec_()

                                                            #Right toolbar actions definitions
    @Slot()
    def paintAction(self, checked):
        print("painting enabled")
        self.copyOfPicture = self.picture
        self.selectPainterSizeWindow = SelectPainterSizeWindow()
        self.selectPainterSizeWindow.painterSizeSignal.connect(self.view.painterSizeSlot)
        self.selectPainterSizeWindow.exec_()

        if (self.view.paintingEnabled == True):
            self.rightToolBar.applyPaintAction.setEnabled(True)
            self.rightToolBar.cancelPaintAction.setEnabled(True)
            self.rightToolBar.paintAction.setEnabled(False)
            self.rightToolBar.createTemplateAction.setEnabled(False)
            self.leftToolBar.openAction.setEnabled(False)
            self.leftToolBar.openDirAction.setEnabled(False)
            self.leftToolBar.deleteImgAction.setEnabled(False)
            self.leftToolBar.nextAction.setEnabled(False)
            self.leftToolBar.previousAction.setEnabled(False)
            self.leftToolBar.editAction.setEnabled(False)
            self.leftToolBar.deleteAction.setEnabled(False)
            self.leftToolBar.createAction.setEnabled(False)
            self.leftToolBar.duplicateAction.setEnabled(False)

    @Slot()
    def applyPaintAction(self, checked):
        self.view.paintingEnabled = False
        print("enabled false")
        self.view.netZoomFactor = 1
        self.setUpWindow()
        self.rightToolBar.paintAction.setEnabled(True)
        self.rightToolBar.applyPaintAction.setEnabled(False)
        self.rightToolBar.cancelPaintAction.setEnabled(False)
        self.rightToolBar.createTemplateAction.setEnabled(True)
        self.leftToolBar.openAction.setEnabled(True)
        self.leftToolBar.openDirAction.setEnabled(True)
        self.leftToolBar.nextAction.setEnabled(True)
        self.leftToolBar.previousAction.setEnabled(True)
        self.leftToolBar.editAction.setEnabled(False)
        self.leftToolBar.createAction.setEnabled(False)
        self.leftToolBar.deleteAction.setEnabled(False)
        self.leftToolBar.duplicateAction.setEnabled(False)

    @Slot()
    def cancelPaintAction(self, clicked):
        print("cancel paint")
        self.scene.addNewPixmap(self.copyOfPicture)
        self.copyOfPicture.save(self.rightToolBar.fileListWidget.item(self.currentFileListIndex).text(), "JPG")
        self.view.netZoomFactor = 1
        self.setUpWindow()
        self.view.paintingEnabled = False
        self.rightToolBar.paintAction.setEnabled(True)
        self.rightToolBar.applyPaintAction.setEnabled(False)
        self.rightToolBar.cancelPaintAction.setEnabled(False)
        self.rightToolBar.createTemplateAction.setEnabled(True)
        self.leftToolBar.openAction.setEnabled(True)
        self.leftToolBar.openDirAction.setEnabled(True)
        self.leftToolBar.nextAction.setEnabled(True)
        self.leftToolBar.previousAction.setEnabled(True)
        self.leftToolBar.createAction.setEnabled(True)
        self.leftToolBar.editAction.setEnabled(False)
        self.leftToolBar.deleteAction.setEnabled(False)
        self.leftToolBar.duplicateAction.setEnabled(False)

    @Slot()
    def createTemplateAction(self, checked):
        self.copyOfPicture = self.picture
        self.selectPainterSizeWindow = SelectPainterSizeWindow()
        self.selectPainterSizeWindow.painterSizeSignal.connect(self.view.painterSizeTempSlot)
        self.selectPainterSizeWindow.exec_()
        if (self.view.createTemplateEnabled == True):
            self.Template = QPixmap(self.rightToolBar.fileListWidget.item(self.currentFileListIndex).text())
            self.Template.fill(Qt.transparent)
            self.rightToolBar.applyTemplateAction.setEnabled(True)
            self.rightToolBar.cancelTemplateAction.setEnabled(True)
            self.rightToolBar.createTemplateAction.setEnabled(False)
            self.rightToolBar.paintAction.setEnabled(False)
            self.leftToolBar.openAction.setEnabled(False)
            self.leftToolBar.openDirAction.setEnabled(False)
            self.leftToolBar.deleteImgAction.setEnabled(False)
            self.leftToolBar.nextAction.setEnabled(False)
            self.leftToolBar.previousAction.setEnabled(False)
            self.leftToolBar.editAction.setEnabled(False)
            self.leftToolBar.deleteAction.setEnabled(False)
            self.leftToolBar.createAction.setEnabled(False)
            self.leftToolBar.duplicateAction.setEnabled(False)

    @Slot()
    def applyTemplateAction(self, checked):
        print("add template")
        self.view.createTemplateEnabled = False
        self.selectTempRangeWindow = SelectTemplateRangeWindow()
        currentNumberOfImages = self.currentFileListIndex
        maxNumberOfImages = self.rightToolBar.fileListWidget.count()
        self.selectTempRangeWindow.numberOfPictures(currentNumberOfImages, maxNumberOfImages)
        self.selectTempRangeWindow.tempRangeSignal.connect(self.tempRangeSlot)
        self.selectTempRangeWindow.exec_()
        self.view.netZoomFactor = 1
        self.setUpWindow()
        self.rightToolBar.createTemplateAction.setEnabled(True)
        self.rightToolBar.applyTemplateAction.setEnabled(False)
        self.rightToolBar.cancelTemplateAction.setEnabled(False)
        self.rightToolBar.paintAction.setEnabled(True)
        self.leftToolBar.openAction.setEnabled(True)
        self.leftToolBar.openDirAction.setEnabled(True)
        self.leftToolBar.nextAction.setEnabled(True)
        self.leftToolBar.previousAction.setEnabled(True)
        self.leftToolBar.createAction.setEnabled(True)
        self.leftToolBar.deleteImgAction.setEnabled(True)
        self.leftToolBar.editAction.setEnabled(False)
        self.leftToolBar.deleteAction.setEnabled(False)
        self.leftToolBar.duplicateAction.setEnabled(False)


    def cancelTemplateAction(self, checked):
        self.view.createTemplateEnabled = False
        self.scene.addNewPixmap(self.copyOfPicture)
        self.copyOfPicture.save(self.rightToolBar.fileListWidget.item(self.currentFileListIndex).text(), "JPG")
        self.view.netZoomFactor = 1
        self.setUpWindow()
        # self.view.scale(self.view.netZoomFactor, self.view.netZoomFactor)
        # self.view.viewSettingsChanged()
        self.rightToolBar.createTemplateAction.setEnabled(True)
        self.rightToolBar.applyTemplateAction.setEnabled(False)
        self.rightToolBar.cancelTemplateAction.setEnabled(False)
        self.rightToolBar.paintAction.setEnabled(True)
        self.leftToolBar.openAction.setEnabled(True)
        self.leftToolBar.openDirAction.setEnabled(True)
        self.leftToolBar.nextAction.setEnabled(True)
        self.leftToolBar.previousAction.setEnabled(True)
        self.leftToolBar.createAction.setEnabled(True)
        self.leftToolBar.deleteImgAction.setEnabled(True)
        self.leftToolBar.editAction.setEnabled(False)
        self.leftToolBar.deleteAction.setEnabled(False)
        self.leftToolBar.duplicateAction.setEnabled(False)

    def checkListWidgetRowChanged(self, currentRow):
        self.currentCheckListIndex = currentRow
        if currentRow == (-1):
            self.currentCheckListIndex = 0
        self.view.checkListWidgetRowChanged(currentRow)
        self.leftToolBar.editAction.setEnabled(True)
        self.leftToolBar.deleteAction.setEnabled(True)
        self.leftToolBar.duplicateAction.setEnabled(True)
        self.leftToolBar.createAction.setEnabled(False)
        self.leftToolBar.deleteImgAction.setEnabled(False)

    @Slot()
    def fileListWidgetRowChaged(self):
        print("listWidgetRowChaged")
       # self.rightToolBar.fileListWidget.sortItems(Qt.AscendingOrder)
        self.currentFileListIndex = self.rightToolBar.fileListWidget.currentRow()
        self.leftToolBar.labelImgNo.setText(
            str(self.currentFileListIndex) + "/" + str(self.rightToolBar.fileListWidget.count() - 1))
        if (self.rightToolBar.fileListWidget.item(self.currentFileListIndex)):
            self.setWindowTitle(self.rightToolBar.fileListWidget.item(self.currentFileListIndex).text())
        if self.files:
            self.setUpWindow()
            self.leftToolBar.editAction.setEnabled(False)
            self.leftToolBar.deleteAction.setEnabled(False)
            self.leftToolBar.createAction.setEnabled(True)
            self.leftToolBar.deleteImgAction.setEnabled(True)
            self.leftToolBar.duplicateAction.setEnabled(False)


                                                                        #Other fundtions definitions

    def setUpWindow(self):
        print ("setup window")
        self.picture=QPixmap(self.rightToolBar.fileListWidget.item(self.currentFileListIndex).text())
        self.pixmapItem=QGraphicsPixmapItem(self.picture)
        self.pic_width=self.picture.width()
        self.pic_height=self.picture.height()
        if self.pic_width>self.pic_height:
            self.rectThickness=self.pic_width/320
        else:
            self.rectThickness=self.pic_height/320
        try:
          self.mainWindowHeight=self.height()
          self.mainWindowWidth=self.width()
        except:
            print (" ")
        self.view.viewWidth=self.screenWidth-self.leftToolBar.leftToolBarWidth-self.rightToolBar.rightToolBarWidth
        self.view.viewHeight=self.mainWindowHeight-self.menuHeight
        self.view.setMaximumSize(self.view.viewWidth,self.view.viewHeight)
        self.scene.clear()
        self.scene.addNewPixmap(self.picture)
        self.scene.setSceneRect(QtCore.QRectF(0,0,self.pic_width,self.pic_height))
        self.view.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)   #Qt.IgnoreAspectRatio // KeepAspectRatio
        self.sceneWidth=self.view.sceneRect().width()
        self.sceneHeight=self.view.sceneRect().height()
        if (self.view.viewWidth/self.sceneWidth)>(self.view.viewHeight/self.sceneHeight):
            self.graphScale=self.view.viewHeight/self.sceneHeight
            self.heightMargin=0
            self.widthMargin=(self.view.viewWidth-(self.sceneWidth*self.graphScale))/2
        else:
            self.graphScale=self.view.viewWidth/self.sceneWidth
            self.widthMargin=0
            self.heightMargin=(self.view.viewHeight-(self.sceneHeight*self.graphScale))/2

        self.view.viewSettingsChanged()
        self.loadRectsFromTxt(self.rightToolBar.fileListWidget.item(self.currentFileListIndex).text())
        self.loadCheckListFromTxt(self.rightToolBar.fileListWidget.item(self.currentFileListIndex).text())
        self.paintPointer=QGraphicsEllipseItem()
        self.paintPointer.setData(1,-1)
        self.scene.addItem(self.paintPointer)
        if (self.view.drawRect==True):
            lineItem1=QGraphicsLineItem()
            lineItem2=QGraphicsLineItem()
            self.scene.addItem(lineItem1)
            self.scene.addItem(lineItem2)

            tempItem=QGraphicsRectItem()
            tempItem.setBrush(QBrush(QtCore.Qt.transparent, style = QtCore.Qt.BDiagPattern))
            tempItem.setPen(QtGui.QPen(QtCore.Qt.red, 3))
            tempItem.setOpacity(0.5)

            self.scene.addItem(tempItem)

    def editClassesTxtActionFunc(self):
        list=self.dirName.split("/")
        list.append("classes.txt")
        path="/".join(list)
        self.editClassesTxtWindow=EditClassesTxtWindow()
        self.editClassesTxtWindow.pathOfClassesTxt(path)
        self.editClassesTxtWindow.exec_()
        self.classes=self.readClassesTxt()

    def readClassesTxt(self):
        list=self.dirName.split("/")
        list.append("classes.txt")
        path="/".join(list)
        if (os.path.isfile(path)):
            f=open(path, "r")
            content=f.readlines()
            f.close()
            return content
        else:
            self.errorMessage.showMessage("classes.txt does not exist")
            #self.deleteLater()

    def itemSelectionChangedSlot(self,selectedIndex):
        if ((self.view.paintingEnabled==False)and(self.view.createTemplateEnabled==False)):
            self.currentCheckListIndex=selectedIndex
            self.rightToolBar.checkListWidget.setCurrentRow(self.currentCheckListIndex)
            self.leftToolBar.editAction.setEnabled(True)
            self.leftToolBar.deleteAction.setEnabled(True)
            self.leftToolBar.duplicateAction.setEnabled(True)
            self.leftToolBar.createAction.setEnabled(False)
            self.leftToolBar.deleteImgAction.setEnabled(False)

    def loadRectsFromTxt(self,img_path):
        self.txt_path=img_path[:-3]+"txt"

        content=[]
        if os.path.exists(self.txt_path):
            self.file_txt=open(self.txt_path,"r")
            content=self.file_txt.readlines()
            self.file_txt.close()
        else:
            self.file_txt= open(self.txt_path,"w+")
            self.file_txt.close()
        self.rectCounter=0
        for c in content:
            yolo_x = float(c.split()[1])
            yolo_y = float(c.split()[2])
            yolo_width =float(c.split()[3])
            yolo_height =float(c.split()[4])
            abs_x=int(yolo_x*self.scene.width())
            abs_y=int(yolo_y*self.scene.height())
            abs_width=int(yolo_width*self.scene.width())
            abs_height=int(yolo_height*self.scene.height())
            self.item_rect=RectItem(self.rectThickness,self.rectCounter,(abs_x-int(abs_width/2)),(abs_y-int(abs_height/2)),abs_width,abs_height)
            self.item_rect.rectThickness=self.rectThickness
            self.scene.addNewItem(self.rectCounter,self.item_rect)
            self.rectCounter=self.rectCounter+1

    def loadCheckListFromTxt(self,img_path):
        print ("loadCheckListFromTxt")
        self.txt_path=img_path[:-3]+"txt"

        content=[]
        if os.path.exists(self.txt_path):
            self.file_txt=open(self.txt_path,"r")
            content=self.file_txt.readlines()
            self.file_txt.close()
        else:
            self.file_txt= open(self.txt_path,"w+")
            self.file_txt.close()
        self.rightToolBar.checkListWidget.clear()
        for k in content:
            id = int(k.split()[0])
            item = QtWidgets.QListWidgetItem()
            if ((0<=id)and(id<len(self.classes))):
                if (self.classes[id][-1]=="\n"):
                    item.setText(self.classes[id][:-1])
                else:
                    item.setText(self.classes[id])
            else:
                self.errorMessage.showMessage("The id no could not found in the classes.txt")

            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)
            self.rightToolBar.checkListWidget.addItem(item)

        self.rightToolBar.checkListWidget.setCurrentRow(self.currentCheckListIndex)

    def updateIdOnYoloTxt(self,id):
        content=[]
        self.file_txt=open(self.txt_path,"r")
        content=self.file_txt.readlines()
        self.file_txt.close()
        temp=content[self.currentCheckListIndex]
        list=temp.split()
        list[0]=str(id)
        content[self.currentCheckListIndex]=" ".join(list)+"\n"
        self.file_txt=open(self.txt_path,"w")
        self.file_txt.writelines(content)
        self.file_txt.close()

    @Slot()
    def updateIdSlot(self,id,rectCreated):
        print ("updateIdSlot")
        self.lastChoosenId=id
        self.lastChoosenIdExist=True
        if rectCreated==True:
            self.currentCheckListIndex=self.rectCounter-1
        item=self.rightToolBar.checkListWidget.item(self.currentCheckListIndex)
        if (self.classes[id][-1]=="\n"):
            item.setText(self.classes[id][:-1])
        else:
            item.setText(self.classes[id])
        self.rightToolBar.checkListWidget.insertItem(self.currentCheckListIndex,item)
        self.updateIdOnYoloTxt(id)
        self.leftToolBar.createAction.setEnabled(True)
        self.leftToolBar.deleteImgAction.setEnabled(True)

    @Slot()
    def cancelCreatingRectSlot(self):
        print("cancelCreatingRectSlot")
        content=[]
        self.file_txt=open(self.txt_path,"r")
        content=self.file_txt.readlines()
        self.file_txt.close()
        del content[-1]
        self.file_txt=open(self.txt_path,"w")
        self.file_txt.writelines(content)
        self.file_txt.close()
        self.setUpWindow()
        self.view.scale(self.view.netZoomFactor, self.view.netZoomFactor)
        self.view.viewSettingsChanged()
        self.leftToolBar.editAction.setEnabled(False)
        self.leftToolBar.deleteAction.setEnabled(False)
        self.leftToolBar.duplicateAction.setEnabled(False)
        

    @Slot()
    def createdRectPositionSlot(self,x, y, width, height):
        print ("createdRectPositionSlot")
        self.x=float(x)
        self.y=float(y)
        self.width=float(width)
        self.height=float(height)

        yolo_x=(self.x+(self.width/2))/self.sceneWidth
        yolo_y=(self.y+(self.height/2))/self.sceneHeight
        yolo_width=self.width/self.sceneWidth
        yolo_height=self.height/self.sceneHeight

        yolo_x_f = "%.6f" % yolo_x
        yolo_y_f = "%.6f" % yolo_y
        yolo_width_f = "%.6f" % yolo_width
        yolo_height_f = "%.6f" % yolo_height
        contentToWrite=str(0)+" "+yolo_x_f+" "+yolo_y_f +" "+yolo_width_f+" "+yolo_height_f+"\n"
        self.txtContentForDrawing[self.rowIndexOfTxt-1]=contentToWrite
        self.file_txt=open(self.txt_path,"w")
        self.file_txt.writelines(self.txtContentForDrawing)
        self.file_txt.close()
        self.setUpWindow()
        self.view.scale(self.view.netZoomFactor, self.view.netZoomFactor)
        self.view.viewSettingsChanged()

    @Slot()
    def movedRectPositionSlot(self,x,y,width,height):
        self.x=float(x)
        self.y=float(y)
        self.width=float(width)
        self.height=float(height)

        yolo_x=(self.x+(self.width/2))/self.sceneWidth
        yolo_y=(self.y+(self.height/2))/self.sceneHeight
        yolo_width=self.width/self.sceneWidth
        yolo_height=self.height/self.sceneHeight

        yolo_x_f = "%.6f" % yolo_x
        yolo_y_f = "%.6f" % yolo_y
        yolo_width_f = "%.6f" % yolo_width
        yolo_height_f = "%.6f" % yolo_height
        content=[]
        self.file_txt=open(self.txt_path,"r")
        content=self.file_txt.readlines()
        self.file_txt.close()
        temp=content[self.currentCheckListIndex]
        list=temp.split()
        list[1]=yolo_x_f
        list[2]=yolo_y_f
        list[3]=yolo_width_f
        list[4]=yolo_height_f
        content[self.currentCheckListIndex]=" ".join(list)+"\n"
        self.file_txt=open(self.txt_path,"w")
        self.file_txt.writelines(content)
        self.file_txt.close()

    @Slot()
    def resizedRectPositionalSlot(self,x,y,width,height):
        self.x=float(x)
        self.y=float(y)
        self.width=float(width)
        self.height=float(height)

        yolo_x=(self.x+(self.width/2))/self.sceneWidth
        yolo_y=(self.y+(self.height/2))/self.sceneHeight
        yolo_width=self.width/self.sceneWidth
        yolo_height=self.height/self.sceneHeight

        yolo_x_f = "%.6f" % yolo_x
        yolo_y_f = "%.6f" % yolo_y
        yolo_width_f = "%.6f" % yolo_width
        yolo_height_f = "%.6f" % yolo_height
        content=[]
        self.file_txt=open(self.txt_path,"r")
        content=self.file_txt.readlines()
        self.file_txt.close()
        temp=content[self.currentCheckListIndex]
        list=temp.split()
        list[1]=yolo_x_f
        list[2]=yolo_y_f
        list[3]=yolo_width_f
        list[4]=yolo_height_f
        content[self.currentCheckListIndex]=" ".join(list)+"\n"
        self.file_txt=open(self.txt_path,"w")
        self.file_txt.writelines(content)
        self.file_txt.close()

    @Slot()
    def enableIdInputOfCreatedRectSlot(self):
        self.editWindow=EditWindow()
        self.editWindow.readClassesTxt(self.dirName)
        self.editWindow.rectCreated=True
        if (self.lastChoosenIdExist==True):
            self.editWindow.setLastChoosenId(self.lastChoosenId)
        self.editWindow.updateIdSignal.connect(self.updateIdSlot)
        self.editWindow.cancelCreatingRectSignal.connect(self.cancelCreatingRectSlot)
        self.editWindow.exec_()

    @Slot()
    def mousePressedOnNoItemSlot(self):
        self.leftToolBar.editAction.setEnabled(False)
        self.leftToolBar.deleteAction.setEnabled(False)
        self.leftToolBar.createAction.setEnabled(True)
        self.leftToolBar.deleteImgAction.setEnabled(True)
        self.leftToolBar.duplicateAction.setEnabled(False)

    @Slot()
    def tempRangeSlot(self,rangeBegins,rangeEnds):
        self.rangeBegins=rangeBegins
        self.rangeEnds=rangeEnds
        self.applyTemplateEnabled=True

    def paintEvent(self, e):

        if (self.view.paintEventEnabled==True):
            qp = QtGui.QPainter(self.picture)
            qp.begin(self)
            qp.setBrush(QBrush(self.view.paintingColor, style = QtCore.Qt.BDiagPattern))
            qp.setPen(QtGui.QPen(self.view.paintingColor))
            qp.drawEllipse(self.view.paintPos.x(), self.view.paintPos.y(), self.view.painterSize, self.view.painterSize)
            self.scene.addNewPixmap(self.picture)
            self.picture.save(self.rightToolBar.fileListWidget.item(self.currentFileListIndex).text(), "JPG")
            qp.end()
            self.update()
            self.paintPointer=QGraphicsEllipseItem()
            self.paintPointer.setData(1,-1)
            self.scene.addItem(self.paintPointer)
          #  self.setUpWindow()
          #  self.view.scale(self.view.netZoomFactor, self.view.netZoomFactor)
           # self.view.translate(self.view.totalDelta.x(), self.view.totalDelta.y())
          #  self.view.viewSettingsChanged()

        if (self.view.createTemplateEventEnabled==True):
            qp = QtGui.QPainter(self.picture)
            qp.begin(self)
            qp.setBrush(QBrush(self.view.paintingColor, style = QtCore.Qt.BDiagPattern))
            qp.setPen(QtGui.QPen(self.view.paintingColor))
            qp.drawEllipse(self.view.paintPos.x(), self.view.paintPos.y(), self.view.painterSize, self.view.painterSize)
            self.scene.addNewPixmap(self.picture)
            self.picture.save(self.rightToolBar.fileListWidget.item(self.currentFileListIndex).text(), "JPG")
            qp.end()
            self.update()
            self.paintPointer=QGraphicsEllipseItem()
            self.paintPointer.setData(1,-1)
            self.scene.addItem(self.paintPointer)
           # self.setUpWindow()
          #  self.view.scale(self.view.netZoomFactor, self.view.netZoomFactor)
           # self.view.viewSettingsChanged()

            qp = QtGui.QPainter(self.Template)
            qp.begin(self)
            qp.setBrush(QBrush(self.view.paintingColor, style = QtCore.Qt.BDiagPattern))
            qp.setPen(QtGui.QPen(self.view.paintingColor))
            qp.drawEllipse(self.view.paintPos.x(), self.view.paintPos.y(), self.view.painterSize, self.view.painterSize)
            qp.end()

        if (self.applyTemplateEnabled==True):
            source_pic=self.Template.toImage()
            for i in range(self.rangeBegins, (self.rangeEnds+1)):
                dest_pic=QPixmap(self.rightToolBar.fileListWidget.item(i).text())
                qp = QtGui.QPainter(dest_pic)
                qp.setCompositionMode(QPainter.CompositionMode_SourceOver)
                if (dest_pic.size()==source_pic.size()):
                    qp.drawImage(0, 0, source_pic)
                dest_pic.save(self.rightToolBar.fileListWidget.item(i).text(), "JPG")
                qp.end()
          #  self.setUpWindow()
           # self.view.scale(self.view.netZoomFactor, self.view.netZoomFactor)
           # self.view.viewSettingsChanged()
            self.applyTemplateEnabled=False

    @Slot()
    def errorOccurred(self):
        error = str(self.process.readAllStandardError())

    @Slot()
    def exitActionFunc(self, checked):
        QApplication.quit()

    @Slot()
    def advancedModeActionFunc(self,checked):
        if (checked==True):
            self.advancedMode=True
            self.view.advancedMode=True
        else:
            self.advancedMode=False
            self.view.advancedMode=False

    def createTraintTxt(self):
        content=[]
        list= self.dirName.split("/")
        self.dirName=self.dirName
        pathOfTrainTxt=self.dirName+"/"+list[-1]+"_train.txt"
        for index in range(self.rightToolBar.fileListWidget.count()):
            content.append(self.rightToolBar.fileListWidget.item(index).text()+"\n")
        self.trainTxt= open(pathOfTrainTxt,"w")
        self.trainTxt.writelines(content)
        self.trainTxt.close()



if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    editWindow=EditWindow()
    scene=Scene()
    view=GraphicsView(scene)
    window = MainWindow(view)
    window.show()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

    # Execute application
    sys.exit(app.exec_())
