from memcnn.trainers.classification import train
from memcnn.experiment.manager import ExperimentManager
from memcnn.data.cifar import get_cifar_data_loaders
from memcnn.utils.loss import CrossEntropyLossTF
import torch
from torchvision.datasets.cifar import CIFAR10


def test_train(tmp_path):
    expdir = str(tmp_path / "testexp")
    tmp_data_dir = str(tmp_path / "tmpdata")
    num_klasses = 10

    class TestModel(torch.nn.Module):
        def __init__(self, klasses):
            super(TestModel, self).__init__()
            self.conv = torch.nn.Conv2d(3, klasses, 1)
            self.avgpool = torch.nn.AvgPool2d(32)
            self.klasses = klasses

        def forward(self, x):
            return self.avgpool(self.conv(x)).reshape(x.shape[0], self.klasses)

    model = TestModel(num_klasses)
    optimizer = torch.optim.SGD(params=model.parameters(), lr=0.01)
    manager = ExperimentManager(expdir, model, optimizer)
    manager.make_dirs()

    train_loader, test_loader = get_cifar_data_loaders(CIFAR10, tmp_data_dir, 40000, 2, 0)
    loss = CrossEntropyLossTF()

    train(manager,
          train_loader,
          test_loader,
          start_iter=39999,
          disp_iter=1,
          save_iter=1,
          valid_iter=1,
          use_cuda=False,
          loss=loss)
