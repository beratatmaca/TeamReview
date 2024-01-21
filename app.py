# -*- coding: utf-8 -*-

from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session, jsonify
import json
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only


def create_xml(output_file):
    root = ET.Element("root")
    category_element = ET.SubElement(root, "category", name="My Documents")
    
    scan_path(category_element, "uploads")

    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)


def scan_path(root, folder_path):
    folders = [ f.name for f in os.scandir(folder_path) if f.is_dir() ]
    files = [ f.name for f in os.scandir(folder_path) if f.is_file() ]
    for folder_name in folders:
        folder_element = ET.SubElement(root, "folder", name=folder_name)
        scan_path(folder_element, folder_path + "/" + folder_name)
    for file_name in files:
        file_element = ET.SubElement(root, "file")
        file_element.text = file_name

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if helpers.credentials_valid(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = helpers.get_user()
    return render_template('home.html', user=user, root=folder_contents_root, level = 1, index = 0, render_tree=render_tree)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


# -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            password = helpers.hash_password(request.form['password'])
            email = request.form['email']
            if form.validate():
                if not helpers.username_taken(username):
                    helpers.add_user(username, password, email)
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Signup successful'})
                return json.dumps({'status': 'Username taken'})
            return json.dumps({'status': 'User/Pass required'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))


# -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                password = helpers.hash_password(password)
            email = request.form['email']
            helpers.change_user(password=password, email=email)
            return json.dumps({'status': 'Saved'})
        user = helpers.get_user()
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))



def render_tree(element, level, index):
    result = ''
    if element.tag == "folder":
        result += f"<li role=\"treeitem\" aria-level=\"{level}\" aria-setsize=\"3\" aria-posinset=\"{index}\" aria-expanded=\"false\" aria-selected=\"false\" type=\"folder\">"
        result += f'<span>{element.get("name")}</span>'
        result += "<ul role=\"group\">"
        for index, child in enumerate(element):
            result += render_tree(child, level+1, index)
        result += "</ul></li>"
    elif element.tag == "file":
        result += f'<li role=\"treeitem\" aria-level=\"{level}\" aria-setsize=\"5\" aria-posinset=\"{index}\" aria-selected=\"false\" class=\"doc\" type=\"file\">{element.text}</li>'
    elif element.tag == "root":
        for index, child in enumerate(element):
            result += render_tree(child, 0, index)
    elif element.tag == "category":
        for index, child in enumerate(element):
            result += render_tree(child, 1, index)

    return result

@app.route('/process_data', methods=['GET', 'POST'])
def process_data():
    response = {
        "change" : False,
        "content": ""
    }
    data_from_js = request.json  # Assuming data is sent as JSON
    if data_from_js['type'] == 'file':
        root_folder = "./uploads"
        for parent in data_from_js['parents']:
            root_folder = os.path.join(root_folder, parent)
        file_path = os.path.join(root_folder, data_from_js['label'])
        with open(file_path, 'r') as file:
            text = file.read()
            file.close()
            response["change"] = True
            response["content"] = text
    return jsonify(response)

with app.app_context():
    create_xml('folder_contents.xml')
    with open('folder_contents.xml', 'r') as file:
        xml_data = file.read()
        file.close()
        folder_contents_root = ET.fromstring(xml_data)

# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")
