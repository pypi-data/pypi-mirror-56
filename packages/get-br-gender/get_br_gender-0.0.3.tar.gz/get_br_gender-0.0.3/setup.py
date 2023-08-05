from distutils.core import setup

setup(

    name='get_br_gender',
    packages=['get_br_gender'],
    data_files=[('get_br_gender', ['get_br_gender/nome_genero.xlsx'])],
    version='0.0.3',
    license='MIT',
    description='Classify the gender through the first name. Trained in Brazilian names',
    author='Pável Emmanuel Pereira Lelis and Gabriel Rodrigues dos Santos',
    author_email='pavel.ep.lelis@gmail.com',
    url='https://github.com/pavellelis/get-br-gender',
    download_url='https://github.com/pavellelis/get-br-gender/archive/v0.0.3.tar.gz',
    keywords=['brazilian names', 'gender', 'feature engineering'],
    install_requires=[
        'unidecode', 'pandas', 'xlrd'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
