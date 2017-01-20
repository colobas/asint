        <!--COMMENT: Tudo o que está em HTML é estático. São os elementos que aparecem no browser-->
        <html>
            <head>
            <p id="register"></p>

            <!--COMMENT: Script JS, responsável por tudo o que é dinâmico-->
            <script>

                // Função que submete para o servidor o username inserido e faz o login ou registo
                //  Recebe como argumento "reg" ou "log", dependendo do botao clicado

                function submit(mode) {

                    // str guarda o username introduzido, do respectivo campo login/registo-->

                    if(mode=="reg"){
                        var str = document.getElementById("username_reg").value;
                    }else{
                        var str = document.getElementById("username_log").value
                    }

                    var xmlhttp = new XMLHttpRequest();

                    //Espera pela resposta. Quando é recebida, corre a função, e faz o que tem a fazer de acordo com a resposta recebida

                    xmlhttp.onreadystatechange = function() {

                        if (this.readyState == 4 && this.status == 200) {

                            //Divide a resposta do servidor em username e id

                            var response = xmlhttp.responseText.split(",");
                            if (response != "0") {
                                window.location = "/user/"+response
                            } else {
                                window.location = "/admin"
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
                <center><h1>Login</h1>
                    Username:<br>
                    <input method="post" id="username_log" type="text" />
                    <br>
                    <button onclick="submit('log')">Login</button>
                <br><br>
                <center><h3>Register</h3>
                    Username:<br>
                    <input method="post" id="username_reg" type="text" />
                    <br>
                    <button onclick="submit('reg')">Register</button>
                </center>
            </body>
        </html>
