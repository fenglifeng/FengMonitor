
var xmlHttp

function GetMainInverter()
{
	
	xmlHttp=GetXmlHttpObject()
	if (xmlHttp==null){
		alert ("Browser does not support HTTP Request")
		return;
	  } 
	var url= "Inverter/MainInverter.php";
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
	 	var arystr = str.split("-");
 
	 	//SetPValue("allpower",arystr[0].replace(/[^\d]/g,""));
	 	SetPValue("planpower",arystr[1]);
	 	SetPValue("AC_P",arystr[2]);
	 	SetPValue("daypower",arystr[3]);

	 	var allpower = parseInt(arystr[0].replace(/[^\d]/g,""));
	 	var  unit = "kWh";
	 	if(allpower >=1000000){
	 		allpower = allpower/1000000;
	 		unit = "GWh";
	 	}else if(allpower>1000){
	 		allpower = allpower/1000;
	 		unit = "MWh";	 		
	 	}
	 	allpower = Math.round(allpower*100)/100;
	 	SetPValue("unit","总发电量"+unit);
	 	SetPValue("allpower",allpower);
	 
	 	  //	document.form2.("AC_P"+sinum).value = info[1];
	 	  	//document.getElementById(AC_P).innerHTML =info[1];	 	 
	} 
}
function SetPValue(id,value)
{
	var p= document.getElementById(id);
	if(p){
	 	p.innerHTML = value;
	}
}

function timer()
{
	GetMainInverter();
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