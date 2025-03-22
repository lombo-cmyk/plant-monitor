from dotenv import dotenv_values
from jinja2 import Environment, FileSystemLoader

config = dotenv_values(".env")
is_spi = (
    config["THERMISTOR"].lower() == "true" or config["PHOTORESISTOR"].lower() == "true"
)

environment = Environment(loader=FileSystemLoader("."), trim_blocks=True)
template = environment.get_template("docker-compose.yml.jinja2")

rendered = template.render(is_spi=is_spi)
print(f"Generating docker-compose file with arguments: is_spi:{is_spi}")
with open("docker-compose.yml", mode="w", encoding="utf-8") as f:
    f.write(rendered)
