        <html>
            <head>
            <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
            <script>

                // Função que submete para o servidor o username inserido e faz o login ou registo
                //  Recebe como argumento "reg" ou "log", dependendo do botao clicado


                function loginUser() {
                    cont = document.getElementById("maincontainer");
                    content = '\
                       <div class="row">\
                            <div class="col-lg-6">\
                                <div class="input-group">\
                                <div class="input-group-btn">\
                                    <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Action <span class="caret"></span></button>\
                                      <ul class="dropdown-menu">\
                                      <li><a href="#" onclick="submit(\'log\', false)">Login</a></li>\
                                      <li role="separator" class="divider"></li>\
                                      <li><a href="#" onclick="submit(\'reg\', false)">Register</a></li>\
                                      </ul>\
                                      </div><!-- /btn-group -->\
                                      <input type="text" id="nameinput" class="form-control" aria-label="...">\
                                </div><!-- /input-group -->\
                            </div><!-- /.col-lg-6 -->\
                        </div><!-- /.row -->\
                    ';
                    cont.innerHTML = content;
                }

                function submit(mode, admin) {
                    if (admin) {
                        window.location = "/admin";
                        return;
                    }

                    // str guarda o username introduzido, do respectivo campo login/registo-->
                    var str = document.getElementById("nameinput").value

                    if (str.length == 0) {
                        window.alert("user can't have empty name");
                    }

                    var xmlhttp = new XMLHttpRequest();

                    //Espera pela resposta. Quando é recebida, corre a função, e faz o que tem a fazer de acordo com a resposta recebida

                    xmlhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            var response = xmlhttp.responseText;
                            if (response == "-1") {
                                window.alert("User not registered");
                            } else if (response != "0") {
                                window.location = "/user/"+response;
                            } else {
                                window.location = "/admin";
                            }
                        }
                    }

                    // Envia o nome introduzido e o modo (log ou reg) para o servidor (app.post('/'))
                    xmlhttp.open("POST", "/", true);
                    xmlhttp.send("data="+str+","+mode);
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
                    <a class="navbar-brand" href="#" onclick="clearContainer()">Login/Register</a>
                  </div>
                  <div id="navbar" class="navbar-collapse collapse">
                    <ul class="nav navbar-nav">
                     <li class="active"><a href="#" onclick="loginUser()">User</a></li>
                     <li class="active"><a href="#" onclick="submit('log',true)">Admin</a></li>
                    </ul>
                  </div><!--/.nav-collapse -->
                </div><!--/.container-fluid -->
                </nav>
                <div class="jumbotron" id="maincontainer">
                </div> <!-- /container --> 

                </center>
            </body>
        </html>
