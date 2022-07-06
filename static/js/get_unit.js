function get_unit() {

    var units = document.getElementById("gc").getAttribute("unit_data");
    var par = JSON.parse(units);
    
    if( ( document.theForm.unit_belong.value == "" ) ) { 
       alert("The entry is empty!");
       return false;
    } 

    for (let i = 0; i < par.length; i++) {
        if ( par[i][0] == document.theForm.unit_belong.value) {
            alert("Unit Settings Found!");
            var c_fun = par[i][1][0];
            var c_sub = par[i][1][1];
            document.theForm.functions.value = c_fun;
            document.theForm.subsystems.value = c_sub;
            return true;
        } 
    }

    alert("Unit data does NOT exist, please create the unit");
    return false;
  }
