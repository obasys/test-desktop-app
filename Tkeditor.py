from tkinter import *
from tkinter import messagebox, filedialog
# from PyInstaller.utils.hooks import copy_metadata
# datas = copy_metadata('tkinter')
import os


root = Tk()
root.geometry('800x500')
root.title('Untitled - File Editor Based on Tkinter')
root.iconbitmap('icons/pypad.ico')

def popup(event):
    cmenu.tk_popup(event.x_root, event.y_root, 0)

#theme choice
def theme():
        global bgc,fgc
        val = themechoice.get()
        clrs = clrschms.get(val)
        fgc, bgc = clrs.split('.')
        fgc, bgc = '#'+fgc, '#'+bgc
        textPad.config(bg=bgc, fg=fgc)

def show_info_bar():
    val = showinbar.get()
    if val:
        infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
    elif not val:
        infobar.pack_forget()

def update_line_number(event=None):
    txt = ''
    if showln.get(): 
        endline, endcolumn = textPad.index('end-1c').split('.')
        txt = '\n'.join(map(str, range(1, int(endline))))
    lnlabel.config(text=txt, anchor='nw')
    currline, curcolumn = textPad.index("insert").split('.')
    infobar.config(text='Line: %s | Column: %s'  %(currline,curcolumn) )

def highlight_line(interval=100):
    textPad.tag_remove("active_line", 1.0, "end")
    textPad.tag_add("active_line", "insert linestart", "insert lineend+1c")
    textPad.after(interval, toggle_highlight)

def undo_highlight():
    textPad.tag_remove("active_line", 1.0, "end")

def toggle_highlight(event=None):
    val = hltln.get()
    undo_highlight() if not val else highlight_line()


#########################################################################
def about():
    messagebox.showinfo("About", "A Editor using Tkinter by Oleh Basystiuk")

def help_box(event=None):
    messagebox.showinfo("Help", "For help email to obasystiuk@gmail.com", icon='question')

def exit_editor():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()
root.protocol('WM_DELETE_WINDOW',exit_editor)

#########################################################################

#demo of indexing and tagging features of text widget
def select_all(event=None):   
	textPad.tag_add('sel', '1.0', 'end')

def on_find(event=None):
	t2 = Toplevel(root)
	t2.title('Find')
	t2.geometry('300x65+200+250')
	t2.transient(root)
	Label(t2,text="Find All:").grid(row=0, column=0, pady=4, sticky='e')
	v=StringVar()
	e = Entry(t2, width=25, textvariable=v)
	e.grid(row=0, column=1, padx=2, pady=4, sticky='we')
	c=IntVar()
	Checkbutton(t2, text='Ignore Case', variable=c).grid(row=1, column=1, sticky='e', padx=2, pady=2)
	Button(t2, text='Find All', underline=0, command=lambda:search_for(v.get(), c.get(), textPad, t2, e)).grid(row=0, column=2, sticky='e'+'w', padx=2, pady=4)
	def close_search():
		textPad.tag_remove('match', '1.0', END)
		t2.destroy()
	t2.protocol('WM_DELETE_WINDOW', close_search)

def search_for(needle,cssnstv, textPad, t2,e) :
        textPad.tag_remove('match', '1.0', END)
        count =0
        if needle:
                pos = '1.0'
                while True:
                    pos = textPad.search(needle, pos, nocase=cssnstv, stopindex=END)
                    if not pos: break
                    lastpos = '%s+%dc' % (pos, len(needle))
                    textPad.tag_add('match', pos, lastpos)
                    count += 1
                    pos = lastpos
                textPad.tag_config('match', foreground='red', background='yellow')
        e.focus_set()
        t2.title('%d matches found' %count)

########################################################################
#Levaraging built in text widget functionalities

def undo():
    textPad.event_generate("<<Undo>>")
    update_line_number()
    
def redo():
    textPad.event_generate("<<Redo>>")
    update_line_number()

def cut():
    textPad.event_generate("<<Cut>>")
    update_line_number()
    
def copy():
    textPad.event_generate("<<Copy>>")
    update_line_number()

def paste():
    textPad.event_generate("<<Paste>>")
    update_line_number()


######################################################################
def new_file(event=None):
    global filename
    filename = None
    root.title("Untitled - Tkeditor")
    textPad.delete(1.0, END)
    update_line_number()


