import pytest
from memcnn.data.sampling import NSamplesRandomSampler
import torch.utils.data as data
import numpy as np


@pytest.mark.parametrize('nsamples,data_samples', [(1, 1), (14, 10), (10, 14), (5, 1), (1, 5), (0, 10)])
def test_random_sampler(nsamples, data_samples):

    class TestDataset(data.Dataset):
        def __init__(self, elements):
            self.elements = elements

        def __getitem__(self, idx):
            return idx, idx

        def __len__(self):
            return self.elements

    datasrc = TestDataset(data_samples)
    sampler = NSamplesRandomSampler(datasrc, nsamples=nsamples)
    count = 0
    elements = []
    for e in sampler:
        elements.append(e)
        count += 1
        if count % data_samples == 0:
            assert len(np.unique(elements)) == len(elements)
            elements = []
    assert count == nsamples
    assert len(sampler) == nsamples
    assert sampler.__len__() == nsamples
