import unittest
import nne
import torchvision
import torch
import numpy as np

class TFliteTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TFliteTests, self).__init__(*args, **kwargs)
    
    def test_tflite(self):
        input_shape = (1, 3, 64, 64)
        tflite_file = 'mobilenet.tflite'
        model = torchvision.models.mobilenet_v2(pretrained=True)
        dummy_input = torch.randn(input_shape)
        nne.cv2tflite(model , dummy_input, tflite_file)
        
        input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
        out_tflite = nne.infer_tflite(tflite_file, input_data)
        model.eval()
        out_pytorch = model(torch.from_numpy(input_data)).detach().cpu().numpy()
        np.testing.assert_allclose(out_tflite, out_pytorch, rtol=1e-03, atol=1e-05)        

if __name__ == "__main__":
    unittest.main()        
