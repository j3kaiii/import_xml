from src import copy_xml_tree as cp
import os
import glob

# Получаем все обозначения языков
def _getLangs(targetDir: str):
    return os.listdir(targetDir)

# Получаем файл из sourcePath по обозначению языка.
# Некорорые обозначения из sourcePath нужно смапить на используемые в проекте
# no(res) - nb(proj)
# iw(res) - he(proj)
# pt(res) - pt_BR(proj)
# sr(res) - sr_Latin(proj)
# Проверь имя файла, если нужно - поправь. Суффикс должен быть `_xx_`
def _getSourceByLang(lang: str, sourceFiles: list[str], sourcePath: str):
    suffix = ''
    match lang:
        case 'nb':
            suffix = '_no_'
        case 'he':
            suffix = '_iw_'
        case 'pt_BR':
            suffix = '_pt_'
        case 'sr_Latn':
            suffix = '_sr_'
        case 'zh_CN':
            suffix = '_zh-CN_'
        case 'zh_TW':
            suffix = '_zh-TW_'
        case _:
            suffix = '_' + lang + '_'
    for item in sourceFiles:
        if item.__contains__(suffix):
            return sourcePath + item
    return ''

# Получаем файл из targetPath по обозначению языка
def _getTargetByLang(lang:str, targetPath: str):
    targetFileName = '/intl.xml'
    res = targetPath + lang + targetFileName
    if os.path.isfile(res):
        return res
    else:
        return ''

# Идем пить пиво и смотреть Сверхъестественное

def run():
    # Получаем директорию с ресурсами
    # Тут все файлы хранятся вместе, иимеют суффикс равный обозначению языка
    # Например: *_ko_*.xml -- _ko_ - корейский язык

    # !!! в директории не должно быть поддиректорий, только файлы с переводами !!!
    sourcePath = ''
    query = 'Source dir (end with /) or `q` to exit: '
    while not os.path.isdir(sourcePath):
        sourcePath = input(query)
        if sourcePath == 'q':
            exit()
        if not glob.glob('*.xml', root_dir=sourcePath):
            print('No XML found in selected dir. Enter correct path')
            sourcePath = input(query)

    # если лень вводить в консоли
    # код выше комментим, а этот открываем
    # sourcePath = 'путь/к/файлам/diffs/'

    sourceFiles = os.listdir(sourcePath)

    # Получаем директорию, куда нужно скопировать ресурсы
    # Тут файлы хранятся по поддиректориям по обозначению языка
    # Файлы имеют одно и то же имя
    # Например:
    # ar:
    #   intl.xml
    # bg:
    #   intl.xml

    targetPath = ''
    while not os.path.isdir(targetPath):
        print('Path to dir, that contains subdirs with `intl` xmls')
        targetPath = input('(end with /): ')
        if not glob.glob('*/intl.xml', root_dir=targetPath):
            print('No intl.xml found.')

    # чтобы не вводить вручную
    # код выше комментим, а этот открываем
    # targetPath = 'путь/к/файлам/l10n/google_play/'

    langs = _getLangs(targetPath)

    for lang in langs:
        s = _getSourceByLang(lang, sourceFiles, sourcePath)
        t = _getTargetByLang(lang, targetPath)
        if s == '':
            print('Not found source for lang ' + lang)
            continue
        elif t == '':
             print('Not found resource for lang ' + lang)
             continue
        else:
            # Копируем строки из sourcePath в targetPath
            cp.importXml(s, t)
