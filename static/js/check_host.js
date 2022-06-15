function validate() {

    var hosts = document.getElementById("ch").getAttribute("hosts");  
    var hosts = hosts.replace(/[\][']/g, '');
    
    if( ( document.theForm.hostname.value == "" ) ) { 
       alert("The entry is empty!");
       return false;
    } else if ( hosts == document.theForm.hostname.value) {
       alert( "Change hostname! This Hostname is alreaedy in the database" );
       document.theForm.hostname.focus() ;
       return false;
    }
    alert( "All good! This is a new hostname" );
    return( true );
  }