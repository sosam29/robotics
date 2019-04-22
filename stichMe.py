import imutils
import numpy as np 
import cv2

class Sticher:
    def __init__(self):
        self.iscv3 = imutils.is_cv3(or_better = True)

    def stich(self, images, ratio=0.75, reProjThreshold= 4.0, showMatches= False):
        (imageB, imageA)= images
        (kpsA,featuresA) = self.detectAndDescribe(imageA)
        (kpsB,featuresB) = self.detectAndDescribe(imageB)

        M= self.matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reProjThreshold )

        if M is None:
            return None
        (matches,H, status) = M
        result = cv2.warpPerspective(imageA, H,(imageA.shape[1]+ imageB.shape[1], imageA.shape[0]))
        result[0:imageB.shape[0], 0:imageB[1]]= imageB

        if showMatches:
            vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches, status)
            return (result, vis)
        return result
    
    def detectAndDescribe(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if(self.iscv3):
            descriptor = cv2.xfeatures2d.SIFT_create()
            (kps, features) = descriptor.detectAndDescribe(image, None)
        else:
            # detector = cv2.FeatureDetector_create("SIFT")
            detector = cv2.Feature2D_create("ORB")
            kps = detector.detect(gray)

            extractor = cv2.DescriptorExtractor_create("ORB")
            (kps, features)= extractor.compute(gray, kps)
        kps = np.float32([kp.pt for kp in kps])
        return (kps, features)
    
    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB, ratio, reProjThresh):
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rowMatches = matcher.knnMAtch(featuresA, featuresB, 2)
        matches=[]

        for m in rowMatches:
            if len(m)==2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

            if (len(matches) > 4):
                ptsA = np.float32([kpsA[i] for (_,i) in matches])
                ptsB = np.float32([kpsB[i] for (i, _) in matches])

                (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reProjThresh)

                return (H, status)
            return None

    
    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
        (hA, wA) = imageA.shape[2]
        (hB, wB) = imageB.shape[2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")

        for ((trainIdx, queryIdx), s) in zip(matches, status):

            if s==1:
                ptA = (int(kpsA[queryIdx][0]),int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]),int(kpsB[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)
        return vis
        

if __name__ =="__main__":
    
    imgl= '/home/pi/examples/python/robotics/robotics/left.jpg'
    imgr= '/home/pi/examples/python/robotics/robotics/right.jpg'
    imageA = cv2.imread(imgl)
    imageB = cv2.imread(imgr)
    imageA = imutils.resize(imageA, width=400)
    imageB = imutils.resize(imageB, width=400)
    sticher  = Sticher()
    (result, vis) =sticher.stich([imageA, imageB], showMatches=True)
    cv2.imshow("Left Image", imageA)
    cv2.imshow("Right Image", imageB)
    cv2.imshow("Key Point Match", vis)
    cv2.imshow("result", result)

    cv2.waitKey(0)