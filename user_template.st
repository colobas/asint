<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        <script>



            function clearContainer(){
                document.getElementById("maincontainer").innerHTML = "";
            }

            function listRooms(){
                document.getElementById("maincontainer").innerHTML = "lista de salas";
            } 

            function userFeed(){
                document.getElementById("maincontainer").innerHTML = "história de utilizacao";
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
              <li class="active"><a href="#" onclick="userFeed()">Feed</a></li>
              <li><a href="#" onclick="listRooms()">Rooms</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div><!--/.container-fluid -->
      </nav>



      <div class="jumbotron" id="maincontainer">
            historia de utilizacao
      </div> <!-- /container -->


    </body>
</html>

