epsilon = 0.00001;

import pylab as pl

def get_features(positions):
    manyFeatures = 7

    wMin = 5
    wMax = 20

    trackLength = pl.shape(positions)[0]

    steps = getSteps(positions,trackLength)
    angles = getAngles(steps,trackLength)

    feats = pl.zeros([trackLength,manyFeatures])
    manyTimes = pl.zeros(trackLength)

    for i in range(trackLength-wMax+1):
        for j in range(wMin,wMax+1):
            feats[i:i+j,0] += getStraight(angles[i:i+j-2],j-1)
            feats[i:i+j,1] += getBend(angles[i:i+j-2],j-1)
            feats[i:i+j,2] += getEff(positions[i:i+j,:],steps[i:i+j-1,:],j-1)

            '''
            feats[i:i+j,3] +=
            feats[i:i+j,4] +=
            feats[i:i+j,5] +=
            feats[i:i+j,6] +=
            '''
            manyTimes[i:i+j] += 1


    for i in range(manyFeatures):
        feats[:,i] /= manyTimes

    return feats

# Features

def getStraight(windowAngles,windowLength):
    cosb = 0
    for i in range(windowLength-2):
        cosb += pl.cos(windowAngles[i])
    
    straightness = (1./(windowLength-1))*cosb
    return straightness

def getBend(windowAngles,windowLength):
    sinb = 0
    for i in range(windowLength-2):
        sinb += pl.sin(windowAngles[i])
    
    bending = (1./(windowLength-1))*sinb
    return bending

def getEff(windowPositions,windowSteps,windowLength):
    s2 = 0
    dispVec = windowSteps[windowLength-1,:] - windowSteps[0,:]
    disp = pl.dot(dispVec,dispVec)
    for i in range(windowLength-1):
        s2 += pl.dot(windowSteps[i,:],windowSteps[i,:])

    efficiency = disp/(windowLength*s2+epsilon)

    if (efficiency > 1.5):
        efficiency = 1.5
        
    return efficiency


# Intermediate Functions

def getSteps(positions,trackLength):
    steps = pl.zeros([trackLength-1,2])
    for i in range(trackLength-1):
        steps[i,:] = positions[i+1,:]-positions[i,:]
    return steps

def getAngles(steps,trackLength):
    angles = pl.zeros([trackLength-2,1])
    polar = pl.zeros(pl.shape(steps))
    for i in range(trackLength-1):
        polar[i,0] = pl.norm(steps[i,:])
        polar[i,1] = pl.arctan(steps[i,0]/steps[i,1])

        if pl.isnan( polar[i,1]):
            polar[i,1] = 0

        if (steps[i,0] >= 0):
            if (steps[i,1] >= 0):
                pass
            elif (steps[i,1] < 0):
                polar[i,1] += 2.*pl.pi
        elif (steps[i,0] < 0):
            if (steps[i,1] >= 0):
                polar[i,1] += pl.pi
            elif (steps[i,1] < 0):
                polar[i,1] += pl.pi

    for i in range(trackLength-2):
        angles[i] = polar[i+1,1] - polar[i,1]

    return angles
