import numpy as np
from numpy import pi
import csv


class SCSA:

    def __init__(self, signal, h=1, method='fourier', auto=True):
        self.signal = signal
        self.M = len(signal)
        self.h = h
        self.reconstructed = np.zeros(self.M)
        self.D = np.zeros((self.M, self.M))
        self.eig = np.zeros(self.M)
        self.mse = 0

        self.diffMatrix(method)
        if auto:
            self.reconstruct()

    def diffMatrix(self, method):

        if method == 'fourier':
            delta = 2 * pi / self.M

            for i in range(self.M):
                for j in range(self.M):
                    if self.M % 2 == 0:
                        if i == j:
                            self.D[i, j] = - pi ** 2 / (3 * delta ** 2) - 1 / 6
                        else:
                            self.D[i, j] = -(-1) ** (i - j) * .5 * np.sin((i - j) * delta / 2) ** (-2)
                    else:
                        if i == j:
                            self.D[i, j] = - pi ** 2 / (3 * delta ** 2) - 1 / 12
                        else:
                            self.D[i, j] = -(-1) ** (i - j) * .5 * (np.sin((i - j) * delta / 2)**(-1))\
                                           * (np.tan((i - j) * delta / 2)**(-1))
            self.D = (delta ** 2) * self.D
        elif method == 'finite':
            self.D = -2*np.eye(self.M) + np.eye(self.M, k=1) + np.eye(self.M, k=-1)

    def reconstruct(self):
        I = np.diag(self.signal - np.min(self.signal))
        H = -(self.h**2)*self.D - I

        self.eig, func = np.linalg.eig(H)

        indx = self.eig.argsort()
        self.eig = self.eig[indx]
        func = np.real(func[:, indx])
        self.km = np.sqrt(-np.real(self.eig[self.eig <= 0]))
        self.psi = func[:, self.eig <= 0]


        for i in range(len(self.km)):
            self.reconstructed += 4*self.h*self.km[i]*np.square(func[:, i])

        self.reconstructed = self.reconstructed + np.min(self.signal)

        self.mse = np.square(self.signal - self.reconstructed).mean()

    def writeEigToTxt(self, path):
        f = open(path, 'w+')
        for i in range(len(self.eig)):
            f.write(str(self.eig[i]) + '\n')
        f.close()

