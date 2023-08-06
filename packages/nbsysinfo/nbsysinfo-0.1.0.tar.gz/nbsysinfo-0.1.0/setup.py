import setuptools

setuptools.setup(
    name="nbsysinfo",
    version='0.1.0',
    url="https://github.com/Yohox/nbsysinfo",
    author="yoho",
    description="Add SysInfo to your jupyter notebook.",
    packages=setuptools.find_packages(),
    install_requires=[
        'psutil',
        'notebook'
    ],
    data_files=[
        ('etc/jupyter/jupyter_notebook_config.d', ['nbsysinfo/etc/server_sysinfo.json']),
        ('etc/jupyter/nbconfig/notebook.d', ['nbsysinfo/etc/nbext_sysinfo.json'])
    ],
    zip_safe=False,
    include_package_data=True
)