def open_file(event=None):
    global filename
    filename = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    if filename == "": # If no file chosen.
        filename = None # Absence of file.
    else:
        root.title(os.path.basename(filename) + " - Tkeditor") # Returning the basename of 'file'
        textPad.delete(1.0,END)         
        fh = open(filename,"r")        
        textPad.insert(1.0,fh.read()) 
        fh.close()
    update_line_number()

def save(event=None):
    global filename
    try:
        f = open(filename, 'w')
        letter = textPad.get(1.0, 'end')
        f.write(letter)
        f.close()
    except:
        save_as()

def save_as():
    try:
        # Getting a filename to save the file.
        f = filedialog.asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        fh = open(f, 'w')           
        global filename
        filename = f
        textoutput = textPad.get(1.0, END)
        fh.write(textoutput)              
        fh.close()                
        root.title(os.path.basename(f) + " - Tkeditor") # Setting the title of the root widget.
    except:
        pass

######################################################################
#defining icons for compund menu demonstration
newiconString = b'R0lGODlhEAAQAPcAAJaXt52nx6uqw6yrw6m83LvA17PH5LXJ5MDB08HB1MLC1MTE1dTS2tbU29fV3MTX68fY68bZ7Mna7czc7s/f78HZ9sHZ98jd99Ph8NPj9Njl89vp99/q9Ovr6+zs7O3t7e7t7u7u7u/v7+Lq8uLs9uTr8urw9uzy+PDw8PHx8fHx8vLy8vT09PX19/f39/f2+Pn5+vv7+////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAEAAQAAAImQBlyDhhoqDBgjAEKoyR4YTDhyc2GGihUEYMDS4yanRB4sIBigJjYGBBsiQLDhYqEHgRksKKlzBXqCgxokCDkBNS6NzJcwGDkBJQCB1K1CdQokhFKPhpMUKIp1ChfkDANMYDD1izaqUa8kGHr2DDJqjqNazZpSEhaF3rAa1FtWyzuo0RQICAAXYH6NULwIFCFSACCx4MIoaMgAA7'
openiconString = b'R0lGODlhEAAQAPcAABB6AEV/MgmPAAmbAAiaBhCICRifGACiACCZGEiZQFqbUF2aUGeVWWSbVHiVa3m+ebyjV7ykW7ylX8etWMmuUsmuV8mvXcmvX9nDYuXISOXISuXLXPLXTvDVUvHYUvLYVPPaVPPaVvLbZfTdZfTdZ/TdaPTeaPTeafnhUvzmVf3oVv7pWP7pWf3pXv3pX/7qX/rlY/nla/zoYv7qY/7qZP7rZf7qZv7rZ/7raP7raf7rav7sa/7sbPfkffrncvvqdP3rcf7scf3sc/7tdf7tdv7teP7teYW6hJWtiqDDnLDPrLTIrbTOrbbZtrnWtcq7gse/rsnBsN/NoN/UqebXme3dm+3dnOTZvfrqhf7ugP3ugv7vhP7vhfrqifrrjfrrj/7viP7viv3vjf3vjvDgnPHhnfDhnvHhn/nrnP7wj/3wkP3wkf3wk/3wlP3wlv7wl/3xmeziv/DhofDipfDjrPnso/HlufHluvrvtfnvt/70tP71tv71t/71uOfdwPPowPPpx/74y+vq6vX09PX19fv7+/z8/P39/f7+/v///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAEAAQAAAI6QATCRxI0FAhQwQTCkR0pIAAAg+aKFEoMAmAAAwSHDCgQCCgO3fiHEq0xIEgRE4QDFiQyA6eQIHyTBmJSCCTBg2Q/EGjh0+fPXWo0BnqB5FRRHPEtHEDB84bNmvUjHlSU6AcIEJ+iDhhokQJEiMwkLFyJZGZFi482Fhro8aMFyxUZICSqMyKFCBq4MiR4wYNuCggDDLbggMNHkOMGCESRIcMDXQTnZERYkeRLWDAcMlSJEaEwZI/3BDCJQ0bNmrCaNkQOVGVDjB8YPHy5YuXLj0kgE4khQKFChYuCL9gYUKUgoSSK18+cmBAADs='
saveiconString = b'R0lGODlhEAAQAPcAAEJCQkVFRVxcXF9fX2ZmZnV1dS5y0DRvyDZwyDZ2zzF00DN20Dd30Dd40Dp50F9qlUJyvXB2kXF3kkF90SqB4y2D4y+E4zGE4TGF4zeI4TGN7TKO7TSP7TiI4zyN5jaQ7TiR7TmS7TuT7j6T7DyT7j6U7kqD0UqK006L00+M006N1lCAzFCN01yM01aV3UCN5ECV7kSX7kqT5E+e712c5F2d5l+e5l+e51yl8GyU1GOg6GSh6G6l53Wp53Wp6Haz8o+p0Zuv0qCmwbK307m/2pDB9bvB3K7I6rnL5bzO6M7LztbT1tjY2Orq6u/v7/Dw8PHw8fLy8vT09Pf39/v7+/z8/P7+/v///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAEAAQAAAIzgCfPKEisKDBgVYEHvGRBInDhw6T9AhShQqPIlOkaNyocUqRHEue1PjhpInJkyad/Gih5IkMHBk5bpyCw0TLFzNiypQyZcaElh1ilER50kkMBy0tgNApcwoIBS0pbJjK4YPVDxw2aNhgIOoGDmCvYv3KtWWFDyEynFDhgoaNGx5AfID6xEIIESgKEGASpcoVHSJC0MVAokQKAQD4+t1RgsQCJVQulIDBYkAAxVcYjzigxAqQBA0gRJAgZAgRIysYIHgA5UmVJUpiy56tpHVAADs='
cuticonString = b'R0lGODlhEAAQAPcAAHx8fDx7vjB2wDF3wTN4wTJ5xTZ5wDR5wjR7xDd8xT+Eyz2F0mOCo2WHqWWGqmqLrkKBxEKGzkmIyUmIykqJy1KR1FCR1laU1nqizIKCgoWFhYaGho2NjZSUlJaWlp2dnZ6enp+fn4maraCgoKOjo6ampqenp6mpqaurq6ysrK+vr7CwsLKysri4uIWny4qz3ZCuzZOy05S22Jq52J294K68y7TF2KvI563J58PDw87Ozs3Q09DQ0NHR0dPT09TU1NXV1dfX19jY2NnZ2dvb29zc3N3d3d7e3t7n8ebm5ujo6Orq6uzs7O/v7/Dw8PPz8/T09PP2+fr6+vv7+/z8/P39/f7+/gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAEAAQAAAIpwCdCHRCZeBAKlYMCqSiIojBJiuKKHQyxQQKKQNzmOgx0QoLEDwEMgnRYclEJ0c8jMDYwkOKhBOrlOCgYwmHDUpOCiSiwcMJDSZgnqzyIUMGADl1ChRilITQkzciLFigYEbBkzgGNLBg4QECGE8FWqHg4MmFCz1kGEgSs0CNKBUq7EBSwEfMBC5eSJiAgYaAHydjHAggwgYEAgygDDUyZIqTJEAUDwwIADs='
copyiconString = b'R0lGODlhEAAQAPcAAJytx5+63J+63Z+73qK0zKSyyKq+2qq/26q/3K7C3rHE36fG6KrC4bXI4bXM5rnS7b3V777W77fT8LXT9bfU9rrT8L3W8b7X8r/Y8b7Y8rzY9MTL1MfO2M3T3d3d3t7e38LT5sDV68LY7sPZ78XY7MbZ7cTZ787c6szd78DY8sDa9MHa9cbd9Mjc8cnd8s7e8Mzf99Hd7M7g883h9Mzg9c/i9tfh69Xh79Xi79ji7Nrk7tvl793j69/m7dDg8tLi89Lj9NDj9tbi8Nbm9tfn99jk8tnl89nm89rn9Nzp9t3q9+rq6/Dw8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAEAAQAAAIpACZCBxIsOBAIEcSHvHRw+DAIUkiJqnxgIdDJjRWsEiBQUKFBSccykCyg4iSk0qCODDowogOiBJpwFhJ0EKGEjNU6FShgcKEAQRHCMnxQ6FRBR8GisBhw0eRp1CLJPAwEIIFEi0uaN1qQQBVgSaYvhBCtiwOBF+ZMGgAAgWOt3BvHEjbgcOGCBby6rUQIO3AEDECC45hwK9AAgUSKy4AYMnFxwEBADs='
pasteiconString = b'R0lGODlhEAAQAPcAANGqL9awN+u9HOy+H+q+JuW+O9O0VM65ddO5Zu3AJerALO3AKOrBMv/NIv/OJf/OJ//OKv/PK//PLP7QL//QMP7QMv/RM/7RNP/SNf/SOP/SOf/TPP/TPerEQurIU/7UQf7UQv7UQ/7ZV/7ZWOrNZ+jQfP7eb/7ecIibvLGykJOox52qwJ2rwai9xqO936S+26q/3K3B3LHC27LD3bbH3LXG3rfQ6r3V777W77zX87zX9NTCisTMrNHFotPUqtPWsObRiOjSierUiOjbsP/liv/qo//rpNDQ0dLS1NPT1djY2tra2sPY7sTZ78HZ8cTa8Mfd88Xc9Mbe98jd8cjc9sjd98jf983g9M7g99fj79Lj9dbm9tbm99jk8Nnl8dvn897p9d/r9+Dg4fDw8PT09Pb29vn5+fv7+/z8/P39/QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAEAAQAAAI0wDHjElz5sqNgzdsmEEjsOGQIEJaLJm45IUQID3SCExTwogRHzxChixS5ICYhiSIqFzJEkGShh5MnDghxYpNmz8MvBTYQYSIEVvCCA3DpUoKJA0ZfAARQguYp2C0YKFCg+EYAhMqXIASpWuUKzpyuFAiUECDBxCmfFnL9kuNnQMcRKDwxIvdu15m7EwgwUIGHE4CC3YCY+cCChk2MMnCuHEWGS/RKMCggUOTLpgzd4EscAeAAAUADw4cY2caMUmOqGDBmvWKFSjINhRYhozt27Y1BgQAOw=='
undoiconString = b'R0lGODlhEAAQAPcAAClk0yto1S1q1S5q1i9t2DZp0jZq0jZq0zVr1Dds1Ddu1Tdv1jpr0Dlt0zht1Dht1Thu1Thv1jRz2Tlw1jpx1ztz1jpy1zxw1Txy1j1z1zx02D112T522D542zt/4UB01UZ61EF93UF+3kyI31+P20KB4ECG5UWD4EaO6UyX7Vid62CK2G2Q2GyQ2WyR2m6T23GS13WX1XKW23Cw8Yai1oWk3o+t34Os54q254298pi05J624Z6646u826W746S85Kq74LC/4ZzB6KfB5KLB66HF76vC5KnH7LTK6L7N57/N6MLP58HQ5snV6czW6c/Y59Pa6dLc6Nzf59Lf8N/i6N3i6+Hk6ubn6+Tn7ubo7ers7urs7+/v7+zu8e7w8/Dw8PHx8fLy8gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAEAAQAAAIsAC/CBz4BYuTJlXAEISiUOCSFx8mTMiwQslAGEHAbKlxAcIEChY0bOCwQyELBkBkOPBoAQMIDh1iJvnSokCDlRMq0JDCxYqNECJIgGlhAMGDCRh6NPwCRkeJE09aHEgQwUKMMAS/dBnhwYgLBAoWDBDgY6nAGyZ4tGiAAEAAAhJ+mCWCYkgWKnjzWsE68EgKJlkDCyyi4orgwDlwmD0MZkaUw1mnCFl8GIkWyFm9DAwIADs='
redoiconString = b'R0lGODlhEAAQAPcAABtSyitp1ixr1y1s2C5u2TFv2Dhq0j1u0jFy2zJ03DRz2jZ22z922T932jl53Dp73T942jx93kZ21kZ310d61UJ720V42EV52UZ62UZ62kd820Z+3Eh21Uh21kp400p510970k5600x51kx810h92lB71lB91V6G1miN12iQ23KT1XWX2Xqe332e3oKg3IWj3Ymm3Ymn3o2p3ZOu3ZSx3pez35mw3Jmx3Zix35qy3Zqz3oOj4Iun4Jqy4J204p215Km626q836W64qa85qy/5LvH363A5rvJ5cXQ5cHQ6cfU68nT5svW6dLZ59HZ6dLa6dfd6tXd69/i6Nzj7+Dk6eHm7ufo6unq7evs7+/v7+7v8O/w8O/w8e7w8/Dw8PDw8QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAEAAQAAAIrwC9CPTyBQoTJ1gGKhSohcgJER0+mHgRReETL1pcdOAgoaOECSOEfPECw4YXHx06SPAA4qMFCxhwxMhwo0qJDiGAWMnSZMUFDBlIaNCQw8jGIiMFfpHBoAGECht08OigIunALxQCCBhAYEaLDkEWbmHBFUGCBDR2SECiUAuLAgoWOHgQocYPA0sUcqEipa/fK0oAHFlIWOmBHoULD0FhNbHSFAkdK5ySRPLCLpa9BAQAOw=='
onfindiconString = b'R0lGODlhEAAQAPcAAEBAQENDQ0dHR1tbW2VlZXR0dIGBgYODg4yMjJOTk5WVlZ2dnZedpJ2gpaGjpKKjpqCip6Kkp6enp6enqKusraarsqGsvLi5vKa0xq280LG9z7C/07fAy77EzbnE1rrH27HH5LLI5cLCwsPDw8XFxcDGz8bIzMvLy8nQ2tDQ0NLS0tPT09XX2tra2tzc3N3d3dLi+9fl/dfn/9jm/Nrn/9no/dno/9zo/Nzp/9/r/d3q/9/s/+Xl5eDr/+Ls+eHs/+Lu/+Tu/uTu/+fw/ubw/+rw+ejx/+vz/ury/+7z+O70//Dw8PD1/vD2/QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAEAAQAAAIjwCXCBxIsCBBHig2ZCjhwuBAFiFgEDFy48MFhy9ABEFihIiQHx5GGOwAo+NHHTZiQDCIAchJGzBzMDBo4UcPHDJs6AAypIHBCjNoyNDxgwiSIg4MktBQY4cQJEqamBDhkAIHH0eYJDGhYIXDJSkeNIgwQcWCAwi+GgQwwIDaggEIFHhLUECCE3QHSmiRt2BAADs='
abouticonString = b'R0lGODlhEAAQAPcAAB9xxh5wxyFyyCt0wC52wSl3ySl3yix5yi56yC16yi56yzB7yjJ9zDN+zDV/zUp/tjaAzTmBzjmCzjyDzj2Ez1CCt2OOvG2VvkCDyU2HxEGH0EWJ0EiL0kqM0kyO0k2O01aRzlCQ01KR1FKS1FST1FST1VWU1ViV1VqW1lyY1l+a12uVwG2WwG2bzGGY0mCa12Oc2Gme2Gif2W2j2m6j23Sk1XWm2Xqr3nys3oGhwoimxImoyoqqyoGt2oCv34ax34203IGv4IKw4Iay4Yi04Y+34Yy24pO75Ja85Zm+5aa2xqS92J3B5rPH3KLE56TC4aTC4qXG6KrH5qzG46zI5bXM5LPN6L/Q473T6sDI0cHJ0sLK0sLK08DN2sHO2sPR4MLU58fT4MDV68LW7MjW5dHi8/Dw8Pb29vT3+vj4+Pj4+fj7/fn7/v7+/v///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAEAAQAAAI4ADNCDSDRgwVKE+mgFEzsOGYIlEiRnQChEybhlKMHNnIceOPJhfNYLnho6QPJGWImLQRhmAMGjBhMlkTJCaNFmmsoNi5E8aQIS94oijRpQeHo0dlsHGTAulRHi4gSJ0qxI2HqVJXgBBgIIGCrzjcbPh6oIAACzUEKJBAoe0QNyPaSlAQIEcVARI+lNiLxI2MEiQ6OACQRQ2GBh94JnEzA8WJDgoenDFzpQCFEDtTqHD8QcKALQLbLEEwocMIEyVEcIhAQElIM22+ZGBAQYMGCQsqcHk9MI2XHSwu6NAyeWBAADs='


