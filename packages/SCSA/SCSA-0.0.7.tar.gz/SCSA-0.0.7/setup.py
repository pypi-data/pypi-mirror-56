import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SCSA",
    version="0.0.7",
    author="Taous-Meriem Laleg-Kirati, Julio Mario Orozco Lopez, Evangelos Piliouras, Abderrazak chahid, Peihao Li",
    author_email="taousmeriem.laleg@kaust.edu.sa ,jmorozcol@unal.edu.co, evangelos.piliouras@kaust.edu.sa, "
                 "abderrazak.chahid@kaust.edu.sa, "
                 "peihao.li@kaust.edu.sa",
    description="A novel algorithm for signal representation and denoising",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://emang.kaust.edu.sa/Pages/Home.aspx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
