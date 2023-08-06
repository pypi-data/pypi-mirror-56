import setuptools

pkg_name = "ephys_viz"

setuptools.setup(
    name=pkg_name,
    version="0.9.3",
    author="Jeremy Magland",
    description="Neurophysiology visualization widgets",
    packages=setuptools.find_packages(),
    scripts=['bin/ephys_viz'],
    include_package_data=True,
    install_requires=[
        'simplejson',
        'jupyter',
        'numpy',
        'mountaintools',
        'kachery',
        'scipy',
        'vtk',
        'imageio',
        'imageio-ffmpeg',
        'spikeextractors',
        'h5_to_json',
        'h5py'
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)