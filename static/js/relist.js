
var xmlHttp

function GetListInverter()
{
	
	xmlHttp=GetXmlHttpObject()
	if (xmlHttp==null){
		alert ("Browser does not support HTTP Request")
		return;
	  } 
	var url= "Inverter/ListInverter.php";
	url=url+"?";
	url=url+"&sid="+Math.random();
	xmlHttp.onreadystatechange=stateChanged ;
	xmlHttp.open("GET",url,true);
	xmlHttp.send(null);
} 

function stateChanged() 
{ 
	if (xmlHttp.readyState==4 || xmlHttp.readyState=="complete"){ 
		 var str = xmlHttp.responseText;
	 	 var arystr = str.split("~");
	 	 for(var i in arystr){
	 	  	var info = arystr[i].split("@");
	 	  	sinum = info[0].replace(/[^\d]/g,"");

	 	  	AC_P = "AC_P"+sinum;
	 	  	SetTdValue(AC_P,info[1]);

	 	  	SIStatus = "SIStatus"+sinum;
	 	  	SetTdValue(SIStatus,info[2]);

	 	  	Hz = "HZ"+sinum;
	 	  	SetTdValue(Hz,info[3]);

	 	  	Exception = "Exception"+sinum;
	 	  	SetTdValue(Exception,info[4]);
	 
	 	  //	document.form2.("AC_P"+sinum).value = info[1];
	 	  	//document.getElementById(AC_P).innerHTML =info[1];
	 	 }
	 	 
	} 
}
function SetTdValue(id,value)
{
	var td = document.getElementById(id);
	if(td){
	 	td.innerHTML = value;
	}
}

function timer()
{
	GetListInverter();
	setTimeout('timer()',5000);
}

function GetXmlHttpObject()
{
	var xmlHttp=null;
	try{
		 // Firefox, Opera 8.0+, Safari
		 xmlHttp=new XMLHttpRequest();
	}
	catch (e){
		// Internet Explorer
		try{
			xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
		}catch (e){
		 	xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
		}
	}

	return xmlHttp;
}