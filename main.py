from typing import Dict
import pandas as pd
import re
import wget
from colorama import Fore, Style
from os.path import exists
import ssl
from tkinter import Tk
from tkinter.filedialog import askdirectory

screenSaversPath = 'screenSavers/'

class Screensaver:
    def __init__(self, url, name) -> None:
        self.url = url
        self.name = self.parseName(name)
        self.type = self.parseType(name)

    def parseName(self, name) -> str:
        return re.sub(r'\s[a-zA-Z0-9_-]*\.', '.', name)

    def parseType(self, name) -> str:
        type = re.findall(r'\.[a-z]*', name)[0]
        self.name = self.name.replace(type, '')
        return type

    def download(self, overwrite = True) -> None:
        if overwrite or not self.exists():
            fileLocation = self.getFileLocation()

            print(f'Now downloading: {Fore.BLUE}{self.name}{Style.RESET_ALL}')
            print(f'Downloading from: {Fore.YELLOW}{self.url}{Style.RESET_ALL}')
            print(f'Downloading to: {Fore.MAGENTA}{fileLocation}{Style.RESET_ALL}')

            ssl._create_default_https_context = ssl._create_unverified_context
            wget.download(self.url, fileLocation)

            print(f'\n{Fore.GREEN}Downloaded!\n{Style.RESET_ALL}')
        else:
            print(f'{Fore.GREEN}Screensaver is already downloaded!{Style.RESET_ALL}')

    def getFileName(self) -> str:
        return f'{self.name}{self.type}'

    def getFileLocation(self) -> str:
        return f'{screenSaversPath}{self.getFileName()}'

    def exists(self) -> bool:
        return exists(self.getFileLocation())

    def __str__(self) -> str:
        return f'name: {self.name} \nurl: {self.url} \ntype: {self.type}\n'

class Downloader:
    manifest:pd.DataFrame = None
    def readCSVFile(self):
        self.manifest = pd.read_csv(
            'https://gist.githubusercontent.com/dmn001/e99027118fe3267596e93132971cbe04/raw/0109e0a71db8ad9e91609085873c51de072be915/urls.csv',
            # 'https://raw.githubusercontent.com/dmn001/apple_tv_screensaver_downloader/master/urls.csv',
            names=['url', 'name'])

    def convertToScreenSavers(self) -> Dict[str, Screensaver]:
        screenSavers : Dict[str, Screensaver] = {}

        def addToDict(screenSaver : Screensaver) -> None:
            name : str = screenSaver.name
            index = 2

            while screenSavers.get(name) != None:
                if (index == 2):
                    name = f'{name} {index}'
                else:
                    name = re.sub(r'[0-9]+', f'{index}', name)
                index += 1
            
            screenSaver.name = name
            screenSavers[name] = screenSaver

        for index, row in self.manifest.iterrows():
            screenSaver : Screensaver = Screensaver(row['url'], row['name'])
            addToDict(screenSaver)

        return screenSavers



def main():
    global screenSaversPath
    
    screenSavers : Dict[str, Screensaver] = []

    screenSaversPath = askdirectory(title='Select Folder to store the screensavers in.')

    downloader = Downloader()

    downloader.readCSVFile()

    screenSavers = sorted(downloader.convertToScreenSavers().items())

    for key, value in screenSavers:
        value.download(False)

if __name__ == "__main__":
    main()
