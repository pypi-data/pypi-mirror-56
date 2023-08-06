import re
import setuptools


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
    version = re.search(r'https:\/\/img\.shields\.io\/badge\/version-v([\d\.]+)-blue\.svg', long_description).group(1)

setuptools.setup(
    name="vlibras-translate",
    version=version,
    author="MoraesCaio (LAVID-UFPB)",
    author_email="caiomoraes.cesar@gmail.com",
    description="VLibras (LAVID-UFPB) translation module for translating brazilian portuguese to LIBRAS.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.vlibras.gov.br/",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'vlibras-translate=vlibras_translate.translation:main',
            # 'vlibras-translate-file=vlibras_translate.file_translation:main'
        ],
    },
    install_requires=[
        # 'Cython',  # precisa ser instalado manualmente antes
        'nltk',
        'unidecode',
        'pygtrie',
        'pyjnius',
        'pyparsing',  # sem esse pacote funciona, mas lança um warning
        'psutil',
        'hunspell;platform_system=="Linux"',  # https://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=install_requires#declaring-platform-specific-dependencies
        'interruptingcow',
    ],
    extras_require={
        'deeplearning': ['vlibras-deeplearning'],  # TODO: confirmar se será esse o nome do pacote
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Text Processing :: Linguistic",
        "Natural Language :: Portuguese (Brazilian)",
    ],
)
