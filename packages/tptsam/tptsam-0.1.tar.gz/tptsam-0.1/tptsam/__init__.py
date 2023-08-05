import os

def getArrayFromText(path):
    f = open(path, "r")
    line = f.readlines()
    array=[]
    for linha in line:
            array.append(linha)
    return array

def createPypiPKG(nome):
    os.mkdir(nome)
    readmeMd =['# {}\n'.format(nome),'\n','\n','Brief explanation\n','\n','License\n','----\n','\n','MIT\n','\n',
               '\n','**Samuelson Esteves Vieira**\n','\n']
    licenseText = ['MIT License\n',
    '\n',
    'Copyright (c) 2019 Samuelson Esteves Vieira\n',
    '\n',
    'Permission is hereby granted, free of charge, to any person obtaining a copy\n',
    'of this software and associated documentation files (the "Software"), to deal\n',
    'in the Software without restriction, including without limitation the rights\n',
    'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n',
    'copies of the Software, and to permit persons to whom the Software is\n',
    'furnished to do so, subject to the following conditions:\n',
    '\n',
    'The above copyright notice and this permission notice shall be included in all\n',
    'copies or substantial portions of the Software.\n',
    '\n',
    'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n',
    'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n',
    'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n',
    'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n',
    'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n',
    'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n',
    'SOFTWARE\n',]
    setupText =('from setuptools import setup\n','\n','\n',"setup(name='{}',\n".format(nome),"      version='0.1',\n",
                "      description='InsertDescription',\n",
                "      url='https://github.com/samuelsonsev/{}',\n".format(nome),"      author='Samuelson Esteves Vieira',\n",
                "      author_email='none@example.com',\n","      license='MIT',\n","      packages=['{}'],\n".format(nome),
                '      zip_safe=False)\n')

    setup = open("setup.py", "w+")
    setup.writelines(setupText)
    setup.close()

    initFile =open(nome +"/"+"__init__.py","w+")
    initFile.close( )

    license = open("LICENSE.txt", "w+")
    license.writelines(licenseText)
    license.close()

    readmeMdFile = open("README.md", "w+")
    readmeMdFile.writelines(readmeMd)
    readmeMdFile.close()
