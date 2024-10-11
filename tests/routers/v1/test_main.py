import pytest
from fastapi.templating import Jinja2Templates
from app.routers.v1.main import templates_path

def test_jinja2_templates_initialization():
    templates = Jinja2Templates(directory=str(templates_path))
    assert isinstance(templates, Jinja2Templates)
    assert templates.directory == str(templates_path) # pylint: disable=no-member

def test_templates_path_exists():
    assert templates_path.exists()
    assert templates_path.is_dir()

def test_templates_directory_contains_files():
    template_files = list(templates_path.glob('*.html'))
    assert len(template_files) > 0

def test_jinja2_templates_render():
    templates = Jinja2Templates(directory=str(templates_path))
    template = templates.get_template("test_template.html")
    rendered = template.render({"variable": "test"})
    assert "test" in rendered

@pytest.mark.parametrize("invalid_path", [
    "nonexistent_path",
    "/tmp",
    __file__,
])
def test_jinja2_templates_invalid_directory(invalid_path):
    with pytest.raises(ValueError):
        Jinja2Templates(directory=invalid_path)
