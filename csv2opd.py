# CSV2OPD parses each row of a CSV file into a separate OPD file
# and names each new file after the value contained in the Name field.
#
# The CSV file must have a header and must not have an "OPDObject type"
# column.

import csv
import os
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox


class Parser():
    '''This class provides the functionality to the application.'''

    def __init__(self, csvFile, xmlFile, separator):
        '''This method is called when the object parser is created from Parser.

        :param csvFile: This is the path of the output file.
        :param xmlFile: This is the path of the output directory.
        :param separator: This is the type of delimiter used by the CSV file.
        '''
        self.csvFile = csvFile
        self.xmlFile = xmlFile
        self.separator = separator
        self.converter()

    def converter(self):
        '''This method transforms each row of a given CSV file into separate
        OPD files and names each new file after the value contained in the Name
        field.
        '''
        csvData = csv.reader(open(self.csvFile, 'r'), delimiter=self.separator)

        os.chdir(self.xmlFile)

        rowNum = 0
        for row in csvData:
            xmlData = open('xmlFile.xml', 'w')
            if rowNum == 0:
                tags = row
            else:
                self.write_xml(rowNum, row, xmlData, tags)
            rowNum += 1
            xmlData.close()

        gui.conversion_completed()

    def write_xml(self, rowNum, row, xmlData, tags):
        xmlData.write('<OPDObject type="PD_DOCS">\n<ListAttr>\n')
        for i in range(len(tags)):
            xmlData.write(f'<Attr Name="{tags[i]}">{row[i]}</Attr>\n')
            if tags[i] == 'Name':
                os.rename('xmlFile.xml', f'{row[i]}.opd')
        xmlData.write('</ListAttr></OPDObject>\n')


class GUI():
    '''This class provides the graphical user interface to the application.'''

    def __init__(self, master):
        '''This method is called when the object gui is created from GUI.

        :param master: This is the parent widget of the window.
        '''
        self.master = master

        W = tk.W

        self.label = tk.Label(master, text='Input CSV').grid(row=0)
        self.label = tk.Label(master, text='Output Directory').grid(row=1)
        self.label = tk.Label(master, text='Column delimiter').grid(row=2)

        self.button = tk.Button(master, text='Quit', command=master.quit
                                ).grid(row=8, column=0, sticky=W, pady=4)
        self.button = tk.Button(master, text='Browse', command=self.import_csv
                                ).grid(row=0, column=2, sticky=W, pady=4)
        self.button = tk.Button(master, text='Browse',
                                command=self.output_directory
                                ).grid(row=1, column=2, sticky=W, pady=4)
        self.button = tk.Button(master, text='Convert', command=self.do_parser
                                ).grid(row=8, column=1, sticky=W, pady=4)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        self.separator = {'Tab': '\t',
                          'Comma': ',',
                          'Semicolon': ';',
                          'Colon': ':',
                          'Space': ' ',
                          'Pipe': '|'}

        self.v = tk.StringVar()
        self.v.set(self.separator['Tab'])
        i = 0
        for val, separator in enumerate(self.separator):
            tk.Radiobutton(root, text=separator, padx=20,
                           variable=self.v, value=self.separator[separator]
                           ).grid(row=2 + i, sticky=W, column=1)
            i += 1

    def import_csv(self):
        '''This method is called when the user clicks the Input CSV Browse
        button.

        :returns: It returns the path of the CSV into GUI.e1.
        '''
        file = filedialog.askopenfile(parent=root, mode='rb',
                                      title='Choose the CSV file to convert',
                                      filetypes=[('CSV files', '*.csv')])
        self.e1.insert(0, file.name)

    def output_directory(self):
        '''This method is called when the user clicks the Output Directory
        button.

        :returns: It returns the path of the output directory into self.e2.
        '''
        directory = filedialog.askdirectory(parent=root,
                                            title='Choose an output directory')
        self.e2.insert(0, directory)

    def do_parser(self):
        '''This method is called when the user clicks the Convert button.

        :returns: If one or more fields are empty, it returns an error message.
        If all the fields are fullfiled, it returns the parameters csvFile,
        xmlFile and separator into the class Parser.
        '''
        try:
            Parser(self.e1.get(), self.e2.get(), self.v.get())
        except OSError as e:
            messagebox.showerror('Error', e.strerror)

    def conversion_completed(self):
        '''This method is called at the end of parser.converter.

        :returns: It returns a message and clears gui.e1 and gui.e2.
        '''
        messagebox.showinfo('Info', 'Conversion completed!')
        self.e1.delete(0, tk.END)
        self.e2.delete(0, tk.END)


if __name__ == '__main__':
    '''This statement runs the application.'''
    root = tk.Tk()
    root.title('CSV2OPD v1.1.0')
    gui = GUI(root)
    root.mainloop()
