import yaml

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)    # load the yaml file safely in 'r' read mode
    return config       