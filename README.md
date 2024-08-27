# bind_cpp

1. Install poetry
`pip install poetry`

2. Install dependencies
`poetry install`

3. Build .so file by running
`poetry run python setup.py build_ext --inplace`

4. Move the generated .so file to `bind_cpp` folder and rename it to html_generator.so