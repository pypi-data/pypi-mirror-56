from torch.utils.data import Dataset
from learner.data import Data


def test_data_init():
    ds = Dataset()
    data = Data(ds)
    assert isinstance(data, Data)
