function get_cluster() {

    var clusters = document.getElementById("gc").getAttribute("cluster_data");
    var par = JSON.parse(clusters);
    
    if( ( document.theForm.cluster_belong.value == "" ) ) { 
       alert("The entry is empty!");
       return false;
    } 

    for (let i = 0; i < par.length; i++) {
        if ( par[i][0] == document.theForm.cluster_belong.value) {
            alert("Cluster Settings Found!");
            var c_fun = par[i][1][0];
            var c_sub = par[i][1][1];
            document.theForm.functions.value = c_fun;
            document.theForm.subsystems.value = c_sub;
            return true;
        } 
    }

    alert("Cluster data does NOT exist, please create the Cluster");
    return false;
  }
