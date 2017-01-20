<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        <script>

            function clearContainer(){
                document.getElementById("maincontainer").innerHTML = "";
            }

            function addRoom(){
                clearContainer();
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {

                          content = '\
                                <h2 class="form-signin-heading">Add a Room</h2>\
                                <label for="inputCampus" class="sr-only">Campus</label>\
                                <input type="campus" id="inputCampus" class="form-control" placeholder="Campus" required autofocus>\
                                <label for="inputBuilding" class="sr-only">Building</label>\
                                <input type="building" id="inputBuilding" class="form-control" placeholder="Building" required>\
                                <label for="inputRoom" class="sr-only">Room Name</label>\
                                <input type="room" id="inputRoom" class="form-control" placeholder="Room Name" required>\
                                <div class="checkbox">\
                                </div>\
                                <button class="btn btn-lg btn-primary btn-block" type="submit">Add</button>\
                              </form>\
                             </div>';

                          content = content + '</tbody> </table> </div>';
                          document.getElementById("maincontainer").innerHTML = content;
                    }
                };
                xhttp.open("GET", "/addroom", true);
                xhttp.send();
            }

            function showRoom(roomid){
                clearContainer();
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        room = JSON.parse(this.responseText);
                        content = '\
                            <h1>'+room.name+'</h1>\
                            <h2>'+room.campus+'</h2>\
                            <h2>'+room.building+'</h2>\
                            <h2> Occupancy:'+room.occupancy+'</h2>\
                            <h2> Capacity:'+room.capacity+'</h2>\
                            <button type="button" class="btn btn-lg btn-default">Check In</button>\
                            <div class="table-responsive" id="roomuserscont">\
                                <table class="table table-condensed">\
                                    <tr>\
                                        <th><h2>Users</h2></th>\
                                    </tr>\
                                    <tbody>';

                        for (var i=0; i<room.users.length; i++) {
                           content = content + '<tr><td>'+room.users[i].username+'</td></tr>';
                        }

                        content = content + '</tbody> </table> </div>';
                    }
                    document.getElementById("maincontainer").innerHTML = content;
                };
                xhttp.open("GET", "/room/"+roomid, true);
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
                                            <th>Building</th>\
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
                                            <td>'+room.building+'</td>\
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
    <body>

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
            <a class="navbar-brand" href="#" onclick="clearContainer()">{{username}}</a>
          </div>
          <div id="navbar" class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
             <li class="active"><a href="#" onclick="addRoom()">Add Room</a></li>
             <li class="active"><a href="#" onclick="listRooms()">Rooms</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div><!--/.container-fluid -->
      </nav>



      <div class="jumbotron" id="maincontainer">

      </div> <!-- /container -->


    </body>
</html>
