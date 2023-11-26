import xml.etree.ElementTree as ET
import os

# Копирует строки из одного XML-файла в другой.
# Принимает путь к файлу-донору и путь к файлу-приемнику
# Оба файла должны быть корректными xml-файлами

def importXml(sourceFile: str, targetFile: str,):
    if _correct(sourceFile) and _correct(targetFile):
        _copyElements(sourceFile, targetFile)

# Проверяет на корректность переданный файл
def _correct(fileName: str):
    if not os.path.isfile(fileName):
        print(fileName + ' not exist')
        return False
    if not fileName.endswith('.xml'):
        print(fileName + ' is not XML. Check file')
        return False
    else:
        return True

# Предлагает заменить строку, если такая уже существует в файле назначения.
def _createOrUpdate(targetRoot: ET.Element, item: ET.Element, targetFile:str):
    isNewString = True
    key = list(item.attrib.keys())[0]
    stringName = item.attrib.get(key)
    for oldItem in targetRoot.findall('string'):
        key = list(oldItem.attrib.keys())[0]
        oldString = oldItem.attrib.get(key)
        if oldString == stringName:
            isNewString = False
            # в старом файле уже есть эта строка
            print('String ' + oldString + ' exist in target file ' + targetFile)
            action = input('Print `y` to repalce or any key to continue: ')
            if action == 'y':
                oldItem.text = item.text
            break
    if isNewString:
        strValue = ET.Element(item.tag, name=stringName)
        strValue.text = item.text
        targetRoot.append(strValue)
        ET.indent(targetRoot)



# Копирует элементы одного XML-дерева
# в другое
def _copyElements(sourceFile: str, targetFile: str):
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    sourceTree = ET.parse(sourceFile)
    targetTree = ET.parse(targetFile, parser)
    sourceRoot = sourceTree.getroot()
    targetRoot = targetTree.getroot()
    for item in sourceRoot:
        if "function Comment" in str(item.tag):
            print(item.text)
        _createOrUpdate(targetRoot, item, targetFile)
    ET.indent(targetRoot)
    etree = ET.ElementTree(targetRoot)
    myfile = open(targetFile , "wb")
    etree.write(myfile, encoding='utf-8', xml_declaration=True)