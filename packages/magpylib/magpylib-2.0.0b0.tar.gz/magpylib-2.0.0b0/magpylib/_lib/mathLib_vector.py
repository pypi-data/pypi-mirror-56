# -------------------------------------------------------------------------------
# magpylib -- A Python 3 toolbox for working with magnetic fields.
# Copyright (C) Silicon Austria Labs, https://silicon-austria-labs.com/,
#               Michael Ortner <magpylib@gmail.com>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program.  If not, see <https://www.gnu.org/licenses/>.
# The acceptance of the conditions of the GNU Affero General Public License are
# compulsory for the usage of the software.
#
# For contact information, reach out over at <magpylib@gmail.com> or our issues
# page at https://www.github.com/magpylib/magpylib/issues.
# -------------------------------------------------------------------------------

import numpy as np

def QmultV(Q, P):
    """
    Implementation of the quaternion multiplication
    """
    Sig = np.array([[1,-1,-1,-1],[1,1,1,-1],[1,-1,1,1],[1,1,-1,1]])
    M = Q*np.array([P,np.roll(P[:,::-1],2,axis=1),np.roll(P,2,axis=1),P[:,::-1]])
    M = np.swapaxes(M,0,1)
    return np.sum(M*Sig,axis=2)


def QconjV(Q):
    """
    Implementation of the conjugation of a quaternion
    """
    Sig = np.array([1,-1,-1,-1])
    return Q*Sig


def getRotQuatV(ANGLE, AXIS):
    """
    ANGLE in [deg], AXIS dimensionless
    vectorized version of getRotQuat, returns the rotation quaternion which 
    describes the rotation given by angle and axis (see paper)
    NOTE: axis cannot be [0,0,0] !!! this would not describe a rotation. however
        sinPhi = 0 returns a 0-axis (but just in the Q this must still be 
        interpreted correctly as an axis)
    """
    Lax = np.linalg.norm(AXIS,axis=1)
    Uax = AXIS/Lax[:,None]   # normalize

    Phi = ANGLE/180*np.pi/2
    cosPhi = np.cos(Phi)
    sinPhi = np.sin(Phi)
    
    Q = np.array([cosPhi] + [Uax[:,i]*sinPhi for i in range(3)])

    return np.swapaxes(Q,0,1)

def QrotationV(Q,v):
    """
    replaces angle axis rotation by direct Q-rotation to skip this step speed
    when multiple subsequent rotations are given
    """
    Qv = np.pad(v,((0,0),(1,0)), mode='constant') 
    Qv_new = QmultV(Q, QmultV(Qv, QconjV(Q)))
    return Qv_new[:,1:]


def getAngAxV(Q):
    # UNUSED - KEEP FOR UNDERSTANDING AND TESTING
    # returns angle and axis for a quaternion orientation input
    angle = np.arccos(Q[:,0])*180/np.pi*2
    axis = Q[:,1:]
    
    # a quaternion with a 0-axis describes a unit rotation (0-angle).
    # there should still be a proper axis output but it is eliminated
    # by the term [Uax[:,i]*sinPhi for i in range(3)]) with sinPhi=0.
    # since for 0-angle the axis doesnt matter we can set it to [0,0,1] 
    # which is our defined initial orientation
    
    Lax = np.linalg.norm(axis,axis=1)
    mask = Lax!=0
    Uax = np.array([[0,0,1.]]*len(axis))     # set all to [0,0,1]
    Uax[mask] = axis[mask]/Lax[mask,None]   # use mask to normalize non-zeros
    return angle,Uax


def angleAxisRotationV_priv(ANGLE, AXIS, V):
    # vectorized version of angleAxisRotation_priv
    P = getRotQuatV(ANGLE, AXIS)
    Qv = np.pad(V,((0,0),(1,0)), mode='constant') 
    Qv_new = QmultV(P, QmultV(Qv, QconjV(P)))
    return Qv_new[:,1:]


def randomAxisV(N):
    """
    This is the vectorized version of randomAxis(). It generates an 
    N-sized vector of random `axes` (3-vector of length 1) from equal 
    angular distributions using a MonteCarlo scheme.

    Parameters
    -------
    N : int
        Size of random axis vector.

    Returns
    -------
    axes : Nx3 arr
        A  vector of random axes from an equal angular distribution of length 1.
    """
    
    # R = np.random.rand(N,3)*2-1
    
    # while True:
    #     lenR = np.linalg.norm(R,axis=1)
    #     mask = lenR > 1  #bad = True
    #     Nbad = np.sum(mask)
    #     if Nbad==0:
    #         return R/lenR
    #     else:
    #         R[mask] = np.random.rand(Nbad,3)*2-1

    R = np.random.rand(N,3)*2-1
        
    while True:
        lenR = np.linalg.norm(R,axis=1)
        mask = lenR > 1  #bad = True
        Nbad = np.sum(mask)
        if Nbad==0:
            return R/lenR[:,np.newaxis]
        else:
            R[mask] = np.random.rand(Nbad,3)*2-1



def axisFromAnglesV(ANG):
    """
    This is the vectorized version of axisFromAngles(). 
    This function generates an `axis` (3-vector of length 1) from two `angles` = [phi,th]
    that are defined as in spherical coordinates. phi = azimuth angle, th = polar angle.

    Parameters
    ----------
    ANG : arr Nx2 [deg]
        Array of size N of the two angels [phi,th], azimuth and polar, in units of deg.

    Returns    
    -------
    AXIS : arr Nx3
        An N-sized array of axis vectors (length 1) oriented as given by the input ANG.
    """
    PHI = ANG[:,0]/180*np.pi
    TH = ANG[:,1]/180*np.pi

    return np.array([np.cos(PHI)*np.sin(TH), np.sin(PHI)*np.sin(TH), np.cos(TH)]).transpose()



def anglesFromAxisV(AXIS):
    """
    This is the vectorized version of anglesFromAxis().

    This function takes an array of arbitrary axes and returns 
    the orientations given by the angles = [phi,th] that are defined as in 
    spherical coordinates. phi = azimuth angle, th = polar angle.

    Parameters
    ----------
    AXIS : arr Nx3
        N sized array of axis-vectors (arr3 with length 1).

    Returns
    -------
    ANGLES : arr Nx2 [deg]
        An array of angles [phi,th], azimuth and polar, that anchorrespond to 
        the orientations given by the input axes.
    """

    Lax = np.linalg.norm(AXIS,axis=1)
    Uax = AXIS/Lax[:,np.newaxis]

    TH = np.arccos(Uax[:,2])/np.pi*180
    PHI = np.arctan2(Uax[:,1], Uax[:,0])/np.pi*180
    return np.array([PHI, TH]).transpose()


def angleAxisRotationV(POS,ANG,AXIS,ANCHOR):
    """
    This is the vectorized version of angleAxisRotation.
    This function uses angle-axis rotation to rotate the `position` vector by
    the `angle` argument about an axis defined by the `axis` vector which passes
    through the center of rotation `anchor` vector.

    Parameters
    ----------
    POS : arrNx3
        The input vectors to be rotated.

    ANG : arrN [deg]
        Rotation angles in units of [deg]

    AXIS : arrNx3
        Vector of rotation axes.

    anchor : arrNx3
        Vector of rotation anchors.

    Returns    
    -------
    newPositions : arrNx3
        Vector of rotated positions.
    """

    POS12 = POS-ANCHOR
    POS12rot = angleAxisRotationV_priv(ANG,AXIS,POS12)
    POSnew = POS12rot+ANCHOR

    return POSnew