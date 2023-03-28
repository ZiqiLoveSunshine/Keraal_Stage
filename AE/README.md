1. copy preprocessed data to the folder 'datasets/train_set' and 'datasets/test_set'.
2. use train.py with your parameter. e.g.: python train.py  --save_dir ./pretrained_AE0814after --epoch_num 40001.
3. when train process finished, use tensorboard to see the loss, command: tensorboard --logdir=pretrained_AE0814after /logs/ --port=6666
4. if you want to evaluate the test set, you use command: python eval.py
5. python visualization.py for generate graph or animation.