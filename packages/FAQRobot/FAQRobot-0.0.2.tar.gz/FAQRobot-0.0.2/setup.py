import setuptools

with open('README.rst', 'r', encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='FAQRobot',
    version='0.0.2',
    description='guoruili markdown editor',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='guoruili',
    author_email='guoruili@mail.emotibot.com',
    url='https://markdown.felinae.net',
    keywords='FAQRobot markdown editor editormd',
    packages=setuptools.find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=()
)
