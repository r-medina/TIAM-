import pylab as pl
import math
epsilon = 0.00001;

# Features

def get_straight(windowAngles,windowLength):
    cosb = 0
    for i in range(windowLength-2):
        cosb += pl.cos(windowAngles[i])
    
    straightness = (1./(windowLength-1))*cosb
    return straightness

def get_bend(windowAngles,windowLength):
    sinb = 0
    for i in range(windowLength-2):
        sinb += pl.sin(windowAngles[i])
    
    bending = (1./(windowLength-1))*sinb
    return bending

def get_eff(windowPositions,windowSteps,windowLength):
    s2 = 0
    dispVec = windowSteps[windowLength-1,:] - windowSteps[0,:]
    disp = pl.dot(dispVec,dispVec)
    for i in range(windowLength-1):
        s2 += pl.dot(windowSteps[i,:],windowSteps[i,:])

    efficiency = disp/(windowLength*s2+epsilon)
    
    return efficiency

def get_asymm(eig1,eig2):
    asymmetry = -pl.log(1-((eig1-eig2)**2./(2*(eig1+eig2)**2.+epsilon)))
    return asymmetry

def get_skew(projection,proj_mean,windowLength):
    num = 0
    denom = 0
    proj_mean = pl.mean(projection)

    for i in range(windowLength):
        num += (projection[i] - proj_mean)**3.
        denom += (projection[i] - proj_mean)**2.

    denom = denom**(3./2.)
    skewness = math.sqrt(windowLength+1)*(num/(denom+epsilon))
    return skewness

def get_kurt(projection,proj_mean,windowLength):
    num = 0
    denom = 0

    for i in range(windowLength):
        num += (projection[i] - proj_mean)**4.
        denom += (projection[i] - proj_mean)**2.

    denom = denom**(2.)
    skewness = (windowLength+1)*(num/(denom+epsilon))
    return skewness

# Intermediate Functions

def get_steps(positions,trackLength):
    steps = pl.zeros([trackLength-1,2])
    for i in range(trackLength-1):
        steps[i,:] = positions[i+1,:]-positions[i,:]
    return steps

def get_angles(steps,trackLength):
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

def get_gyration_tensor(windowPositions):
    gyrationTensor = pl.zeros([2,2])
    x = windowPositions[:,0]
    y = windowPositions[:,1]
    gyrationTensor[0,0] = pl.mean(x**2.) - pl.mean(x)**2.
    gyrationTensor[0,1] = pl.mean(x*y) - (pl.mean(x)*pl.mean(y))
    gyrationTensor[1,0] = gyrationTensor[0,1]
    gyrationTensor[1,1] = pl.mean(y**2.) - pl.mean(y)**2.
    return gyrationTensor

def get_projection(windowPositions,domEig,windowLength):
    s_proj = pl.zeros([windowLength,1])
    for i in range(windowLength):
        s_proj[i] = pl.dot(windowPositions[i,:],domEig)
    return s_proj


class FeatureSpace():
    
    # The main method
    
    @staticmethod
    def get_features(positions):
        manyFeatures = 7

        wMin = 5
        wMax = 14

        trackLength = pl.shape(positions)[0]
        
        steps = get_steps(positions,trackLength)
        angles = get_angles(steps,trackLength)
        
        feats = pl.zeros([trackLength,manyFeatures])
        manyTimes = pl.zeros(trackLength)

        for i in range(trackLength-wMax+1):
            for j in range(wMin,wMax+1):
                feats[i:i+j,0] += get_straight(angles[i:i+j-2],j-1)
                feats[i:i+j,1] += get_bend(angles[i:i+j-2],j-1)
                feats[i:i+j,2] += get_eff(positions[i:i+j,:],steps[i:i+j-1,:],j-1)
                
                gyrationTensor = get_gyration_tensor(positions[i:i+j,:])
                [eig_vals, eig_vecs] = pl.eig(gyrationTensor)
                eig_vals = pl.array([eig_vals[0],eig_vals[1]])

                feats[i:i+j,3] += get_asymm(eig_vals[0],eig_vals[1])

                dom_index = pl.argmax(eig_vals)
                dom_vec = eig_vecs[:,dom_index]
                pos_proj = get_projection(positions[i:i+j,:],dom_vec,j-1)
                proj_mean = pl.mean(pos_proj)

                feats[i:i+j,4] += get_skew(pos_proj,proj_mean,j-1)
                feats[i:i+j,5] += get_kurt(pos_proj,proj_mean,j-1)
                #feats[i:i+j,6] +=

                manyTimes[i:i+j] += 1

        '''
        for i in range(trackLength-wMin+1):
            j = 5
            feats[i:i+j,0] += get_straight(angles[i:i+j-2],j-1)
            feats[i:i+j,1] += get_bend(angles[i:i+j-2],j-1)
            feats[i:i+j,2] += get_eff(positions[i:i+j,:],steps[i:i+j-1,:],j-1)
            
            gyrationTensor = get_gyration_tensor(positions[i:i+j,:])
            [eig_vals, eig_vec] = pl.eig(gyrationTensor)
            eig_vals = pl.array([eig_vals[0],eig_vals[1]])
        
            feats[i:i+j,3] += get_asymm(eig_vals[0],eig_vals[1])

            #feats[i:i+j,4] +=
            #feats[i:i+j,5] +=
            #feats[i:i+j,6] +=
            
            manyTimes[i:i+j] += 1
        '''

        for i in range(manyFeatures):
            feats[:,i] /= manyTimes


        return feats
