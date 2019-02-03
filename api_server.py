import flask
from flask import request
import sqlite3
import json
from string import Template
import uuid

app = flask.Flask(__name__)
#app.config["DEBUG"] = True


def all():
	db = sqlite3.connect('resources.db')
	db_c = db.cursor()
	db_c.execute('SELECT * FROM links where approved=1')
	links = db_c.fetchall()

	db_c.execute('SELECT * from categories')
	categories = db_c.fetchall()

	db.close()


	return (links, categories)

@app.route('/', methods=['GET'])
def home():

	all_things = all()



	html_open = '''
	<!doctype html>
<html class="no-js" lang="">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link rel="manifest" href="site.webmanifest">

        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

		<script src="https://code.jquery.com/jquery-3.2.1.min.js" integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=" crossorigin="anonymous"></script>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>

		<script>
function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("myTable2");
  switching = true;
  dir = "asc"; 
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount ++; 
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
</script>

		<script>
			function myFunc(){
				$.post('/add', {'inputTitle': $("#inputTitle").val(), 'inputURL': $("#inputURL").val(), 'inputDesc': $("#inputDesc").val(), 'inputCat': $("#inputCategory option:selected").text()}, function(data, stat){ alert("Thanks for the submission!");  $("#inputTitle").val(''); $("#inputURL").val(""); $("#inputDesc").val(""); });
			}
		</script>

    </head>
    <body class="container">
    
    <!-- 
    	<div class="alert alert-success alert-dismissible fade show" role="alert" id="successAlert">
	  		Link submitted, thanks!
	  		<button type="button" class="close" data-dismiss="alert" aria-label="Close">
		    <span aria-hidden="true">&times;</span>
	  		</button>
		</div>
     banner -->
     <! -- Modal -->
        <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h4 class="modal-title" id="myModalLabel">
                  Add a resource
                </h4>
              </div>
              <div class="modal-body">
  					

  					<form id="modalForm" action="/add" method="POST">
  <div class="form-row">
    <div class="form-group col-md-6">
      <input type="text" class="form-control" id="inputTitle" placeholder="Title">
    </div>
    <div class="form-group col-md-6">
      
      <input type="text" class="form-control" id="inputURL" placeholder="URL">
    </div>
  </div>
  <div class="form-group">
    
    <input type="text" class="form-control" id="inputDesc" placeholder="Description">
  </div>
  <div class="form-group">
  	<select class="form-control" id="inputCategory"> ''' 


  	html_body = '''

  	</select>
  </div>

  	</form>
              </div>
              <div class="modal-footer">
                              <button type="button" class="btn btn-success" data-dismiss="modal" onclick="myFunc()">Submit
                </button>

                <button type="button" class="btn btn-default" data-dismiss="modal">
                  Close
                </button>
              </div>
            </div><!-- /.modal-content -->
          </div><!-- /.modal-dialog -->
        </div><!-- /.modal -->
        <h1 style="display:inline-block; padding-right:20px;">Community Resources</h1><button class="btn btn-primary" data-toggle="modal" data-target="#myModal">Add A Resource</button><table class="table table-striped table-hover table-sm" id="myTable2"><thead><tr><td onclick="sortTable(0)">Name</td><td>URL</td><td>Description</td><td onclick="sortTable(3)">Category</td><td>GO!</td></tr></thead><tbody>'''

	html_close = '''</tbody></table></body><script>window.ga=function(){ga.q.push(arguments)};ga.q=[];ga.l=+new Date;ga('create','UA-129297535-8','auto');ga('send','pageview')</script><script src="https://www.google-analytics.com/analytics.js" async defer></script></html>'''

	return_string = html_open;

	for cat in all_things[1]:
		return_string += "<option>" + cat[0] + "</option>"

	return_string += html_body

	for link in all_things[0]:
		return_string += '<tr><td>' + link[0] + '</td>' + '<td>' + link[1] + '</td>' + '<td>' + link[2] + '</td><td>' + link[3] +  '</td><td><a class="btn btn-primary" href="' + link[1]  +  '" target="_blank">GO!</a></td></tr>'

	return_string += html_close
	return return_string



@app.route('/add', methods=['POST'])
def add():
	title = request.form['inputTitle']
	url = request.form['inputURL']
	desc = request.form['inputDesc']
	category = request.form['inputCat']


	print("trying to add: " + title)
	db = sqlite3.connect('resources.db')
	db_c = db.cursor()

	db_c.execute('SELECT * FROM links')
	links = db_c.fetchall()


	rand_uuid = str(uuid.uuid4())
	sql_statement = ''' INSERT INTO links VALUES(?,?,?,?,?,?) '''
	db_c.execute(sql_statement, (title, url, desc, category,0, rand_uuid[0:4] ))
	db.commit()
	db.close()

	return '200'

@app.route('/a/b/c/d/e/f/g/admin', methods=['GET'])
def admin():
	db = sqlite3.connect('resources.db')
	db_c = db.cursor()

	db_c.execute('SELECT * FROM links where approved=0')
	links = db_c.fetchall()


	html_open = '''
	<!doctype html>
<html class="no-js" lang="">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link rel="manifest" href="site.webmanifest">

        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

		<script src="https://code.jquery.com/jquery-3.2.1.min.js" integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=" crossorigin="anonymous"></script>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>

		<script>
			function myFunc(){
				$.post('/add', {'inputTitle': $("#inputTitle").val(), 'inputURL': $("#inputURL").val(), 'inputDesc': $("#inputDesc").val()}, function(data, stat){ console.log(data); });
			}
		</script>

    </head>
    <body class="container">
        <h1>Community Resources</h1><table class="table"><thead><tr><td>ID</td><td>Name</td><td>URL</td><td>Description</td><td>Category</td><td>Approve</td><td>Deny</td></tr></thead><tbody>'''

	html_close = '''</tbody></table></body><script>window.ga=function(){ga.q.push(arguments)};ga.q=[];ga.l=+new Date;ga('create','UA-129297535-8','auto');ga('send','pageview')</script><script src="https://www.google-analytics.com/analytics.js" async defer></script></html>'''

	return_string = html_open;

	for link in links:
		return_string += '<tr><td>'+str(link[5])+'</td><td>' + link[0] + '</td>' + '<td>' + link[1] + '</td>' + '<td>' + link[2] + '</td><td>' + link[3]  + '</td><td> <a class="btn btn-success" href="approve/'+ str(link[5]) +'">Yes</a></td><td><a class="btn btn-danger" href="deny/' + str(link[5]) + '">No</a></td></tr>'

	return_string += html_close
	return return_string

app.run()
