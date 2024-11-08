import numpy as np

dataset = np.load("../Nodule_data/DataSet_all.npy", allow_pickle=True)
print(dataset.shape)

for i in range(dataset.shape[0]):
    filename = "../Nodule_data/nodule_{}.npy".format(i)
    np.save(filename, dataset[i,0])