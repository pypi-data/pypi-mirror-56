from pathlib import Path
import os
import time
import pandas as pd

class TableWriter:
    
    VERBOSE = 0
    @classmethod
    def set_verbose(cls, v):
        TableWriter.VERBOSE = v
    @classmethod
    def printv(cls, s):
        if TableWriter.VERBOSE > 0:
            print(s)
    
    def __init__(self, **kwargs):
    
        self.__header = ""
        self.__body = ""
        self.__footer = ""
        
        expected = ["data", "path", "label", "caption", "col_names", "row_names",
                    "packages_commands", "load"]
        for name in kwargs:
            if not name in expected:
                raise ValueError("Unexpected argument " + name)
        self.__data = kwargs.get("data", pd.DataFrame())
        self.__path = kwargs.get("path", "")
        self.__label = kwargs.get("label", "")
        self.__caption = kwargs.get("caption", "")
        col_names = kwargs.get("col_names", [])
        row_names = kwargs.get("row_names", [])
        load = kwargs.get("load", False)
        self.__packages_commands = kwargs.get("packages_commands", [])
        if not type(self.__path) == Path:
            self.__path = Path(self.__path)
        if load:
            if not self.load_from_file():
                sys.exit(0)
        else:
            if type(self.__data) != pd.DataFrame:
                self.__data = pd.DataFrame(columns=col_names,
                                           index=row_names,
                                           data=self.__data)

# setters
    def set_data(self, data):
        if type(data) != pd.DataFrame:
            data = pd.DataFrame(data=data)
        self.__data = data
    def set_label(self, label):
        self.__label = label
    def set_caption(self, caption):
        self.__caption = caption
    def set_packages_commands(self, packages_commands):
        self.__packages_commands = packages_commands
    def set_path(self, path):
        self.__path = path
    def set_col_names(self, col_names):
        self.__data.columns = col_names
    def set_row_names(self, row_names):
        self.__data.index = row_names

#getters
    def get_ncols(self):
        return len(self.__data.columns)
    def get_nrows(self):
        return len(self.__data.index)
    def get_data(self, df = False):
        if df:
            return self.__data
        else:
            return self.__data.values
    def get_path(self):
        return self.__path
    def get_label(self):
        return self.__label
    def get_caption(self):
        return self.__caption
    def get_col_names(self):
        return self.__data.columns
    def get_row_names(self):
        return self.__data.index

