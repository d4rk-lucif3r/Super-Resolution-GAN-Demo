from servicefoundry import Build, DockerBuild, Resources, Service
import os

os.environ["TFY_HOST"] = "https://app.truefoundry.com/"
os.environ["TFY_API_KEY"] = "<your-api-key>"  # replace this


service = Service(
    name="image-colorizer",
    image=Build(
        build_spec=DockerBuild(),
    ),
    ports=[{"port": 8080}],
    resources=Resources(memory_limit=1000, memory_request=500,
                        cpu_limit=2, cpu_request=1.5),
)
service.deploy(workspace_fqn="<your-workspace-fqn>")
