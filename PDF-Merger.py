from PyPDF2 import PdfFileMerger, PdfFileReader
from tkinter import Tk, filedialog, Button, Label, Entry, StringVar, Frame
from os import getcwd, listdir
import re
from datetime import datetime

_title = 'PDF-Merger'
_version = '0.2'
program_title = f'{_title} V{_version}'
selected_folder = None
filter_text = None
filtered_and_sorted_files = None
dynamic_widgets = []
result_frame = None
button_merge_files = None
entry_filter_text = None

def on_button_open_folder_clicked():
    global selected_folder, entry_filter_text, button_merge_files
    folder = None
    while folder == None or folder == '':
        folder = filedialog.askdirectory(initialdir=getcwd())
    selected_folder.set(folder)
    on_filter_text_changed()
    button_merge_files.configure(state='normal')
    entry_filter_text.configure(state='normal')

def on_button_merge_files_clicked():
    global filtered_and_sorted_files
    pdf_merger = PdfFileMerger()
    for _ in filtered_and_sorted_files:
        filepath = f'{selected_folder.get()}/{_[1]}'
        with open(filepath, 'rb') as file:
            pdf_reader = PdfFileReader(file)
            pdf_merger.append(pdf_reader)
    file_path = filedialog.asksaveasfile(mode='wb', title='Select file to save', initialdir=selected_folder, filetypes=(('PDF','*.pdf'),('all files', '*.*')))
    pdf_merger.write(file_path)
    pdf_merger.close()

def on_filter_text_changed(*args):
    global filtered_and_sorted_files, dynamic_widgets, result_frame
    all_files = get_all_pdf_files_in_folder(selected_folder.get())
    filtered_and_sorted_files = filter_and_sort_files(filter_text.get(), all_files)
    for widget in dynamic_widgets:
        widget.grid_forget()
    dynamic_widgets=[]
    for idx, file in enumerate(filtered_and_sorted_files):
        l = Label(master=result_frame, text=f'{file[0]:%d.%m.%Y }: {file[1]}')
        l.grid(row=idx, column=0, sticky='w')
        dynamic_widgets.append(l)

def get_all_pdf_files_in_folder(folderpath):
    return [file for file in listdir(folderpath) if file.endswith('.pdf')]

def filter_and_sort_files(filter_text, files):
    pre_filtered_files = [file for file in files if filter_text in file] if filter_text != '' else files
    output = []
    pattern = re.compile(r'(19\d\d|20\d\d)[.-_]?(\d\d)[.-_]?(\d\d)')
    for file in pre_filtered_files:
        match = re.search(pattern, file)
        if match:
            output.append((datetime(year=int(match[1]), month=int(match[2]), day=int(match[3])), file))
    output.sort(key=lambda tup: tup[0])
    return output


if __name__ == "__main__":
    window = Tk()
    selected_folder = StringVar(master=window)
    filter_text = StringVar(master=window)
    window.resizable(False, False)
    window.title(program_title)
    header_frame = Frame(master=window)
    result_frame = Frame(master=window)
    button_open_folder = Button(master=header_frame, text='Select Folder', command=on_button_open_folder_clicked)
    label_selected_folder = Label(master=header_frame, textvariable=selected_folder)
    button_merge_files = Button(master=header_frame, text='Merge Files', command=on_button_merge_files_clicked, state='disabled')
    entry_filter_text = Entry(master=header_frame, width=50, textvariable=filter_text, state='disabled')
    filter_text.trace_add("write", on_filter_text_changed)


    header_frame.grid(row=0, column=0, sticky='w')
    result_frame.grid(row=1, column=0, sticky='w')
    label_selected_folder.grid(row=0, column=0, sticky='w')
    button_open_folder.grid(row=0, column=1, sticky='w')
    entry_filter_text.grid(row=1, column=0, sticky='w')
    button_merge_files.grid(row=1, column=1, sticky='w')


    window.mainloop()