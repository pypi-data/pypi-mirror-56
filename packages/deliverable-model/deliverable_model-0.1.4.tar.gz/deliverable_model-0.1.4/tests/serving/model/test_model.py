from deliverable_model.request import Request
from deliverable_model.response import Response
from deliverable_model.serving.model.model import Model

import numpy as np


def test_serving(datadir):
    metadata = {'version': '1.0', 'type': 'dummy_model', "custom_object_dependency": [], "converter_for_request": "", "converter_for_response": ""}
    model_obj = Model.load(datadir, metadata)

    request = Request([[1, 2, 3], [3, 2, 1]])
    response = model_obj.parse(request)

    assert np.all(response.data == Response([[11, 12, 13], [13, 12, 11]]).data)