#   Table makers
    def set_line(self, line, name = ""):
        """Adds or updates a line
        """
        
        TableWriter.printv("Adding/changing line in table.")
        if name != "":
            self.__data.loc[name] = line
            return
        else:
            self.__data.loc[str(len(self.__data.index))] = line
            return
    
    def set_column(self, column, name = ""):
        """Adds or updates a column
        """
        
        TableWriter.printv("Adding/changing column in table.")
        if name != "":
            self.__data[name] = column
            return
        else:
            self.__data[str(len(self.__data.columns))] = column
            return
    
    def load_from_file(self):
        """Loads a table from a tex file
        
        NOT WORKING IF TEXFILE HAS PACKAGES
        """
        
        self.__data = []
        row_names = []
        col_names = []
        if not self.__path.is_file():
            raise ValueError("Tex file " + str(self.__path) + " not found.")
    
        lines = []
        with open(self.__path, "r") as ifile:
            lines = [line.split("\n")[0].split(" ") for line in ifile.readlines()]
        self.__header = ""
        nlines_header = 8
        for iline in range(len(lines)):
            #  Reads Header if iline inferior to number of lines in header
            if iline <= nlines_header:
                #  Fetchs caption and label if any
                for item in lines[iline]:
                    if item != "":
                        if "caption{" in item:
                            nlines_header += 1
                            for item2 in lines[iline]:
                                self.__caption += item2 + " "
                            self.__caption = self.__caption[
                                self.__caption.find("{")+1:][:-2]
                        
                        if "label{" in item:
                            nlines_header += 1
                            for item2 in lines[iline]:
                                self.__label += item2 + " "
                            self.__label = self.__label[
                                self.__label.find("{")+1:][:-2]
                        break
            
            #  Reads table content if iline is superior to number of line in header
            if iline >= nlines_header:
                #  Reads column names if __has_col_names is True and col_names empty
                if len(col_names) == 0:
                    name = ""
                    for item in lines[iline]:
                        if item == "":
                            continue
                        if item == "&" or item == "\\\\":
                            if name != "":
                                name = name[:-1] if name[-1] == " " else name
                                col_names.append(name)
                                name = ""
                        else:
                            name += item + " "
                else:
                    #  Reads data
                    self.__data.append([])
                    name = ""
                    first_found = False
                    for item in lines[iline]:
                        if item == "":
                            continue
                        if item == "&" or item == "\\\\":
                            #  Reads row name if first item and rows have names
                            if not first_found:
                                name = name[:-1] if name[-1] == " " else name
                                row_names.append(name)
                                name = ""
                                first_found = True
                                continue
                            if name != "":
                                name = name[:-1] if name[-1] == " " else name
                                self.__data[-1].append(name)
                                name = ""
                        else:
                            name += item + " "
                    
        self.__data = (self.__data[:-1] if len(self.__data[-1]) == 0
                                        else self.__data)
        self.__data = pd.DataFrame(columns=col_names,
                                   index=row_names,
                                   data=self.__data)
        return True
    
    def make_header(self):
        TableWriter.printv("Making Header...")
        charswidth = (len("".join(list(self.__data.columns)))
                    + len(str(self.__data.index[0])))*0.167
        paperwidth = charswidth + 0.8*(len(self.__data.columns))+1  # pifometre!
        paperheight = 3.5+(len(self.__data.index))*0.42  # pifometre!
        if paperwidth < 9:
            paperwidth = 9
        if paperheight < 4:
            paperheight = 4 
        if paperheight > 24:
            paperheight = 24  # Limit page height to A4's 24 cm
        self.__header = "\\documentclass{article}\n"
        self.__header += ("\\usepackage[margin=0.5cm,paperwidth="
                        + str(paperwidth) + "cm, paperheight="
                        + str(paperheight) + "cm]{geometry}\n")
        self.__header += ("\\usepackage{longtable}\n\\usepackage{xcolor}\n"
                        + "\\usepackage{booktabs}\n")
        for package in self.__packages_commands:
            self.__header += package + "\n"
        
        self.__header += "\\begin{document}\n\\nonstopmode\n"
        
        TableWriter.printv("...done")
    
    def make_body(self):
        TableWriter.printv("Making Body...")
        column_format = "|l|" + len(self.__data.columns)*"c" + "|"
        self.__body = self.__data.to_latex(longtable=True,
                                           escape=False,
                                           column_format=column_format)
        append_newline = False
        if self.__caption != "":
            in_table = self.__body.find("\\toprule")
            pre_table = self.__body[:in_table]
            post_table = self.__body[in_table:]
            pre_table += "\\caption{" + self.__caption + "}\n"
            self.__body = pre_table + post_table
            append_newline = True
        
        if self.__label != "":
            in_table = self.__body.find("\\toprule")
            pre_table = self.__body[:in_table]
            post_table = self.__body[in_table:]
            pre_table += "\\label{" + self.__label + "}\n"
            self.__body = pre_table + post_table
            append_newline = True
        if append_newline:
            self.__body = self.__body.replace("\n\\toprule","\\\\\n\\toprule")
        TableWriter.printv("...done")
    
    def make_footer(self):
        TableWriter.printv("Making Footer...")
        self.__footer = ("\\end{document}\n")
        TableWriter.printv("...done")

#  Write and compile
    def create_tex_file(self):
        if self.__path == "":
            raise ValueError("Must specify a file path.")
        
        with open(self.__path, "w") as outfile:
            self.make_header()
            outfile.write(self.__header)
            self.make_body()
            outfile.write(self.__body)
            self.make_footer()
            outfile.write(self.__footer)
        return True
    
    def compile_pdf_file(self, silenced = True, recreate = True):
        if self.__path == "":
            raise ValueError("Must specify a file path.")
        
        if recreate or not self.__path.is_file():
            if not self.create_tex_file():
                return False
        
        if not self.__path.is_file():
            raise ValueError("Tex file " + str(self.__path) + " not found.")
        
        command = "pdflatex -synctex=1 -interaction=nonstopmode "
        parent = self.__path.parents[0]
        if parent != ".":
            command = command + "-output-directory=" + str(parent) + " "
        
        command = command + str(self.__path)
        if silenced:
            command = command + " > /dev/null"
        
        TableWriter.printv(command)
        os.system(command)
        time.sleep(0.5)
        os.system(command)
        time.sleep(0.5)
        os.system(command)
        return True
    
    def export_to_csv(self, path):
        if path == "":
            path = str(self.__path).replace(".tex", ".csv")
        with open(path, "w") as outfile:
            if self.__has_col_names:
                outfile.write(",")
                for j in range(len(self.__data.columns)):
                    if j != len(self.__data.columns) - 1:
                        outfile.write(self.remove_color(self.__data.columns[j]) + ",")
                    else:
                        outfile.write(self.remove_color(self.__data.columns[j]))
            
            for i in range(nrows):
                outfile.write(self.remove_color(self.__data.index[i]) + ",")
                for j in range(len(self.__data.columns)):
                    if j != len(self.__data.columns) - 1:
                        outfile.write(self.remove_color(self.__data[i][j]) + ",")
                    else:
                        outfile.write(self.remove_color(self.__data[i][j]))
        return True
    
    def remove_color(self, obj):
        has_color = "textcolor" in obj
        if not "\\textcolor{" in obj:
            return obj
        to_find = "\\textcolor{"
        before_color = obj[:obj.find(to_find)]
        after_color = obj[obj.find("textcolor")+10:]
        no_color = after_color[after_color.find("{")+1:].replace("}","",1)
        return before_color + no_color
    
