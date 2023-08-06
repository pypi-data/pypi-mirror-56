from setuptools import setup  # , find_packages

# Clasificadores: https://pypi.org/pypi?%3Aaction=list_classifiers


def get_readme():
    readme_txt = ""
    try:
        readme_txt = open('README.md').read()
    except Exception as e:
        print("Ha ocurrido un inconveniente: " + str(e))
    return readme_txt


setup(
    name='sicomor-especificaciones',
    version='0.1.1',
    author='Ecom Developers',
    author_email='simono@ecom.com.ar',
    description=('Especificaciones para Sistema de Control de Inventario'),
    long_description=get_readme(),
    license='BSD',
    keywords='sicomor inventario recursos',
    url='http://git.ecom.com.ar/ibanezlucas/sicomor-especificaciones',
    packages=['sicomor_especificaciones', ],
    # packages=find_packages(),
    package_data={
        # 'starwars_ipsum': ['*.txt']
    },
    install_requires=[],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ]
)
