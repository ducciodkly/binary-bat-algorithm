import numpy as np
import random
import matplotlib.pyplot as plt

# from Main import noP


class BinaryBatAlgorithm1():


  def __init__(self, Qmin, Qmax, Max_iter, pop , A, r, dim,function):  # ,I,n,Qmin,Qmax,N_iter,d,Max_iter,fmin,r,A
    self.f_min = 0.0

    self.Qmin = Qmin
    self.Qmax = Qmax
    # N_iter = N_iter
    self.pop = pop
    self.dim = dim
    self.Max_iter = Max_iter
    self.r = r
    self.A = A

    self.Q = np.zeros(shape=(self.pop, 1))
    self.v = np.zeros(shape=(self.pop, self.dim))
    self.Sol = np.zeros(shape=(self.pop, self.dim), dtype=int)

    self.Fitness = np.zeros(shape=(self.pop))
    self.cg_curve = np.zeros(shape=(self.Max_iter+1))
    self.best = np.zeros(shape=self.dim, dtype=int)
    self.Func = function

  def best_bat(self):
    i = 0
    j = 0
    for i in range(self.pop):
      if self.Fitness[i] < self.Fitness[j]:
        j = i
    for i in range(self.dim):
      self.best[i] = self.Sol[j][i]
    self.f_min = self.Fitness[j]
    self.cg_curve[0] = self.f_min
    c = 1

  def init_bat(self):
    for i in range(self.pop):
      for j in range(self.dim):
        rnd = np.random.uniform(0, 1)
        if rnd <= 0.5:
          self.Sol[i][j] = 0
        else:
          self.Sol[i][j] = 1
      self.Fitness[i] = self.Func(self.Sol[i])
    self.best_bat()
  def StartIteration(self):
    self.init_bat()
    for N_iter in range(self.Max_iter):
      for i in range(self.pop):
        rnd = np.random.uniform(0, 1, size=self.dim)
        self.Q = self.Qmin + (self.Qmin - self.Qmax) * rnd
        self.v[i][:] = self.v[i][:] + (self.Sol[i][:] - self.best[:]) * self.Q[:]

        V_shaped_transfer_function = np.abs((2 / np.pi) * np.arctan(((np.pi / 2) * self.v[i][:])))

        rnd = np.random.uniform(0, 1, size=self.dim)
        Ind = rnd < V_shaped_transfer_function
        self.Sol[i][Ind] = 1 - self.Sol[i][Ind]

        rnd = np.random.uniform(0, 1, size=self.dim)
        Ind = rnd > self.r
        self.Sol[i][Ind] = self.best[Ind]



        # for j in range(self.dim):
        #   rnd = np.random.uniform(0, 1)
        #   self.Q[i] = self.Qmin + (self.Qmin - self.Qmax) * rnd
        #   self.v[i][j] = self.v[i][j] + (self.Sol[i][j] - self.best[j]) * self.Q[i]
        #
        #   V_shaped_transfer_function = np.abs((2 / np.pi) * np.arctan(((np.pi / 2) * self.v[i][j])))
        #   if rnd < V_shaped_transfer_function:
        #     self.Sol[i][j] = 1 - (self.Sol[i][j])
        #   else:
        #     self.Sol[i][j] = self.Sol[i][j]
        #   if rnd > self.r:
        #     self.Sol[i][j] = self.best[j]
        pass # end for dim

        Fnew = self.Func(self.Sol[i])
        rnd = np.random.uniform(0, 1)
        if (Fnew <= self.Fitness[i]) & (rnd < self.A):
          self.Sol[i] = self.Sol[i]
          self.Fitness[i] = Fnew
        if Fnew <= self.f_min:
          self.best = self.Sol[i]
          self.f_min = Fnew
          c = 1
          pass
        pass

      self.cg_curve[N_iter + 1] = self.f_min
      c=1
      pass  # end while
    return self.cg_curve
