
import os
import sys
import yaml

HERE_PATH =  os.path.abspath( os.path.dirname( __file__ ))
PROJECT_ROOT = os.path.abspath( os.path.join(HERE_PATH, "..") )
if sys.path.count(PROJECT_ROOT) == 0:
    sys.path.insert(0, PROJECT_ROOT)


from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, flash, redirect


from ogt import ags4, ogt_doc


app = Flask(__name__,
            static_url_path="",
            static_folder=os.path.join(PROJECT_ROOT, "static"))



ALLOWED_UPLOADS = ['ags', 'ags4']


nav = [
    {"url": "/", "label": "Home"},
    #{"url": "/about", "label": "About"},
    {"url": "/ags4", "label": "AGS4 Data Dict"},
    {"url": "/viewer", "label":"Viewer"},
    {"url": "/convert", "label":"Convert"}
]

class Context(object):
    pass

def make_page_context(url, page_title):
    """Simple way to bang all vaiables into context"""
    c = Context()
    c.error = None
    c.site_name = "OGT Server"
    c.nav = nav
    c.url = url
    c.page_title = page_title
    return c
    """
    c = {"site_name": "OGT Server",
        "nav": nav,
        "url": url,
        "page_title": page_title
    }
    return c
    """

def xrender(ext, data):
    """Our custom function to knock out the stuff"""
    pass

@app.route('/')
def h_index():
    c = make_page_context("/", "OGT Server")
    return render_template('index.html', c=c)

@app.route('/about')
def h_about():
    c = make_page_context("/about", "About")
    return render_template('about.html', c=c)

@app.route('/viewer')
def h_viewer():
    c = make_page_context("/viewer", "Viewer")
    return render_template('viewer.html', c=c)


@app.route('/ags4')
def h_ags4_index():
    c = make_page_context("/ags4", "AGS4 Data Dict")
    return render_template('ags4.html', c=c)

@app.route('/ags4/<page>')
@app.route('/ags4/<page>/<xcode>')
def h_ags4_widget(page, xcode=None):

    tabs = [
        {"url": "groups", "label": "Groups"},
        {"url": "abbrs", "label": "Abbreviations"},
        {"url": "types_units", "label": "Types & Units"},
        #{"url": "data_types", "label": "Data Types"},
        {"url": "widget", "label": "Widget"},
    ]

    c = make_page_context("/ags4", "AGS4")
    c.tabs = tabs
    c.page = page

    tpl = "ags4.html"
    if page == "widget":
        tpl = 'ags4_widget.html'

    elif page == "abbrs":
        c.ags4_abbrs = ags4.DD.abbrs_dict
        tpl = "ags4_abbrs.html"

    elif page == "groups":
        c.ags4_classified_groups = ags4.DD.classified_groups()
        tpl = "ags4_groups.html"

    elif page == "group":
        c.page = "groups"
        c.ags4_group = ags4.DD.group(xcode)
        tpl = "ags4_group.html"

    elif page == "types_units":
        c.data_types = ags4.DD.data_types_list
        c.units = ags4.DD.units_list
        tpl = "ags4_types_units.html"


    return render_template(tpl, c=c)


@app.route('/ags4/groups.<ext>')
def ags4_groups(ext="json"):
    if ext == "json":
        return jsonify({"groups": ags4.groups(), "success": True})

    if ext in ["yml", "yaml"]:
        return yaml.dump(ags4.all())


@app.route('/ags4/groups_list.<ext>')
def ags4_groups_list(ext="json"):
    if ext == "json":
        return jsonify({"groups_list": ags4.DD.groups_dict().values(), "success": True})


@app.route('/ags4/group/<group_code>.<ext>')
def ags4_group(group_code, ext="json"):
    if ext == "json":
        return jsonify({"group": ags4.DD.group(group_code), "success": True})

    if ext in ["yml", "yaml"]:
        return yaml.dump(ags4.all())





@app.route('/ags4/abbrs_list.<ext>')
def ags4_abbrs_list(ext="html"):
    if ext == "json":
        return jsonify({"abbrs_list": ags4.abbrs(), "success": True})

    if ext in ["yml", "yaml"]:
        return yaml.dump(ags4.all())

    c = make_page_context("/ags4/groups", "AGS4 Groups")

    # TODO Make its nested based on class
    c['ags4_classified_groups'] = ags4.classified_groups()
    #print c['ags4_classified_groups']
    return render_template("ags4_groups.html", c=c)






@app.route('/ags4/examples/all')
@app.route('/ags4/examples/all.<ext>')
def ags4_examples_all(ext="html"):

    if ext == "json":
        return jsonify({"examples": ags4.examples(), "success": True})

    c = make_page_context("/ags4/examples", "AGS4 Widget")
    return render_template('ags4_examples.html', c=c)

@app.route('/ags4/examples')
def ags4_examples_page():
    """Examples list page"""
    c = make_page_context("/ags4/examples", "AGS4 Examples")
    c.examples, c.error = ags4.examples_list()
    return render_template('ags4_examples.html', c=c)

@app.route('/ags4/examples.json')
def ags4_examples_json():
    """Examples list json"""
    return jsonify({"examples": ags4.examples_list(), "success": True})


@app.route('/ags4/example')
@app.route('/ags4/example.<ext>')
def ags4_example(ext="html"):

    file_name = request.args.get('file_name')
    if not file_name:
        panic
    ex, err = ags4.example(file_name)
    if ex:
        #print "EX=", ex
        doc = ogt_doc.OGTDocument()

        #doc.source_file_path = ex['file_name']
        err = doc.add_ags4_string(ex['contents'], file_name)
        doc.opts.extended = True
        doc.opts.include_stats = False
        doc.opts.include_source = True
        #if request.args.get('format') == "json":
        #        return jsonify(doc.to_dict())
        if ext == "json":
            return jsonify({"document": doc.to_dict(), "success": True})

    c = make_page_context("/ags4/examples", "AGS4 Widget")
    return render_template('ags4_example.html', c=c)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOADS

@app.route('/convert', methods=["GET", "POST"])
def c_convert():

    c = make_page_context("/convert", "AGS4 Convert")
    c['err_mess'] = None
    if request.method == "POST":
        if 'ags_file' not in request.files:
            c['err_mess'] = "Need a file"

        else:
            file = request.files['ags_file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                c['err_mess'] = "Need a file"

            else:
                if file and allowed_file(file.filename):


                    doc = ogt_doc.OGTDocument()
                    doc.source_file_path = secure_filename(file.filename)
                    err = doc.load_ags4_string(file.read())

                    return jsonify(doc.to_dict())

    ## convert example
    """
    if request.method == "GET":
        ex_name = request.args.get('example')
        if ex_name:

            ex = ags4.example(ex_name)
            #print "EX=", ex
            doc = ogt_doc.OGTDocument()
            doc.source_file_path = ex_name
            err = doc.load_ags4_string(ex['contents'])

            if request.args.get('format') == "json":
                return jsonify(doc.to_dict())
    """

    return render_template('convert.html', c=c)

"""
@app.route('/convert.json', methods=["GET", "POST"])
def ajax_convert():

    ex_name = request.args.get('example')
    if ex_name:
        ex = ags4.example(ex_name)
        #print "EX=", ex
        doc = ogt_doc.OGTDocument()
        doc.source_file_path = ex_name
        err = doc.load_ags4_string(ex['contents'])

        return jsonify(doc.to_dict())
"""
