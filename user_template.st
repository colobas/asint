<html>
    <head>
<!-- Latest compiled and minified CSS -->
        <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
        <script>

            function checkIn(roomid){
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    listRooms();
                }
                xhttp.open("GET", "/checkin/"+roomid+"/{{user.id}}", true);
                xhttp.send();
            }

            function checkOut(roomid){
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    listRooms();
                }
                xhttp.open("GET", "/checkout/{{user.id}}", true);
                xhttp.send();
            }

            function clearContainer(){
                document.getElementById("maincontainer").innerHTML = "";
            }

            function printRoom(room, roomid) {
                content = '';
                if (!room.checkedin) {
                    content = content + '<button align="center" type="button" onclick="checkIn('+roomid+')" class="btn btn-lg btn-default">Check In</button>';
                } else {
                    content = content + '<button align="center" type="button" onclick="checkOut('+roomid+')" class="btn btn-lg btn-default">Check Out</button>';
                }
                content = content + '\
                <div class="table-responsive">\
                <table class="table table-striped">\
                <thead>\
                   <th>Room name</th>\
                   <th>Campus</th>\
                   <th>Occupancy</th>\
                   <th>Capacity</th>\
                </thead>\
                <tbody>\
                <tr>\
                    <td>'+room.name+'</td>\
                    <td>'+room.campus+'</td>\
                    <td>'+room.occupancy+'</td>\
                    <td>'+room.capacity+'</td>\
                </tr>\
                </tbody>\
                </table>\
                </div>';


                if (room.occupancy > 0) {
                    content = content + '\
                            <h3><b>Users</b></h3>\
                            <ul>';

                    for (var i=0; i<room.users.length; i++) {
                       content = content + '<li>'+room.users[i].username+'</li>';
                    }

                    content = content + '</ul>';
                }
                document.getElementById("maincontainer").innerHTML = content;
            }


            function showRoom(roomid){
                clearContainer();
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        room = JSON.parse(this.responseText);
                        printRoom(room, roomid);
                    }
                };
                xhttp.open("GET", "/room/"+roomid+"/{{user.id}}", true);
                xhttp.send();
            }


            function listRooms(){
                clearContainer();
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {

                        rooms = JSON.parse(this.responseText);


                        content = '\
                            <div class="table-responsive" id="roomtablecont">\
                                <table class="table table-striped">\
                                    <thead>\
                                        <tr>\
                                            <th>Name</th>\
                                            <th>Campus</th>\
                                            <th>Occupancy</th>\
                                            <th>Capacity</th>\
                                        </tr>\
                                    </thead>\
                                    <tbody>\
                       ';

                        for (var i=0; i<rooms.length; i++){
                           var room = rooms[i];


                           content = content + '\
                                        <tr>\
                                            <td><a href="#" onclick="showRoom('+room.id+')">'+room.name+'</a></td>\
                                            <td>'+room.campus+'</td>\
                                            <td>'+room.occupancy+'</td>\
                                            <td>'+room.capacity+'</td>\
                                        </tr>'
                        }

                        content = content + '</tbody> </table> </div>';
                        document.getElementById("maincontainer").innerHTML = content;
                    }
                };
                xhttp.open("GET", "/listrooms", true);
                xhttp.send(); 
            }


        </script>
    </head>
    <body onload="listRooms()">

    <div class="container">
      <!-- Static navbar -->
      <nav class="navbar navbar-default">
        <div class="container-fluid">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
              <span class="sr-only">Toggle navigation</span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="#" onclick="clearContainer()">{{user.username}}</a>
          </div>
          <div id="navbar" class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
              <li class="active"><a href="#" onclick="listRooms()">Rooms</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div><!--/.container-fluid -->
      </nav>
      <div class="jumbotron" id="maincontainer">
            historia de utilizacao
      </div> <!-- /container -->

    </div>
    </body>
</html>

