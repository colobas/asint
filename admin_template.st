<html>
    <head>
        <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
        <script>

            function clearContainer(){
                document.getElementById("maincontainer").innerHTML = "";
            }

            function listCampi(){
                clearContainer();
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        parsed = JSON.parse(this.responseText);
                        content = '\
                            <h2 class="form-signin-heading">Add a Room</h2>\
                            <div class="dropdown">\
                                <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">\
                    Campus\ <span class="caret"></span>\
                                </button>\
                                <ul class="dropdown-menu" aria-labelledby="Campus">';

                        for (var i=0; i<parsed.length; i++){
                            content = content + '<li><a href="#" onclick="listCampusBuildings(';
                            content = content + parsed[i]['id']+')';
                            content = content + '">'+parsed[i]['name']+'</a></li>';
                        }
                        content = content + '</ul> </div>';
                        document.getElementById("maincontainer").innerHTML = content;
                    }
                };
                xhttp.open("GET", "/admin/campi", true);
                xhttp.send();
            }

            function deleteDropdown(id){
                var el = document.getElementById(id);
                if (el) {
                    el.parentNode.removeChild(el);
                }
            }


            function listCampusBuildings(campus_id){
                deleteDropdown("buildings");
                deleteDropdown("rooms");
                deleteDropdown("floors");

                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        parsed = JSON.parse(this.responseText);
                        content = '\
                            <div class="dropdown" id="buildings">\
                                <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu2" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">\
                    Buildings\ <span class="caret"></span>\
                                </button>\
                                <ul class="dropdown-menu" aria-labelledby="Building">';

                        for (var i=0; i<parsed.length; i++){
                            content = content + '<li><a href="#" onclick="listBuildingFloors(';
                            content = content + parsed[i]['id']+')';
                            content = content + '">'+parsed[i]['name']+'</a></li>';
                        }
                        content = content + '</ul> </div>';
                        container = document.getElementById("maincontainer");
                        container.innerHTML = container.innerHTML + content;
                    }
                };
                xhttp.open("GET", "/admin/campus/" + campus_id, true);
                xhttp.send();
            }

            function listBuildingFloors(building_id){
                deleteDropdown("rooms");
                deleteDropdown("floors");

                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        parsed = JSON.parse(this.responseText);
                        content = '\
                            <div class="dropdown" id="floors">\
                                <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu3" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">\
                    Floors\ <span class="caret"></span>\
                                </button>\
                                <ul class="dropdown-menu" aria-labelledby="Floor">';

                        for (var i=0; i<parsed.length; i++){
                            content = content + '<li><a href="#" onclick="listFloorRooms(';
                            content = content + parsed[i]['id']+')';
                            content = content + '">'+parsed[i]['name']+'</a></li>';
                        }
                        content = content + '</ul> </div>';
                        container = document.getElementById("maincontainer");
                        container.innerHTML = container.innerHTML + content;
                    }
                };
                xhttp.open("GET", "/admin/building/" + building_id, true);
                xhttp.send();
            }

            function listFloorRooms(floor_id){
                deleteDropdown("rooms");

                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        parsed = JSON.parse(this.responseText);
                        content = '\
                            <div class="dropdown" id="rooms">\
                                <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu4" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">\
                    Rooms\ <span class="caret"></span>\
                                </button>\
                                <ul class="dropdown-menu" aria-labelledby="Room">';

                        for (var i=0; i<parsed.length; i++){
                            content = content + '<li><a href="#" onclick="addRoom(';
                            content = content + parsed[i]['id']+')';
                            content = content + '">'+parsed[i]['name']+'</a></li>';
                        }
                        content = content + '</ul> </div>';
                        container = document.getElementById("maincontainer");
                        container.innerHTML = container.innerHTML + content;
                    }
                };
                xhttp.open("GET", "/admin/floor/" + floor_id, true);
                xhttp.send();
            }

            function addRoom(room_id){
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        if (this.responseText == "-1"){
                            window.alert("Invalid room ID.");
                            clearContainer();
                        } else if(this.responseText == "-2"){
                            window.alert("Room doesn't have capacity");
                            clearContainer();
                        } else {
                            room = JSON.parse(this.responseText);
                            printRoom(room, room_id);
                        }
                   }
                };
                xhttp.open("GET", "/admin/addroom/" + room_id, true);
                xhttp.send();
            }

            function printRoom(room, roomid) {
                content = '';
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
                xhttp.open("GET", "/room/"+roomid+"/0", true);
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
             <li class="active"><a href="#" onclick="listCampi()">Add Room</a></li>
             <li class="active"><a href="#" onclick="listRooms()">Rooms</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div><!--/.container-fluid -->
      </nav>



      <div class="jumbotron" id="maincontainer">

      </div> <!-- /container -->


    </body>
</html>

