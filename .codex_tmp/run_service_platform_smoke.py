import os
import runpy

runpy.run_path(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "Macros-de-Freecad",
        "FacilArquitecturaWB",
        "tests",
        "freecad_service_platform_smoke.py",
    ),
    run_name="__main__",
)