newicon = PhotoImage(data=newiconString)
openicon = PhotoImage(data=openiconString)
saveicon = PhotoImage(data=saveiconString)
cuticon = PhotoImage(data=cuticonString)
copyicon = PhotoImage(data=copyiconString)
pasteicon = PhotoImage(data=pasteiconString)
undoicon = PhotoImage(data=undoiconString)
redoicon = PhotoImage(data=redoiconString)

#Define a menu bar
menubar = Menu(root)

#File menu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", accelerator='Ctrl+N', compound=LEFT, image=newicon, underline=0, command=new_file)
filemenu.add_command(label="Open", accelerator='Ctrl+O', compound=LEFT, image=openicon, underline=0, command=open_file)
filemenu.add_command(label="Save", accelerator='Ctrl+S', compound=LEFT, image=saveicon, underline=0, command=save)
filemenu.add_command(label="Save as", accelerator='Shift+Ctrl+S', command=save_as)
filemenu.add_command(label="Exit", accelerator='Alt+F4', command=exit_editor)
menubar.add_cascade(label="File", menu=filemenu) 

#Edit menu
editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="Undo", compound=LEFT, image=undoicon, accelerator='Ctrl+Z', command=undo)
editmenu.add_command(label="Redo", compound=LEFT, image=redoicon, accelerator='Ctrl+Y', command=redo)
editmenu.add_separator()
editmenu.add_command(label="Cut", compound=LEFT, image=cuticon, accelerator='Ctrl+X', command=cut)
editmenu.add_command(label="Copy", compound=LEFT, image=copyicon, accelerator='Ctrl+C', command=copy)
editmenu.add_command(labe="Paste", compound=LEFT, image=pasteicon, accelerator='Ctrl+V', command=paste)
editmenu.add_separator()
editmenu.add_command(label="Find", underline=0, accelerator='Ctrl+F', command=on_find)
editmenu.add_separator()
editmenu.add_command(label="Select All", accelerator='Ctrl+A', underline=7, command=select_all)

