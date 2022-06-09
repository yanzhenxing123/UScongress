import yaml
import utils

base_path = utils.get_project_path()

with open(base_path + "\\config\\config.yaml", encoding="utf-8") as file:
    Config = yaml.full_load(file)
    MONGO = Config.get('Mongo')
    Kafka = Config.get('Kafka')
    Mysql = Config.get('Mysql')
