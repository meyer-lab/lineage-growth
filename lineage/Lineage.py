# author : shakthi visagan (shak360), adam weiner (adamcweiner)
# description: a file to hold the lineage class and population class

import sys
import math
import numpy as np
import scipy.stats as sp
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from .CellNode import CellNode as c, generateLineageWithNum, generateLineageWithTime

class Lineage:
    def __init__(self):
        self.tree = list()
    
    def loadTree(self, csv_file):
        #TODO: write function to import a tree from external file
        pass
    
    def plotTree(self):
        '''plots a lineage tree based on list generated by a generate method or from the imported file'''
        lineage = self.tree # assign variable to tree list
        
        timebarpos = 0
        endTime = 0
        
        plt.figure(figsize=(16,9)) # set up figure for plotting, width and height in inches
        
        for cell in lineage:
            if cell.plotVal < timebarpos:
                timebarpos = cell.plotVal
                
            if cell.endT > endTime:
                endTime = cell.endT
            
            plt.plot([cell.startT,cell.endT],[cell.plotVal,cell.plotVal], 'k') # plot the cell lifetime
            
            if cell.isRootParent():
                plt.plot(cell.startT, cell.plotVal, 'bo', markersize=10) # plot the root parent cell as a blue dot
            
            if cell.fate:
                #TODO: replace the below if statement with the isUnfinished() method for clarity
                if not cell.isUnfinished(): # check for nan when some cells don't get a chance to be assigned their fate, before the experiment ends
                    plt.plot([cell.endT,cell.endT],[cell.left.plotVal,cell.right.plotVal],'k') # plot a splitting line if the cell divides
            
            else:
                plt.plot(cell.endT, cell.plotVal, 'ro', markersize=5) # plot a red dot if the cell dies
                
            if cell.isUnfinished():
                plt.plot(cell.endT, cell.plotVal, 'go', markersize=5) # plot a green dot if the unfinished
            
        for cell in lineage:
            plt.plot([cell.startT,cell.endT], [timebarpos-0.1,timebarpos-0.1], linewidth=8, alpha=0.25)
        
        plt.yticks([])        
        plt.title("Simulated Lineage Tree with Bernoulli Parameter of ____ and Gompertz Parameters _________")
        plt.xlabel('Time (Hours)')
        plt.tight_layout()
        #plt.savefig('foo.png')
        plt.show()
        
        
def generatePopulationWithNum(numLineages, numCells, locBern, cGom, scaleGom):
    #TODO: go over how to organize and make various generate() methods
    ''' generates list given a maximum number of lineage trees, and parameters to describe the underlying distribution'''
    
    #create first lineage
    lineage0 = Lineage()
    
    # put first lineage in list
    population = [lineage0]
    
    while len(population) < numLineages:
        tempLineage = Lineage()
        tempLineage.tree = generateLineageWithNum(numCells, locBern, cGom, scaleGom)
        population.append(tempLineage)
    
    return(population)


def generatePopulationWithTime(numLineages, experimentTime, locBern, cGom, scaleGom):
    #TODO: go over how to organize and make various generate() methods
    ''' generates list given a maximum number of lineage trees, and parameters to describe the underlying distribution'''
    
    #create first lineage
    lineage0 = Lineage()
    
    # put first lineage in list
    population = [lineage0]
    
    while len(population) < numLineages:
        tempLineage = Lineage()
        tempLineage.tree = generateLineageWithTime(experimentTime, locBern, cGom, scaleGom)
        population.append(tempLineage)
    
    return(population)
        
class Population:
    def __init__(self, option, numLineages, numCellsOrTime, locBern, cGom, scaleGom):
        if option == "num":
            self.group = generatePopulationWithNum(numLineages, numCellsOrTime, locBern, cGom, scaleGom)
        if option == "time":
            self.group = generatePopulationWithTime(numLineages, numCellsOrTime, locBern, cGom, scaleGom)
        
    def loadPopulation(self, csv_file):
        #TODO: write function to import a population from external file
        pass
    
    def plotPopulation(self):
        '''plots a population growth'''
        #TODO
        pass
    
    def doublingTime(self):
        '''For a given population, calculates the population-level growth rate (i.e. doubling time)'''
        #TODO
        pass
    
    def bernoulliParameterEstimatorAnalytical(self):
        '''Estimates the Bernoulli parameter for a given population using MLE analytically'''
        population = self.group # assign population to a variable
        fate_holder = [] # instantiates list to hold cell fates as 1s or 0s
        for lineage in population: # go through every lineage in the population
            for cell in lineage.tree: # go through ever cell in the lineage
                if not cell.isUnfinished(): # if the cell has lived a meaningful life and matters
                    fate_holder.append(cell.fate*1) # append 1 for dividing, and 0 for dying
                
        return ( sum(fate_holder) / len(fate_holder) ) # add up all the 1s and divide by the total length (finding the average)
            
    def bernoulliParameterEstimatorNumerical(self):
        '''Estimates the Bernoulli parameter for a given population using MLE numerically'''
        population = self.group # assign population to a variable
        fate_holder = [] # instantiates list to hold cell fates as 1s or 0s
        for lineage in population: # go through every lineage in the population
            for cell in lineage.tree: # go through ever cell in the lineage
                if not cell.isUnfinished(): # if the cell has lived a meaningful life and matters
                    fate_holder.append(cell.fate*1) # append 1 for dividing, and 0 for dying
                            
        def LogLikelihoodBern(locBernGuess, fate_holder):
            return(np.sum(sp.bernoulli.logpmf(k=fate_holder, p=locBernGuess)))
        
        nllB = lambda *args: -LogLikelihoodBern(*args)
        
        res = minimize(nllB, x0=0.5, bounds=((0,1),), method="SLSQP", args=(fate_holder))
        
        return(res.x[0])
        
    def gompertzParameterEstimatorNumerical(self):
        '''Estimates the Gompertz parameters for a given population using MLE numerically'''
        population = self.group # assign population to a variable
        tau_holder = [] # instantiates list to hold cell fates as 1s or 0s
        for lineage in population: # go through every lineage in the population
            for cell in lineage.tree: # go through ever cell in the lineage
                if not cell.isUnfinished(): # if the cell has lived a meaningful life and matters
                    tau_holder.append(cell.tau) # append the cell lifetime
                            
        def LogLikelihoodGomp(gompParams, tau_holder):
            return(np.sum(sp.gompertz.logpdf(x=tau_holder,c=gompParams[0], scale=gompParams[1])))
        
        nllG = lambda *args: -LogLikelihoodGomp(*args)
        
        res = minimize(nllG, x0=[1,1e3], bounds=((0,5),(0,None)), method="SLSQP", options={'maxiter': 1e6}, args=(tau_holder))
        
        return(res.x)