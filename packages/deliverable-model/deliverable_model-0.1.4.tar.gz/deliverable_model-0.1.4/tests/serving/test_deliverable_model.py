from deliverable_model.request import Request
from deliverable_model.serving.deliverable_model import DeliverableModel

import numpy as np


def test_serving(datadir):
    deliverable_model = DeliverableModel.load(datadir)

    request = Request(["abc", "cba"])

    response = deliverable_model.parse(request)

    assert np.all(
        response.data
        == [["tag-a", "tag-b", "tag-c"], ["tag-c", "tag-b", "tag-a"]]
    )
