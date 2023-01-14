function validate() {

    var hosts = document.getElementById("ch").getAttribute("hosts");  
    
    if( ( document.theForm.hostname.value == "" ) ) { 
       alert("The entry is empty!");
       return false;
    } else if ( JSON.parse(hosts).includes(document.theForm.hostname.value)) {
       alert( "Change hostname! This Hostname is alreaedy in the database" );
       document.theForm.hostname.focus() ;
       return false;
    }
    alert( "All good! This is a new hostname" );
    return( true );
  }