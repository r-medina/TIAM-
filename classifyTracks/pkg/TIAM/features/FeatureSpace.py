import pylab as pl
import math

epsilon = 0.0000001;


# Main Class

class FeatureSpace():
    
    _many_features = 8

    @property
    def many_features(self):
        return self._many_features

    # Intermediate Functions

    @staticmethod
    def _get_steps(positions,track_length):
        steps = pl.zeros([track_length-1,2])
        for i in range(track_length-1):
            steps[i,:] = positions[i+1,:]-positions[i,:]
        return steps

    @staticmethod
    def _get_angles(steps,track_length):
        angles = pl.zeros(track_length-2)
        polar = pl.zeros(pl.shape(steps))
        for i in range(track_length-1):
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

        for i in range(track_length-2):
            angles[i] = polar[i+1,1] - polar[i,1]

        return angles

    @staticmethod
    def _get_gyration_tensor(window_positions):
        gyrationTensor = pl.zeros([2,2])
        x = window_positions[:,0]
        y = window_positions[:,1]
        gyrationTensor[0,0] = pl.mean(x**2.) - pl.mean(x)**2.
        gyrationTensor[0,1] = pl.mean(x*y) - (pl.mean(x)*pl.mean(y))
        gyrationTensor[1,0] = gyrationTensor[0,1]
        gyrationTensor[1,1] = pl.mean(y**2.) - pl.mean(y)**2.
        return gyrationTensor

    @staticmethod
    def _get_projection(window_positions,domEig,window_length):
        s_proj = pl.zeros(window_length)
        for i in range(window_length):
            s_proj[i] = pl.dot(window_positions[i,:],domEig)
        return s_proj

    @staticmethod
    def _get_msd(positions,track_length):
        maxdt = 5#int(pl.floor((track_length-1)/4.))
        msd = pl.zeros(maxdt)
        for i in range(maxdt):
            for j in range(maxdt):
                ds = positions[i+j] - positions[j]
                disp = pl.norm(ds)**2.
                msd[i] += disp
            msd[i] = msd[i]/maxdt
        return msd

    # Features

    @staticmethod
    def _get_straight(window_angles,window_length):
        cosb = 0
        for i in range(window_length-2):
            cosb += pl.cos(window_angles[i])
    
        straightness = (1./(window_length-1))*cosb
        return straightness

    @staticmethod
    def _get_bend(window_angles,window_length):
        sinb = 0
        for i in range(window_length-2):
            sinb += pl.sin(window_angles[i])
    
        bending = (1./(window_length-1))*sinb
        return bending

    @staticmethod
    def _get_eff(window_positions,window_steps,window_length):
        s2 = 0
        dispVec = window_steps[window_length-1,:] - window_steps[0,:]
        disp = pl.dot(dispVec,dispVec)
        for i in range(window_length-1):
            s2 += pl.dot(window_steps[i,:],window_steps[i,:])

        efficiency = disp/(window_length*s2+epsilon)
    
        return efficiency

    @staticmethod
    def _get_asymm(eig1,eig2):
        asymmetry = -pl.log(1-((eig1-eig2)**2./(2*(eig1+eig2)**2.+epsilon)))
        return asymmetry

    @staticmethod
    def _get_skew(projection,proj_mean,window_length):
        num = 0
        denom = 0
        proj_mean = pl.mean(projection)

        for i in range(window_length):
            num += (projection[i] - proj_mean)**3.
            denom += (projection[i] - proj_mean)**2.

        denom = denom**(3./2.)
        skewness = math.sqrt(window_length+1)*(num/(denom+epsilon))
        return skewness

    @staticmethod
    def _get_kurt(projection,proj_mean,window_length):
        num = 0
        denom = 0

        for i in range(window_length):
            num += (projection[i] - proj_mean)**4.
            denom += (projection[i] - proj_mean)**2.

        denom = denom**(2.)
        skewness = (window_length+1)*(num/(denom+epsilon))
        return skewness

    @staticmethod
    def _get_disp(window_positions):
        displacement = pl.norm(window_positions[-1] - window_positions[0])
        return displacement

    @staticmethod
    def _get_conf(window_positions,window_length,diffusion_coefficient):
        R = 0
        for i in range(1,window_length):
            d = pl.norm(window_positions[i,:])
            if (d > R):
                R = d
        log_psi = 0.2048-2.5117*diffusion_coefficient*window_length/(R+epsilon);
        L = -log_psi-1
        return L

    # Main method
    def get_features(self,positions):
        wMin = 5
        wMax = 18

        track_length = pl.shape(positions)[0]
        
        steps = self._get_steps(positions,track_length)
        angles = self._get_angles(steps,track_length)
        
        feats = pl.zeros([track_length,self.many_features])
        manyTimes = pl.zeros(track_length)

        msd = self._get_msd(positions,track_length)
        # following code is to _get diffusion coefficient
        xi = pl.arange(4)
        A = pl.array([xi, pl.ones(4)]).T
        diff_coeff = pl.lstsq(A,msd[:4])[0][0]

        for i in range(track_length-wMax+1):
            for j in range(wMin,wMax+1):
                feats[i:i+j,0] += self._get_straight(angles[i:i+j-2],j-1)
                feats[i:i+j,1] += self._get_bend(angles[i:i+j-2],j-1)
                feats[i:i+j,2] += self._get_eff(positions[i:i+j,:],steps[i:i+j-1,:],j-1)

                gyrationTensor = self._get_gyration_tensor(positions[i:i+j,:])
                [eig_vals, eig_vecs] = pl.eig(gyrationTensor)
                eig_vals = pl.array([eig_vals[0],eig_vals[1]])

                feats[i:i+j,3] += self._get_asymm(eig_vals[0],eig_vals[1])

                dom_index = pl.argmax(eig_vals)
                dom_vec = eig_vecs[:,dom_index]
                pos_proj = self._get_projection(positions[i:i+j,:],dom_vec,j-1)
                proj_mean = pl.mean(pos_proj)

                feats[i:i+j,4] += self._get_skew(pos_proj,proj_mean,j-1)
                feats[i:i+j,5] += self._get_kurt(pos_proj,proj_mean,j-1)
                feats[i:i+j,6] += self._get_disp(positions[i:i+j,:])
                feats[i:i+j,7] += self._get_conf(positions[i:i+j,:],j-1,diff_coeff)

                manyTimes[i:i+j] += 1

        for i in range(self.many_features):
            feats[:,i] /= manyTimes

        return feats
