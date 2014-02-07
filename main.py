__author__ = 'James Charnock'

from tkinter import *
# from tkinter import ttk
import sys
import os
from tkinter import filedialog


entries = []
checkboxes = []
tags = []


def get_list_of_files():
    pathname = os.path.dirname(sys.argv[0])
    l = []
    for file in os.listdir(pathname):
        if file.endswith('.txt'):
            l.append(file)
    return l


def choose_XML():
    print(radio_file.get())
    make_tags_list(radio_file.get())
    print(tags)
    make_grid(tags)
    # grey out radio choices
    # for i in radio_array:
    #     i.config(state=DISABLED)


def make_tags_list(f):
    global tags
    tags = []
    with open(f) as inputfile:
        for line in inputfile:
            tags.append(line.strip())
    return tags


def make_grid(t):
    global entries
    global checkboxes
    global frame_tags
    entries = []
    checkboxes = []

# new 04-feb-14
    frame_tags.destroy()
    frame_tags = Frame(master)
    frame_tags.grid(row=1)

# create labels, text entry boxes, checkboxes from tags
    for i, a in enumerate(t):
        Label(frame_tags, text=a.title(), width=10, anchor=W).grid(row=i+len(list_of_files), column=0, sticky=W)
        e = Entry(frame_tags, width=50)
        e.grid(row=i+len(list_of_files), column=1, sticky=W)
        entries.append(e)
        entries[i].insert(INSERT, 'Enter ' + a)
        v = IntVar()
        c = Checkbutton(frame_tags, variable=v)
        c.grid(row=i+len(list_of_files), column=2, sticky=W)
        c.var = v
        checkboxes.append(c)
        checkboxes[i].toggle()
        if a == 'episode':
            up_episodes_button = Button(frame_tags, text="^", command=increment_episodes)
            up_episodes_button.grid(row=i+len(list_of_files), column=5)
            down_episodes_button = Button(frame_tags, text="v", command=decrement_episodes)
            down_episodes_button.grid(row=i+len(list_of_files), column=6)

    return entries, checkboxes


def increment_episodes():
    try:
        x = int(entries[tags.index('episode')].get())
        entries[tags.index('episode')].delete(0, END)
        entries[tags.index('episode')].insert(0, x + 1)
    except ValueError:
        entries[tags.index('episode')].delete(0, END)
        entries[tags.index('episode')].insert(0, 1)


def decrement_episodes():
    try:
        x = int(entries[tags.index('episode')].get())
        entries[tags.index('episode')].delete(0, END)
        entries[tags.index('episode')].insert(0, x - 1)
    except ValueError:
        entries[tags.index('episode')].delete(0, END)
        entries[tags.index('episode')].insert(0, 1)


# create XML tag
def make_XML_Tag(tag, value):
    return '    <' + str(tag) + '>' + str(value) + '</' + str(tag) + '>'


def make_NFO():
#     print('<movie>')
#     for i, a in enumerate(entries):
#         if checkboxes[i].var.get():
#             val = entries[i].get()
#             print(makeTag(tags[i], val))
#     print('</movie>')
    print(make_nfo_str())
    nfo_textbox.delete(1.0, END)
    nfo_textbox.insert("1.0", make_nfo_str())
    filename_entry.delete(0, END)
    filename_entry.insert(0, make_filename())
    nfo_textbox.focus_set()
    nfo_textbox.tag_add(SEL, "1.0", END)
    print(radio_file.get())


def create_NFO_file():
    f = open(filename_entry.get() + '.nfo', 'w')
    f.write(make_nfo_str())


def save_as_NFO_file():
    f = open(filedialog.asksaveasfilename(defaultextension="nfo", initialfile=filename_entry.get()), 'w')
    f.write(make_nfo_str())

def make_nfo_str():
    nfo = '<' + radio_file.get()[:-4] + '>\n'
    for i, a in enumerate(entries):
        if checkboxes[i].var.get():
            val = entries[i].get()
            nfo += ((make_XML_Tag(tags[i], val)))

            nfo += '\n'
    nfo += '</' + radio_file.get()[:-4] + '>'
    return nfo


def make_filename():
    if radio_file.get() == 'episodedetails.txt':
        s = entries[tags.index('season')].get()
        e = entries[tags.index('episode')].get()
        return series_entry.get() + ' - S' + s.zfill(2) + 'E' + e.zfill(2)
    elif radio_file.get() == 'movies.txt':
        return entries[tags.index('title')].get() + '.nfo'
    else:
        return 'dodo'

list_of_files = get_list_of_files()


master = Tk()
master.title("XBMC NFO generator")

frame_header = Frame(master)
frame_header.grid(sticky=W, row=0)

frame_tags = Frame(master)
frame_tags.grid(row=1)

frame_footer = Frame(master)
frame_footer.grid(row=2)

print(list_of_files)

radio_file = StringVar()
radio_array = []

# create XML choice
for i, x in enumerate(list_of_files):
    r = Radiobutton(frame_header, text=x.title()[:-4], variable=radio_file, value=x, command=choose_XML)
    r.grid(sticky=W)
    radio_array.append(r)

radio_file.set(list_of_files[0])
# for i in radio_array:
#     i.deselect()


generate_button = Button(frame_footer, text="Show XML", command=make_NFO)
generate_button.grid()

create_nfo_button = Button(frame_footer, text="Create NFO file", command=create_NFO_file)
create_nfo_button.grid()

save_as_nfo_button = Button(frame_footer, text="Save as...", command=save_as_NFO_file)
save_as_nfo_button.grid(row=create_nfo_button.grid_info()["row"], column=1)


series_entry = Entry(frame_footer, width=70)
series_entry.grid()
series_entry.insert(INSERT, 'Enter series name')


filename_entry = Entry(frame_footer, width=80)
filename_entry.grid()

nfo_textbox_scrollbar = Scrollbar(frame_footer)
nfo_textbox_scrollbar.grid(column=1, sticky=N+S)

nfo_textbox = Text(frame_footer, width=70, height=10, yscrollcommand=nfo_textbox_scrollbar.set)
nfo_textbox.grid(row=nfo_textbox_scrollbar.grid_info()["row"])

nfo_textbox_scrollbar.config(command=nfo_textbox.yview)


print(radio_file.get())
master.mainloop()