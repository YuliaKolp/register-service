from scripts_to_generate_project.utils import run_command


def genearte_api(package_name: str, swagger_url: str, templates: str| None=None) ->None:
    command = ["java", "-jar", "openapi-generator-cli-7.16.0.jar",
               "generate", "-i", swagger_url,
               "-g", "python",
               "-o", package_name,
               "--library", "asyncio",
               "--package-name", package_name,
               "--skip-validate-spec",
               ]
    if templates:
        command.extend(["-t", templates])
    run_command(command)


swagger_url = "http://185.185.143.231:8085/register/openapi.json"
templates = "C:\\Users\\skolp\\PycharmProjects\\openapi-generator\\modules\\openapi-generator\\src\\main\\resources\\python"


genearte_api(package_name='register_service', swagger_url=swagger_url)