# -*- coding: utf-8 -*-
# -------------------------------------------------------------------#
#         	Создание карты тестового покрытия.                       #
#--------------------------------------------------------------------#
#     P.S.: -Чего хочешь?                                            #
#           -Марионеточную машинку.                                  #
#           -Это че еще за хуйня?                                    #
#           -Марионеточную машинку.                                  #
#           -Я понял. Марионеточную машинку. Отлично.                #
#--------------------------------------------------------------------#
import funcy

__author__ = 'm.senchuk'


import os
import fnmatch
import json


class GetCoverage():

    MASK_PY = 'test_*.py'
    PATTERN_DOC = '"""'
    PATTERN_TEST_METHOD = "def test_"
    PATTERN_CLASS = "class "
    PATTERN_END = "("
    DIRECTORY = '.\\tests\\front_office\\not_sorted'
    #DIRECTORY = 'C:\Data\ToDeveloper\QA_PROJECTS\\api-tests\\tests\\front_office'
    P_FEATURE = "Feature:"
    P_STORY = "Story:"
    P_SKIP = "@skip"
    P_PRIORITY = "@priority"
    P_END = ")"

    def __init__(self):
        pass

    def get_feature(self, data, start_pos=0):
        """ Получить feature из файла
        :return:
        """
        first_class_position = data.find(self.PATTERN_CLASS)
        doc_open_position = data.find(self.PATTERN_DOC)
        doc_close_position = data.find(self.PATTERN_DOC, len(self.PATTERN_DOC), first_class_position)
        doc_feature = data[doc_open_position+len(self.PATTERN_DOC):doc_close_position]
        list_desc = doc_feature.split('Description:')
        if len(list_desc) == 2 and doc_close_position != -1:
            feature_description = self.editing(list_desc[1])
        else:
            feature_description = None
        list_name = list_desc[0].split(self.P_FEATURE)
        if len(list_name) == 2 and doc_close_position != -1:
            feature_name = self.editing(list_name[1])
        else:
            feature_name = None
        return feature_name, feature_description

    def get_class(self, data, start_pos=0):
        """ Получить класс.
        :param data:
        :return:
        """
        class_start_position = data.find(self.PATTERN_CLASS, start_pos)
        class_end_position = data.find(self.PATTERN_END, class_start_position+start_pos)
        name_class = data[class_start_position+len(self.PATTERN_CLASS)+start_pos:class_end_position+start_pos]
        name_c = self.editing(name_class)
        first_method_position = data.find(self.PATTERN_TEST_METHOD)
        doc_start_position = data.find(self.PATTERN_DOC, class_end_position, first_method_position)
        doc_end_position = data.find(self.PATTERN_DOC, doc_start_position+start_pos+len(self.PATTERN_DOC), first_method_position)
        if doc_end_position != -1:
            doc_class = data[doc_start_position+start_pos+len(self.PATTERN_DOC):doc_end_position+start_pos]
            doc_class = self.editing(doc_class)
            doc_class = doc_class.split(self.P_STORY)
            doc = doc_class[1:]
            doc = self.editing(' '.join(doc))
        else:
            doc = None
        if len(name_c) > 2:
            name = name_c
        else:
            name = None
        return name, doc

    def get_method(self, data, start_pos=0):
        """
        Получить тест-метод
        :param data:
        :param start_pos:
        :return:
        """
        test_start_position = data.find(self.PATTERN_TEST_METHOD, start_pos)
        test_end_position = data.find(self.PATTERN_END, test_start_position+start_pos)
        name_class = data[test_start_position+4+start_pos:test_end_position+start_pos]
        name = self.editing(name_class)
        if len(name) > 2:
            return name
        else:
            return None

    def get_method_doc(self, data, start_pos=0):
        """ Получить feature из файла.
        :return:
        """
        doc_start_position = data.find(self.PATTERN_DOC, start_pos)
        doc_end_position = data.find(self.PATTERN_DOC, doc_start_position+start_pos+len(self.PATTERN_DOC))
        doc_method = data[doc_start_position+start_pos+len(self.PATTERN_DOC):doc_end_position+start_pos]
        doc_method = self.editing(doc_method).replace(":return:", '')
        #doc = editing(doc_method)
        if len(doc_method) > 2 and doc_start_position != -1 and doc_end_position != -1:
            title, description = self.get_title_doc(doc_method)
        else:
            title = None
            description = None
        return title, description


    def get_title_doc(self, doc):
        """
        Получить Title из doc-string тест метода
        :param doc:
        :return:
        """
        title = doc.split('Title:')
        if len(title) > 1:
            title_method = self.editing(title[1])
            description = title_method.split('Description:')
            if len(description) > 1:
                title_method = description[0]
                description_method = self.editing(description[1])
            else:
                description_method = None
        else:
            title_method = None
            description = doc.split('Description:')
            if len(description) > 1:
                description_method = self.editing(description[1])
            else:
                description_method = self.editing(doc)
        return title_method, description_method

    def get_attr(self, data):
        """ Получить дата-атрибуты.
        :param data:
        :return:
        """
        skip_start_position = data.find(self.P_SKIP)
        if skip_start_position != -1:
            skip_end_position = data[skip_start_position:].find(self.P_END, 0, 30)
            if skip_end_position != -1:
                skip_value = data[skip_start_position+len(self.P_SKIP):skip_start_position+len(self.P_SKIP)+skip_end_position]
                skip_value = self.editing(skip_value.replace("'", '').replace("(", '').replace(")", '').replace('"', ''))
                skip = skip_value
            else:
                skip = 'skip'
        else:
            skip = None
        priority_start_position = data.find(self.P_PRIORITY)
        if priority_start_position != -1:
            priority_end_position = data[priority_start_position:].find(self.P_END, 0, 30)
            if priority_end_position != -1:
                priority_value = data[priority_start_position+len(self.P_PRIORITY):priority_start_position+priority_end_position]
                priority_value = self.editing(priority_value.replace("'", '').replace("(", '').replace(")", '').replace('"', ''))
                priority = priority_value
            else:
                priority = 'empty'
        else:
            priority = None
        return skip, priority

    @staticmethod
    def get_folder_name(path):
        """ Получить название папки теста.
        :param path: путь
        :return: имя папки
        """
        end_folder_pos = path.rfind("\\")
        start_folder_pos = path.rfind("\\", 0, end_folder_pos)
        folder_name = path[start_folder_pos+len("\\"):end_folder_pos]
        return folder_name

    def get_init_title(self, path):
        """
        Получить описание папки из init файла
        :param path:
        :return:
        """
        pos = path.rfind("test_")
        init_path = path[:pos] + "__init__.py"
        data = open(init_path, 'rb').read()
        start_title_pos = data.find(self.PATTERN_DOC)
        end_title_pos = data.rfind(self.PATTERN_DOC)
        if start_title_pos and end_title_pos != -1:
            title_folder = self.editing(data[start_title_pos+len(self.PATTERN_DOC):end_title_pos])
        else:
            title_folder = None
        return title_folder

    def editing(self, string):
        """
        Преобразовать строку, удалить лишние пробелы и символы
        :param string:
        :return:
        """
        string = string.strip()
        string = string.replace('\r', '').replace('\n', ' ').replace('\t', '')
        return string

    def read_file(self, data, file_name, file_path):
        """
        Обработка файла
        :param data:
        :param file_name:
        :param file_path:
        :return:
        """
        tests_list = list()
        split_on_feature = data.split(self.P_FEATURE)
        feature_block = split_on_feature[-1]
        feature_name, feature_description = self.get_feature(self.PATTERN_DOC+self.P_FEATURE+feature_block)
        split_on_class = feature_block.split(self.PATTERN_CLASS)
        list_on_class_blocks = split_on_class[1:]
        for class_block in list_on_class_blocks:
            class_name, class_doc = self.get_class(self.PATTERN_CLASS+class_block)
            split_on_method = class_block.split(self.PATTERN_TEST_METHOD)
            list_on_method_blocks = split_on_method[1:]
            count_tests = 0
            for method_block in list_on_method_blocks:
                data_attr = split_on_method[count_tests]
                skip, priority = self.get_attr(data_attr)
                method_name = self.get_method(self.PATTERN_TEST_METHOD+method_block)
                method_title, method_description = self.get_method_doc(method_block)
                folder_title = self.get_init_title(file_path)
                folder_name = self.get_folder_name(file_path)
                tests_list.append({
                    'code_name_folder': folder_name,
                    'code_name_file': file_name,
                    'code_name_class': class_name,
                    'code_name_test': method_name,
                    'code_name_path': file_path,
                    'folder_title': folder_title,
                    'feature': feature_name,
                    'feature_description': feature_description,
                    'story': class_doc,
                    'name': method_title,
                    'description': method_description,
                    'skip': skip.lower(),
                    'priority': priority.lower(),
                })
                count_tests += 1
        return tests_list

    def get_default_directory(self):
        """ Получить директорию по умолчанию.
        :return: путь до директории по умолчанию
        """
        return self.DIRECTORY

    def walk(self, f_dir=None, f_files=None, flag_to_json=False):
        """ Проверяем есть ли в папке dir файлы подходящие по маске mask_py.
        Отсюда можно отправить результат j_files наружу
        :param f_dir: диреткорию для поиска тестов
        :param f_files:
        :param flag_to_json: флаг, говорит, нужно ли конвертировать результат в json
        :return: список словарей с данными по всем тестам в указанной диреткории
        """

        f_files = list() if f_files is None else f_files
        f_dir = self.get_default_directory() if f_dir is None else f_dir

        for file_name in os.listdir(f_dir):
            path = os.path.join(f_dir, file_name)
            if os.path.isfile(path):
                if fnmatch.fnmatch(file_name, self.MASK_PY):
                    try:
                        data = open(path, 'rb').read()
                        file_info = self.read_file(data, file_name, path)
                        f_files.extend(file_info)
                    except Exception, tx:
                        print "\n Error: %s \n" % str(tx)
            else:
                self.walk(path, f_files)
        return json.dumps(f_files) if flag_to_json else f_files

    @staticmethod
    def get_suits(source_data):
        """ Группируем по сьютам.
        :param source_data: список словарей всех тестов.
        :return: список папок с файлами и описанием.
        """

        folders_code_name = set([index['code_name_folder'] for index in source_data])  # выборка папок
        folders_array = list()
        for folder in folders_code_name:
            sorting_files = funcy.where(source_data, code_name_folder=folder)
            # выборка файлов для конкретной папки
            f_code_name = set([(index['code_name_file'], index['feature']) for index in sorting_files])
            pages = list()
            for file_array in f_code_name:
                code_name = file_array[0].decode('utf-8')
                name = str(file_array[1]).decode('utf-8')
                pages.append({"code_name": code_name, "name": name})
            folders_array.append({"name": sorting_files[0]['folder_title'], "code_name": folder, "pages": pages})
        return folders_array

    def get_tests(self, file_name, source_data):
        """

        :param file_name:
        :param source_data:
        :return:
        """
        tests_array = funcy.where(source_data, code_name_file=file_name)
        classes_name = set([(index['code_name_class'], str(index['story'])) for index in tests_array])
        classes_array = list()
        for c_name in classes_name:
            #tests_for_class = funcy.where(source_data, code_name_class=c_name)
            tests_for_class = list()
            for t in tests_array:
                if t['code_name_class'] == c_name[0]:
                    p = {"name": t['name'],
                         "code_name": t["code_name_class"],
                         "description": t["description"],
                         "skip": t["skip"],
                         "priority": t["priority"]}
                    tests_for_class.append(p)
            classes_array.append({"name": c_name[1].decode('utf-8'),
                                  "code_name": c_name[0],
                                  "tests": tests_for_class})
        return {file_name: classes_array}

a = GetCoverage()
p = a.walk()
pass