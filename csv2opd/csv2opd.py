"""CSV2OPD.

CSV2OPD parses each row of a given CSV file into separate OPD files and
names each new file after the value contained in the Name field.

OPD is the XML implementation used by the open source DMS OpenProdoc.

The CSV file must have a header. The 'OPDObject type' column is optional.
"""

import csv
import os
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
        csvData: Content of the input CSV file.
        rowNum: Number of times the loop has iterated through csvData.
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
        self.rowNum = 0

    def read_csv(self):
        """Opens and reads the input CSV file."""
        csvData = csv.reader(open(self.csvFile, 'r'), delimiter=self.separator)
        if self.separator is not self.dialect:
            raise DelimiterError
        return csvData

    def converter(self):
        """Converts the CSV file into separate OPD files.

        Transforms each row of the input CSV file into separate OPD files
        and names each new file after the value contained in the Name
        field, using write_xml internal method.
        """
        os.chdir(self.xmlFile)

        for row in self.csvData:
            xmlData = open('xmlFile.xml', 'w')
            if self.rowNum == 0:
                tags = row
            else:
                self._write_xml(row, xmlData, tags)
            self.rowNum += 1
            xmlData.close()

    def _write_xml(self, row, xmlData, tags):
        """Writes the output OPD files.

        Args:
            row: Current row.
            xmlData: Content of the current output XML file.
            tags: Tags used for the output XML files.
        """
        xmlData.write('<OPDObject type="PD_DOCS">\n<ListAttr>\n')
        for i in range(len(tags)):
            if tags[i] == 'OPDObject type':
                continue
            xmlData.write(f'<Attr Name="{tags[i]}">{row[i]}</Attr>\n')
            if tags[i] == 'Name':
                fileName = row[i]
                os.rename('xmlFile.xml', f'{fileName}.opd')
        xmlData.write('</ListAttr></OPDObject>\n')


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
            tk.Radiobutton(text=separator, padx=20,
                           variable=self.v, value=self.separator[separator]
                           ).grid(row=2 + i, sticky=W, column=1)
            i += 1

    def import_csv(self):
        """Broswes the input CSV file."""
        file = filedialog.askopenfile(mode='rb',
                                      title='Choose the CSV file to convert',
                                      filetypes=[('CSV files', '*.csv')])
        self.e1.insert(0, file.name)

    def output_directory(self):
        """Browses the output XML file directory."""
        directory = filedialog.askdirectory(title='Choose an output directory')
        self.e2.insert(0, directory)

    def parse_csv(self):
        """Executes Parser.run_parser() if csvFile and xmlFile are valid.

        Raises:
            OSError: If one or more fields are empty or have an invalid path.
            DelimiterError: If separator does not match dialect.
            IndexError: If the number of fields in the current row is not equal
            to the number of headers of the input CSV file.
        """
        try:
            parser = Parser(self.e1.get(), self.e2.get(), self.v.get())
            parser.converter()
            self.conversion_completed()
        except OSError as e:
            messagebox.showerror('Error', e.strerror)
            self.clean_input()
            raise e
        except DelimiterError as e:
            messagebox.showerror('Error', f'Separator "{parser.dialect}" '
                                 f'expected, got "{parser.separator}".')
            raise e
        except IndexError as e:
            messagebox.showerror('Error', 'There was an error converting row '
                                 f'{parser.rowNum}.')
            self.clean_input()
            raise e

    def conversion_completed(self):
        """Shows the result of the conversion.

        Evaluates the number of errors and displays a message box with the
        result of the conversion (completed without errors, completed with
        1 error or converted with 2 or more errors.)
        """
        messagebox.showinfo('Info', 'Conversion completed!')
        self.clean_input()

    def clean_input(self):
        """Cleans the paths input by the user in the entry widgets."""
        self.e1.delete(0, tk.END)
        self.e2.delete(0, tk.END)


def main():
    """Starts the application in graphical mode."""
    root = tk.Tk()
    root.title('CSV2OPD v1.1.0')
    GUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
