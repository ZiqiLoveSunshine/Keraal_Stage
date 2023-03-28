def create_model(args, dataset):
    from models.architecture2 import DEEP_model
    return DEEP_model(args, dataset)
