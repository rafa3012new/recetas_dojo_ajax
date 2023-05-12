    function iniciando(){
        document.getElementById('date_made_receta').valueAsDate = new Date();
    }


    function limpiar_formulario1(){
            let input_user = document.getElementById("user")
            let input_firstname = document.getElementById("firstname")
            let input_lastname = document.getElementById("lastname")
            let input_email = document.getElementById("email")
            let input_password_reg = document.getElementById("password_reg")
            let input_cpassword_reg = document.getElementById("cpassword_reg")

            input_user.value = ""
            input_firstname.value = ""
            input_lastname.value = ""
            input_email.value = ""
            input_password_reg.value = ""
            input_cpassword_reg.value = ""

        }

        function procesar_login() {

             let input_user = document.getElementById("user")
             let input_firstname = document.getElementById("firstname")
             let input_lastname = document.getElementById("lastname")
             let input_email = document.getElementById("email")
             let input_password_reg = document.getElementById("password_reg")
             let input_cpassword_reg = document.getElementById("cpassword_reg")

                    //se envia la informacion del prompt via ajax usando fetch
                    //se arma una variable json tipo objeto dict
                    //al no usar un form el body se reemplaza de form por un objeto
                    let data = {
                        "user": input_user.value,
                        "firstname": input_firstname.value,
                        "lastname": input_lastname.value,
                        "email": input_email.value,
                        "password_reg": input_password_reg.value,
                        "cpassword_reg": input_cpassword_reg.value
                    }

                    //se ejecuta el fetch de tipo POST y la promesa
                    fetch("/procesar_registro", {
                        "method": "POST",
                        "headers": {"Content-Type": "application/json"},
                        "body":  JSON.stringify(data),
                        }).then(function(response){
                         return response.json();
                        }).then(function(data_response){
                            procesar_crear_registro_usuario(data_response);
                            return console.log(data_response);
                        });
        }


        function procesar_crear_registro_usuario(data){
            if ("mensaje_validar" in data['data_respuesta_json'][0]){
                //se llama al mensaje flash tipo snackbar
                for (i of data['data_respuesta_json'][0]['mensaje_validar'])
                   snackbar('error', i, 3000);
            }
            else if ("usuario" in data['data_respuesta_json'][0]){
                limpiar_formulario1();
                //se llama al mensaje flash tipo snackbar
                snackbar('success', 'Se creo el registro de usuario con exito', 3000);
            }
            else{
                limpiar_formulario2();
                snackbar('error', "error en los datos devueltos por el server", 3000);
            }
        }



        function limpiar_formulario2(){
            let input_nombre_receta = document.getElementById("nombre_receta");
            let input_descripcion_receta = document.getElementById("descripcion_receta");
            let input_instrucciones_receta = document.getElementById("instrucciones_receta");
            let input_date_made_receta = document.getElementById("date_made_receta");
            let input_under30_receta = document.getElementById("under30_yes");

            input_nombre_receta.value = ""
            input_descripcion_receta.value = ""
            input_instrucciones_receta.value = ""
            input_date_made_receta.valueAsDate = new Date();
            input_under30_receta.checked = true;
        }

        function crear_receta(usuario_sesion) {

             let input_nombre_receta = document.getElementById("nombre_receta");
             let input_descripcion_receta = document.getElementById("descripcion_receta");
             let input_instrucciones_receta = document.getElementById("instrucciones_receta");
             let input_date_made_receta = document.getElementById("date_made_receta");
             let input_under30_yes = document.getElementById("under30_yes");
             let under30 = 0;
             let input_operacion_receta = document.getElementById("operacion_receta");

                    if (input_under30_yes.checked)
                    {
                        under30 = 1;
                    }
                    else
                    {
                        under30 = 0;
                    }

                     //se envia la informacion del prompt via ajax usando fetch
                    //se arma una variable json tipo objeto dict
                    //al no usar un form el body se reemplaza de form por un objeto
                    let data = {
                        "nombre_receta": input_nombre_receta.value,
                        "descripcion_receta": input_descripcion_receta.value,
                        "instrucciones_receta": input_instrucciones_receta.value,
                        "date_made_receta": input_date_made_receta.value,
                        "under30":under30,
                        "operacion_receta": input_operacion_receta.value
                    }

                    //se ejecuta el fetch de tipo POST y la promesa
                    fetch("/recetas/procesar_receta", {
                        "method": "POST",
                        "headers": {"Content-Type": "application/json"},
                        "body":  JSON.stringify(data),
                        }).then(function(response){
                         return response.json();
                        }).then(function(data_response){
                            procesar_crear_receta(data_response,usuario_sesion);
                            return console.log(data_response);
                        });
        }

        function procesar_crear_receta(data,usuario_sesion){
            if ("mensaje_validar" in data['data_respuesta_json'][0]){
                //se llama al mensaje flash tipo snackbar
                for (i of data['data_respuesta_json'][0]['mensaje_validar'])
                   snackbar('error', i, 3000);
            }
            else if ("autor" in data['data_respuesta_json'][0]){
                llenar_tabla_receta(data,usuario_sesion);
                limpiar_formulario2();
                //se llama al mensaje flash tipo snackbar
                snackbar('success', 'Se creo la receta con exito', 3000);
            }
            else{
                limpiar_formulario2();
                snackbar('error', "error en los datos devueltos por el server", 3000);
            }
        }


        function llenar_tabla_receta(data,usuario_sesion){
            let tabla_receta = document.getElementById('tabla_receta');
            let h2total = document.getElementById('h2total');
            var largo_tabla_receta = tabla_receta.rows.length;
            let id_receta;

            var fila = tabla_receta.insertRow(largo_tabla_receta);
            var celda1 = fila.insertCell(0);
            var celda2 = fila.insertCell(1);
            var celda3 = fila.insertCell(2);
            var celda4 = fila.insertCell(3);

            celda1.innerHTML = data['data_respuesta_json'][0]['nombre'];
            celda2.innerHTML = data['data_respuesta_json'][0]['under30'] == 1  ? "Si" : "No";
            celda3.innerHTML = data['data_respuesta_json'][0]['nombre_autor'];
            id_receta = data['data_respuesta_json'][0]['id'];

            if (data['data_respuesta_json'][0]['autor'] == usuario_sesion)
            {
              celda4.innerHTML = '<a href="/recetas/detalle_receta/' + id_receta + '">ver receta</a> | <a href="/recetas/editar_receta/' + id_receta + '">editar</a> | <p class="myhyperlink" onclick="eliminar_receta(' + data['data_respuesta_json'][0]['id']  + ', this)">eliminar</p>';
            }
            else
            {
              celda4.innerHTML = '<a href="/detalle_receta/' + id_receta + '>ver receta</a>';
            }

            h2total.innerHTML = 'Todas las Recetas Creadas : ' + largo_tabla_receta;

        }


        function eliminar_receta(id_receta, objeto) {
            if (confirm('Desea eliminar la receta?'))
            {
                   //se envia la informacion del prompt via ajax usando fetch
                   //se arma una variable json tipo objeto dict
                   //al no usar un form el body se reemplaza de form por un objeto
                   let data = {
                       "id": id_receta
                   }

                   //se ejecuta el fetch de tipo POST y la promesa
                   fetch("/recetas/eliminar_receta", {
                       "method": "POST",
                       "headers": {"Content-Type": "application/json"},
                       "body":  JSON.stringify(data),
                       }).then(function(response){
                          return response.json();
                       }).then(function(data_response){
                           eliminar_receta_tabla(objeto, data_response);
                           return console.log(data_response);
                        });
            }
        }


        function eliminar_receta_tabla(objeto, data){
            //se obtinene la referencia de la tabla
            let tabla_receta = document.getElementById('tabla_receta');
            //elemento p -> td -> tr
            let indice_eliminar = objeto.parentNode.parentNode.rowIndex;
            let h2total = document.getElementById('h2total');

            //se elimina la fila de la tabla de recetas
            tabla_receta.deleteRow(indice_eliminar);

            let largo_tabla_receta = tabla_receta.rows.length - 1;

            h2total.innerHTML = 'Todas las Recetas Creadas : ' + largo_tabla_receta;

            //se llama al mensaje flash tipo snackbar
            snackbar(data['data_respuesta_json']['type'], data['data_respuesta_json']['message'], 3000);

        }

        function editar_receta(id_receta,usuario_sesion) {

            let input_id_receta = document.getElementById("id_receta_edit");
            let input_nombre_receta = document.getElementById("nombre_receta");
            let input_descripcion_receta = document.getElementById("descripcion_receta");
            let input_instrucciones_receta = document.getElementById("instrucciones_receta");
            let input_date_made_receta = document.getElementById("date_made_receta_edit");
            let input_under30_yes = document.getElementById("under30_yes");
            let under30 = 0;
            let input_operacion_receta = document.getElementById("operacion_receta");

                   // under30 = input_under30_yes.checked ? 1 : 0;

                   if (input_under30_yes.checked)
                   {
                       under30 = 1;
                   }
                   else
                   {
                       under30 = 0;
                   }

                    //se envia la informacion del prompt via ajax usando fetch
                   //se arma una variable json tipo objeto dict
                   //al no usar un form el body se reemplaza de form por un objeto
                   let data = {
                       "id":input_id_receta.value,
                       "nombre_receta": input_nombre_receta.value,
                       "descripcion_receta": input_descripcion_receta.value,
                       "instrucciones_receta": input_instrucciones_receta.value,
                       "date_made_receta": input_date_made_receta.value,
                       "under30":under30,
                       "operacion_receta": input_operacion_receta.value
                   }

                   //se ejecuta el fetch de tipo POST y la promesa
                   fetch("/recetas/procesar_receta", {
                       "method": "POST",
                       "headers": {"Content-Type": "application/json"},
                       "body":  JSON.stringify(data),
                       }).then(function(response){
                        return response.json();
                       }).then(function(data_response){
                           procesar_editar_receta(data_response);
                           return console.log(data_response);
                       });
       }


       function procesar_editar_receta(data){
        if ("mensaje_validar" in data['data_respuesta_json']){
            //se llama al mensaje flash tipo snackbar
            for (i of data['data_respuesta_json']['mensaje_validar'])
               snackbar('error', i, 3000);
        }
        else if ("autor" in data['data_respuesta_json']){
            llenar_detalle_receta(data);
            //se llama al mensaje flash tipo snackbar
            snackbar('success', 'Se actualizo la receta con exito', 3000);
        }
        else{
            snackbar('error', "error en los datos devueltos por el server", 3000);
        }
    }


    function llenar_detalle_receta(data) {

            let lista_receta = document.getElementById('lista_detalle_receta');
            let h3nombrereceta = document.getElementById('h3nombre_receta');

            let fila1 = lista_receta.getElementsByTagName("li")[0].querySelector('div:last-child');
            let fila2 = lista_receta.getElementsByTagName("li")[1].querySelector('div:last-child');
            let fila3 = lista_receta.getElementsByTagName("li")[2].querySelector('div:last-child');
            let fila4 = lista_receta.getElementsByTagName("li")[3].querySelector('div:last-child');

            h3nombrereceta.innerText = data['data_respuesta_json']['nombre'];
            fila1.innerText = data['data_respuesta_json']['descripcion'];
            fila2.innerText = data['data_respuesta_json']['under30'] == 1  ? "Si" : "No";
            fila3.innerText = data['data_respuesta_json']['instrucciones'];
            fila4.innerText = data['data_respuesta_json']['date_made'];
}