#View menu

viewmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=viewmenu)
showln = IntVar()
showln.set(1)
viewmenu.add_checkbutton(label="Show Line Number", variable=showln)
showinbar = IntVar()
showinbar.set(1)
viewmenu.add_checkbutton(label="Show Info Bar at Bottom", variable=showinbar, command=show_info_bar)
hltln = IntVar()
viewmenu.add_checkbutton(label="Highlight Current Line", variable=hltln, command=toggle_highlight)
themesmenu = Menu(viewmenu, tearoff=0)
viewmenu.add_cascade(label="Themes", menu=themesmenu)

#we define a color scheme dictionary containg name and color code as key value pair
clrschms = {
'1. Default White': '000000.FFFFFF',
'2. Greygarious Grey':'83406A.D1D4D1',
'3. Lovely Lavender':'202B4B.E1E1FF' , 
'4. Aquamarine': '5B8340.D1E7E0',
'5. Bold Beige': '4B4620.FFF0E1',
'6. Cobalt Blue':'ffffBB.3333aa',
'7. Olive Green': 'D1E7E0.5B8340',
}
themechoice= StringVar()
themechoice.set('1. Default White')
for k in sorted(clrschms):
    themesmenu.add_radiobutton(label=k, variable=themechoice, command=theme)

#About menu
aboutmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="About", menu=aboutmenu)
aboutmenu.add_command(label="About", command=about)
aboutmenu.add_command(label="Help", command=help_box)

