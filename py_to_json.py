import json
import data

def convert_from_py_to_json(py_file):
    with open('data.json', 'w', encoding='utf-8') as fp:
        json.dump(py_file, fp, ensure_ascii=False)

if __name__ == "__main__":
    convert_from_py_to_json(data.teachers)
    print('JSON file saved, {} elements.'.format(len(data.teachers)))