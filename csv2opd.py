"""CSV2OPD.

CSV2OPD parses each row of a given CSV file into separate OPD files and
names each new file after the value contained in the Name field.

OPD is the XML implementation used by the open source DMS OpenProdoc.

The CSV file must have a header. The 'OPDObject type' column is optional.
"""

import csv
import os
import sys
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox


class DelimiterError(Exception):
    """The column delimiter does not match the CSV dialect."""


class Parser():
    """Provides the functionality to the application.

    Attributes:
        csvFile: Path to the input CSV file.
        xmlFile: Path to the input CSV file.
        separator: Delimiter selected by the user.
        dialect: Delimiter actually used in the CSV file.
    """

    def __init__(self, csvFile, xmlFile, separator):
        """Inits Parser.

        Args:
            csvFile: Path to the input CSV file.
            xmlFile: Path to the input CSV file.
            separator: Delimiter selected by the user.
        """
        self.csvFile = csvFile
        self.xmlFile = xmlFile
        self.separator = separator
        self.dialect = csv.Sniffer().sniff(
            open(csvFile, 'r').readline()).delimiter
        self.csvData = self.read_csv()
        self.errors = 0

    def run_parser(self):
        self.errors = self.converter()
        gui.conversion_completed(self.errors)

    def read_csv(self):
        """Opens and reads the input CSV file.

        Raises:
            DelimiterError: If separator does not match dialect.
        """
        try:
            csvData = csv.reader(open(self.csvFile, 'r'),
                                 delimiter=self.separator)
            if self.separator is not self.dialect:
                raise DelimiterError
            else:
                return csvData
        except DelimiterError as e:
            messagebox.showerror('Error', f'Separator "{self.dialect}" '
                                 f'expected, got "{self.separator}".')
            raise e

    def converter(self):
        """Converts the CSV file into separate OPD files.

        Transforms each row of the input CSV file into separate OPD files
        and names each new file after the value contained in the Name
        field, using write_xml internal method.
        """
        os.chdir(self.xmlFile)

        rowNum = 0
        for row in self.csvData:
            xmlData = open('xmlFile.xml', 'w')
            if rowNum == 0:
                tags = row
            else:
                if not self._write_xml(rowNum, row, xmlData, tags):
                    self.errors += 1
            rowNum += 1
            xmlData.close()

        return self.errors

    def _write_xml(self, rowNum, row, xmlData, tags):
        """Writes the output OPD files.

        Args:
            rowNum: Number of times the loop has iterated through csvData.
            row: Current row.
            xmlData: Content of the current output XML file.
            tags: Tags used for the output XML files.

        Raises:
            IndexError: If the number of fields in the current row is not equal
            to the number of headers of the input CSV file.
        """
        xmlData.write('<OPDObject type="PD_DOCS">\n<ListAttr>\n')
        try:
            for i in range(len(tags)):
                if tags[i] == 'OPDObject type':
                    continue
                xmlData.write(f'<Attr Name="{tags[i]}">{row[i]}</Attr>\n')
                if tags[i] == 'Name':
                    fileName = row[i]
                    os.rename('xmlFile.xml', f'{fileName}.opd')
            xmlData.write('</ListAttr></OPDObject>\n')
            return True
        except IndexError:
            os.remove(f'{fileName}.opd')
            GUI.conversion_warning(self, rowNum)
            return False


class GUI():
    """Provides the graphical user interface to the application.

    Attributes:
        master: Parent widget of the window.
        label: Label widgets of the window.
        button: Button widgets of the window.
        e1: Entry widget for the path to the input CSV file.
        e2: Entry widget for the path to the output XML files directory.
        separator: CSV delimiter selected by the user.
        v: StringVar instance used to get the separator value.
    """

    def __init__(self, master):
        """Inits GUI.

        Args:
            master: Parent widget of the window.
        """
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
        self.button = tk.Button(master, text='Convert', command=self.parse_csv
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
        """Broswes the input CSV file."""
        file = filedialog.askopenfile(parent=root, mode='rb',
                                      title='Choose the CSV file to convert',
                                      filetypes=[('CSV files', '*.csv')])
        self.e1.insert(0, file.name)

    def output_directory(self):
        """Browses the output XML file directory."""
        directory = filedialog.askdirectory(parent=root,
                                            title='Choose an output directory')
        self.e2.insert(0, directory)

    def parse_csv(self):
        """Executes Parser.run_parser() if csvFile and xmlFile are valid.

        Raises:
            OSError: If one or more fields are empty or have an invalid path.
        """
        try:
            parser = Parser(self.e1.get(), self.e2.get(), self.v.get())
            parser.run_parser()
        except OSError as e:
            messagebox.showerror('Error', e.strerror)
            raise e

    def conversion_completed(self, errors):
        """Shows the result of the conversion.

        Evaluates the number of errors and displays a message box with the
        result of the conversion (completed without errors, completed with
        1 error or converted with 2 or more errors.)

        Args:
            errors: Number of errors that the conversion loop has encountered.
        """
        if errors == 0:
            messagebox.showinfo('Info', 'Conversion completed!')
        elif errors == 1:
            messagebox.showinfo('Info', 'Conversion completed with 1 error.')
        else:
            messagebox.showinfo('Info',
                                f'Conversion completed with {errors} errors.')
        self.e1.delete(0, tk.END)
        self.e2.delete(0, tk.END)

    def conversion_warning(self, rowNum):
        """Asks the user if they want to stop or continue the conversion.

        Displays a warning message after Parser.converter encounters an error
        and allows the user to terminates the application or continue the
        conversion, skipping the row which caused the error.

        Args:
            rowNum: Number of times the loop has iterated through csvData.
        """
        msg = messagebox.askquestion('Warning',
                                     'There was an error converting row '
                                     f'{rowNum}. Do you want to continue?')
        if msg == 'no':
            messagebox.showinfo('Info',
                                f'Conversion interrupted at row {rowNum}.')
            sys.exit()


if __name__ == '__main__':
    """Executes GUI__init__."""
    root = tk.Tk()
    root.title('CSV2OPD v1.1.0')
    gui = GUI(root)
    root.mainloop()