root.config(menu=menubar)

#shortcut bar and line number 
shortcutbar = Frame(root, height=25)
icons = [newiconString, openiconString, saveiconString, cuticonString, copyiconString, pasteiconString, undoiconString, redoiconString, onfindiconString, abouticonString]
commands = ['new_file', 'open_file', 'save', 'cut', 'copy', 'paste', 'undo', 'redo', 'on_find', 'about']
for i, icon in enumerate(icons):
    tbicon = PhotoImage(data=icon)
    cmd = eval(commands[i])
    toolbar = Button(shortcutbar, image=tbicon, command=cmd)
    toolbar.image = tbicon  #http://effbot.org/tkinterbook/photoimage.htm
    toolbar.pack(side=LEFT)
shortcutbar.pack(expand=NO, fill=X)

lnlabel = Label(root,  width=2,  bg = 'antique white')
lnlabel.pack(side=LEFT, fill=Y)

#Text widget and scrollbar widget
#####################################
textPad = Text(root, undo=True)
textPad.pack(expand=YES, fill=BOTH)
scroll=Scrollbar(textPad)
textPad.configure(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT, fill=Y)

#Info Bar
infobar = Label(textPad, text='Line: 1 | Column:0')
infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')


#context popup menu
cmenu = Menu(textPad,tearoff=0)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    cmenu.add_command(label=i, compound=LEFT, command=cmd)  
cmenu.add_separator()
cmenu.add_command(label='Select All', underline=7, command=select_all)
textPad.bind("<Button-3>", popup)

#################################################
#Add events
#Binding events
textPad.bind('<Control-N>', new_file)
textPad.bind('<Control-n>', new_file)
textPad.bind('<Control-O>', open_file)
textPad.bind('<Control-o>', open_file)
textPad.bind('<Control-S>', save)
textPad.bind('<Control-s>', save)
textPad.bind('<Control-A>', select_all)
textPad.bind('<Control-a>', select_all)
textPad.bind('<Control-f>', on_find)
textPad.bind('<Control-F>', on_find)
textPad.bind('<KeyPress-F1>', help_box)

textPad.bind("<Any-KeyPress>", update_line_number)
textPad.tag_configure("active_line", background="ivory2")
root.mainloop()