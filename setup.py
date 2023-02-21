from setuptools import setup, find_namespace_packages

with open('README.md','r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='personal_assistant_cli_bot',
    version='1.0.4',
    description='A personal assistant with a command line interface',
    # long_description=long_description,
    url='https://github.com/tetianakondra/Python_core_Team_3/blob/main/Python_core_Team_3.py',
    author='Tetiana Kondra, Natalia Sokil, Yevhen Kosarev, Oleksandr Chepkanich, Andrii Holubenko',
    author_email='t_prischepa@ukr.net, sokilnatalka@gmail.com, kossik89@gmail.com, a.chepkanich@gmail.com, andrii.holub82@gmail.com',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    packages=find_namespace_packages(),
    data_files=[
        ('personal_assistant', ['personal_assistant/NoteBook.txt'],), ('docs', ['docs/main_menu.jpg'],)],
    include_package_data=True,
    install_requires=['prompt_toolkit', 'console-menu', 'termcolor'],
    entry_points={'console_scripts': [
        'pacb = personal_assistant.Main_menu:main_menu']}
)
