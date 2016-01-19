from jinja2 import Environment, FileSystemLoader

jinja2_env = Environment(loader=FileSystemLoader('templates'),auto_reload=True)