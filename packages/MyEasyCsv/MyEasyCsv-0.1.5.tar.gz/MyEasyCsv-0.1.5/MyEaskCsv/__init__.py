import csv
import os


class Row(list):
    def __init__(self, record, super_cls):
        self.append(record)
        self.super_cls = super_cls

    def get(self, arr):
        if arr in self.super_cls.id.keys():
            return self[0][self.super_cls.id[arr]]
        else:
            raise Exception("没有找到这个字段")

    def set(self, arr, want):
        if arr in self.super_cls.id.keys():
            if not want == None:
                self[0][self.super_cls.id[arr]] = want
        else:
            raise Exception("没有找到这个字段")

    def __str__(self):
        return str(self[0])


class Easy_CSV(list):
    filename = ""
    encoding = ""

    def __init__(self, filename, encoding='utf-8'):
        super().__init__()
        self.filename = filename
        filename = filename
        self.encoding = encoding
        encoding = encoding
        self.file = open(self.filename, 'r', encoding=self.encoding)
        self.csv_file = csv.reader(self.file)
        self.id = {}
        flag = True
        self.n = 0
        for c in self.csv_file:
            if flag:
                flag = False
                for i in c:
                    self.id[i] = self.n
                    self.n += 1
            else:
                self.append(Row(c, self))
            # print(self.id)
        self.file.close()

    def save(self, filename=filename, encoding=encoding, title=True):
        if filename == "":
            filename = self.filename
            encoding = self.encoding
        else:
            filename = filename
            if encoding == "":
                encoding = self.encoding
            else:
                encoding = encoding
        file = open(filename, 'w', encoding=encoding, newline="")
        write = csv.writer(file)
        if title:
            write.writerow([i for i in self.id.keys()])
        for i in self:
            for j in i:
                write.writerow(j)
        file.close()

    def disp_field(self):
        print(self.id)
        if len(self.id.keys()) > 0:
            for k, v in self.id.items():
                print(v, k)
            # return
        else:
            raise Exception("你的表没有表头")

    def del_field_only(self, field):
        if field in self.id.keys():
            for i in self:
                i[0].pop(self.id[field])
            for i in self.id.keys():
                if i == field:
                    self.id.pop(field)
                break
        else:
            raise Exception("没有找到这个字段")

    def add_field(self, file_name):
        if isinstance(file_name, str) or isinstance(file_name, int):
            if isinstance(file_name, list):
                self.id = {}
                n = 0
                for i in file_name:
                    if isinstance(file_name, str) or isinstance(file_name, int):
                        self.id[i] = n
                        n += 1
                    else:
                        raise Exception("你输入的字段有问题")
                self.save(self.filename, self.encoding)
            else:
                self.id[file_name] = self.n
                self.save(self.filename, self.encoding)
        else:
            raise Exception("你输入的字段有问题")

    def add_record(self, record):
        if isinstance(record, list):
            self.append(Row(record, self))
        else:
            raise Exception("请键入一个字典")

    def find_record(self,where):
        for w,v in where.items():
            if w.find("__>") != -1:
                pass
            elif w.find("__<")!= -1:
                pass
            elif w.find("__>=")!= -1:
                pass
            elif w.find("__<=")!= -1:
                pass
            elif w.find("__!=")!= -1:
                pass
            else:
                for i in self:
                    if str(i.get(w)) == str(v):
                        print(i)

