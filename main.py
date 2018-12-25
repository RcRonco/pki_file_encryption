import rco.file_crypto as fcrypt

fcrypt.encrypt_file('/home/ron/workspace/Tensorflow_test_cc/models/faster_rcnn_inception_resnet_v2_atrous_coco_2018_01_28/frozen_inference_graph.pb', 'default.model', 'public.pem')
fcrypt.decrypt_file('default.model', 'frozen_inference_graph.pb', 'private.pem', 'GC::Encryption::Keys')
#fcrypt.encrypt_file('myfile.txt', 'myfile.encrypted.txt', 'public.pem')
