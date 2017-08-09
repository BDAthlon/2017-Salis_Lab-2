import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import random
import math
from collections import namedtuple

glob = namedtuple('glob','x y radius color')

class Puzzle(object):

    # difficulty is an integer on a scale from 1-10
    # {'easy':3,'medium':5,'hard':7}

    globs = []
    axes = []
    xlim = (0,200)
    ylim = (0,200)

    def __init__(self,difficulty=10):
        self.difficulty = difficulty
        self._generate_globs()

    def _generate_globs(self):
        i = math.floor(20 - 0.75*self.difficulty)
        self.nglobs = random.randint(i-3,i+3)
        for _ in xrange(self.nglobs):
            rmin = math.floor((20.0 - 5.0)/self.difficulty**0.5)
            rmax = math.floor((20.0 + 5.0)/self.difficulty**0.5)
            r = random.randint(rmin,rmax)
            x = random.uniform(self.xlim[0]+r,self.xlim[1]-r)
            y = random.uniform(self.ylim[0]+r,self.ylim[1]-r)
            self.globs.append(glob(x=x,y=y,radius=r,color='green'))

    def plot(self,save=False,initFigureName=None):

        fig,ax = plt.subplots()
        ax = plt.axes(xlim=self.xlim,ylim=self.ylim)
        plt.gca().set_aspect('equal', adjustable='box')

        for glob in self.globs:
            circle = plt.Circle((glob.x,glob.y),glob.radius,color=glob.color)
            ax.add_artist(circle)

        plt.show()
        if save:
            fig.savefig(initFigureName)

class Graphics(object):

    curves = []
    xlim = (0,200)
    ylim = (0,200)

    def __init__(self,t,reporters,globs):
        self.t = t
        self.reporters = reporters
        self.globs = globs
        self.N = len(reporters)
        self.G = len(globs)

    def generate(self,save=False,filename=None):

        # set up the figure, the axis, and the plot element we want to animate
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=self.xlim, ylim=self.ylim)
        plt.gca().set_aspect('equal', adjustable='box')

        for glob in self.globs:
            self.curves.append(plt.Circle((glob.x,glob.y),glob.radius,color=glob.color))

        for _ in self.reporters:
            self.curves.append(plt.plot([],[])[0])

        # call the animator
        # blit=True means only re-draw the parts that have changed
        anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init,
                                       frames=len(self.t), interval=1e-7, repeat_delay=1e3, blit=True)

        plt.show()

        # save the animation as an mp4
        # requires ffmpeg or mencoder to be installed
        # extra_args ensure that the x264 codec is used, so that the video can be embedded
        # in html5. You made need to adjust this for your system. For more information, see
        # http://matplotlib.sourceforge.net/api/animation_api.html
        if save:
            if filename is None:
                filename = 'unnamed_animation.mp4'
            anim.save(filename, fps=30, extra_args=['-vcodec', 'libx264'])

    # initialization function: plot the background of each frame
    def init(self):

        # initialize globs
        for indx in xrange(self.G):
            glob = self.globs[indx]
            self.curves[indx].center = (glob.x,glob.y)
            self.ax.add_patch(self.curves[indx])
            self.curves[indx].set_facecolor(glob.color)

        # initialize curves
        for indx in xrange(self.N):
            self.curves[self.G+indx].set_data([],[])

        return self.curves

    # animation function (called sequentially)
    def animate(self,i):

        for indx in xrange(self.G):
            glob = self.globs[indx]

            # check logic if delete globs!
            # delete_glob_check()
            # if i == 100:
            #     self.curves[indx].set_facecolor('white')

            self.curves[indx].center = (glob.x,glob.y)
            self.ax.add_patch(self.curves[indx])

        for indx in xrange(self.N):
            t = self.t[:i]
            y = self.reporters[indx][:i]
            self.curves[self.G+indx].set_data(t,y)

        return self.curves


if __name__ == "__main__":
    pass