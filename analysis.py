import numpy as np
import matplotlib.pyplot as plt
from DLA import Simulator

class Dataset:
    
    def __init__(self, nSamples: int):
        '''
        initializes a dataset class
        
        input:
            nSamples: no. of samples in the dataset
        '''
        self.nSamples = nSamples
    
    def generate_images(self, parameter_list: list):
        '''
        generate images from the simulation

        input:
            parameter_list: list of the parameters to run the simulation
        
        output:
            images: a 2d numpy array of shape (len(parameter_list), M, M)
        '''
        images = []
        for i in parameter_list:
            simulation = Simulator(stickiness=i)
            images.append(simulation.run())
        return np.array(images)
    
    def extractFeature(self, arrays: np.ndarray, q: int):
        centralSection = self.getCentralSection(arrays,q)
        centralParticleDensity = centralSection.sum(axis = (1, 2))/(q**2)
        return centralParticleDensity

    def getCentralSection(self, arrays: np.ndarray, q: int):
        [nSamples, M, N] = arrays.shape
        if M != N:
            print('not a sqare')
        midPoint = int(M/2)
        centralSection = arrays[:, int(midPoint-(q/2)):int(midPoint+(q/2)), \
                                int(midPoint-(q/2)):int(midPoint+(q/2))]
        return centralSection
    
    def plot

arrays  = []
features = []
stickiness = np.linspace(0.001, 0.05, 51)
for file in files4:
    array = np.load(file, allow_pickle = True)
    arrays.append(array)


arrays = np.array(arrays)

'''
print(features)
print(len(stickiness), len(features))


'''

'''features = extractFeature(arrays, q=7)
print(max(features))
plt.scatter(features/7**2, stickiness)
plt.title('q=7')
plt.ylabel('stickiness')
plt.xlabel('N_q/q^2')
plt.show()'''
from scipy import stats
from statsmodels.regression import linear_model
from statsmodels.api import add_constant
features = extractFeature(arrays, q=35)
model = linear_model.OLS(stickiness, add_constant(features))
results = model.fit()
print(results.summary())
#print(results.pvalues)
'''
N_q = []
p_values = []
from scipy import stats
for i in range(15, 3, -1):
    print(i)
    features = extractFeature(arrays, q=i)
    N_q.append(i)
    p_values.append(stats.pearsonr(stickiness, features)[1])'''

'''plt.scatter(N_q, p_values)
plt.title('p_values vs N_q')
plt.xlabel('N_q')
plt.ylabel('p_value')
plt.show()'''

#ideally 20+, 300
#or 6+ , 40
# -0.95 corr
# -0.0026*N_q + 0.1233 lin reg