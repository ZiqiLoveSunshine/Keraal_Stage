1. copy preprocessed data to the folder 'datasets/train_set' and 'datasets/test_set'.
2. use train.py with your parameter. e.g.: python train.py --dis_linear true --save_dir ./pretrained_less_deep0814after --model deep --epoch_num 40001 --lambda_rec 10 --lambda_cycle 4 --lambda_gan 1
3. when train process finished, use tensorboard to see the loss, command: tensorboard --logdir=pretrained/logs/ --port=6666
4. if you want to evaluate the test set, you use command: python eval.py
5. python visualization.py for generate graph or animation.