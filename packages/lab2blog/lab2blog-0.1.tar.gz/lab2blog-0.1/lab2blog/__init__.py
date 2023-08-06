import nbformat
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
import os


# ----------------------------------------------------------------------
def get_custom_css():
    """"""
    return os.path.join(os.path.dirname(__file__), 'custom.css')


# ----------------------------------------------------------------------
def convert_notebook(notebookPath):
    """"""
    with open(notebookPath) as fh:
        nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)

    exporter = HTMLExporter()
    source, meta = exporter.from_notebook_node(nb)

    source = format_html(source)

    with open(notebookPath.replace('.ipynb', '.html'), 'wb+') as fh:
        fh.write(source.encode('utf-8'))


# ----------------------------------------------------------------------
def format_html(html):
    """"""
    soup = BeautifulSoup(html, 'html.parser')
    style = soup.new_tag(name='style')
    with open(get_custom_css(), 'r') as file:
        style.string = file.read()
    soup.head.append(style)

    intro = soup.find_all(class_='inner_cell')

    title = soup.findAll(name='title')[0]
    title.string = intro[0].text

    break_ = BeautifulSoup("""
<br />
<!--more--><br />
    """, 'html.parser')

    title.insert_after(break_)

    return soup
